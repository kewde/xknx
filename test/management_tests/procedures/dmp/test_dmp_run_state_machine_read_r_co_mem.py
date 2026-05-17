"""Tests for dmp_run_state_machine_read_r_co_mem — KNX 03.05.02 §3.36.2 DMP_RunStateMachineRead_RCo_Mem."""

import pytest

from xknx.management.procedures.dmp.dmp_run_state_machine_read_r_co_mem import (
    dmp_run_state_machine_read_r_co_mem,
)

pytestmark = pytest.mark.skip(
    reason="dmp_run_state_machine_read_r_co_mem — implementation pending"
)


async def test_dmp_run_state_machine_read_r_co_mem_placeholder() -> None:
    """Placeholder for §3.36.2 DMP_RunStateMachineRead_RCo_Mem scenarios. Add real cases when impl lands."""
    _ = dmp_run_state_machine_read_r_co_mem  # silence unused-import for the skipped test
