"""Tests for dmp_lc_ext_mem_write_rco — KNX 03.05.02 §3.41.2 DMP_LCExtMemWrite_Rco."""

import pytest

from xknx.management.procedures.dmp.dmp_lc_ext_mem_write_rco import (
    dmp_lc_ext_mem_write_rco,
)

pytestmark = pytest.mark.skip(
    reason="dmp_lc_ext_mem_write_rco — implementation pending"
)


async def test_dmp_lc_ext_mem_write_rco_placeholder() -> None:
    """Placeholder for §3.41.2 DMP_LCExtMemWrite_Rco scenarios. Add real cases when impl lands."""
    _ = dmp_lc_ext_mem_write_rco  # silence unused-import for the skipped test
