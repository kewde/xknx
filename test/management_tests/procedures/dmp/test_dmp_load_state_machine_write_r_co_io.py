"""Tests for dmp_load_state_machine_write_r_co_io — KNX 03.05.02 §3.31.3 DMP_LoadStateMachineWrite_RCo_IO."""

import pytest

from xknx.management.procedures.dmp.dmp_load_state_machine_write_r_co_io import (
    dmp_load_state_machine_write_r_co_io,
)

pytestmark = pytest.mark.skip(
    reason="dmp_load_state_machine_write_r_co_io — implementation pending"
)


async def test_dmp_load_state_machine_write_r_co_io_placeholder() -> None:
    """Placeholder for §3.31.3 DMP_LoadStateMachineWrite_RCo_IO scenarios. Add real cases when impl lands."""
    _ = dmp_load_state_machine_write_r_co_io  # silence unused-import for the skipped test
