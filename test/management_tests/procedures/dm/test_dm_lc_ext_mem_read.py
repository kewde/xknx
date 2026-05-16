"""Tests for dm_lc_ext_mem_read — KNX 03.05.02 §3.43 DM_LCExtMemRead."""

import pytest

from xknx.management.procedures.dm.dm_lc_ext_mem_read import dm_lc_ext_mem_read

pytestmark = pytest.mark.skip(reason="dm_lc_ext_mem_read — implementation pending")


async def test_dm_lc_ext_mem_read_placeholder() -> None:
    """Placeholder for §3.43 DM_LCExtMemRead scenarios. Add real cases when impl lands."""
    _ = dm_lc_ext_mem_read  # silence unused-import for the skipped test
