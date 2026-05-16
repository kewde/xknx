"""
Tests for the §2.6 Discovery of maximal frame length procedure.

Covers the topology helper, the local-only and target-read legs
(§2.6.2.1 - §2.6.2.2). The in-between coupler walk (§2.6.2.3) is
exercised once that path lands.
"""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, call

from xknx import XKNX
from xknx.management import nm_discover_max_apdu_length
from xknx.management.procedures import _derive_in_between_couplers
from xknx.telegram import (
    IndividualAddress,
    Telegram,
    TelegramDirection,
    apci,
    tpci,
)


def _ack(source: IndividualAddress, sequence: int) -> Telegram:
    return Telegram(
        source_address=source,
        destination_address=IndividualAddress(0),
        direction=TelegramDirection.INCOMING,
        tpci=tpci.TAck(sequence),
    )


def _response(source: IndividualAddress, sequence: int, payload: apci.APCI) -> Telegram:
    return Telegram(
        source_address=source,
        destination_address=IndividualAddress(0),
        direction=TelegramDirection.INCOMING,
        tpci=tpci.TDataConnected(sequence),
        payload=payload,
    )


def _property_value_response(value: int | None) -> apci.PropertyValueResponse:
    if value is None:
        return apci.PropertyValueResponse(
            object_index=0, property_id=56, count=0, start_index=0, data=b""
        )
    return apci.PropertyValueResponse(
        object_index=0,
        property_id=56,
        count=1,
        start_index=1,
        data=value.to_bytes(2, byteorder="big"),
    )


def test_same_line_yields_no_couplers() -> None:
    """Devices on the same line need no in-between coupler hop."""
    source = IndividualAddress("1.1.1")
    target = IndividualAddress("1.1.5")
    assert _derive_in_between_couplers(source, target) == []


def test_cross_line_same_area_yields_destination_line_coupler() -> None:
    """A cross-line path within one area traverses the destination line coupler."""
    source = IndividualAddress("1.1.1")
    target = IndividualAddress("1.2.5")
    assert _derive_in_between_couplers(source, target) == [
        IndividualAddress("1.2.0"),
    ]


def test_cross_area_yields_area_then_line_coupler() -> None:
    """A cross-area path traverses the destination area coupler then line coupler."""
    source = IndividualAddress("1.1.1")
    target = IndividualAddress("3.2.5")
    assert _derive_in_between_couplers(source, target) == [
        IndividualAddress("3.0.0"),
        IndividualAddress("3.2.0"),
    ]


def test_cross_area_target_on_trunk_skips_line_coupler() -> None:
    """When the target is on the area trunk (main=0), only the area coupler is in-between."""
    source = IndividualAddress("1.1.1")
    target = IndividualAddress("3.0.5")
    assert _derive_in_between_couplers(source, target) == [
        IndividualAddress("3.0.0"),
    ]


async def test_local_le_15_disables_extended_frames() -> None:
    """A local cap ≤ 15 returns immediately without touching the target."""
    xknx = XKNX()
    xknx.cemi_handler = AsyncMock()
    target = IndividualAddress("1.1.5")

    result = await nm_discover_max_apdu_length(xknx, target, local_max_apdu_length=15)

    assert result.extended_frames is False
    assert result.max_frame_length == 15
    assert result.local_length == 15
    assert result.target_length is None
    assert result.coupler_lengths == ()
    # No telegrams sent to the target.
    assert xknx.cemi_handler.send_telegram.call_args_list == []


async def test_target_property_absent_disables_extended_frames() -> None:
    """A target that reports ``count=0`` for PID_MAX_APDU_LENGTH disables extended frames."""
    xknx = XKNX()
    xknx.cemi_handler = AsyncMock()
    target = IndividualAddress("1.1.5")

    task = asyncio.create_task(nm_discover_max_apdu_length(xknx, target))
    await asyncio.sleep(0)
    xknx.management.process(_ack(target, 0))
    xknx.management.process(_response(target, 0, _property_value_response(None)))
    result = await task

    assert result.extended_frames is False
    assert result.max_frame_length == 15
    assert result.local_length == 254
    assert result.target_length is None


async def test_target_value_le_15_disables_extended_frames() -> None:
    """A target whose PID_MAX_APDU_LENGTH is ≤ 15 disables extended frames."""
    xknx = XKNX()
    xknx.cemi_handler = AsyncMock()
    target = IndividualAddress("1.1.5")

    task = asyncio.create_task(nm_discover_max_apdu_length(xknx, target))
    await asyncio.sleep(0)
    xknx.management.process(_ack(target, 0))
    xknx.management.process(_response(target, 0, _property_value_response(14)))
    result = await task

    assert result.extended_frames is False
    assert result.max_frame_length == 15
    assert result.local_length == 254
    assert result.target_length == 14


