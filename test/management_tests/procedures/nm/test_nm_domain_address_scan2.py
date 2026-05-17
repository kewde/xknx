"""Tests for nm_domain_address_scan2 — KNX 03.05.02 §2.14.1.2.2 NM_DomainAddress_Scan2."""

import pytest

from xknx.management.procedures.nm.nm_domain_address_scan2 import (
    nm_domain_address_scan2,
)

pytestmark = pytest.mark.skip(reason="nm_domain_address_scan2 — implementation pending")


async def test_nm_domain_address_scan2_placeholder() -> None:
    """Placeholder for §2.14.1.2.2 NM_DomainAddress_Scan2 scenarios. Add real cases when impl lands."""
    _ = nm_domain_address_scan2  # silence unused-import for the skipped test
