"""Tests for ftp_store_file — KNX 03.05.02 §8.3 FTP_StoreFile."""

import pytest

from xknx.management.procedures.ftp.ftp_store_file import ftp_store_file

pytestmark = pytest.mark.skip(reason="ftp_store_file — implementation pending")


async def test_ftp_store_file_placeholder() -> None:
    """Placeholder for §8.3 FTP_StoreFile scenarios. Add real cases when impl lands."""
    _ = ftp_store_file  # silence unused-import for the skipped test