async def test_local_and_target_extended_returns_minimum() -> None:
    """When local and target both support extended frames the minimum is taken."""
    xknx = XKNX()
    xknx.cemi_handler = AsyncMock()
    target = IndividualAddress("1.1.5")

    expected_request = Telegram(
        destination_address=target,
        tpci=tpci.TDataConnected(0),
        payload=apci.PropertyValueRead(
            object_index=0, property_id=56, count=1, start_index=1
        ),
    )

    task = asyncio.create_task(nm_discover_max_apdu_length(xknx, target, couplers=[]))
    await asyncio.sleep(0)
    # First telegram out is TConnect, second is the PropertyValueRead.
    sent = xknx.cemi_handler.send_telegram.call_args_list
    assert call(expected_request) in sent

    xknx.management.process(_ack(target, 0))
    xknx.management.process(_response(target, 0, _property_value_response(55)))
    result = await task

    assert result.extended_frames is True
    assert result.max_frame_length == 55
    assert result.local_length == 254
    assert result.target_length == 55
    assert result.coupler_lengths == ()


# --- §2.6.2.3 in-between coupler walk -----------------------------------------


async def _yield_many(times: int = 10) -> None:
    """Yield control to the event loop several times to let chained awaits run."""
    for _ in range(times):
        await asyncio.sleep(0)


async def _feed_target_property(
    xknx: XKNX, target: IndividualAddress, value: int
) -> None:
    """Feed the ack+response pair for the target's PID_MAX_APDU_LENGTH read."""
    await _yield_many()
    xknx.management.process(_ack(target, 0))
    xknx.management.process(_response(target, 0, _property_value_response(value)))


async def _feed_descriptor_response(
    xknx: XKNX, coupler: IndividualAddress, sequence: int, value: int
) -> None:
    """Feed the ack+response pair for a DeviceDescriptorRead(0) on the coupler."""
    await _yield_many()
    xknx.management.process(_ack(coupler, sequence))
    xknx.management.process(
        _response(
            coupler,
            sequence,
            apci.DeviceDescriptorResponse(descriptor=0, value=value),
        )
    )


async def _feed_scan_step_match(
    xknx: XKNX,
    coupler: IndividualAddress,
    description_sequence: int,
    value_sequence: int,
    object_type: int,
) -> None:
    """
    Feed responses for one scan iteration that matches ``object_type``.

    Emits ``A_PropertyDescription_Response(PID=1)`` followed by
    ``A_PropertyValue_Response`` carrying the 2-octet object type.
    """
    await _yield_many()
    xknx.management.process(_ack(coupler, description_sequence))
    xknx.management.process(
        _response(
            coupler,
            description_sequence,
            apci.PropertyDescriptionResponse(
                object_index=0, property_id=1, property_index=0
            ),
        )
    )
    await _yield_many()
    xknx.management.process(_ack(coupler, value_sequence))
    xknx.management.process(
        _response(
            coupler,
            value_sequence,
            apci.PropertyValueResponse(
                object_index=0,
                property_id=1,
                count=1,
                start_index=1,
                data=object_type.to_bytes(2, byteorder="big"),
            ),
        )
    )


async def _feed_property_value(
    xknx: XKNX, coupler: IndividualAddress, sequence: int, value: int | None
) -> None:
    """Feed responses for a property value read; ``value=None`` encodes count=0."""
    await _yield_many()
    xknx.management.process(_ack(coupler, sequence))
    if value is None:
        payload = apci.PropertyValueResponse(
            object_index=0, property_id=0, count=0, start_index=0, data=b""
        )
    else:
        payload = apci.PropertyValueResponse(
            object_index=0,
            property_id=0,
            count=1,
            start_index=1,
            data=value.to_bytes(2, byteorder="big"),
        )
    xknx.management.process(_response(coupler, sequence, payload))


async def test_coupler_dd0_0910h_disables_extended_frames() -> None:
    """A coupler with DD0=0x0910 (Coupler 1.0) forces extended_frames=False."""
    xknx = XKNX()
    xknx.cemi_handler = AsyncMock()
    target = IndividualAddress("1.1.5")
    coupler = IndividualAddress("1.2.0")

    task = asyncio.create_task(
        nm_discover_max_apdu_length(xknx, target, couplers=[coupler])
    )
    await _feed_target_property(xknx, target, 254)
    await _feed_descriptor_response(xknx, coupler, sequence=0, value=0x0910)
    result = await task

    assert result.extended_frames is False
    assert result.max_frame_length == 15
    assert result.target_length == 254
    assert result.coupler_lengths == ()


