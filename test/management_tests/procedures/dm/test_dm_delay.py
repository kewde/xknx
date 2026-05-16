"""Tests for dm_delay — KNX 03.05.02 §3.8 DM_Delay."""

import pytest

from xknx.management.procedures.dm.dm_delay import dm_delay

pytestmark = pytest.mark.skip(reason="dm_delay — implementation pending")


async def test_dm_delay_placeholder() -> None:
    """Placeholder for §3.8 DM_Delay scenarios. Add real cases when impl lands."""
    _ = dm_delay  # silence unused-import for the skipped test
