"""Tests for dm_individual_address_write — KNX 03.05.02 §3.10 DM_IndividualAddressWrite."""

import pytest

from xknx.management.procedures.dm.dm_individual_address_write import (
    dm_individual_address_write,
)

pytestmark = pytest.mark.skip(
    reason="dm_individual_address_write — implementation pending"
)


async def test_dm_individual_address_write_placeholder() -> None:
    """Placeholder for §3.10 DM_IndividualAddressWrite scenarios. Add real cases when impl lands."""
    _ = dm_individual_address_write  # silence unused-import for the skipped test
