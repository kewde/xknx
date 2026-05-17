"""Tests for dmp_user_mem_write_r_co_v — KNX 03.05.02 §3.19.3 DMP_UserMemWrite_RCoV."""

import pytest

from xknx.management.procedures.dmp.dmp_user_mem_write_r_co_v import (
    dmp_user_mem_write_r_co_v,
)

pytestmark = pytest.mark.skip(
    reason="dmp_user_mem_write_r_co_v — implementation pending"
)


async def test_dmp_user_mem_write_r_co_v_placeholder() -> None:
    """Placeholder for §3.19.3 DMP_UserMemWrite_RCoV scenarios. Add real cases when impl lands."""
    _ = dmp_user_mem_write_r_co_v  # silence unused-import for the skipped test
