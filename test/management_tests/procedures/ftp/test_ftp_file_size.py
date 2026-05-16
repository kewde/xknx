"""Tests for ftp_file_size — KNX 03.05.02 §8.9 FTP_FileSize."""

import pytest

from xknx.management.procedures.ftp.ftp_file_size import ftp_file_size

pytestmark = pytest.mark.skip(reason="ftp_file_size — implementation pending")


async def test_ftp_file_size_placeholder() -> None:
    """Placeholder for §8.9 FTP_FileSize scenarios. Add real cases when impl lands."""
    _ = ftp_file_size  # silence unused-import for the skipped test
