"""Tests for dm_restart — KNX 03.05.02 §3.7 DM_Restart."""

import pytest

from xknx.management.procedures.dm.dm_restart import dm_restart

pytestmark = pytest.mark.skip(reason="dm_restart — implementation pending")


async def test_dm_restart_placeholder() -> None:
    """Placeholder for §3.7 DM_Restart scenarios. Add real cases when impl lands."""
    _ = dm_restart  # silence unused-import for the skipped test
