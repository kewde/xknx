"""Tests for nm_domain_address_serial_number_write — KNX 03.05.02 §2.12 NM_DomainAddressSerialNumber_Write."""

import pytest

from xknx.management.procedures.nm.nm_domain_address_serial_number_write import (
    nm_domain_address_serial_number_write,
)

pytestmark = pytest.mark.skip(
    reason="nm_domain_address_serial_number_write — implementation pending"
)


async def test_nm_domain_address_serial_number_write_placeholder() -> None:
    """Placeholder for §2.12 NM_DomainAddressSerialNumber_Write scenarios. Add real cases when impl lands."""
    _ = nm_domain_address_serial_number_write  # silence unused-import for the skipped test
