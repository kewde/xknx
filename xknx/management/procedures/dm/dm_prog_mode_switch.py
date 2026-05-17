"""
DM_ProgMode_Switch — KNX 03.05.02 §3.13 (PDF p. 93).

Spec text (verbatim from spec):

    3.13.1 Use
    This device Management Procedure shall switch the Programming Mode of the device.
    A DM_Connect shall be executed before executing this Management Procedure.

    DM_ProgMode_Switch (flags, mode)
        flags  All bits are reserved. These shall be set to 0. This shall be tested
               by the Management Client.
        mode   0: switch Programming Mode off
               1: switch Programming Mode on

    3.13.2 Procedure: DMP_ProgModeSwitch_RCo
    This Management Procedure shall use the connection oriented communication mode.
    The Programming Mode shall be realised as "Programming Mode – Realisation Type 2" as specified
    in [05].
    NOTE  This means that the state of the Programming Mode is located at memory address 60h.

    Used Application Layer Services for Management
    - A_Memory_Read
    - A_Memory_Write

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        C->>S: A_Memory_Read-PDU (Addr = 60h, Length = 1)
        S->>C: A_Memory_Response-PDU (Addr = 60h, Length = 1, Data = DD)
        Note right of S: A_Disconnect.ind ⇒ error, different or no data received ⇒ error
        C->>S: A_Memory_Write-PDU (Addr = 60h, Length = 1, Data = DD)
        Note right of C: In the data (DD) bit 0 has to be set according to the mode. The parity (bit 7) has to be calculated.
    ```

    Exception handling
    The general exception handling shall apply.

    3.13.3 Procedure: DMP_ProgModeSwitch_LEmi1
    This Management Procedure shall use the local communication with EMI 1.
    The Programming Mode shall be realised as "Programming Mode – Realisation Type 2" as specified
    in [05].
    NOTE  This means that the state of the Programming Mode is located at memory address 60h.

    Used EMI-services for Management
    - PC_Get_Value.req
    - PEI_Memory_Write

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        C->>S: PC_Get_Value-PDU (Addr = 60h, Length = 1)
        S->>C: PC_Get_Value-PDU (Addr = 60h, Length = 1, Data = DD)
        Note right of S: different or no data received ⇒ error
        C->>S: PEI_Memory_Write-PDU (Addr = 60h, Length = 1, Data = DD)
        Note right of C: In the data (DD) bit 0 has to be set according to the mode. The parity (bit 7) has to be calculated.
    ```

    Exception handling
    The general exception handling shall apply.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dm_prog_mode_switch(xknx: XKNX) -> None:
    """DM_ProgMode_Switch — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DM_ProgMode_Switch (KNX 03.05.02 §3.13) — implementation pending"
    )