async def test_coupler_dd0_0911h_disables_extended_frames() -> None:
    """A coupler with DD0=0x0911 (Coupler 1.1) forces extended_frames=False."""
    xknx = XKNX()
    xknx.cemi_handler = AsyncMock()
    target = IndividualAddress("1.1.5")
    coupler = IndividualAddress("1.2.0")

    task = asyncio.create_task(
        nm_discover_max_apdu_length(xknx, target, couplers=[coupler])
    )
    await _feed_target_property(xknx, target, 254)
    await _feed_descriptor_response(xknx, coupler, sequence=0, value=0x0911)
    result = await task

    assert result.extended_frames is False
    assert result.coupler_lengths == ()


async def test_coupler_router_object_property_taken() -> None:
    """When the Router Object exposes PID 58, that value is taken for the coupler."""
    xknx = XKNX()
    xknx.cemi_handler = AsyncMock()
    target = IndividualAddress("1.1.5")
    coupler = IndividualAddress("1.2.0")

    task = asyncio.create_task(
        nm_discover_max_apdu_length(xknx, target, couplers=[coupler])
    )
    await _feed_target_property(xknx, target, 254)
    # Coupler responses, in order: DD0=0x57B0 (extended-capable), scan finds
    # Router Object at index 0, PID 58 returns 64.
    await _feed_descriptor_response(xknx, coupler, sequence=0, value=0x57B0)
    await _feed_scan_step_match(
        xknx,
        coupler,
        description_sequence=1,
        value_sequence=2,
        object_type=0x0006,
    )
    await _feed_property_value(xknx, coupler, sequence=3, value=64)
    result = await task

    assert result.extended_frames is True
    assert result.max_frame_length == 64
    assert result.target_length == 254
    assert result.coupler_lengths == ((coupler, 64),)


async def test_coupler_router_property_missing_falls_back_to_device_object() -> None:
    """When PID 58 is absent on the Router Object, fall back to PID 56 on the Device Object."""
    xknx = XKNX()
    xknx.cemi_handler = AsyncMock()
    target = IndividualAddress("1.1.5")
    coupler = IndividualAddress("1.2.0")

    task = asyncio.create_task(
        nm_discover_max_apdu_length(xknx, target, couplers=[coupler])
    )
    await _feed_target_property(xknx, target, 254)
    await _feed_descriptor_response(xknx, coupler, sequence=0, value=0x57B0)
    await _feed_scan_step_match(
        xknx,
        coupler,
        description_sequence=1,
        value_sequence=2,
        object_type=0x0006,
    )
    # PID 58 on Router Object missing (count=0)
    await _feed_property_value(xknx, coupler, sequence=3, value=None)
    # Fallback: PID 56 on Device Object returns 128
    await _feed_property_value(xknx, coupler, sequence=4, value=128)
    result = await task

    assert result.extended_frames is True
    assert result.max_frame_length == 128
    assert result.coupler_lengths == ((coupler, 128),)


async def test_explicit_couplers_override_derivation() -> None:
    """An explicit coupler list bypasses the auto-derived topology walk."""
    xknx = XKNX()
    xknx.cemi_handler = AsyncMock()
    # current_address is in area 3 — auto-derivation would normally yield
    # [1.0.0, 1.1.0] for a target at 1.1.5; the explicit list overrides this.
    xknx.current_address = IndividualAddress("3.1.255")
    target = IndividualAddress("1.1.5")
    overridden_coupler = IndividualAddress("9.9.0")

    task = asyncio.create_task(
        nm_discover_max_apdu_length(xknx, target, couplers=[overridden_coupler])
    )
    await _feed_target_property(xknx, target, 254)
    # Only the overridden coupler is probed — assertions on send_telegram
    # would show no traffic to 1.0.0 or 1.1.0.
    await _feed_descriptor_response(xknx, overridden_coupler, sequence=0, value=0x0910)
    result = await task

    assert result.extended_frames is False
    sent_destinations = {
        c.args[0].destination_address
        for c in xknx.cemi_handler.send_telegram.call_args_list
    }
    assert IndividualAddress("1.0.0") not in sent_destinations
    assert IndividualAddress("1.1.0") not in sent_destinations
    assert overridden_coupler in sent_destinations
