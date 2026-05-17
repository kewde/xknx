"""Tests for dm_device_descriptor_info_report — KNX 03.05.02 §3.2.7 DM_DeviceDescriptor_InfoReport."""

import pytest

from xknx.management.procedures.dm.dm_device_descriptor_info_report import (
    dm_device_descriptor_info_report,
)

pytestmark = pytest.mark.skip(
    reason="dm_device_descriptor_info_report — implementation pending"
)


async def test_dm_device_descriptor_info_report_placeholder() -> None:
    """Placeholder for §3.2.7 DM_DeviceDescriptor_InfoReport scenarios. Add real cases when impl lands."""
    _ = dm_device_descriptor_info_report  # silence unused-import for the skipped test
