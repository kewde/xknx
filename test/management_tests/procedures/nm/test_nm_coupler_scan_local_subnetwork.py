"""Tests for nm_coupler_scan_local_subnetwork — KNX 03.05.02 §2.23.5 NM_Coupler_Scan_LocalSubnetwork."""

import pytest

from xknx.management.procedures.nm.nm_coupler_scan_local_subnetwork import (
    nm_coupler_scan_local_subnetwork,
)

pytestmark = pytest.mark.skip(
    reason="nm_coupler_scan_local_subnetwork — implementation pending"
)


async def test_nm_coupler_scan_local_subnetwork_placeholder() -> None:
    """Placeholder for §2.23.5 NM_Coupler_Scan_LocalSubnetwork scenarios. Add real cases when impl lands."""
    _ = nm_coupler_scan_local_subnetwork  # silence unused-import for the skipped test
