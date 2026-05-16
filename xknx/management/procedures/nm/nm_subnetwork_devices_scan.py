"""
NM_SubnetworkDevices_Scan — KNX 03.05.02 §2.16 (PDF p. 31).

Spec pseudocode (verbatim from spec):

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
    [in] SNA, [out] DA[]
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
