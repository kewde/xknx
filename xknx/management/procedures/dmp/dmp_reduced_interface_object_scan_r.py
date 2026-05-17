"""
DMP_ReducedInterfaceObjectScan_R — KNX 03.05.02 §3.28.3 (PDF p. 128).

Spec text (verbatim from spec):

    Use
    This Management Procedure shall scan the Interface Objects in a device with Reduced Interface
    Objects. Prior to this Management Procedure the Management Procedure DMP_Connect_RCl can be
    executed to identify the remote device.

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        Note over C: objectNr = 0
        loop repeat until PID = 0
            opt Interface Object scan is enabled
                C->>S: A_PropertyValue_Read-PDU (object_index = objectNr, PID = 01h, start_index = 01h, element_count = 01h)
                Note right of S: PID 01h is the Object Type
                S->>C: A_PropertyValue_Response-PDU (object_index = objectNr, PID = 01h, start_index = 01h, element_count = 01h, data = object_type)
                Note right of S: A_Disconnect.ind ⇒ error, no data received ⇒ error
            end
            Note over C: objectNr++
        end
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


async def dmp_reduced_interface_object_scan_r(xknx: XKNX) -> None:
    """DMP_ReducedInterfaceObjectScan_R — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_ReducedInterfaceObjectScan_R (KNX 03.05.02 §3.28.3) — implementation pending"
    )
