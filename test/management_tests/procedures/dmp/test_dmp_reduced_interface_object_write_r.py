"""Tests for dmp_reduced_interface_object_write_r — KNX 03.05.02 §3.25.3 DMP_ReducedInterfaceObjectWrite_R."""

import pytest

from xknx.management.procedures.dmp.dmp_reduced_interface_object_write_r import (
    dmp_reduced_interface_object_write_r,
)

pytestmark = pytest.mark.skip(
    reason="dmp_reduced_interface_object_write_r — implementation pending"
)


async def test_dmp_reduced_interface_object_write_r_placeholder() -> None:
    """Placeholder for §3.25.3 DMP_ReducedInterfaceObjectWrite_R scenarios. Add real cases when impl lands."""
    _ = dmp_reduced_interface_object_write_r  # silence unused-import for the skipped test
