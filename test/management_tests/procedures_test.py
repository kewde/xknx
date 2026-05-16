"""Test management procedures."""

import asyncio
from unittest.mock import AsyncMock, call

import pytest

from xknx import XKNX
from xknx.exceptions import ManagementConnectionError
from xknx.management import interface_object, max_apdu, procedures
from xknx.management.management import MANAGAMENT_CONNECTION_TIMEOUT, P2PConnection
from xknx.telegram import (
    GroupAddress,
    IndividualAddress,
    Telegram,
    TelegramDirection,
    apci,
    tpci,
)

from ..conftest import EventLoopClockAdvancer


async def _open_connection(
    xknx: XKNX, address: IndividualAddress, *, rate_limit: int = 0
) -> P2PConnection:
    """
    Open a P2P connection for procedure tests that exercise the live transport.

    ``rate_limit`` defaults to ``0`` (disabled) so that tests chaining many
    requests do not block on the inter-request throttle. Tests that need to
    exercise rate-limiting behaviour can override.
    """
    connection = await xknx.management.connect(address, rate_limit=rate_limit)
    # discard the TConnect telegram from the call log so the test sees only the
    # telegrams produced by the procedure under test
    xknx.cemi_handler.send_telegram.reset_mock()
    return connection


def _incoming_ack(source: IndividualAddress, sequence: int) -> Telegram:
    return Telegram(
        source_address=source,
        destination_address=IndividualAddress(0),
        direction=TelegramDirection.INCOMING,
        tpci=tpci.TAck(sequence),
    )


def _incoming_response(
    source: IndividualAddress, sequence: int, payload: apci.APCI
) -> Telegram:
    return Telegram(
        source_address=source,
        destination_address=IndividualAddress(0),
        direction=TelegramDirection.INCOMING,
        tpci=tpci.TDataConnected(sequence),
        payload=payload,
    )


async def test_nm_read_max_apdu_length_returns_value() -> None:
    """Returns the integer value when the device exposes PID_MAX_APDU_LENGTH."""
    xknx = XKNX()
    xknx.cemi_handler = AsyncMock()
    target = IndividualAddress("1.1.5")
    connection = await _open_connection(xknx, target)

    task = asyncio.create_task(max_apdu.nm_read_max_apdu_length(connection))
    await asyncio.sleep(0)

    expected_request = Telegram(
        destination_address=target,
        tpci=tpci.TDataConnected(0),
        payload=apci.PropertyValueRead(
            object_index=0, property_id=56, count=1, start_index=1
        ),
    )
    assert xknx.cemi_handler.send_telegram.call_args_list == [call(expected_request)]

    xknx.management.process(_incoming_ack(target, 0))
    xknx.management.process(
        _incoming_response(
            target,
            0,
            apci.PropertyValueResponse(
                object_index=0,
                property_id=56,
                count=1,
                start_index=1,
                data=b"\x00\xfe",
            ),
        )
    )
    assert await task == 254
    await xknx.management.disconnect(target)


async def test_nm_read_max_apdu_length_property_absent_returns_none() -> None:
    """Returns None when the device responds with count=0 (property does not exist)."""
    xknx = XKNX()
    xknx.cemi_handler = AsyncMock()
    target = IndividualAddress("1.1.5")
    connection = await _open_connection(xknx, target)

    task = asyncio.create_task(max_apdu.nm_read_max_apdu_length(connection))
    await asyncio.sleep(0)

    xknx.management.process(_incoming_ack(target, 0))
    xknx.management.process(
        _incoming_response(
            target,
            0,
            apci.PropertyValueResponse(
                object_index=0, property_id=56, count=0, start_index=0, data=b""
            ),
        )
    )
    assert await task is None
    await xknx.management.disconnect(target)


