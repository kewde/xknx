"""Tests for nm_network_parameter_write_r — KNX 03.05.02 §2.22.1 NM_NetworkParameter_Write_R."""

import pytest

from xknx.management.procedures.nm.nm_network_parameter_write_r import (
    nm_network_parameter_write_r,
)

pytestmark = pytest.mark.skip(
    reason="nm_network_parameter_write_r — implementation pending"
)


async def test_nm_network_parameter_write_r_placeholder() -> None:
    """Placeholder for §2.22.1 NM_NetworkParameter_Write_R scenarios. Add real cases when impl lands."""
    _ = nm_network_parameter_write_r  # silence unused-import for the skipped test
