"""Tests for nm_individual_address_check_local_sub_network — KNX 03.05.02 §2.22.3 NM_IndividualAddress_Check_LocalSubNetwork."""

import pytest

from xknx.management.procedures.nm.nm_individual_address_check_local_sub_network import (
    nm_individual_address_check_local_sub_network,
)

pytestmark = pytest.mark.skip(
    reason="nm_individual_address_check_local_sub_network — implementation pending"
)


async def test_nm_individual_address_check_local_sub_network_placeholder() -> None:
    """Placeholder for §2.22.3 NM_IndividualAddress_Check_LocalSubNetwork scenarios. Add real cases when impl lands."""
    _ = nm_individual_address_check_local_sub_network  # silence unused-import for the skipped test
