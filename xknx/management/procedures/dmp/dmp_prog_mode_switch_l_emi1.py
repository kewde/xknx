"""
DMP_ProgModeSwitch_LEmi1 — KNX 03.05.02 §3.13.3 (PDF p. 94).

Spec text (verbatim from spec):

    This Management Procedure shall use the local communication with EMI 1.
    The Programming Mode shall be realised as "Programming Mode - Realisation Type 2" as specified
    in [05].
    NOTE: This means that the state of the Programming Mode is located at memory address 60h.

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
        Note right of S: In the data (DD) bit 0 has to be set according to the mode. The parity (bit 7) has to be calculated.
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


async def dmp_prog_mode_switch_l_emi1(xknx: XKNX) -> None:
    """DMP_ProgModeSwitch_LEmi1 — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_ProgModeSwitch_LEmi1 (KNX 03.05.02 §3.13.3) — implementation pending"
    )
