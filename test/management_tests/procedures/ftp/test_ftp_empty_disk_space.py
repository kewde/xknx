"""Tests for ftp_empty_disk_space — KNX 03.05.02 §8.10 FTP_EmptyDiskSpace."""

import pytest

from xknx.management.procedures.ftp.ftp_empty_disk_space import ftp_empty_disk_space

pytestmark = pytest.mark.skip(reason="ftp_empty_disk_space — implementation pending")


async def test_ftp_empty_disk_space_placeholder() -> None:
    """Placeholder for §8.10 FTP_EmptyDiskSpace scenarios. Add real cases when impl lands."""
    _ = ftp_empty_disk_space  # silence unused-import for the skipped test
