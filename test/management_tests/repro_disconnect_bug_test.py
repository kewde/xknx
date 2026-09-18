"""
Regression guards for peer TDisconnect during ACK-wait in P2P management.

When the peer sends ``TDisconnect`` while a ``P2PConnection.request()`` is
awaiting its ACK inside ``_send_data`` (i.e. ``_ack_waiter`` is truthy),
``P2PConnection.process()`` must resolve the *awaited* ``_ack_waiter`` future
rather than the not-yet-awaited ``_response_waiter`` future.

These guards cover three behaviours that broke on the unpatched code:
- the in-flight ``request()`` promptly raises ``ManagementConnectionRefused``
  and the ``_ack_waiter`` future is completed (ordering #2),
- ``nm_individual_address_check`` still returns ``True`` (occupied) when the
  peer disconnects during the ACK-wait, with no procedure-level regression, and
- no asyncio ``Future exception was never retrieved`` warning is emitted.
"""

import asyncio
import gc
from unittest.mock import AsyncMock, call

import pytest

from xknx import XKNX
from xknx.exceptions import (
    ManagementConnectionRefused,
    ManagementConnectionTimeout,
)
from xknx.management import procedures
from xknx.management.management import MANAGAMENT_ACK_TIMEOUT, P2PConnection
from xknx.telegram import (
    IndividualAddress,
    Telegram,
    TelegramDirection,
    apci,
    tpci,
)

from ..conftest import EventLoopClockAdvancer

_PARK_ITERATIONS = 100


async def _park_on_ack_waiter(
    conn: P2PConnection, task: asyncio.Task[Telegram]
) -> None:
    """Drive the loop until *task* (a ``conn.request``) is awaiting its ACK future."""
    for _ in range(_PARK_ITERATIONS):
        await asyncio.sleep(0)
        if conn._ack_waiter is not None and not conn._ack_waiter.done():
            return
        if task.done():
            pytest.fail("request() task finished before parking on _ack_waiter")
    pytest.fail("request() never parked on _ack_waiter")


def _disconnect_telegram(ia: IndividualAddress) -> Telegram:
    """Build an incoming TDisconnect from the peer at *ia*."""
    return Telegram(
        source_address=ia,
        destination_address=IndividualAddress(0),
        direction=TelegramDirection.INCOMING,
        tpci=tpci.TDisconnect(),
    )


async def test_disconnect_during_ack_wait_unblocks_ack_waiter(
    time_travel: EventLoopClockAdvancer,
) -> None:
    """TDisconnect during ACK-wait resolves the awaited _ack_waiter promptly."""
    xknx = XKNX()
    xknx.cemi_handler = AsyncMock()
    ia = IndividualAddress("4.0.1")

    conn = await xknx.management.connect(ia)
    xknx.cemi_handler.send_telegram.reset_mock()

    device_desc_read = Telegram(
        destination_address=ia,
        tpci=tpci.TDataConnected(0),
        payload=apci.DeviceDescriptorRead(descriptor=0),
    )

    task = asyncio.create_task(
        conn.request(
            payload=apci.DeviceDescriptorRead(descriptor=0),
            expected=apci.DeviceDescriptorResponse,
        )
    )
    await _park_on_ack_waiter(conn, task)
    original_ack_waiter = conn._ack_waiter
    assert original_ack_waiter is not None

    # Peer sends TDisconnect while _send_data is awaiting the ACK (ordering #2).
    xknx.management.process(_disconnect_telegram(ia))

    # The awaited ACK future must be resolved immediately, not left pending.
    assert original_ack_waiter.done()

    # request() must surface the disconnect promptly - far below the 6s timeout.
    with pytest.raises(ManagementConnectionRefused):
        await time_travel(0.5)
        task.result()

    # No spurious TDataConnected retransmit to the now-disconnected peer.
    assert xknx.cemi_handler.send_telegram.call_args_list == [call(device_desc_read)]

    try:
        await conn.disconnect()
    except ManagementConnectionRefused:
        pass


async def test_nm_individual_address_check_refused_during_ack_wait(
    time_travel: EventLoopClockAdvancer,
) -> None:
    """nm_individual_address_check returns True (occupied) when peer disconnects during ACK-wait."""
    xknx = XKNX()
    xknx.cemi_handler = AsyncMock()
    ia = IndividualAddress("4.0.1")

    task = asyncio.create_task(procedures.nm_individual_address_check(xknx, ia))

    # Wait until the procedure has connected and parked on _ack_waiter
    # so the peer TDisconnect lands during the ACK-wait (ordering #2).
    conn = None
    for _ in range(_PARK_ITERATIONS):
        await asyncio.sleep(0)
        conn = xknx.management._connections.get(ia)
        if (
            conn is not None
            and conn._ack_waiter is not None
            and not conn._ack_waiter.done()
        ):
            break
        if task.done():
            pytest.fail(
                "nm_individual_address_check finished before parking on _ack_waiter"
            )
    else:
        pytest.fail("nm_individual_address_check never parked on _ack_waiter")
    assert conn is not None

    xknx.management.process(_disconnect_telegram(ia))

    # Allow the (fixed) prompt refusal and the (unpatched) 2 x ACK-timeout path
    # to complete; the procedure result is True on both, just delivered promptly
    # with the fix instead of after the ~6 s delay.
    await time_travel(MANAGAMENT_ACK_TIMEOUT)
    await time_travel(MANAGAMENT_ACK_TIMEOUT)

    assert await task is True


async def test_no_unretrieved_future_exception_on_disconnect_during_ack_wait(
    time_travel: EventLoopClockAdvancer,
) -> None:
    """No asyncio 'Future exception was never retrieved' warning on disconnect during ACK-wait."""
    xknx = XKNX()
    xknx.cemi_handler = AsyncMock()
    ia = IndividualAddress("4.0.1")

    captured: list[dict[str, object]] = []
    loop = asyncio.get_running_loop()
    loop.set_exception_handler(lambda _loop, context: captured.append(context))
    try:
        conn = await xknx.management.connect(ia)
        task = asyncio.create_task(
            conn.request(
                payload=apci.DeviceDescriptorRead(descriptor=0),
                expected=apci.DeviceDescriptorResponse,
            )
        )
        await _park_on_ack_waiter(conn, task)

        xknx.management.process(_disconnect_telegram(ia))

        # Drive the scenario to completion: fixed code refuses promptly,
        # unpatched code raises after the doubled ACK timeout.
        await time_travel(MANAGAMENT_ACK_TIMEOUT)
        await time_travel(MANAGAMENT_ACK_TIMEOUT)

        # Retrieve the task's own exception so it does not emit a separate
        # "Task exception was never retrieved" at finalisation.
        try:
            await task
        except (ManagementConnectionRefused, ManagementConnectionTimeout):
            pass

        # Drop the connection from the management registry (raises because the
        # peer already set _connected = False, before the finally that would
        # cancel _response_waiter) so the connection becomes collectable.
        try:
            await conn.disconnect()
        except ManagementConnectionRefused:
            pass

        del task
        del conn
        gc.collect()
    finally:
        loop.set_exception_handler(None)

    assert not any(
        context.get("message") == "Future exception was never retrieved"
        for context in captured
    ), captured
