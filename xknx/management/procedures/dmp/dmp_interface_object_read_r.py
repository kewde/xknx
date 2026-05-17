"""
DMP_InterfaceObjectRead_R — KNX 03.05.02 §3.27.2 (PDF p. 123).

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
        opt Property of management control is unknown to the Management Client
            C->>S: A_PropertyDescription_Read-PDU (object_index = OO, PID = PP)
            S->>C: A_PropertyDescription_Response-PDU (object_index = OO, PID = PP, type = .. , ...)
            Note right of S: A_Disconnect.ind ⇒ error, Property does not exist ⇒ error
        end
        loop for each data block, until all data are transmitted
            C->>S: A_PropertyValue_Read-PDU (object_index = OO, PID = PP, start_index = SSSS, element_count = EE)
            S->>C: A_PropertyValue_Response-PDU (object_index = OO, PID = PP, start_index = SSSS, element_count = EE, data = XX, ..)
            Note right of S: A_Disconnect.ind ⇒ error, no data received ⇒ error
        end
    ```

    Exception handling
    The general exception handling shall apply.
    The Management Client shall not interpret the value of the Property Index contained in the
    A_PropertyDescription_Response-PDU at the level of this Management Procedure. Possibly, error
    handling in case an unexpected value of the Property Index can be handled at the level of the
    Configuration Procedure in which this Management Procedure is used.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dmp_interface_object_read_r(xknx: XKNX) -> None:
    """DMP_InterfaceObjectRead_R — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_InterfaceObjectRead_R (KNX 03.05.02 §3.27.2) — implementation pending"
    )
