"""Tests for nm_domain_and_individual_address_write3 — KNX 03.05.02 §2.11 NM_DomainAndIndividualAddress_Write3."""

import pytest

from xknx.management.procedures.nm.nm_domain_and_individual_address_write3 import (
    nm_domain_and_individual_address_write3,
)

pytestmark = pytest.mark.skip(
    reason="nm_domain_and_individual_address_write3 — implementation pending"
)


async def test_nm_domain_and_individual_address_write3_placeholder() -> None:
    """Placeholder for §2.11 NM_DomainAndIndividualAddress_Write3 scenarios. Add real cases when impl lands."""
    _ = nm_domain_and_individual_address_write3  # silence unused-import for the skipped test
