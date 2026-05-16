"""Tests for dm_prog_mode_switch — KNX 03.05.02 §3.13 DM_ProgMode_Switch."""

import pytest

from xknx.management.procedures.dm.dm_prog_mode_switch import dm_prog_mode_switch

pytestmark = pytest.mark.skip(reason="dm_prog_mode_switch — implementation pending")


async def test_dm_prog_mode_switch_placeholder() -> None:
    """Placeholder for §3.13 DM_ProgMode_Switch scenarios. Add real cases when impl lands."""
    _ = dm_prog_mode_switch  # silence unused-import for the skipped test
