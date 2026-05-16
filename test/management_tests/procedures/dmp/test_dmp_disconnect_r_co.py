"""Tests for dmp_disconnect_r_co — KNX 03.05.02 §3.3.2 DMP_Disconnect_RCo."""

import pytest

from xknx.management.procedures.dmp.dmp_disconnect_r_co import dmp_disconnect_r_co

pytestmark = pytest.mark.skip(reason="dmp_disconnect_r_co — implementation pending")


async def test_dmp_disconnect_r_co_placeholder() -> None:
    """Placeholder for §3.3.2 DMP_Disconnect_RCo scenarios. Add real cases when impl lands."""
    _ = dmp_disconnect_r_co  # silence unused-import for the skipped test
