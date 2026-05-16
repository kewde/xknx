"""Tests for dmp_load_state_machine_read_r_co_mem — KNX 03.05.02 §3.33.2 DMP_LoadStateMachineRead_RCo_Mem."""

import pytest

from xknx.management.procedures.dmp.dmp_load_state_machine_read_r_co_mem import (
    dmp_load_state_machine_read_r_co_mem,
)

pytestmark = pytest.mark.skip(
    reason="dmp_load_state_machine_read_r_co_mem — implementation pending"
)


async def test_dmp_load_state_machine_read_r_co_mem_placeholder() -> None:
    """Placeholder for §3.33.2 DMP_LoadStateMachineRead_RCo_Mem scenarios. Add real cases when impl lands."""
    _ = dmp_load_state_machine_read_r_co_mem  # silence unused-import for the skipped test
