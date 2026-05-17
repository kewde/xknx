"""Tests for dm_secure_sync_sbc — KNX 03.05.02 §4.1 DM_SecureSync_SBC."""

import pytest

from xknx.management.procedures.dm.dm_secure_sync_sbc import dm_secure_sync_sbc

pytestmark = pytest.mark.skip(reason="dm_secure_sync_sbc — implementation pending")


async def test_dm_secure_sync_sbc_placeholder() -> None:
    """Placeholder for §4.1 DM_SecureSync_SBC scenarios. Add real cases when impl lands."""
    _ = dm_secure_sync_sbc  # silence unused-import for the skipped test
