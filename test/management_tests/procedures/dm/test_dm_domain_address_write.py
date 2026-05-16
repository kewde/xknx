"""Tests for dm_domain_address_write — KNX 03.05.02 §3.12 DM_DomainAddressWrite."""

import pytest

from xknx.management.procedures.dm.dm_domain_address_write import (
    dm_domain_address_write,
)

pytestmark = pytest.mark.skip(reason="dm_domain_address_write — implementation pending")


async def test_dm_domain_address_write_placeholder() -> None:
    """Placeholder for §3.12 DM_DomainAddressWrite scenarios. Add real cases when impl lands."""
    _ = dm_domain_address_write  # silence unused-import for the skipped test
