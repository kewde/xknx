"""Tests for dm_user_mem_read — KNX 03.05.02 §3.21 DM_UserMemRead."""

import pytest

from xknx.management.procedures.dm.dm_user_mem_read import dm_user_mem_read

pytestmark = pytest.mark.skip(reason="dm_user_mem_read — implementation pending")


async def test_dm_user_mem_read_placeholder() -> None:
    """Placeholder for §3.21 DM_UserMemRead scenarios. Add real cases when impl lands."""
    _ = dm_user_mem_read  # silence unused-import for the skipped test
