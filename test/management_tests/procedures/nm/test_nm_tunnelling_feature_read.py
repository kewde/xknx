"""Tests for nm_tunnelling_feature_read — KNX 03.05.02 §6.6 NM_TunnellingFeature_Read."""

import pytest

from xknx.management.procedures.nm.nm_tunnelling_feature_read import (
    nm_tunnelling_feature_read,
)

pytestmark = pytest.mark.skip(
    reason="nm_tunnelling_feature_read — implementation pending"
)


async def test_nm_tunnelling_feature_read_placeholder() -> None:
    """Placeholder for §6.6 NM_TunnellingFeature_Read scenarios. Add real cases when impl lands."""
    _ = nm_tunnelling_feature_read  # silence unused-import for the skipped test
