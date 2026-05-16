"""
NM_SubnetworkDevices_Scan — KNX 03.05.02 §2.16 (PDF p. 30).

Spec text (verbatim from spec):

    Use
    This Network Management Procedure shall be used to determine which devices exist on a
    Subnetwork.
    The Management Client shall try to build up a connection using every possible correct Individual
    Address in this Subnetwork. It shall collect all A_Disconnect-PDUs. All devices from which an
    A_Disconnect-PDU is received shall be considered as existing on the Subnetwork.
    For this procedure the Individual Address of the used Routers and the Domain Address have to be
    configured.
    Used Application Layer Services for Management
          • A_Connect

    Parameters of the Management Procedure
    NM_SubnetworkDevices_Scan(/* [in] */ SNA, /* [out] */ DA[])
      SNA:                   Subnetwork Address of the Subnetwork in which the occupied
                             Individual Addresses are to be scanned.
      DA[]:                  The collection of all Device Addresses of the devices discovered in
                             the investigated Subnetwork.

    Variables
          DA_Current:           The current Device Address of which it will be checked whether a device
                                with this Device Address exists on the Subnetwork that is being checked.

    Sequence
    Management                                                            Network /               remark
    Client                                                                Management
                                                                          Server

    for (DA_Current = 0; DA_Current = 255; DA_Current = DA_Current+1)
                                    A_Connect-PDU
                           (destination_address.SNA =SNA,
                        destination_address.DA = DA_Current)

                                      delay for 0,1 s
                                      collect all
                                  A_Disconnect-PDU()

       The Device Address part of all possible received
       A_Disconnect-PDUs shall be collected in DA[].
    endfor
                 wait longer Transport Layer time-out (>6 s) after last
                                sent A_Connect-PDY

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def nm_subnetwork_devices_scan(xknx: XKNX) -> None:
    """NM_SubnetworkDevices_Scan — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "NM_SubnetworkDevices_Scan (KNX 03.05.02 §2.16) — implementation pending"
    )
