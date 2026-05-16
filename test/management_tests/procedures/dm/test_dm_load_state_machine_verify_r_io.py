"""Tests for dm_load_state_machine_verify_r_io — KNX 03.05.02 §3.32.3 DM_LoadStateMachineVerify_R_IO."""

import pytest

from xknx.management.procedures.dm.dm_load_state_machine_verify_r_io import (
    dm_load_state_machine_verify_r_io,
)

pytestmark = pytest.mark.skip(
    reason="dm_load_state_machine_verify_r_io — implementation pending"
)


async def test_dm_load_state_machine_verify_r_io_placeholder() -> None:
    """Placeholder for §3.32.3 DM_LoadStateMachineVerify_R_IO scenarios. Add real cases when impl lands."""
    _ = dm_load_state_machine_verify_r_io  # silence unused-import for the skipped test
