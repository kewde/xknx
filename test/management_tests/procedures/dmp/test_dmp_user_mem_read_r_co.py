"""Tests for dmp_user_mem_read_r_co — KNX 03.05.02 §3.21.2 DMP_UserMemRead_RCo."""

import pytest

from xknx.management.procedures.dmp.dmp_user_mem_read_r_co import dmp_user_mem_read_r_co

pytestmark = pytest.mark.skip(reason="dmp_user_mem_read_r_co — implementation pending")


async def test_dmp_user_mem_read_r_co_placeholder() -> None:
    """Placeholder for §3.21.2 DMP_UserMemRead_RCo scenarios. Add real cases when impl lands."""
    _ = dmp_user_mem_read_r_co  # silence unused-import for the skipped test
