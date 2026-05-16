"""Tests for nm_domain_and_individual_address_read — KNX 03.05.02 §2.8 NM_DomainAndIndividualAddress_Read."""

import pytest

from xknx.management.procedures.nm.nm_domain_and_individual_address_read import (
    nm_domain_and_individual_address_read,
)

pytestmark = pytest.mark.skip(
    reason="nm_domain_and_individual_address_read — implementation pending"
)


async def test_nm_domain_and_individual_address_read_placeholder() -> None:
    """Placeholder for §2.8 NM_DomainAndIndividualAddress_Read scenarios. Add real cases when impl lands."""
    _ = nm_domain_and_individual_address_read  # silence unused-import for the skipped test
