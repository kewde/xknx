"""Tests for ftp_delete — KNX 03.05.02 §8.6 FTP_Delete."""

import pytest

from xknx.management.procedures.ftp.ftp_delete import ftp_delete

pytestmark = pytest.mark.skip(reason="ftp_delete — implementation pending")


async def test_ftp_delete_placeholder() -> None:
    """Placeholder for §8.6 FTP_Delete scenarios. Add real cases when impl lands."""
    _ = ftp_delete  # silence unused-import for the skipped test
