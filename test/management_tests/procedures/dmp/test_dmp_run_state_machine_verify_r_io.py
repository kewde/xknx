"""Tests for dmp_run_state_machine_verify_r_io — KNX 03.05.02 §3.35.3 DMP_RunStateMachineVerify_R_IO."""

import pytest

from xknx.management.procedures.dmp.dmp_run_state_machine_verify_r_io import (
    dmp_run_state_machine_verify_r_io,
)

pytestmark = pytest.mark.skip(
    reason="dmp_run_state_machine_verify_r_io — implementation pending"
)


async def test_dmp_run_state_machine_verify_r_io_placeholder() -> None:
    """Placeholder for §3.35.3 DMP_RunStateMachineVerify_R_IO scenarios. Add real cases when impl lands."""
    _ = dmp_run_state_machine_verify_r_io  # silence unused-import for the skipped test
