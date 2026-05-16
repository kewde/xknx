"""
DMP_Restart_LEmi1 — KNX 03.05.02 §3.7.4 (PDF p. 89).

Spec text (verbatim from spec):

    This Management Procedure shall use the local communication with EMI 1.
    Used EMI-services for Management
        •     PC_Set_Value

    Parameters of the Management Procedure
    DMP_Restart_LEmi1(/* [out] */ DmpError)
        DmpError:                              Possible error indication.

    Sequence
    Management                                                              Management                remark
    Client                                                                  Server
                                 PC_Set_Value.req message
                       (Length = 1 octet, Address = 0060h, data = C0h)

                  wait until Management Server was restarted

    Exception handling
    The general exception handling shall apply.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dmp_restart_l_emi1(xknx: XKNX) -> None:
    """DMP_Restart_LEmi1 — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_Restart_LEmi1 (KNX 03.05.02 §3.7.4) — implementation pending"
    )
