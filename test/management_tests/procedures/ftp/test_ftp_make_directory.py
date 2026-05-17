"""Tests for ftp_make_directory — KNX 03.05.02 §8.8 FTP_MakeDirectory."""

import pytest

from xknx.management.procedures.ftp.ftp_make_directory import ftp_make_directory

pytestmark = pytest.mark.skip(reason="ftp_make_directory — implementation pending")


async def test_ftp_make_directory_placeholder() -> None:
    """Placeholder for §8.8 FTP_MakeDirectory scenarios. Add real cases when impl lands."""
    _ = ftp_make_directory  # silence unused-import for the skipped test
