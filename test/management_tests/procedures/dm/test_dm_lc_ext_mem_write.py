"""Tests for dm_lc_ext_mem_write — KNX 03.05.02 §3.41 DM_LCExtMemWrite."""

import pytest

from xknx.management.procedures.dm.dm_lc_ext_mem_write import dm_lc_ext_mem_write

pytestmark = pytest.mark.skip(reason="dm_lc_ext_mem_write — implementation pending")


async def test_dm_lc_ext_mem_write_placeholder() -> None:
    """Placeholder for §3.41 DM_LCExtMemWrite scenarios. Add real cases when impl lands."""
    _ = dm_lc_ext_mem_write  # silence unused-import for the skipped test
