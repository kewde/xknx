"""
NM_SubnetworkDevices_Scan2 — KNX 03.05.02 §2.17 (PDF p. 31).

Spec text (verbatim from spec):

    Use
    This Network Management Procedure shall be used to determine which devices exist on a
    Subnetwork.
    The MaC shall to this one after the other address each possible Individual Address in the Subnetwork
    by reading the Device Descriptor Type 0 with the service A_DeviceDescriptor_Read, using point-to-
    point connectionless communication mode. If the MaC does not receive a response within one second,
    it shall repeat the request once and wait again for one second for a possible response.
    - If the MaC receives a response then it shall assume that the tested IA is occupied.
    - If the MaC receives no response, then it shall assume that the tested IA is not occupied.
    For this procedure the Individual Address of the used Routers and the Domain Address have to be
    configured.

    Used Application Layer Services for Management
    - A_DeviceDescriptor_Read

    Parameters of the Management Procedure
    NM_SubnetworkDevices_Scan2(/* [in] */ SNA, /* [out] */ DA[])
        SNA:  Subnetwork Address of the Subnetwork in which the occupied
              Individual Addresses are to be scanned.
        DA[]: The collection of all Device Addresses of the devices discovered in
              the investigated Subnetwork.

    Variables
        DA_Current: The current Device Address of which it will be checked whether a device
                    with this Device Address exists on the Subnetwork that is being checked.

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Network / Management Server
        loop for DA_Current = 0 to 255
            Note over C: start time-out timer of 1 s
            C->>S: A_DeviceDescriptor_Read-PDU (destination_address.SNA = SNA, destination_address.DA = DA_Current)
            alt response received
                S->>C: A_DeviceDescriptor_Response-PDU (DD0)
                Note over C: add SNA.DA to the list in DA[]
            else timer expires without response
                Note over C: start time-out timer of 1 s (retry)
                C->>S: A_DeviceDescriptor_Read-PDU (destination_address.SNA = SNA, destination_address.DA = DA_Current)
                opt response received
                    S->>C: A_DeviceDescriptor_Response-PDU (DD0)
                    Note over C: add SNA.DA to the list in DA[]
                end
            end
        end
    ```

    Constraints
    1. This procedure uses the connectionless communication mode for the service A_Device-
       Descriptor_Read. This service will therefore give incomplete results if there are KNX devices in
       the Subnetwork that do not support this service in connectionless communication mode.
    2. Additionally, this procedure does not use the T_Connect-service. Devices that do not react to
       A_DeviceDescriptor_Read but only negatively react to a T_Connect-PDU by sending a
       T_Disconnect-PDU, will not be discovered with this procedure.
       EXAMPLE 2 Certain KNX Profiles support multiple Individual Addresses in one device, like the KNXnet/IP Tunnelling
       Server. These Additional IA may not be discovered.

    3. The MaC shall only apply this Management Procedure if the target Subnetwork is of the KNX RF
       Communication Medium.

Inputs (from spec):
    (see body)
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
