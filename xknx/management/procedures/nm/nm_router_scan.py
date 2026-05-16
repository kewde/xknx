"""
NM_Router_Scan — KNX 03.05.02 §2.15 (PDF p. 29).

Spec text (verbatim from spec):

    Use
    This Network Management Procedure shall be used to determine what Routers are installed in a
    network.
    The Management Client shall try to build up a connection to each possible Router. To this, it shall
    issue an A_Connect-PDU to each possible Router Individual Address. The Destination Address of this
    A_Connect-PDU shall be composed of:
         -    the Subnetwork Address field that shall start with 00h and be incremented by one for each
              next transmission of the A_Connect-PDU, and
         -    the Device Address field that shall have the fixed value 00h for each call of the
              A_Connect-PDU.
    In this way, 255 A_Connect-PDUs will be transmitted.
    The Management Client shall collect all A_Disconnect-PDUs. All Routers from which an
    A_Disconnect-PDU is received exist in the network.
    For this procedure the Individual Address of the Routers and the Domain Address have to be
    configured.
    Used Application Layer Services for Management
          • A_Connect

    Variables
          SNA_Current:          The current Subnetwork Address of the current Subnetwork in which the
                                presence of a Router is searched.

    Sequence
    Management                                                            Network /                  remark
    Client                                                                Management
                                                                          Server

    for (SNA_Current = 0; SNA_Current = 255; SNA_Current = SNA_Current+1)
                                   A_Connect-PDU                                       collect all received
                      (destination_address.SNA = SNA_Current;                          A_Disconnect-PDUs
                            destination_address.DA = 00h)

                                      delay for 0,1 s
                                        collect
                                  A_Disconnect-PDU
                      (destination_address.SNA = SNA_Current;
                            destination_address.DA = 00h)

    endfor
                                         collect                                       time-out: 6s after last sent
                                   A_Disconnect-PDU                                    A_Connect
                            (destination_address.SNA = any;
                             destination_address.DA = 00h)

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def nm_router_scan(xknx: XKNX) -> None:
    """NM_Router_Scan — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "NM_Router_Scan (KNX 03.05.02 §2.15) — implementation pending"
    )
