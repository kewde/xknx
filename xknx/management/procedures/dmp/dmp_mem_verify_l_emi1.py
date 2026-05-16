"""
DMP_MemVerify_LEmi1 — KNX 03.05.02 §3.17.3 (PDF p. 105).

Spec text (verbatim from spec):

    This Management Procedure shall use the local communication with EMI 1.
    Used Application Layer Services for Management
        •      PC_Get_Value

    Sequence
    Management                                                             Management                 remark
    Client                                                                 Server

    for each data block (≤12 octet), until all data are transmitted
                                   PC_Get_Value-PDU
                                     (Addr, Length)

                                   PC_Get_Value-PDU                                     different or no data received
                                   (Addr, Length, Data)                                 ⇒ error

    endfor

    Exception handling
    The general exception handling shall apply.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dmp_mem_verify_l_emi1(xknx: XKNX) -> None:
    """DMP_MemVerify_LEmi1 — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_MemVerify_LEmi1 (KNX 03.05.02 §3.17.3) — implementation pending"
    )
