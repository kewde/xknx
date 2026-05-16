"""Tests for nm_tunnelling_feature_info — KNX 03.05.02 §6.8 NM_TunnellingFeature_Info."""

import pytest

from xknx.management.procedures.nm.nm_tunnelling_feature_info import (
    nm_tunnelling_feature_info,
)

pytestmark = pytest.mark.skip(
    reason="nm_tunnelling_feature_info — implementation pending"
)


async def test_nm_tunnelling_feature_info_placeholder() -> None:
    """Placeholder for §6.8 NM_TunnellingFeature_Info scenarios. Add real cases when impl lands."""
    _ = nm_tunnelling_feature_info  # silence unused-import for the skipped test
