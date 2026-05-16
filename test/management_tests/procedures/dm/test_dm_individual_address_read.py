"""Tests for dm_individual_address_read — KNX 03.05.02 §3.9 DM_IndividualAddressRead."""

import pytest

from xknx.management.procedures.dm.dm_individual_address_read import (
    dm_individual_address_read,
)

pytestmark = pytest.mark.skip(
    reason="dm_individual_address_read — implementation pending"
)


async def test_dm_individual_address_read_placeholder() -> None:
    """Placeholder for §3.9 DM_IndividualAddressRead scenarios. Add real cases when impl lands."""
    _ = dm_individual_address_read  # silence unused-import for the skipped test
