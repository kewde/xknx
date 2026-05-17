"""
DMP_ReducedInterfaceObjectWrite_R — KNX 03.05.02 §3.25.3 (PDF p. 118).

Spec text (verbatim from spec):

    Prior to this procedure the procedure DMP_Connect_RCl can be executed to identify the remote
    device.

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        loop for each data block, until all data is transmitted
            C->>S: A_PropertyValue_Write-PDU (objectNr = OO, PID = PP, start_index = SSSS, element_count = EE, data = DD, ..)
            S->>C: A_PropertyValue_Response-PDU (objectNr = OO, PID = PP, start_index = SSSS, element_count = EE, data = XX, ...)
            Note right of S: A_Disconnect.ind ⇒ error, if verify = enabled and different or no data received ⇒ error
        end
    ```

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dmp_reduced_interface_object_write_r(xknx: XKNX) -> None:
    """DMP_ReducedInterfaceObjectWrite_R — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_ReducedInterfaceObjectWrite_R (KNX 03.05.02 §3.25.3) — implementation pending"
    )