async def _drive_scan_step(
    xknx: XKNX,
    source: IndividualAddress,
    seq_description: int,
    seq_value: int,
    description_pid: int,
    object_type_value: int | None,
) -> None:
    """
    Feed the ACK + response pair for one iteration of nm_interface_object_scan.

    ``description_pid`` is the PID echoed in A_PropertyDescription_Response. A
    value of 0 means "no Interface Object at this index" — terminates the
    outer scan and skips the value-read.
    ``object_type_value`` is the 2-octet value of PID_OBJECT_TYPE; ``None``
    encodes "property absent" (count=0, empty data).
    """
    xknx.management.process(_incoming_ack(source, seq_description))
    xknx.management.process(
        _incoming_response(
            source,
            seq_description,
            apci.PropertyDescriptionResponse(
                object_index=0,
                property_id=description_pid,
                property_index=0,
            ),
        )
    )
    if description_pid == 0:
        return
    await asyncio.sleep(0)
    if object_type_value is None:
        data = b""
        count = 0
    else:
        data = object_type_value.to_bytes(2, byteorder="big")
        count = 1
    xknx.management.process(_incoming_ack(source, seq_value))
    xknx.management.process(
        _incoming_response(
            source,
            seq_value,
            apci.PropertyValueResponse(
                object_index=0,
                property_id=1,
                count=count,
                start_index=1,
                data=data,
            ),
        )
    )


async def test_nm_interface_object_scan_finds_device_object_at_index_0() -> None:
    """Device Object (type 0x0000) is found at object_index 0."""
    xknx = XKNX()
    xknx.cemi_handler = AsyncMock()
    target = IndividualAddress("1.1.5")
    connection = await _open_connection(xknx, target)

    task = asyncio.create_task(
        interface_object.nm_interface_object_scan(connection, 0x0000)
    )
    await asyncio.sleep(0)
    await _drive_scan_step(
        xknx, target, 0, 1, description_pid=1, object_type_value=0x0000
    )
    assert await task == 0
    await xknx.management.disconnect(target)


async def test_nm_interface_object_scan_finds_router_object_at_higher_index() -> None:
    """Router Object (type 0x0006) is found by iterating past the Device Object."""
    xknx = XKNX()
    xknx.cemi_handler = AsyncMock()
    target = IndividualAddress("1.1.0")
    connection = await _open_connection(xknx, target)

    task = asyncio.create_task(
        interface_object.nm_interface_object_scan(connection, 0x0006)
    )
    await asyncio.sleep(0)
    # index 0 is Device Object — does not match Router
    await _drive_scan_step(
        xknx, target, 0, 1, description_pid=1, object_type_value=0x0000
    )
    await asyncio.sleep(0)
    # index 1 is Router Object — match
    await _drive_scan_step(
        xknx, target, 2, 3, description_pid=1, object_type_value=0x0006
    )
    assert await task == 1
    await xknx.management.disconnect(target)


async def test_nm_interface_object_scan_stops_when_description_response_pid_is_zero() -> (
    None
):
    """PID=0 in A_PropertyDescription_Response terminates the scan with None."""
    xknx = XKNX()
    xknx.cemi_handler = AsyncMock()
    target = IndividualAddress("1.1.5")
    connection = await _open_connection(xknx, target)

    task = asyncio.create_task(
        interface_object.nm_interface_object_scan(connection, 0x0006)
    )
    await asyncio.sleep(0)
    # No Interface Object at index 0 — PID=0 terminates the loop
    await _drive_scan_step(
        xknx, target, 0, 1, description_pid=0, object_type_value=None
    )
    assert await task is None
    await xknx.management.disconnect(target)


async def test_nm_interface_object_scan_skips_objects_without_object_type_property() -> (
    None
):
    """An object whose PID_OBJECT_TYPE returns count=0 is skipped, not matched."""
    xknx = XKNX()
    xknx.cemi_handler = AsyncMock()
    target = IndividualAddress("1.1.5")
    connection = await _open_connection(xknx, target)

    task = asyncio.create_task(
        interface_object.nm_interface_object_scan(connection, 0x0006)
    )
    await asyncio.sleep(0)
    # index 0: object exists but PID_OBJECT_TYPE returns count=0 — skip
    await _drive_scan_step(
        xknx, target, 0, 1, description_pid=1, object_type_value=None
    )
    await asyncio.sleep(0)
    # index 1: no more objects
    await _drive_scan_step(
        xknx, target, 2, 3, description_pid=0, object_type_value=None
    )
    assert await task is None
    await xknx.management.disconnect(target)


