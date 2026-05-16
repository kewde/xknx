"""Tests for dmp_user_mem_write_r_co — KNX 03.05.02 §3.19.2 DMP_UserMemWrite_RCo."""

import pytest

from xknx.management.procedures.dmp.dmp_user_mem_write_r_co import (
    dmp_user_mem_write_r_co,
)

pytestmark = pytest.mark.skip(reason="dmp_user_mem_write_r_co — implementation pending")


async def test_dmp_user_mem_write_r_co_placeholder() -> None:
    """Placeholder for §3.19.2 DMP_UserMemWrite_RCo scenarios. Add real cases when impl lands."""
    _ = dmp_user_mem_write_r_co  # silence unused-import for the skipped test
