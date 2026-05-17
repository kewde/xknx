"""Tests for dm_secure_sync_r_cl — KNX 03.05.02 §4.2 DM_SecureSync_RCl."""

import pytest

from xknx.management.procedures.dm.dm_secure_sync_r_cl import dm_secure_sync_r_cl

pytestmark = pytest.mark.skip(reason="dm_secure_sync_r_cl — implementation pending")


async def test_dm_secure_sync_r_cl_placeholder() -> None:
    """Placeholder for §4.2 DM_SecureSync_RCl scenarios. Add real cases when impl lands."""
    _ = dm_secure_sync_r_cl  # silence unused-import for the skipped test
