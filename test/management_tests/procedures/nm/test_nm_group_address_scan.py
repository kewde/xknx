"""Tests for nm_group_address_scan — KNX 03.05.02 §2.23.3 NM_GroupAddress_Scan."""

import pytest

from xknx.management.procedures.nm.nm_group_address_scan import nm_group_address_scan

pytestmark = pytest.mark.skip(reason="nm_group_address_scan — implementation pending")


async def test_nm_group_address_scan_placeholder() -> None:
    """Placeholder for §2.23.3 NM_GroupAddress_Scan scenarios. Add real cases when impl lands."""
    _ = nm_group_address_scan  # silence unused-import for the skipped test
