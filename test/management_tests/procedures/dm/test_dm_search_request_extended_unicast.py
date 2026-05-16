"""Tests for dm_search_request_extended_unicast — KNX 03.05.02 §6.2 DM_SearchRequestExtended_Unicast."""

import pytest

from xknx.management.procedures.dm.dm_search_request_extended_unicast import (
    dm_search_request_extended_unicast,
)

pytestmark = pytest.mark.skip(
    reason="dm_search_request_extended_unicast — implementation pending"
)


async def test_dm_search_request_extended_unicast_placeholder() -> None:
    """Placeholder for §6.2 DM_SearchRequestExtended_Unicast scenarios. Add real cases when impl lands."""
    _ = dm_search_request_extended_unicast  # silence unused-import for the skipped test
