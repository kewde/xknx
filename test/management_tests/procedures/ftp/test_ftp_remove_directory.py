"""Tests for ftp_remove_directory — KNX 03.05.02 §8.7 FTP_RemoveDirectory."""

import pytest

from xknx.management.procedures.ftp.ftp_remove_directory import ftp_remove_directory

pytestmark = pytest.mark.skip(reason="ftp_remove_directory — implementation pending")


async def test_ftp_remove_directory_placeholder() -> None:
    """Placeholder for §8.7 FTP_RemoveDirectory scenarios. Add real cases when impl lands."""
    _ = ftp_remove_directory  # silence unused-import for the skipped test
