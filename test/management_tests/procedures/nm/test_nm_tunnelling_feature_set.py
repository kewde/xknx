"""Tests for nm_tunnelling_feature_set — KNX 03.05.02 §6.7 NM_TunnellingFeature_Set."""

import pytest

from xknx.management.procedures.nm.nm_tunnelling_feature_set import (
    nm_tunnelling_feature_set,
)

pytestmark = pytest.mark.skip(
    reason="nm_tunnelling_feature_set — implementation pending"
)


async def test_nm_tunnelling_feature_set_placeholder() -> None:
    """Placeholder for §6.7 NM_TunnellingFeature_Set scenarios. Add real cases when impl lands."""
    _ = nm_tunnelling_feature_set  # silence unused-import for the skipped test
