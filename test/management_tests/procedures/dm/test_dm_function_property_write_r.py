"""Tests for dm_function_property_write_r — KNX 03.05.02 §3.30 DM_FunctionProperty_Write_R."""

import pytest

from xknx.management.procedures.dm.dm_function_property_write_r import (
    dm_function_property_write_r,
)

pytestmark = pytest.mark.skip(
    reason="dm_function_property_write_r — implementation pending"
)


async def test_dm_function_property_write_r_placeholder() -> None:
    """Placeholder for §3.30 DM_FunctionProperty_Write_R scenarios. Add real cases when impl lands."""
    _ = dm_function_property_write_r  # silence unused-import for the skipped test
