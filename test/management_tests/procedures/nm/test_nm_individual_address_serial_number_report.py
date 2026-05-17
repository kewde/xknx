"""Tests for nm_individual_address_serial_number_report — KNX 03.05.02 §2.22.4 NM_IndividualAddress_SerialNumber_Report."""

import pytest

from xknx.management.procedures.nm.nm_individual_address_serial_number_report import (
    nm_individual_address_serial_number_report,
)

pytestmark = pytest.mark.skip(
    reason="nm_individual_address_serial_number_report — implementation pending"
)


async def test_nm_individual_address_serial_number_report_placeholder() -> None:
    """Placeholder for §2.22.4 NM_IndividualAddress_SerialNumber_Report scenarios. Add real cases when impl lands."""
    _ = nm_individual_address_serial_number_report  # silence unused-import for the skipped test
