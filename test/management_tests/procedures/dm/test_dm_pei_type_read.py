"""Tests for dm_pei_type_read — KNX 03.05.02 §3.15 DM_PeiTypeRead."""

import pytest

from xknx.management.procedures.dm.dm_pei_type_read import dm_pei_type_read

pytestmark = pytest.mark.skip(reason="dm_pei_type_read — implementation pending")


async def test_dm_pei_type_read_placeholder() -> None:
    """Placeholder for §3.15 DM_PeiTypeRead scenarios. Add real cases when impl lands."""
    _ = dm_pei_type_read  # silence unused-import for the skipped test
