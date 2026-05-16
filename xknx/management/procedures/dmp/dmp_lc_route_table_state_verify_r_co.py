"""
DMP_LCRouteTableStateVerify_RCo — KNX 03.05.02 §3.46.2 (PDF p. 171).

Spec text (verbatim from spec):

    This Management Procedure shall use the connection oriented communication mode.
    Used Application Layer Services for Management
        •      A_RouterStatus_Read

    Sequence
    Management                                                             Management                 remark
    Client                                                                 Server
                               A_RouterStatus_Read-PDU
                                          ()

                              A_RouterStatus_Response-PDU                               A_Disconnect.ind ⇒
                                   (RouteTableState)                                    error,
                                                                                        different or no data received
                                                                                        ⇒ error

    Exception handling
    The general exception handling shall apply.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dmp_lc_route_table_state_verify_r_co(xknx: XKNX) -> None:
    """DMP_LCRouteTableStateVerify_RCo — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_LCRouteTableStateVerify_RCo (KNX 03.05.02 §3.46.2) — implementation pending"
    )
