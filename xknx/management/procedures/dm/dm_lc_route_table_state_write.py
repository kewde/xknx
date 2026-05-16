"""
DM_LCRouteTableStateWrite — KNX 03.05.02 §3.45 (PDF p. 170).

Spec text (verbatim from spec):

    3.45.1 Use
    This device Management Procedure shall be used to write the state of the routing table to the
    Management Server (line coupler).
    A DM_Connect shall be executed before executing this Management Procedure.
    This device Management Procedure shall not be used for further developments of Management
    Servers.
    DM_LCRouteTableStateWrite                  (flags, routeTableState)
            flags               bit 0       location of data (routeTableState)
                                               0: in data block
                                               1: in management control
                                bit 1       verify enabled / disabled
                                               0: disabled
                                               1: enabled
                                All other bits are reserved. These shall be set to 0. This shall be tested by
                                the Management Client.
            routeTableState     state of the routing table (see description of APDU)

    3.45.2 Procedure: DMP_LCRouteTableStateWrite_RCo
    This Management Procedure shall use the connection oriented communication mode.
    The Verify Mode of the Management Server shall not be used.
    Used Application Layer Services for Management
        •      A_RouterStatus_Write
        •      A_RouterStatus_Read

    Sequence
    Management                                                             Management                 remark
    Client                                                                 Server
                               A_RouterStatus_Write-PDU
                                  (RouteTableState)

    if verify = enabled
                               A_RouterStatus_Read-PDU
                                          ()

                              A_RouterStatus_Response-PDU                               A_Disconnect.ind ⇒
                                   (RouteTableState)                                    error,
                                                                                        different or no data received
                                                                                        ⇒ error
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


async def dm_lc_route_table_state_write(xknx: XKNX) -> None:
    """DM_LCRouteTableStateWrite — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DM_LCRouteTableStateWrite (KNX 03.05.02 §3.45) — implementation pending"
    )
