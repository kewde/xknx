"""Tests for nm_domain_and_individual_address_write — KNX 03.05.02 §2.9 NM_DomainAndIndividualAddress_Write."""

import pytest

from xknx.management.procedures.nm.nm_domain_and_individual_address_write import (
    nm_domain_and_individual_address_write,
)

pytestmark = pytest.mark.skip(
    reason="nm_domain_and_individual_address_write — implementation pending"
)


async def test_nm_domain_and_individual_address_write_placeholder() -> None:
    """Placeholder for §2.9 NM_DomainAndIndividualAddress_Write scenarios. Add real cases when impl lands."""
    _ = nm_domain_and_individual_address_write  # silence unused-import for the skipped test
