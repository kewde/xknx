"""Tests for dm_run_state_machine_read — KNX 03.05.02 §3.36 DM_RunStateMachineRead."""

import pytest

from xknx.management.procedures.dm.dm_run_state_machine_read import (
    dm_run_state_machine_read,
)

pytestmark = pytest.mark.skip(
    reason="dm_run_state_machine_read — implementation pending"
)


async def test_dm_run_state_machine_read_placeholder() -> None:
    """Placeholder for §3.36 DM_RunStateMachineRead scenarios. Add real cases when impl lands."""
    _ = dm_run_state_machine_read  # silence unused-import for the skipped test
