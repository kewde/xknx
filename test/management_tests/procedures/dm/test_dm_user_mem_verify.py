"""Tests for dm_user_mem_verify — KNX 03.05.02 §3.20 DM_UserMemVerify."""

import pytest

from xknx.management.procedures.dm.dm_user_mem_verify import dm_user_mem_verify

pytestmark = pytest.mark.skip(reason="dm_user_mem_verify — implementation pending")


async def test_dm_user_mem_verify_placeholder() -> None:
    """Placeholder for §3.20 DM_UserMemVerify scenarios. Add real cases when impl lands."""
    _ = dm_user_mem_verify  # silence unused-import for the skipped test
