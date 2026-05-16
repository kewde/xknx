"""
DMP_LCExtMemOpen_RCo — KNX 03.05.02 §3.44.2 (PDF p. 170).

Spec text (verbatim from spec):

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


async def dmp_lc_ext_mem_open_r_co(xknx: XKNX) -> None:
    """DMP_LCExtMemOpen_RCo — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_LCExtMemOpen_RCo (KNX 03.05.02 §3.44.2) — implementation pending"
    )