async def test_dm_restart() -> None:
    """Test dm_restart."""
    xknx = XKNX()
    xknx.cemi_handler = AsyncMock()
    individual_address = IndividualAddress("4.0.10")

    connect = Telegram(destination_address=individual_address, tpci=tpci.TConnect())
    restart = Telegram(
        destination_address=individual_address,
        tpci=tpci.TDataConnected(0),
        payload=apci.Restart(),
    )
    disconnect = Telegram(
        destination_address=individual_address,
        tpci=tpci.TDisconnect(),
    )
    await procedures.dm_restart(xknx, individual_address)
    assert xknx.cemi_handler.send_telegram.call_args_list == [
        call(connect),
        call(restart),
        call(disconnect),
    ]


async def test_nm_individual_address_check_success() -> None:
    """Test nm_individual_address_check."""
    xknx = XKNX()
    xknx.cemi_handler = AsyncMock()
    individual_address = IndividualAddress("4.0.10")

    connect = Telegram(destination_address=individual_address, tpci=tpci.TConnect())
    device_desc_read = Telegram(
        destination_address=individual_address,
        tpci=tpci.TDataConnected(0),
        payload=apci.DeviceDescriptorRead(descriptor=0),
    )
    ack = Telegram(
        source_address=individual_address,
        destination_address=IndividualAddress(0),
        direction=TelegramDirection.INCOMING,
        tpci=tpci.TAck(0),
    )
    device_desc_resp = Telegram(
        source_address=individual_address,
        destination_address=IndividualAddress(0),
        direction=TelegramDirection.INCOMING,
        tpci=tpci.TDataConnected(0),
        payload=apci.DeviceDescriptorResponse(),
    )
    task = asyncio.create_task(
        procedures.nm_individual_address_check(xknx, individual_address)
    )
    await asyncio.sleep(0)
    assert xknx.cemi_handler.send_telegram.call_args_list == [
        call(connect),
        call(device_desc_read),
    ]
    # receive response
    xknx.management.process(ack)
    xknx.management.process(device_desc_resp)
    assert await task


async def test_nm_individual_address_check_refused() -> None:
    """Test nm_individual_address_check."""
    xknx = XKNX()
    xknx.cemi_handler = AsyncMock()
    individual_address = IndividualAddress("4.0.10")

    connect = Telegram(destination_address=individual_address, tpci=tpci.TConnect())
    device_desc_read = Telegram(
        destination_address=individual_address,
        tpci=tpci.TDataConnected(0),
        payload=apci.DeviceDescriptorRead(descriptor=0),
    )
    ack = Telegram(
        source_address=individual_address,
        destination_address=IndividualAddress(0),
        direction=TelegramDirection.INCOMING,
        tpci=tpci.TAck(0),
    )
    disconnect = Telegram(
        source_address=individual_address,
        destination_address=IndividualAddress(0),
        direction=TelegramDirection.INCOMING,
        tpci=tpci.TDisconnect(),
    )
    task = asyncio.create_task(
        procedures.nm_individual_address_check(xknx, individual_address)
    )
    await asyncio.sleep(0)
    assert xknx.cemi_handler.send_telegram.call_args_list == [
        call(connect),
        call(device_desc_read),
    ]
    xknx.management.process(disconnect)
    xknx.management.process(ack)
    assert await task


async def test_nm_individual_address_read(time_travel: EventLoopClockAdvancer) -> None:
    """Test nm_individual_address_read."""
    _timeout = 2
    xknx = XKNX()
    xknx.cemi_handler = AsyncMock()
    individual_address_1 = IndividualAddress("1.1.4")
    individual_address_2 = IndividualAddress("15.15.255")

    task = asyncio.create_task(
        procedures.nm_individual_address_read(xknx=xknx, timeout=_timeout)
    )
    address_broadcast = Telegram(
        GroupAddress("0/0/0"), payload=apci.IndividualAddressRead()
    )

    address_reply_message_1 = Telegram(
        source_address=individual_address_1,
        destination_address=GroupAddress("0/0/0"),
        payload=apci.IndividualAddressResponse(),
    )

    address_reply_message_2 = Telegram(
        source_address=individual_address_2,
        destination_address=GroupAddress("0/0/0"),
        payload=apci.IndividualAddressResponse(),
    )

    await asyncio.sleep(0)
    assert xknx.cemi_handler.send_telegram.call_args_list == [
        call(address_broadcast),
    ]
    xknx.management.process(address_reply_message_1)
    xknx.management.process(address_reply_message_2)
    await time_travel(_timeout)
    assert await task


