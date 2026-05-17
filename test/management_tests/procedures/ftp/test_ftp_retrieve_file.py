"""Tests for ftp_retrieve_file — KNX 03.05.02 §8.2 FTP_RetrieveFile."""

import pytest

from xknx.management.procedures.ftp.ftp_retrieve_file import ftp_retrieve_file

pytestmark = pytest.mark.skip(reason="ftp_retrieve_file — implementation pending")


async def test_ftp_retrieve_file_placeholder() -> None:
    """Placeholder for §8.2 FTP_RetrieveFile scenarios. Add real cases when impl lands."""
    _ = ftp_retrieve_file  # silence unused-import for the skipped test
