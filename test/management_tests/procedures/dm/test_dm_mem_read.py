"""Tests for dm_mem_read — KNX 03.05.02 §3.18 DM_MemRead."""

import pytest

from xknx.management.procedures.dm.dm_mem_read import dm_mem_read

pytestmark = pytest.mark.skip(reason="dm_mem_read — implementation pending")


async def test_dm_mem_read_placeholder() -> None:
    """Placeholder for §3.18 DM_MemRead scenarios. Add real cases when impl lands."""
    _ = dm_mem_read  # silence unused-import for the skipped test
