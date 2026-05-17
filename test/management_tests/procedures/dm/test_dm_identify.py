"""Tests for dm_identify — KNX 03.05.02 §3.4 DM_Identify."""

import pytest

from xknx.management.procedures.dm.dm_identify import dm_identify

pytestmark = pytest.mark.skip(reason="dm_identify — implementation pending")


async def test_dm_identify_placeholder() -> None:
    """Placeholder for §3.4 DM_Identify scenarios. Add real cases when impl lands."""
    _ = dm_identify  # silence unused-import for the skipped test
