"""Tests for dmp_ext_interface_object_read_r — KNX 03.05.02 §3.27.4 DMP_ExtInterfaceObjectRead_R."""

import pytest

from xknx.management.procedures.dmp.dmp_ext_interface_object_read_r import (
    dmp_ext_interface_object_read_r,
)

pytestmark = pytest.mark.skip(
    reason="dmp_ext_interface_object_read_r — implementation pending"
)


async def test_dmp_ext_interface_object_read_r_placeholder() -> None:
    """Placeholder for §3.27.4 DMP_ExtInterfaceObjectRead_R scenarios. Add real cases when impl lands."""
    _ = dmp_ext_interface_object_read_r  # silence unused-import for the skipped test
