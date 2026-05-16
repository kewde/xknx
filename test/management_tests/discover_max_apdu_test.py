"""
Tests for the §2.6 Discovery of maximal frame length procedure.

Topology helper coverage lands first; the full ``nm_discover_max_apdu_length``
procedure and its three-step walk follow in subsequent commits.
"""

from __future__ import annotations

from xknx.management.procedures import _derive_in_between_couplers
from xknx.telegram import IndividualAddress


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