async def test_nm_individual_address_read_multiple() -> None:
    """Test nm_individual_address_read."""
    _timeout = 2
    xknx = XKNX()
    xknx.cemi_handler = AsyncMock()
    individual_address_1 = IndividualAddress("1.1.4")
    individual_address_2 = IndividualAddress("15.15.255")

    task = asyncio.create_task(
        procedures.nm_individual_address_read(
            xknx=xknx, timeout=_timeout, raise_if_multiple=True
        )
    )
    address_broadcast = Telegram(
        GroupAddress("0/0/0"), payload=apci.IndividualAddressRead()
    )

    address_reply_message_1 = Telegram(
        source_address=individual_address_1,
        destination_address=GroupAddress("0/0/0"),
        payload=apci.IndividualAddressResponse(),
    )

    address_reply_message_2 = Telegram(
        source_address=individual_address_2,
        destination_address=GroupAddress("0/0/0"),
        payload=apci.IndividualAddressResponse(),
    )

    await asyncio.sleep(0)
    assert xknx.cemi_handler.send_telegram.call_args_list == [
        call(address_broadcast),
    ]
    xknx.management.process(address_reply_message_1)
    xknx.management.process(address_reply_message_2)
    # no need to wait for _timeout due to `raise_if_multiple=True``
    with pytest.raises(ManagementConnectionError):
        await task


async def test_nm_individual_address_write(time_travel: EventLoopClockAdvancer) -> None:
    """Test nm_individual_address_write."""
    xknx = XKNX()
    xknx.cemi_handler = AsyncMock()
    individual_address_old = IndividualAddress("15.15.255")
    individual_address_new = IndividualAddress("1.1.4")

    connect = Telegram(destination_address=individual_address_new, tpci=tpci.TConnect())
    device_desc_read = Telegram(
        destination_address=individual_address_new,
        tpci=tpci.TDataConnected(0),
        direction=TelegramDirection.OUTGOING,
        payload=apci.DeviceDescriptorRead(descriptor=0),
    )

    address_reply_message = Telegram(
        source_address=individual_address_old,
        destination_address=GroupAddress("0/0/0"),
        direction=TelegramDirection.INCOMING,
        payload=apci.IndividualAddressResponse(),
    )

    device_desc_resp = Telegram(
        source_address=individual_address_new,
        destination_address=IndividualAddress(0),
        direction=TelegramDirection.INCOMING,
        tpci=tpci.TDataConnected(0),
        payload=apci.DeviceDescriptorResponse(),
    )
    ack = Telegram(
        source_address=individual_address_new,
        destination_address=IndividualAddress(0),
        direction=TelegramDirection.INCOMING,
        tpci=tpci.TAck(0),
    )
    ack2 = Telegram(
        destination_address=individual_address_new,
        source_address=IndividualAddress(0),
        direction=TelegramDirection.OUTGOING,
        tpci=tpci.TAck(0),
    )
    disconnect = Telegram(
        destination_address=individual_address_new,
        tpci=tpci.TDisconnect(),
    )
    individual_address_read = Telegram(
        GroupAddress("0/0/0"), payload=apci.IndividualAddressRead()
    )
    individual_address_write = Telegram(
        GroupAddress("0/0/0"),
        payload=apci.IndividualAddressWrite(address=individual_address_new),
    )
    task = asyncio.create_task(
        procedures.nm_individual_address_write(
            xknx=xknx, individual_address=individual_address_new
        )
    )

    # make sure first request (address check) times out
    await time_travel(MANAGAMENT_CONNECTION_TIMEOUT)
    await time_travel(MANAGAMENT_CONNECTION_TIMEOUT)

    # send response to device in programming mode
    xknx.management.process(address_reply_message)

    # confirm device is up and running
    await time_travel(MANAGAMENT_CONNECTION_TIMEOUT)
    xknx.management.process(ack)
    xknx.management.process(device_desc_resp)

    assert xknx.cemi_handler.send_telegram.call_args_list == [
        call(connect),
        call(device_desc_read),
        call(device_desc_read),  # due to retransmit
        call(disconnect),
        call(individual_address_read),
        call(individual_address_write),
        call(connect),
        call(device_desc_read),
        call(ack2),
    ]

    await task


