"""Tests for nm_serial_number_default_ia_scan — KNX 03.05.02 §2.24 NM_SerialNumberDefaultIA_Scan."""

import pytest

from xknx.management.procedures.nm.nm_serial_number_default_ia_scan import (
    nm_serial_number_default_ia_scan,
)

pytestmark = pytest.mark.skip(
    reason="nm_serial_number_default_ia_scan — implementation pending"
)


async def test_nm_serial_number_default_ia_scan_placeholder() -> None:
    """Placeholder for §2.24 NM_SerialNumberDefaultIA_Scan scenarios. Add real cases when impl lands."""
    _ = nm_serial_number_default_ia_scan  # silence unused-import for the skipped test
