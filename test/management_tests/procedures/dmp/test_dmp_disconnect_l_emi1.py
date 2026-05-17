"""Tests for dmp_disconnect_l_emi1 — KNX 03.05.02 §3.3.4 DMP_Disconnect_LEmi1."""

import pytest

from xknx.management.procedures.dmp.dmp_disconnect_l_emi1 import dmp_disconnect_l_emi1

pytestmark = pytest.mark.skip(reason="dmp_disconnect_l_emi1 — implementation pending")


async def test_dmp_disconnect_l_emi1_placeholder() -> None:
    """Placeholder for §3.3.4 DMP_Disconnect_LEmi1 scenarios. Add real cases when impl lands."""
    _ = dmp_disconnect_l_emi1  # silence unused-import for the skipped test