async def test_nm_individual_address_write_two_devices_in_programming_mode(
    time_travel: EventLoopClockAdvancer,
) -> None:
    """Test nm_individual_address_write."""
    xknx = XKNX()
    xknx.cemi_handler = AsyncMock()
    individual_address_old = IndividualAddress("15.15.255")
    individual_address_new = IndividualAddress("1.1.4")

    connect = Telegram(destination_address=individual_address_new, tpci=tpci.TConnect())
    device_desc_read = Telegram(
        destination_address=individual_address_new,
        tpci=tpci.TDataConnected(0),
        payload=apci.DeviceDescriptorRead(descriptor=0),
    )
    address_reply_message = Telegram(
        source_address=individual_address_old,
        destination_address=GroupAddress("0/0/0"),
        direction=TelegramDirection.INCOMING,
        payload=apci.IndividualAddressResponse(),
    )
    disconnect = Telegram(
        destination_address=individual_address_new,
        tpci=tpci.TDisconnect(),
    )
    individual_address_read = Telegram(
        GroupAddress("0/0/0"), payload=apci.IndividualAddressRead()
    )

    task = asyncio.create_task(
        procedures.nm_individual_address_write(
            xknx=xknx, individual_address=individual_address_new
        )
    )

    # make sure first request (address check) times out
    await time_travel(0)  # start
    await time_travel(3)  # first timeout
    await time_travel(3)  # second timeout

    assert xknx.cemi_handler.send_telegram.call_args_list == [
        call(connect),
        call(device_desc_read),
        call(device_desc_read),  # due to retransmit
        call(disconnect),
        call(individual_address_read),
    ]
    # receive two responses from devices in programming mode
    xknx.management.process(address_reply_message)
    xknx.management.process(address_reply_message)
    with pytest.raises(
        ManagementConnectionError,
        match="More than one KNX device is in programming mode",
    ):
        await task
    assert len(xknx.cemi_handler.send_telegram.call_args_list) == 5


async def test_nm_individual_address_write_no_device_programming_mode(
    time_travel: EventLoopClockAdvancer,
) -> None:
    """Test nm_individual_address_write."""
    xknx = XKNX()
    xknx.cemi_handler = AsyncMock()
    individual_address_new = IndividualAddress("1.1.4")

    connect = Telegram(destination_address=individual_address_new, tpci=tpci.TConnect())
    device_desc_read = Telegram(
        destination_address=individual_address_new,
        tpci=tpci.TDataConnected(0),
        payload=apci.DeviceDescriptorRead(descriptor=0),
    )
    disconnect = Telegram(
        destination_address=individual_address_new,
        tpci=tpci.TDisconnect(),
    )
    individual_address_read = Telegram(
        GroupAddress("0/0/0"), payload=apci.IndividualAddressRead()
    )

    task = asyncio.create_task(
        procedures.nm_individual_address_write(
            xknx=xknx, individual_address=individual_address_new
        )
    )

    # make sure first request (address check) times out
    await time_travel(0)
    assert xknx.cemi_handler.send_telegram.call_args_list == [
        call(connect),
        call(device_desc_read),
    ]
    # first timeout - retransmit DeviceDescriptorRead
    await time_travel(3)
    assert xknx.cemi_handler.send_telegram.call_args_list[2:] == [
        call(device_desc_read),
    ]
    # retry also timed out
    await time_travel(3)
    assert xknx.cemi_handler.send_telegram.call_args_list[3:] == [
        call(disconnect),
        call(individual_address_read),
    ]
    # IndividualAddressRead also times out
    await time_travel(3)
    with pytest.raises(
        ManagementConnectionError, match="No device in programming mode"
    ):
        await task
    assert len(xknx.cemi_handler.send_telegram.call_args_list) == 5


