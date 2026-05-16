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

    task = asyncio.create_task(nm_discover_max_apdu_length(xknx, target))
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
