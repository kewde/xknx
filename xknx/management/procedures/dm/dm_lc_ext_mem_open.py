"""
DM_LCExtMemOpen — KNX 03.05.02 §3.44 (PDF p. 169).

Spec text (verbatim from spec):

    3.44.1 Use
    This device Management Procedure shall be used to enable writing in the external memory of the
    Management Server (Coupler).
    A DM_Connect shall be executed before executing this Management Procedure.
    This device Management Procedure shall not be used for further developments of Management
    Servers.

    3.44.2 Procedure: DMP_LCExtMemOpen_RCo
    This Management Procedure shall use the connection oriented communication mode.
    Used Application Layer Services for Management
        •      A_FilterTable_Open

    Sequence
    Management                                                            Management                remark
    Client                                                                Server
                               A_FilterTable_Open-PDU
                                          ()

    Exception handling
    The general exception handling shall apply.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dm_lc_ext_mem_open(xknx: XKNX) -> None:
    """DM_LCExtMemOpen — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DM_LCExtMemOpen (KNX 03.05.02 §3.44) — implementation pending"
    )
