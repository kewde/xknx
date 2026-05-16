"""Tests for dmp_ext_function_property_write_r — KNX 03.05.02 §3.30.2 DMP_ExtFunctionProperty_Write_R."""

import pytest

from xknx.management.procedures.dmp.dmp_ext_function_property_write_r import (
    dmp_ext_function_property_write_r,
)

pytestmark = pytest.mark.skip(
    reason="dmp_ext_function_property_write_r — implementation pending"
)


async def test_dmp_ext_function_property_write_r_placeholder() -> None:
    """Placeholder for §3.30.2 DMP_ExtFunctionProperty_Write_R scenarios. Add real cases when impl lands."""
    _ = dmp_ext_function_property_write_r  # silence unused-import for the skipped test
