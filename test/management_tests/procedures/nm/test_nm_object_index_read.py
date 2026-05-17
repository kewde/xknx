"""Tests for nm_object_index_read — KNX 03.05.02 §2.23.4 NM_ObjectIndex_Read."""

import pytest

from xknx.management.procedures.nm.nm_object_index_read import nm_object_index_read

pytestmark = pytest.mark.skip(reason="nm_object_index_read — implementation pending")


async def test_nm_object_index_read_placeholder() -> None:
    """Placeholder for §2.23.4 NM_ObjectIndex_Read scenarios. Add real cases when impl lands."""
    _ = nm_object_index_read  # silence unused-import for the skipped test
