"""Tests for dmp_mem_write_r_co_v — KNX 03.05.02 §3.16.3 DMP_MemWrite_RCoV."""

import pytest

from xknx.management.procedures.dmp.dmp_mem_write_r_co_v import dmp_mem_write_r_co_v

pytestmark = pytest.mark.skip(reason="dmp_mem_write_r_co_v — implementation pending")


async def test_dmp_mem_write_r_co_v_placeholder() -> None:
    """Placeholder for §3.16.3 DMP_MemWrite_RCoV scenarios. Add real cases when impl lands."""
    _ = dmp_mem_write_r_co_v  # silence unused-import for the skipped test
