"""Tests for dm_authorize — KNX 03.05.02 §3.5 DM_Authorize."""

import pytest

from xknx.management.procedures.dm.dm_authorize import dm_authorize

pytestmark = pytest.mark.skip(reason="dm_authorize — implementation pending")


async def test_dm_authorize_placeholder() -> None:
    """Placeholder for §3.5 DM_Authorize scenarios. Add real cases when impl lands."""
    _ = dm_authorize  # silence unused-import for the skipped test
