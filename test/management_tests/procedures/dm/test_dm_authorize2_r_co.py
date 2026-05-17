"""Tests for dmp_authorize2_r_co — KNX 03.05.02 §3.5.2 DM_Authorize2_RCo."""

import pytest

from xknx.management.procedures.dm.dm_authorize2_r_co import dmp_authorize2_r_co

pytestmark = pytest.mark.skip(
    reason="dmp_authorize2_r_co — tests in test_dm_authorize.py"
)


async def test_dmp_authorize2_r_co_placeholder() -> None:
    """Tests for §3.5.2 DM_Authorize2_RCo are in test_dm_authorize.py."""
    _ = dmp_authorize2_r_co
