"""Tests for dmp_connect_lc_emi — KNX 03.05.02 §3.2.5 DMP_Connect_LcEMI."""

import pytest

from xknx.management.procedures.dmp.dmp_connect_lc_emi import dmp_connect_lc_emi

pytestmark = pytest.mark.skip(reason="dmp_connect_lc_emi — implementation pending")


async def test_dmp_connect_lc_emi_placeholder() -> None:
    """Placeholder for §3.2.5 DMP_Connect_LcEMI scenarios. Add real cases when impl lands."""
    _ = dmp_connect_lc_emi  # silence unused-import for the skipped test