async def test_nm_individual_address_write_address_found(
    time_travel: EventLoopClockAdvancer,
) -> None:
    """Test nm_individual_address_write."""
    xknx = XKNX()
    xknx.cemi_handler = AsyncMock()
    individual_address = IndividualAddress("1.1.4")

    connect = Telegram(destination_address=individual_address, tpci=tpci.TConnect())
    device_desc_read = Telegram(
        destination_address=individual_address,
        tpci=tpci.TDataConnected(0),
        payload=apci.DeviceDescriptorRead(descriptor=0),
    )
    ack_in = Telegram(
        source_address=individual_address,
        destination_address=IndividualAddress(0),
        direction=TelegramDirection.INCOMING,
        tpci=tpci.TAck(0),
    )
    ack_out = Telegram(
        source_address=IndividualAddress(0),
        destination_address=individual_address,
        tpci=tpci.TAck(0),
    )
    device_desc_resp = Telegram(
        source_address=individual_address,
        destination_address=IndividualAddress(0),
        direction=TelegramDirection.INCOMING,
        tpci=tpci.TDataConnected(0),
        payload=apci.DeviceDescriptorResponse(),
    )
    disconnect = Telegram(
        destination_address=individual_address,
        tpci=tpci.TDisconnect(),
    )
    individual_address_read = Telegram(
        GroupAddress("0/0/0"), payload=apci.IndividualAddressRead()
    )

    task = asyncio.create_task(
        procedures.nm_individual_address_write(
            xknx=xknx, individual_address=individual_address
        )
    )

    # first request (address check) succeeds
    await time_travel(0)
    xknx.management.process(ack_in)
    xknx.management.process(device_desc_resp)

    assert xknx.cemi_handler.send_telegram.call_args_list == [
        call(connect),
        call(device_desc_read),
        call(ack_out),
    ]
    await time_travel(0)
    assert xknx.cemi_handler.send_telegram.call_args_list[3:] == [
        call(disconnect),
        call(individual_address_read),
    ]
    # second request times out - no device in programming mode
    await time_travel(3)
    with pytest.raises(
        ManagementConnectionError, match="No device in programming mode"
    ):
        await task
    assert len(xknx.cemi_handler.send_telegram.call_args_list) == 5


async def test_nm_individual_address_write_programming_failed(
    time_travel: EventLoopClockAdvancer,
) -> None:
    """Test nm_individual_address_write."""
    xknx = XKNX()
    xknx.cemi_handler = AsyncMock()
    individual_address_old = IndividualAddress("15.15.255")
    individual_address_new = IndividualAddress("1.1.4")

    connect = Telegram(destination_address=individual_address_new, tpci=tpci.TConnect())
    device_desc_read = Telegram(
        destination_address=individual_address_new,
        tpci=tpci.TDataConnected(0),
        direction=TelegramDirection.OUTGOING,
        payload=apci.DeviceDescriptorRead(descriptor=0),
    )

    address_reply_message = Telegram(
        source_address=individual_address_old,
        destination_address=GroupAddress("0/0/0"),
        direction=TelegramDirection.INCOMING,
        payload=apci.IndividualAddressResponse(),
    )
    disconnect = Telegram(
        destination_address=individual_address_new,
        tpci=tpci.TDisconnect(),
    )
    individual_address_read = Telegram(
        GroupAddress("0/0/0"), payload=apci.IndividualAddressRead()
    )
    individual_address_write = Telegram(
        GroupAddress("0/0/0"),
        payload=apci.IndividualAddressWrite(address=individual_address_new),
    )
    task = asyncio.create_task(
        procedures.nm_individual_address_write(
            xknx=xknx, individual_address=individual_address_new
        )
    )

    # make sure first request (address check) times out
    await time_travel(MANAGAMENT_CONNECTION_TIMEOUT)
    await time_travel(MANAGAMENT_CONNECTION_TIMEOUT)

    # send response to device in programming mode
    xknx.management.process(address_reply_message)

    # device experienced error, so set connection request timeout
    await time_travel(MANAGAMENT_CONNECTION_TIMEOUT)
    await time_travel(MANAGAMENT_CONNECTION_TIMEOUT)
    await time_travel(MANAGAMENT_CONNECTION_TIMEOUT)

    assert xknx.cemi_handler.send_telegram.call_args_list == [
        call(connect),
        call(device_desc_read),
        call(device_desc_read),  # due to retransmit
        call(disconnect),
        call(individual_address_read),
        call(individual_address_write),
        call(connect),
        call(device_desc_read),
        call(device_desc_read),
        call(disconnect),
    ]

    with pytest.raises(ManagementConnectionError):
        await task


