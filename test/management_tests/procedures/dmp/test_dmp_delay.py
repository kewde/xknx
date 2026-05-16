"""Tests for dmp_delay — KNX 03.05.02 §3.8.2 DMP_Delay."""

import pytest

from xknx.management.procedures.dmp.dmp_delay import dmp_delay

pytestmark = pytest.mark.skip(reason="dmp_delay — implementation pending")


async def test_dmp_delay_placeholder() -> None:
    """Placeholder for §3.8.2 DMP_Delay scenarios. Add real cases when impl lands."""
    _ = dmp_delay  # silence unused-import for the skipped test
