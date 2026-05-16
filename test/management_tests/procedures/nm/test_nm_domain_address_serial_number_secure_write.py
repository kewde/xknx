"""Tests for nm_domain_address_serial_number_secure_write — KNX 03.05.02 §2.13 NM_DomainAddressSerialNumber_Secure_Write."""

import pytest

from xknx.management.procedures.nm.nm_domain_address_serial_number_secure_write import (
    nm_domain_address_serial_number_secure_write,
)

pytestmark = pytest.mark.skip(
    reason="nm_domain_address_serial_number_secure_write — implementation pending"
)


async def test_nm_domain_address_serial_number_secure_write_placeholder() -> None:
    """Placeholder for §2.13 NM_DomainAddressSerialNumber_Secure_Write scenarios. Add real cases when impl lands."""
    _ = nm_domain_address_serial_number_secure_write  # silence unused-import for the skipped test
