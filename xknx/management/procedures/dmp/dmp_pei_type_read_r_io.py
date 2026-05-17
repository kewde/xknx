"""
DMP_PeiTypeRead_R_IO — KNX 03.05.02 §3.15.3 (PDF p. 98).

Spec text (verbatim from spec):

    This Management Procedure shall use the connection oriented or connectionless communication
    mode.
    The value shall be read via the Interface Objects.

    Used Application Layer Services for Management
    - A_PropertyDescription_Read
    - A_PropertyValue_Read

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        opt Property of management control is unknown to the Management Client
            C->>S: A_PropertyDescription_Read-PDU (object_index = DeviceObject, PID = PID_PEI_TYPE)
            S->>C: A_PropertyDescription_Response-PDU (object_index = DeviceObject, PID = PID_PEI_TYPE, type = .., ...)
            Note right of S: A_Disconnect.ind ⇒ error, Property does not exist ⇒ error
        end
        C->>S: A_PropertyValue_Read-PDU (object_index = DeviceObject, PID = PID_PEI_TYPE, start_index = 01H, element_count = 01h)
        S->>C: A_PropertyValue_Response-PDU (object_index = DeviceObject, PID = PID_PEI_TYPE, start_index = 01H, element_count = 01h, data = PEI-Type)
        Note right of S: A_Disconnect.ind ⇒ error, no data received ⇒ error
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


async def dmp_pei_type_read_r_io(xknx: XKNX) -> None:
    """DMP_PeiTypeRead_R_IO — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_PeiTypeRead_R_IO (KNX 03.05.02 §3.15.3) — implementation pending"
    )
