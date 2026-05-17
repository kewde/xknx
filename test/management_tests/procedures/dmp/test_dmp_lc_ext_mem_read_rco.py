"""Tests for dmp_lc_ext_mem_read_rco — KNX 03.05.02 §3.43.2 DMP_LCExtMemRead_Rco."""

import pytest

from xknx.management.procedures.dmp.dmp_lc_ext_mem_read_rco import (
    dmp_lc_ext_mem_read_rco,
)

pytestmark = pytest.mark.skip(reason="dmp_lc_ext_mem_read_rco — implementation pending")


async def test_dmp_lc_ext_mem_read_rco_placeholder() -> None:
    """Placeholder for §3.43.2 DMP_LCExtMemRead_Rco scenarios. Add real cases when impl lands."""
    _ = dmp_lc_ext_mem_read_rco  # silence unused-import for the skipped test
