"""Tests for dmp_ext_interface_object_verify_r — KNX 03.05.02 §3.26.3 DMP_ExtInterfaceObjectVerify_R."""

import pytest

from xknx.management.procedures.dmp.dmp_ext_interface_object_verify_r import (
    dmp_ext_interface_object_verify_r,
)

pytestmark = pytest.mark.skip(
    reason="dmp_ext_interface_object_verify_r — implementation pending"
)


async def test_dmp_ext_interface_object_verify_r_placeholder() -> None:
    """Placeholder for §3.26.3 DMP_ExtInterfaceObjectVerify_R scenarios. Add real cases when impl lands."""
    _ = dmp_ext_interface_object_verify_r  # silence unused-import for the skipped test
