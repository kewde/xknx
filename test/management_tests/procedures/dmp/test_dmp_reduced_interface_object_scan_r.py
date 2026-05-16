"""Tests for dmp_reduced_interface_object_scan_r — KNX 03.05.02 §3.28.3 DMP_ReducedInterfaceObjectScan_R."""

import pytest

from xknx.management.procedures.dmp.dmp_reduced_interface_object_scan_r import (
    dmp_reduced_interface_object_scan_r,
)

pytestmark = pytest.mark.skip(
    reason="dmp_reduced_interface_object_scan_r — implementation pending"
)


async def test_dmp_reduced_interface_object_scan_r_placeholder() -> None:
    """Placeholder for §3.28.3 DMP_ReducedInterfaceObjectScan_R scenarios. Add real cases when impl lands."""
    _ = dmp_reduced_interface_object_scan_r  # silence unused-import for the skipped test
