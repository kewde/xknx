"""Tests for nm_individual_address_reset — KNX 03.05.02 §2.18 NM_IndividualAddress_Reset."""

import pytest

from xknx.management.procedures.nm.nm_individual_address_reset import (
    nm_individual_address_reset,
)

pytestmark = pytest.mark.skip(
    reason="nm_individual_address_reset — implementation pending"
)


async def test_nm_individual_address_reset_placeholder() -> None:
    """Placeholder for §2.18 NM_IndividualAddress_Reset scenarios. Add real cases when impl lands."""
    _ = nm_individual_address_reset  # silence unused-import for the skipped test
