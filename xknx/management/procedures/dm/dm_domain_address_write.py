"""
DM_DomainAddressWrite — KNX 03.05.02 §3.12 (PDF p. 93).

Spec text (verbatim from spec):

    3.12.1 Use
    This device Management Procedure shall be used to write the Domain Address of the local device,
    independent of the Programming Mode. For remote procedures please refer to the clause 2 "Network
    Management Procedures".
    A DM_Connect shall be executed before executing this Management Procedure.
    DM_DomainAddressWrite (Domain Address)
        Domain Address    contains the Domain Address of the device

    3.12.2 Procedure: DMP_DomainAddressWrite_LEmi1
    This Management Procedure shall use the local communication with EMI 1.
    Used EMI-services for Management
    - PC_Get_Value.req
    - PEI_Memory_Write

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        C->>S: PEI_Memory_Write (Addr = 0102h, Length = 2, Data = BBBB)
        C->>S: PC_Get_Value.req (Addr = 0102h Length = 2)
        S->>C: PC_Get_Value.con (Addr = 0102h,Length = 2, Data = BBBB)
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


async def dm_domain_address_write(xknx: XKNX) -> None:
    """DM_DomainAddressWrite — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DM_DomainAddressWrite (KNX 03.05.02 §3.12) — implementation pending"
    )
