"""Tests for dmp_interface_object_read_ip — KNX 03.05.02 §6.5 DMP_InterfaceObjectRead_IP."""

import pytest

from xknx.management.procedures.dmp.dmp_interface_object_read_ip import (
    dmp_interface_object_read_ip,
)

pytestmark = pytest.mark.skip(
    reason="dmp_interface_object_read_ip — implementation pending"
)


async def test_dmp_interface_object_read_ip_placeholder() -> None:
    """Placeholder for §6.5 DMP_InterfaceObjectRead_IP scenarios. Add real cases when impl lands."""
    _ = dmp_interface_object_read_ip  # silence unused-import for the skipped test