async def test_nm_individual_address_write_address_found_other_in_programming_mode(
    time_travel: EventLoopClockAdvancer,
) -> None:
    """Test nm_individual_address_write."""
    xknx = XKNX()
    xknx.cemi_handler = AsyncMock()
    individual_address = IndividualAddress("1.1.5")
    individual_address_pgm = IndividualAddress("1.1.4")

    connect = Telegram(destination_address=individual_address, tpci=tpci.TConnect())
    device_desc_read = Telegram(
        destination_address=individual_address,
        tpci=tpci.TDataConnected(0),
        payload=apci.DeviceDescriptorRead(descriptor=0),
    )
    ack = Telegram(
        source_address=individual_address,
        destination_address=IndividualAddress(0),
        direction=TelegramDirection.INCOMING,
        tpci=tpci.TAck(0),
    )
    ack2 = Telegram(
        source_address=IndividualAddress(0),
        destination_address=individual_address,
        tpci=tpci.TAck(0),
    )
    device_desc_resp = Telegram(
        source_address=individual_address,
        destination_address=IndividualAddress(0),
        direction=TelegramDirection.INCOMING,
        tpci=tpci.TDataConnected(0),
        payload=apci.DeviceDescriptorResponse(),
    )
    disconnect = Telegram(
        destination_address=individual_address,
        tpci=tpci.TDisconnect(),
    )
    individual_address_read = Telegram(
        GroupAddress("0/0/0"), payload=apci.IndividualAddressRead()
    )
    address_reply_message = Telegram(
        source_address=individual_address_pgm,
        destination_address=GroupAddress("0/0/0"),
        direction=TelegramDirection.INCOMING,
        payload=apci.IndividualAddressResponse(),
    )

    task = asyncio.create_task(
        procedures.nm_individual_address_write(
            xknx=xknx, individual_address=individual_address
        )
    )

    # make sure first request (address check) times out
    await time_travel(0)
    xknx.management.process(ack)
    xknx.management.process(device_desc_resp)
    await time_travel(MANAGAMENT_CONNECTION_TIMEOUT)

    xknx.management.process(address_reply_message)

    assert xknx.cemi_handler.send_telegram.call_args_list == [
        call(connect),
        call(device_desc_read),
        call(ack2),
        call(disconnect),
        call(individual_address_read),
    ]

    with pytest.raises(ManagementConnectionError):
        await task


async def test_nm_individual_address_serial_number_read(
    time_travel: EventLoopClockAdvancer,
) -> None:
    """Test nm_individual_address_serial_number_read."""

    xknx = XKNX()
    xknx.cemi_handler = AsyncMock()
    individual_address = IndividualAddress("1.1.5")
    serial_number = b"aabbccddeeff"

    task = asyncio.create_task(
        procedures.nm_individual_address_serial_number_read(
            xknx=xknx, serial=serial_number
        )
    )

    read_address = Telegram(
        destination_address=GroupAddress("0/0/0"),
        payload=apci.IndividualAddressSerialRead(serial=serial_number),
    )
    address_reply = Telegram(
        source_address=individual_address,
        destination_address=GroupAddress("0/0/0"),
        direction=TelegramDirection.INCOMING,
        payload=apci.IndividualAddressSerialResponse(
            address=individual_address, serial=serial_number
        ),
    )

    await time_travel(0)
    assert xknx.cemi_handler.send_telegram.call_args_list == [
        call(read_address),
    ]
    xknx.management.process(address_reply)

    assert await task == individual_address


async def test_nm_individual_address_serial_number_read_fail(
    time_travel: EventLoopClockAdvancer,
) -> None:
    """Test nm_individual_address_serial_number_read."""

    xknx = XKNX()
    xknx.cemi_handler = AsyncMock()
    serial_number = b"aabbccddeeff"

    task = asyncio.create_task(
        procedures.nm_individual_address_serial_number_read(
            xknx=xknx, serial=serial_number
        )
    )

    read_address = Telegram(
        destination_address=GroupAddress("0/0/0"),
        payload=apci.IndividualAddressSerialRead(serial=serial_number),
    )

    await time_travel(0)
    assert xknx.cemi_handler.send_telegram.call_args_list == [
        call(read_address),
    ]
    await time_travel(3)

    assert await task is None


