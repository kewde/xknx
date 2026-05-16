"""Tests for nm_subnetwork_devices_scan2 — KNX 03.05.02 §2.17 NM_SubnetworkDevices_Scan2."""

import pytest

from xknx.management.procedures.nm.nm_subnetwork_devices_scan2 import (
    nm_subnetwork_devices_scan2,
)

pytestmark = pytest.mark.skip(
    reason="nm_subnetwork_devices_scan2 — implementation pending"
)


async def test_nm_subnetwork_devices_scan2_placeholder() -> None:
    """Placeholder for §2.17 NM_SubnetworkDevices_Scan2 scenarios. Add real cases when impl lands."""
    _ = nm_subnetwork_devices_scan2  # silence unused-import for the skipped test
