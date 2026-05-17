"""Tests for dm_restart_r_cl — KNX 03.05.02 §3.7.2 DM_Restart_RCl."""

import pytest

from xknx.management.procedures.dm.dm_restart_r_cl import dm_restart_r_cl

pytestmark = pytest.mark.skip(reason="dm_restart_r_cl — implementation pending")


async def test_dm_restart_r_cl_placeholder() -> None:
    """Placeholder for §3.7.2 DM_Restart_RCl scenarios. Add real cases when impl lands."""
    _ = dm_restart_r_cl  # silence unused-import for the skipped test
