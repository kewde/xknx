"""
DMP_Connect_LEmi1 — KNX 03.05.02 §3.2.3 (PDF p. 69).

Spec text (verbatim from spec):

    Use
    This Management Procedure shall use the local communication with EMI 1. The Device Descriptor
    Type 0 shall be read from the memory location 4Eh – 4Fh.

    Used EMI-services for Management
    - PC_Get_Value

    Parameters of the Management Procedure
    DMP_Restart_LEmi1(/* [out] */ DD0, /* [out] */ DmpError)
        DD0:        Value of the Device Descriptor 0 as returned by the device.
        DmpError:   Possible error indication.

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        C->>S: PC_Get_Value.req message (Length = 2 octet, Address = 004Eh)
        S->>C: PC_Get_Value.con message (Length = 2 octet, Address = 004Eh, Data = DD0)
    ```

    Exception handling
    The general exception handling is applicable

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dmp_connect_l_emi1(xknx: XKNX) -> None:
    """DMP_Connect_LEmi1 — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_Connect_LEmi1 (KNX 03.05.02 §3.2.3) — implementation pending"
    )
