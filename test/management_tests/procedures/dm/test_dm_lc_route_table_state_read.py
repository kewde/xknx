"""Tests for dm_lc_route_table_state_read — KNX 03.05.02 §3.47 DM_LCRouteTableStateRead."""

import pytest

from xknx.management.procedures.dm.dm_lc_route_table_state_read import (
    dm_lc_route_table_state_read,
)

pytestmark = pytest.mark.skip(
    reason="dm_lc_route_table_state_read — implementation pending"
)


async def test_dm_lc_route_table_state_read_placeholder() -> None:
    """Placeholder for §3.47 DM_LCRouteTableStateRead scenarios. Add real cases when impl lands."""
    _ = dm_lc_route_table_state_read  # silence unused-import for the skipped test
