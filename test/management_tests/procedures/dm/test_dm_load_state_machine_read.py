"""Tests for dm_load_state_machine_read — KNX 03.05.02 §3.33 DM_LoadStateMachineRead."""

import pytest

from xknx.management.procedures.dm.dm_load_state_machine_read import (
    dm_load_state_machine_read,
)

pytestmark = pytest.mark.skip(
    reason="dm_load_state_machine_read — implementation pending"
)


async def test_dm_load_state_machine_read_placeholder() -> None:
    """Placeholder for §3.33 DM_LoadStateMachineRead scenarios. Add real cases when impl lands."""
    _ = dm_load_state_machine_read  # silence unused-import for the skipped test
