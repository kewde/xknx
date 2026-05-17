"""Tests for dm_group_object_link_write_r_cl — KNX 03.05.02 §3.37.3 DM_GroupObjectLink_Write_RCl."""

import pytest

from xknx.management.procedures.dm.dm_group_object_link_write_r_cl import (
    dm_group_object_link_write_r_cl,
)

pytestmark = pytest.mark.skip(
    reason="dm_group_object_link_write_r_cl — implementation pending"
)


async def test_dm_group_object_link_write_r_cl_placeholder() -> None:
    """Placeholder for §3.37.3 DM_GroupObjectLink_Write_RCl scenarios. Add real cases when impl lands."""
    _ = dm_group_object_link_write_r_cl  # silence unused-import for the skipped test
