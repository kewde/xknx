"""Tests for dm_interface_object_read — KNX 03.05.02 §3.27 DM_InterfaceObjectRead."""

import pytest

from xknx.management.procedures.dm.dm_interface_object_read import (
    dm_interface_object_read,
)

pytestmark = pytest.mark.skip(
    reason="dm_interface_object_read — implementation pending"
)


async def test_dm_interface_object_read_placeholder() -> None:
    """Placeholder for §3.27 DM_InterfaceObjectRead scenarios. Add real cases when impl lands."""
    _ = dm_interface_object_read  # silence unused-import for the skipped test
