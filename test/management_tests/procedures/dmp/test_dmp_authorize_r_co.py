"""Tests for dmp_authorize_r_co — KNX 03.05.02 §3.5.1 DMP_Authorize_RCo."""

import pytest

from xknx.management.procedures.dmp.dmp_authorize_r_co import dmp_authorize_r_co

pytestmark = pytest.mark.skip(reason="dmp_authorize_r_co — implementation pending")


async def test_dmp_authorize_r_co_placeholder() -> None:
    """Placeholder for §3.5.1 DMP_Authorize_RCo scenarios. Add real cases when impl lands."""
    _ = dmp_authorize_r_co  # silence unused-import for the skipped test
