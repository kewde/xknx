"""
NM_SubnetworkDevices_Scan2 — KNX 03.05.02 §2.17 (PDF p. 32).

Spec pseudocode (verbatim from spec):

    FOR (DA_Current = 0; DA_Current = 255; DA_Current = DA_Current+1)
         start time-out timer of 1 s

                                 A_DeviceDescriptor_Read-PDU
                                (destination_address.SNA =SNA,
                             destination_address.DA = DA_Current)

                               A_DeviceDescriptor_Response-PDU                                       If there is a MaS with IA = SNA.DA
                                           (DD0)                                                     then it will respond.


         If the MaC receives a response, then it shall add SNA.DA to the list in
         DA[].
         IF the timer expires without response THEN the MaC shall repeat the
         request one time.
              start time-out timer of 1 s

                                 A_DeviceDescriptor_Read-PDU
                                (destination_address.SNA =SNA,
                             destination_address.DA = DA_Current)

                               A_DeviceDescriptor_Response-PDU                                       If there is a MaS with IA = SNA.DA
                                           (DD0)                                                     then it will respond.


              If the MaC receives a response, then it shall add SNA.DA to the list in
              DA[].
    ENDFOR

Inputs (from spec):
    [in] SNA, [out] DA[]
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def nm_subnetwork_devices_scan2(xknx: XKNX) -> None:
    """NM_SubnetworkDevices_Scan2 — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "NM_SubnetworkDevices_Scan2 (KNX 03.05.02 §2.17) — implementation pending"
    )
