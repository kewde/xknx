"""Tests for dmp_interface_object_write_r — KNX 03.05.02 §3.25.2 DMP_InterfaceObjectWrite_R."""

import pytest

from xknx.management.procedures.dmp.dmp_interface_object_write_r import (
    dmp_interface_object_write_r,
)

pytestmark = pytest.mark.skip(
    reason="dmp_interface_object_write_r — implementation pending"
)


async def test_dmp_interface_object_write_r_placeholder() -> None:
    """Placeholder for §3.25.2 DMP_InterfaceObjectWrite_R scenarios. Add real cases when impl lands."""
    _ = dmp_interface_object_write_r  # silence unused-import for the skipped test
