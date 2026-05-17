"""Tests for dmp_interface_object_read_r — KNX 03.05.02 §3.27.2 DMP_InterfaceObjectRead_R."""

import pytest

from xknx.management.procedures.dmp.dmp_interface_object_read_r import (
    dmp_interface_object_read_r,
)

pytestmark = pytest.mark.skip(
    reason="dmp_interface_object_read_r — implementation pending"
)


async def test_dmp_interface_object_read_r_placeholder() -> None:
    """Placeholder for §3.27.2 DMP_InterfaceObjectRead_R scenarios. Add real cases when impl lands."""
    _ = dmp_interface_object_read_r  # silence unused-import for the skipped test
