"""Tests for dmp_connect_r_cl — KNX 03.05.02 §3.2.2 DMP_Connect_RCl."""

import pytest

from xknx.management.procedures.dmp.dmp_connect_r_cl import dmp_connect_r_cl

pytestmark = pytest.mark.skip(reason="dmp_connect_r_cl — implementation pending")


async def test_dmp_connect_r_cl_placeholder() -> None:
    """Placeholder for §3.2.2 DMP_Connect_RCl scenarios. Add real cases when impl lands."""
    _ = dmp_connect_r_cl  # silence unused-import for the skipped test
