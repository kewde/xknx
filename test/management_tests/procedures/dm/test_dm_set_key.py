"""Tests for dm_set_key — KNX 03.05.02 §3.6 DM_SetKey."""

import pytest

from xknx.management.procedures.dm.dm_set_key import dm_set_key

pytestmark = pytest.mark.skip(reason="dm_set_key — implementation pending")


async def test_dm_set_key_placeholder() -> None:
    """Placeholder for §3.6 DM_SetKey scenarios. Add real cases when impl lands."""
    _ = dm_set_key  # silence unused-import for the skipped test
