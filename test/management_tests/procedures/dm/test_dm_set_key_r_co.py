"""Tests for dm_set_key_r_co — KNX 03.05.02 §3.6.1 DM_SetKey_RCo."""

import pytest

from xknx.management.procedures.dm.dm_set_key_r_co import dm_set_key_r_co

pytestmark = pytest.mark.skip(reason="dm_set_key_r_co — implementation pending")


async def test_dm_set_key_r_co_placeholder() -> None:
    """Placeholder for §3.6.1 DM_SetKey_RCo scenarios. Add real cases when impl lands."""
    _ = dm_set_key_r_co  # silence unused-import for the skipped test
