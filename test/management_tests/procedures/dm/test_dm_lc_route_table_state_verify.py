"""Tests for dm_lc_route_table_state_verify — KNX 03.05.02 §3.46 DM_LCRouteTableStateVerify."""

import pytest

from xknx.management.procedures.dm.dm_lc_route_table_state_verify import (
    dm_lc_route_table_state_verify,
)

pytestmark = pytest.mark.skip(
    reason="dm_lc_route_table_state_verify — implementation pending"
)


async def test_dm_lc_route_table_state_verify_placeholder() -> None:
    """Placeholder for §3.46 DM_LCRouteTableStateVerify scenarios. Add real cases when impl lands."""
    _ = dm_lc_route_table_state_verify  # silence unused-import for the skipped test
