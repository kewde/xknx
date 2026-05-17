"""
DM_IndividualAddressRead — KNX 03.05.02 §3.9 (PDF p. 90).

Spec text (verbatim from spec):

    3.9.1 Use
    This device Management Procedure shall be used to read out the Individual Addresses of the local
    device, independent of the Programming Mode. For remote procedures please refer to the clause 2
    "Network Management Procedures".
    A DM_Connect shall be executed before executing this Management Procedure.
    DM_IndividualAddressRead (Individual Address)
        Individual Address    contains the Individual Address of the device

    3.9.2 Procedure: DMP_IndividualAddressRead_LEmi1
    This Management Procedure shall use the local communication with EMI 1.
    Used EMI-services for Management
    - PC_Get_Value.req

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        C->>S: PC_Get_Value.req (Addr = 117h, Length = 2)
        S->>C: PC_Get_Value.con (Addr = 117h, Length = 2, Data = PPPP)
        Note right of S: different or no data received => error
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


async def dm_individual_address_read(xknx: XKNX) -> None:
    """DM_IndividualAddressRead — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DM_IndividualAddressRead (KNX 03.05.02 §3.9) — implementation pending"
    )
