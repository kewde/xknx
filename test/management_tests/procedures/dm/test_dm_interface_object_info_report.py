"""Tests for dm_interface_object_info_report — KNX 03.05.02 §3.29 DM_InterfaceObjectInfoReport."""

import pytest

from xknx.management.procedures.dm.dm_interface_object_info_report import (
    dm_interface_object_info_report,
)

pytestmark = pytest.mark.skip(
    reason="dm_interface_object_info_report — implementation pending"
)


async def test_dm_interface_object_info_report_placeholder() -> None:
    """Placeholder for §3.29 DM_InterfaceObjectInfoReport scenarios. Add real cases when impl lands."""
    _ = dm_interface_object_info_report  # silence unused-import for the skipped test
