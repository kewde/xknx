"""Tests for dmp_ext_interface_object_write_con_r — KNX 03.05.02 §3.25.4 DMP_ExtInterfaceObjectWriteCon_R."""

import pytest

from xknx.management.procedures.dmp.dmp_ext_interface_object_write_con_r import (
    dmp_ext_interface_object_write_con_r,
)

pytestmark = pytest.mark.skip(
    reason="dmp_ext_interface_object_write_con_r — implementation pending"
)


async def test_dmp_ext_interface_object_write_con_r_placeholder() -> None:
    """Placeholder for §3.25.4 DMP_ExtInterfaceObjectWriteCon_R scenarios. Add real cases when impl lands."""
    _ = dmp_ext_interface_object_write_con_r  # silence unused-import for the skipped test
