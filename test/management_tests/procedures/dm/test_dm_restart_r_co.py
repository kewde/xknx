"""Tests for dm_restart_r_co — KNX 03.05.02 §3.7.3 DM_Restart_RCo."""

import pytest

from xknx.management.procedures.dm.dm_restart_r_co import dm_restart_r_co

pytestmark = pytest.mark.skip(reason="dm_restart_r_co — implementation pending")


async def test_dm_restart_r_co_placeholder() -> None:
    """Placeholder for §3.7.3 DM_Restart_RCo scenarios. Add real cases when impl lands."""
    _ = dm_restart_r_co  # silence unused-import for the skipped test
