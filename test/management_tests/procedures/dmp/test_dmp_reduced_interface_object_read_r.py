"""Tests for dmp_reduced_interface_object_read_r — KNX 03.05.02 §3.27.3 DMP_ReducedInterfaceObjectRead_R."""

import pytest

from xknx.management.procedures.dmp.dmp_reduced_interface_object_read_r import (
    dmp_reduced_interface_object_read_r,
)

pytestmark = pytest.mark.skip(
    reason="dmp_reduced_interface_object_read_r — implementation pending"
)


async def test_dmp_reduced_interface_object_read_r_placeholder() -> None:
    """Placeholder for §3.27.3 DMP_ReducedInterfaceObjectRead_R scenarios. Add real cases when impl lands."""
    _ = dmp_reduced_interface_object_read_r  # silence unused-import for the skipped test
