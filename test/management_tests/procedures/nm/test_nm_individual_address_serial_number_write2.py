"""Tests for nm_individual_address_serial_number_write2 — KNX 03.05.02 §2.6 NM_IndividualAddress_SerialNumber_Write2."""

import pytest

from xknx.management.procedures.nm.nm_individual_address_serial_number_write2 import (
    nm_individual_address_serial_number_write2,
)

pytestmark = pytest.mark.skip(
    reason="nm_individual_address_serial_number_write2 — implementation pending"
)


async def test_nm_individual_address_serial_number_write2_placeholder() -> None:
    """Placeholder for §2.6 NM_IndividualAddress_SerialNumber_Write2 scenarios. Add real cases when impl lands."""
    _ = nm_individual_address_serial_number_write2  # silence unused-import for the skipped test
