"""Tests for the MaxApduResult dataclass."""

from __future__ import annotations

import dataclasses

import pytest

from xknx.management import MaxApduResult
from xknx.telegram import IndividualAddress


def test_result_is_frozen() -> None:
    """MaxApduResult is immutable."""
    result = MaxApduResult(
        extended_frames=True,
        max_frame_length=55,
        local_length=254,
        target_length=55,
        coupler_lengths=(),
    )
    with pytest.raises(dataclasses.FrozenInstanceError):
        result.max_frame_length = 200  # type: ignore[misc]


def test_result_holds_non_extended_floor() -> None:
    """Non-extended outcome carries the L_Data_Standard floor of 15 octets."""
    result = MaxApduResult(
        extended_frames=False,
        max_frame_length=15,
        local_length=15,
        target_length=None,
        coupler_lengths=(),
    )
    assert result.extended_frames is False
    assert result.max_frame_length == 15
    assert result.target_length is None
    assert result.coupler_lengths == ()


def test_result_carries_coupler_chain() -> None:
    """Coupler chain is preserved in path order."""
    couplers = (
        (IndividualAddress("1.0.0"), 220),
        (IndividualAddress("1.2.0"), 55),
    )
    result = MaxApduResult(
        extended_frames=True,
        max_frame_length=55,
        local_length=254,
        target_length=128,
        coupler_lengths=couplers,
    )
    assert result.coupler_lengths == couplers
