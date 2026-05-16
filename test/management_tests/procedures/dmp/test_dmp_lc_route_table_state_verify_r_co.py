"""Tests for dmp_lc_route_table_state_verify_r_co — KNX 03.05.02 §3.46.2 DMP_LCRouteTableStateVerify_RCo."""

import pytest

from xknx.management.procedures.dmp.dmp_lc_route_table_state_verify_r_co import (
    dmp_lc_route_table_state_verify_r_co,
)

pytestmark = pytest.mark.skip(
    reason="dmp_lc_route_table_state_verify_r_co — implementation pending"
)


async def test_dmp_lc_route_table_state_verify_r_co_placeholder() -> None:
    """Placeholder for §3.46.2 DMP_LCRouteTableStateVerify_RCo scenarios. Add real cases when impl lands."""
    _ = dmp_lc_route_table_state_verify_r_co  # silence unused-import for the skipped test
