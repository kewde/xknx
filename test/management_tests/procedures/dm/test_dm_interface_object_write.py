"""Tests for dm_interface_object_write — KNX 03.05.02 §3.25 DM_InterfaceObjectWrite."""

import pytest

from xknx.management.procedures.dm.dm_interface_object_write import (
    dm_interface_object_write,
)

pytestmark = pytest.mark.skip(
    reason="dm_interface_object_write — implementation pending"
)


async def test_dm_interface_object_write_placeholder() -> None:
    """Placeholder for §3.25 DM_InterfaceObjectWrite scenarios. Add real cases when impl lands."""
    _ = dm_interface_object_write  # silence unused-import for the skipped test
