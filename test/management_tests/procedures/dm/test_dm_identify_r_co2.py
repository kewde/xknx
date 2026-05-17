"""Tests for dm_identify_r_co2 — KNX 03.05.02 §3.4.3 DM_Identify_RCo2."""

import pytest

from xknx.management.procedures.dm.dm_identify_r_co2 import dm_identify_r_co2

pytestmark = pytest.mark.skip(reason="dm_identify_r_co2 — implementation pending")


async def test_dm_identify_r_co2_placeholder() -> None:
    """Placeholder for §3.4.3 DM_Identify_RCo2 scenarios. Add real cases when impl lands."""
    _ = dm_identify_r_co2  # silence unused-import for the skipped test
