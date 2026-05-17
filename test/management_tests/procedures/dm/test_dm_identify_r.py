"""Tests for dm_identify_r — KNX 03.05.02 §3.4.2 DM_Identify_R."""

import pytest

from xknx.management.procedures.dm.dm_identify_r import dm_identify_r

pytestmark = pytest.mark.skip(reason="dm_identify_r — implementation pending")


async def test_dm_identify_r_placeholder() -> None:
    """Placeholder for §3.4.2 DM_Identify_R scenarios. Add real cases when impl lands."""
    _ = dm_identify_r  # silence unused-import for the skipped test
