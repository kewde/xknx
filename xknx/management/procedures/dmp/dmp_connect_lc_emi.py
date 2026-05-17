"""
DMP_Connect_LcEMI — KNX 03.05.02 §3.2.5 (PDF p. 70).

Spec text (verbatim from spec):

    If local management via the cEMI interface is required, the Management Client shall connect to the
    local device via cEMI and switch the communication mode to cEMI Transport Layer by setting
    PID_COMM_MODE to “cEMI Transport Layer”. Further discovery (Device Descriptor,
    manufacturer…) is then done by the classic Application Layer services transferred via cEMI
    T_Data_Connected and T_Data_Individual.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dmp_connect_lc_emi(xknx: XKNX) -> None:
    """DMP_Connect_LcEMI — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_Connect_LcEMI (KNX 03.05.02 §3.2.5) — implementation pending"
    )
