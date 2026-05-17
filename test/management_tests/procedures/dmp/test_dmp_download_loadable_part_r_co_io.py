"""Tests for dmp_download_loadable_part_r_co_io — KNX 03.05.02 §3.31.4 DMP_DownloadLoadablePart_RCo_IO."""

import pytest

from xknx.management.procedures.dmp.dmp_download_loadable_part_r_co_io import (
    dmp_download_loadable_part_r_co_io,
)

pytestmark = pytest.mark.skip(
    reason="dmp_download_loadable_part_r_co_io — implementation pending"
)


async def test_dmp_download_loadable_part_r_co_io_placeholder() -> None:
    """Placeholder for §3.31.4 DMP_DownloadLoadablePart_RCo_IO scenarios. Add real cases when impl lands."""
    _ = dmp_download_loadable_part_r_co_io  # silence unused-import for the skipped test
