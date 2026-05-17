"""Tests for dmp_pei_type_read_r_co_adc — KNX 03.05.02 §3.15.2 DMP_PeiTypeRead_RCo_ADC."""

import pytest

from xknx.management.procedures.dmp.dmp_pei_type_read_r_co_adc import (
    dmp_pei_type_read_r_co_adc,
)

pytestmark = pytest.mark.skip(
    reason="dmp_pei_type_read_r_co_adc — implementation pending"
)


async def test_dmp_pei_type_read_r_co_adc_placeholder() -> None:
    """Placeholder for §3.15.2 DMP_PeiTypeRead_RCo_ADC scenarios. Add real cases when impl lands."""
    _ = dmp_pei_type_read_r_co_adc  # silence unused-import for the skipped test
