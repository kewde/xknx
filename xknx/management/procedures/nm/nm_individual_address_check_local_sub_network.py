"""
NM_IndividualAddress_Check_LocalSubNetwork — KNX 03.05.02 §2.22.3 (PDF p. 49).

Spec text (verbatim from spec):

    Use
    The procedure shall be used by a Management Client to check whether a given Individual Address is
    occupied on the Subnetwork where it is itself located (the "local" Subnetwork).
    To check whether an Individual Address is occupied on a local Subnetwork the Management Client
    shall transmit an A_NetworkParameter_Write-PDU on point-to-point connectionless communication
    mode addressed at the Individual Address PPPP under test.
    The result of this check will be Occupied or NotOccupied.
    In order to have this procedure not perturb any other Subnetwork than the one on which the
    Management Client is mounted, the A_NetworkParameter_Write-PDU shall be sent with the
    parameter hop_count = 0, so that Routers do not pass this message.
    The Subnetwork Address is assumed to be set.

    Individual Address handling during the procedure
    The Source Address in the A_NetworkParameter_Write-PDU used in the below sequence shall be set
    to the current Individual Address of the device, this is the one stored in NVRAM. During the
    procedure, the device shall acknowledge every telegram sent to this current Individual Address.

    At that time, the Individual Address PPPP checked is not valid for the device. So the device shall not
    acknowledge any telegram sent to this Individual Address PPPP.

    Possible situations and reactions during the Management Procedure
    According to the specification of the Data Link Layer, the user layer of the MAC layer will receive an
    L_Data.con with the possible values of the parameter l_status:
        - ok
        - not_ok.
    - Value ok means that a Layer-2 acknowledge has been received and that the Individual Address is
      occupied.
    - Value not_ok means that:
        - a BUSY-acknowledge is received (on TP 1 only): there is a Management Server (device) that
          occupies the Individual Address that is checked but for internal reasons it cannot handle the
          frame transporting the A_NetworkParameter_Write-PDU.
        - a NACK-acknowledge is received (on TP 1 only): due to frame errors the frame transporting
          the A_NetworkParameter_Write-PDU has not been interpreted.
        - absence of acknowledge. This case demonstrates that the Individual Address is not occupied at
          this moment.
      The probability that the flag l_status is set to not_ok , due to BUSY- or NACK-acknowledges,
      after the specified Layer-2 repetitions, can be neglected compared to the probability that this
      value not_ok is caused by the absence (no acknowledge) of a Layer-2 acknowledge. Therefore,
      the value not_ok shall always lead to the conclusion that the checked Individual Address is free.
      The cases where this is caused by unsuccessful transmission including BUSY and NACK
      retransmissions shall be recovered from by a constant Individual Address conflict detection
      procedure of the Configuration Mode that uses
      NM_IndividualAddress_Check_LocalSubnetwork.

    Used Application Layer Services for Management
    - A_NetworkParameter_Write

    Inputs
    - PPPP: Individual Address of which the occupation on the Subnetwork has to be tested.

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        C->>S: A_NetworkParameter_Write-PDU (ASAP = PPPP, comm_mode = point-to-point connectionless, hop_count_type = 0, object_type = 0 = Device Object, Property_id = PID_ADDR_CHECK = 61, priority = system, value = 00h)
        Note over C,S: The value of a_status in the local confirmation of the A_NetworkParameter_Write-service will depend on the occupancy of PPPP on the Subnetwork.
        S->>C: A_NetworkParameter_Write.Lcon (ASAP = PPPP, comm_mode = point-to-point connectionless, hop_count_type = 0, object_type = 0 = Device Object, Property_id = PID_ADDR_CHECK = 61, priority = system, value = 00h, a_status)
        Note over C,S: If a_status = OK then IA PPPP Occupied
        Note over C,S: else IA PPPP is Not Occupied
    ```

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def nm_individual_address_check_local_sub_network(xknx: XKNX) -> None:
    """NM_IndividualAddress_Check_LocalSubNetwork — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "NM_IndividualAddress_Check_LocalSubNetwork (KNX 03.05.02 §2.22.3) — implementation pending"
    )
