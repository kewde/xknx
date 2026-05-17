"""Tests for dm_user_mem_write — KNX 03.05.02 §3.19 DM_UserMemWrite."""

import pytest

from xknx.management.procedures.dm.dm_user_mem_write import dm_user_mem_write

pytestmark = pytest.mark.skip(reason="dm_user_mem_write — implementation pending")


async def test_dm_user_mem_write_placeholder() -> None:
    """Placeholder for §3.19 DM_UserMemWrite scenarios. Add real cases when impl lands."""
    _ = dm_user_mem_write  # silence unused-import for the skipped test
