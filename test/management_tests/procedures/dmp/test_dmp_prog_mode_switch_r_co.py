"""Tests for dmp_prog_mode_switch_r_co — KNX 03.05.02 §3.13.2 DMP_ProgModeSwitch_RCo."""

import pytest

from xknx.management.procedures.dmp.dmp_prog_mode_switch_r_co import (
    dmp_prog_mode_switch_r_co,
)

pytestmark = pytest.mark.skip(
    reason="dmp_prog_mode_switch_r_co — implementation pending"
)


async def test_dmp_prog_mode_switch_r_co_placeholder() -> None:
    """Placeholder for §3.13.2 DMP_ProgModeSwitch_RCo scenarios. Add real cases when impl lands."""
    _ = dmp_prog_mode_switch_r_co  # silence unused-import for the skipped test
