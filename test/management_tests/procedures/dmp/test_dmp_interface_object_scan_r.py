"""Tests for dmp_interface_object_scan_r — KNX 03.05.02 §3.28.2 DMP_InterfaceObjectScan_R."""

import pytest

from xknx.management.procedures.dmp.dmp_interface_object_scan_r import (
    dmp_interface_object_scan_r,
)

pytestmark = pytest.mark.skip(
    reason="dmp_interface_object_scan_r — implementation pending"
)


async def test_dmp_interface_object_scan_r_placeholder() -> None:
    """Placeholder for §3.28.2 DMP_InterfaceObjectScan_R scenarios. Add real cases when impl lands."""
    _ = dmp_interface_object_scan_r  # silence unused-import for the skipped test
