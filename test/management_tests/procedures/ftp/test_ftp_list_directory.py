"""Tests for ftp_list_directory — KNX 03.05.02 §8.4 FTP_ListDirectory."""

import pytest

from xknx.management.procedures.ftp.ftp_list_directory import ftp_list_directory

pytestmark = pytest.mark.skip(reason="ftp_list_directory — implementation pending")


async def test_ftp_list_directory_placeholder() -> None:
    """Placeholder for §8.4 FTP_ListDirectory scenarios. Add real cases when impl lands."""
    _ = ftp_list_directory  # silence unused-import for the skipped test
