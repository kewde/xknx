"""
DMP_IndividualAddressRead_LEmi1 — KNX 03.05.02 §3.9.2 (PDF p. 91).

Spec text (verbatim from spec):

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
        Note right of S: different or no data received ⇒ error
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


async def dmp_individual_address_read_l_emi1(xknx: XKNX) -> None:
    """DMP_IndividualAddressRead_LEmi1 — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_IndividualAddressRead_LEmi1 (KNX 03.05.02 §3.9.2) — implementation pending"
    )
