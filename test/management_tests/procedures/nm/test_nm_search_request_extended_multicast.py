"""Tests for nm_search_request_extended_multicast — KNX 03.05.02 §6.1 NM_SearchRequestExtended_Multicast."""

import pytest

from xknx.management.procedures.nm.nm_search_request_extended_multicast import (
    nm_search_request_extended_multicast,
)

pytestmark = pytest.mark.skip(
    reason="nm_search_request_extended_multicast — implementation pending"
)


async def test_nm_search_request_extended_multicast_placeholder() -> None:
    """Placeholder for §6.1 NM_SearchRequestExtended_Multicast scenarios. Add real cases when impl lands."""
    _ = nm_search_request_extended_multicast  # silence unused-import for the skipped test
