"""
DMP_DomainAddressRead_LEmi1 — KNX 03.05.02 §3.11.2 (PDF p. 92).

Spec text (verbatim from spec):

    This Management Procedure shall use the local communication with EMI 1.
    Used EMI-services for Management for Management
        •     PC_Get_Value.req

    Sequence
    Management                                                            Management                 remark
    Client                                                                Server

                    PC_Get_Value.req (Addr = 0102h Length = 2)

                                 PC_Get_Value.con                                      different or no data received
                       (Addr = 0102h Length = 2, Data = BBBB)                          ⇒ error

    Exception handling
    The general exception handling shall apply.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dmp_domain_address_read_l_emi1(xknx: XKNX) -> None:
    """DMP_DomainAddressRead_LEmi1 — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_DomainAddressRead_LEmi1 (KNX 03.05.02 §3.11.2) — implementation pending"
    )
