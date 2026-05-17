"""Tests for dm_domain_address_read — KNX 03.05.02 §3.11 DM_DomainAddress_Read."""

import pytest

from xknx.management.procedures.dm.dm_domain_address_read import dm_domain_address_read

pytestmark = pytest.mark.skip(reason="dm_domain_address_read — implementation pending")


async def test_dm_domain_address_read_placeholder() -> None:
    """Placeholder for §3.11 DM_DomainAddress_Read scenarios. Add real cases when impl lands."""
    _ = dm_domain_address_read  # silence unused-import for the skipped test
