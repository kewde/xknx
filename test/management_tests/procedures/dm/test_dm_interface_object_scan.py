"""Tests for dm_interface_object_scan — KNX 03.05.02 §3.28 DM_InterfaceObjectScan."""

import pytest

from xknx.management.procedures.dm.dm_interface_object_scan import (
    dm_interface_object_scan,
)

pytestmark = pytest.mark.skip(
    reason="dm_interface_object_scan — implementation pending"
)


async def test_dm_interface_object_scan_placeholder() -> None:
    """Placeholder for §3.28 DM_InterfaceObjectScan scenarios. Add real cases when impl lands."""
    _ = dm_interface_object_scan  # silence unused-import for the skipped test
