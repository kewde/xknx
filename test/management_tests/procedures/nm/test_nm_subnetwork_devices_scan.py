"""Tests for nm_subnetwork_devices_scan — KNX 03.05.02 §2.16 NM_SubnetworkDevices_Scan."""

import pytest

from xknx.management.procedures.nm.nm_subnetwork_devices_scan import (
    nm_subnetwork_devices_scan,
)

pytestmark = pytest.mark.skip(
    reason="nm_subnetwork_devices_scan — implementation pending"
)


async def test_nm_subnetwork_devices_scan_placeholder() -> None:
    """Placeholder for §2.16 NM_SubnetworkDevices_Scan scenarios. Add real cases when impl lands."""
    _ = nm_subnetwork_devices_scan  # silence unused-import for the skipped test
