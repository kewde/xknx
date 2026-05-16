"""Tests for dm_pei_type_verify — KNX 03.05.02 §3.14 DM_PeiTypeVerify."""

import pytest

from xknx.management.procedures.dm.dm_pei_type_verify import dm_pei_type_verify

pytestmark = pytest.mark.skip(reason="dm_pei_type_verify — implementation pending")


async def test_dm_pei_type_verify_placeholder() -> None:
    """Placeholder for §3.14 DM_PeiTypeVerify scenarios. Add real cases when impl lands."""
    _ = dm_pei_type_verify  # silence unused-import for the skipped test
