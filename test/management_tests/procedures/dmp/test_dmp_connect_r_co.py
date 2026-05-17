"""Tests for dmp_connect_r_co — KNX 03.05.02 §3.2.1 DMP_Connect_RCo."""

import pytest

from xknx.management.procedures.dmp.dmp_connect_r_co import dmp_connect_r_co

pytestmark = pytest.mark.skip(reason="dmp_connect_r_co — implementation pending")


async def test_dmp_connect_r_co_placeholder() -> None:
    """Placeholder for §3.2.1 DMP_Connect_RCo scenarios. Add real cases when impl lands."""
    _ = dmp_connect_r_co  # silence unused-import for the skipped test
