"""Tests for ftp_abort — KNX 03.05.02 §8.11 FTP_Abort."""

import pytest

from xknx.management.procedures.ftp.ftp_abort import ftp_abort

pytestmark = pytest.mark.skip(reason="ftp_abort — implementation pending")


async def test_ftp_abort_placeholder() -> None:
    """Placeholder for §8.11 FTP_Abort scenarios. Add real cases when impl lands."""
    _ = ftp_abort  # silence unused-import for the skipped test
