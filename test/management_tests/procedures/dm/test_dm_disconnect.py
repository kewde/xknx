"""Tests for dm_disconnect — KNX 03.05.02 §3.3 DM_Disconnect."""

import pytest

from xknx.management.procedures.dm.dm_disconnect import dm_disconnect

pytestmark = pytest.mark.skip(reason="dm_disconnect — implementation pending")


async def test_dm_disconnect_placeholder() -> None:
    """Placeholder for §3.3 DM_Disconnect scenarios. Add real cases when impl lands."""
    _ = dm_disconnect  # silence unused-import for the skipped test
