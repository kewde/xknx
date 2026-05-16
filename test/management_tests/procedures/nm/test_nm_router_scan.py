"""Tests for nm_router_scan — KNX 03.05.02 §2.15 NM_Router_Scan."""

import pytest

from xknx.management.procedures.nm.nm_router_scan import nm_router_scan

pytestmark = pytest.mark.skip(reason="nm_router_scan — implementation pending")


async def test_nm_router_scan_placeholder() -> None:
    """Placeholder for §2.15 NM_Router_Scan scenarios. Add real cases when impl lands."""
    _ = nm_router_scan  # silence unused-import for the skipped test