async def test_nm_individual_address_serial_number_write(
    time_travel: EventLoopClockAdvancer,
) -> None:
    """Test nm_individual_address_serial_number_write."""

    xknx = XKNX()
    xknx.cemi_handler = AsyncMock()
    serial_number = b"aabbccddeeff"
    individual_address = IndividualAddress("1.1.5")

    task = asyncio.create_task(
        procedures.nm_individual_address_serial_number_write(
            xknx=xknx, serial=serial_number, individual_address=individual_address
        )
    )

    write_address = Telegram(
        destination_address=GroupAddress("0/0/0"),
        payload=apci.IndividualAddressSerialWrite(
            serial=serial_number, address=individual_address
        ),
    )
    read_address = Telegram(
        destination_address=GroupAddress("0/0/0"),
        payload=apci.IndividualAddressSerialRead(serial=serial_number),
    )
    address_reply = Telegram(
        source_address=individual_address,
        destination_address=GroupAddress("0/0/0"),
        direction=TelegramDirection.INCOMING,
        payload=apci.IndividualAddressSerialResponse(
            address=individual_address, serial=serial_number
        ),
    )

    await time_travel(0)
    assert xknx.cemi_handler.send_telegram.call_args_list == [
        call(write_address),
        call(read_address),
    ]
    xknx.management.process(address_reply)
    await task


async def test_nm_individual_address_serial_number_write_fail_no_response(
    time_travel: EventLoopClockAdvancer,
) -> None:
    """Test nm_individual_address_serial_number_write."""

    xknx = XKNX()
    xknx.cemi_handler = AsyncMock()
    serial_number = b"aabbccddeeff"
    individual_address = IndividualAddress("1.1.5")

    task = asyncio.create_task(
        procedures.nm_individual_address_serial_number_write(
            xknx=xknx, serial=serial_number, individual_address=individual_address
        )
    )

    write_address = Telegram(
        destination_address=GroupAddress("0/0/0"),
        payload=apci.IndividualAddressSerialWrite(
            serial=serial_number, address=individual_address
        ),
    )
    read_address = Telegram(
        destination_address=GroupAddress("0/0/0"),
        payload=apci.IndividualAddressSerialRead(serial=serial_number),
    )

    await time_travel(0)
    assert xknx.cemi_handler.send_telegram.call_args_list == [
        call(write_address),
        call(read_address),
    ]
    await time_travel(3)
    with pytest.raises(ManagementConnectionError):
        await task


async def test_nm_individual_address_serial_number_write_fail_wrong_address(
    time_travel: EventLoopClockAdvancer,
) -> None:
    """Test nm_individual_address_serial_number_write."""

    xknx = XKNX()
    xknx.cemi_handler = AsyncMock()
    serial_number = b"aabbccddeeff"
    individual_address_tx = IndividualAddress("1.1.5")
    individual_address_rx = IndividualAddress("1.1.6")

    task = asyncio.create_task(
        procedures.nm_individual_address_serial_number_write(
            xknx=xknx, serial=serial_number, individual_address=individual_address_tx
        )
    )

    write_address = Telegram(
        destination_address=GroupAddress("0/0/0"),
        payload=apci.IndividualAddressSerialWrite(
            serial=serial_number, address=individual_address_tx
        ),
    )
    read_address = Telegram(
        destination_address=GroupAddress("0/0/0"),
        payload=apci.IndividualAddressSerialRead(serial=serial_number),
    )
    address_reply = Telegram(
        source_address=individual_address_rx,
        destination_address=GroupAddress("0/0/0"),
        direction=TelegramDirection.INCOMING,
        payload=apci.IndividualAddressSerialResponse(
            address=individual_address_rx, serial=serial_number
        ),
    )

    await time_travel(0)
    assert xknx.cemi_handler.send_telegram.call_args_list == [
        call(write_address),
        call(read_address),
    ]
    xknx.management.process(address_reply)
    with pytest.raises(ManagementConnectionError):
        await task
