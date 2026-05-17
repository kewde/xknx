"""
DMP_InterfaceObjectScan_R — KNX 03.05.02 §3.28.2 (PDF p. 126).

Spec text (verbatim from spec):

    This Management Procedure shall use the connection oriented or connectionless communication
    mode.

    Used Application Layer Services for Management
    - A_PropertyDescription_Read
    - A_PropertyValue_Read

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        Note over C,S: object_index = 0;
        loop repeat if Interface Object scan is enabled
            C->>S: A_PropertyDescription_Read-PDU (object_index, PID = 0, Property_index = 0)
            S->>C: A_PropertyDescription_Response-PDU (object_index, Property_index = 0, PID)
            opt Interface Object exists (Property ID <> 0)
                C->>S: A_PropertyValue_Read-PDU (object_index, PID = 01h, start_index = 01h, element_count = 01h)
                S->>C: A_PropertyValue_Response-PDU (object_index, PID = 01h, start_index = 01h, element_count = 01h, data = object_type)
                Note right of S: A_Disconnect.ind ⇒ error, no data received ⇒ error
            end
            Note over C,S: Property_index = 0;
            loop repeat if Property scan is enabled
                C->>S: A_PropertyDescription_Read-PDU (object_index, PID = 0, Property_index = 0)
                S->>C: A_PropertyDescription_Response-PDU (object_index, Property_index = 0, PID)
                Note over C,S: Property_index ++
                Note over C,S: until PID = 0
            end
            Note over C,S: object_index ++
            Note over C,S: until PID = 0
        end
    ```

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dmp_interface_object_scan_r(xknx: XKNX) -> None:
    """DMP_InterfaceObjectScan_R — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_InterfaceObjectScan_R (KNX 03.05.02 §3.28.2) — implementation pending"
    )
