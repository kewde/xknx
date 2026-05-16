"""
DM_LCRouteTableStateRead — KNX 03.05.02 §3.47 (PDF p. 172).

Spec text (verbatim from spec):

    3.47.1 Use
    This device Management Procedure shall be used to read the state of the Routing Table to the
    Management Server (Coupler).
    A DM_Connect shall be executed before executing this Management Procedure.
    This device Management Procedure shall not be used for further developments of Management
    Servers.
    DM_LCRouteTableStateRead                   (flags, routeTableState)
            flags                bit 0       location of data (routeTableState)
                                                0: in data block
                                                1: -
                                 All other bits are reserved. These shall be set to 0. This shall be tested by
                                 the Management Client.
            routeTableState      state of the routing table (see description of APDU)

    3.47.2 Procedure: DMP_LCRouteTableStateRead_RCo
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
                                                                                        no data received ⇒ error

    Exception handling
    The general exception handling shall apply.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dm_lc_route_table_state_read(xknx: XKNX) -> None:
    """DM_LCRouteTableStateRead — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DM_LCRouteTableStateRead (KNX 03.05.02 §3.47) — implementation pending"
    )
