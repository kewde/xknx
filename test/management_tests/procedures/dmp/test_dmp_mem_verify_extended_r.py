"""Tests for dmp_mem_verify_extended_r — KNX 03.05.02 §3.23 DMP_MemVerify_Extended_R."""

import pytest

from xknx.management.procedures.dmp.dmp_mem_verify_extended_r import (
    dmp_mem_verify_extended_r,
)

pytestmark = pytest.mark.skip(
    reason="dmp_mem_verify_extended_r — implementation pending"
)


async def test_dmp_mem_verify_extended_r_placeholder() -> None:
    """Placeholder for §3.23 DMP_MemVerify_Extended_R scenarios. Add real cases when impl lands."""
    _ = dmp_mem_verify_extended_r  # silence unused-import for the skipped test
