"""Tests for dm_lc_ext_mem_open — KNX 03.05.02 §3.44 DM_LCExtMemOpen."""

import pytest

from xknx.management.procedures.dm.dm_lc_ext_mem_open import dm_lc_ext_mem_open

pytestmark = pytest.mark.skip(reason="dm_lc_ext_mem_open — implementation pending")


async def test_dm_lc_ext_mem_open_placeholder() -> None:
    """Placeholder for §3.44 DM_LCExtMemOpen scenarios. Add real cases when impl lands."""
    _ = dm_lc_ext_mem_open  # silence unused-import for the skipped test
