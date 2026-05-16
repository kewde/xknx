"""Tests for nm_domain_and_individual_address_write2 — KNX 03.05.02 §2.10 NM_DomainAndIndividualAddress_Write2."""

import pytest

from xknx.management.procedures.nm.nm_domain_and_individual_address_write2 import (
    nm_domain_and_individual_address_write2,
)

pytestmark = pytest.mark.skip(
    reason="nm_domain_and_individual_address_write2 — implementation pending"
)


async def test_nm_domain_and_individual_address_write2_placeholder() -> None:
    """Placeholder for §2.10 NM_DomainAndIndividualAddress_Write2 scenarios. Add real cases when impl lands."""
    _ = nm_domain_and_individual_address_write2  # silence unused-import for the skipped test
