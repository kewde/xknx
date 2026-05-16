"""
DMP_Authorize_RCo — KNX 03.05.02 §3.5.1 (PDF p. 74).

Spec text (verbatim from spec):

    This Management Procedure shall use the connection oriented communication mode.
    Used Application Layer Services for Management
          •     A Authorize
    Sequence
    Management                                                                        Management                    remark
    Client                                                                            Server

    if authorization is required (key != FFFF FFFFH)
                               A_Authorize_Request-PDU (key)

                          A_Authorize_Response-PDU (key, level)                                     A_Disconnect.ind ⇒
                                                                                                    error: connection was broken
                                                                                                    down
    endif

    Exception handling
    The general exception handling shall apply.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dmp_authorize_r_co(xknx: XKNX) -> None:
    """DMP_Authorize_RCo — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_Authorize_RCo (KNX 03.05.02 §3.5.1) — implementation pending"
    )
