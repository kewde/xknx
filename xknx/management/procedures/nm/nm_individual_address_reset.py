"""
NM_IndividualAddress_Reset — KNX 03.05.02 §2.18 (PDF p. 32).

Spec text (verbatim from spec):

    Use
    This Network Management Procedure shall be used to reset the Individual Address of one or more
    devices in which Programming Mode is active to the default Individual Address FFFFh.

    Used Application Layer Services for Management
    - A_IndividualAddress_Write
    - A_Restart

    - A_IndividualAddress_Read
    - A_Connect
    - A_Disconnect

    Parameters of the Management Procedure
    This Management Procedure does not require any procedure parameters.

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Network / Management Server
        Note over C,S: repeat
        Note over C,S: reset Individual Address of all devices in which the Programming Mode is active
        C->>S: A_IndividualAddress_Write-PDU (newaddress= FFFFh)
        Note over C,S: reset all devices with Individual Address FFFFh (deactivate Programming Mode)
        C->>S: A_Connect-PDU () destination_address= FFFFh
        C->>S: A_Restart-PDU () destination_address = FFFFh
        C->>S: A_Disonnect-PDU () destination_address = FFFFh
        Note over C,S: verify, that all devices are reset
        C->>S: A_IndividualAddress_Read-PDU ()
        S->>C: A_IndividualAddress_Response-PDU ()
        Note right of S: one or more responses may be received from different devices
        Note over C,S: ...
        Note over C,S: until no A_IndividualAddress_Response-PDU is received
    ```

    Do not evaluate any local confirmation, or received telegrams, except the
    A_IndividualAddress_Read.Lcon and the A_IndividualAddress_Response-PDU.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def nm_individual_address_reset(xknx: XKNX) -> None:
    """NM_IndividualAddress_Reset — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "NM_IndividualAddress_Reset (KNX 03.05.02 §2.18) — implementation pending"
    )
