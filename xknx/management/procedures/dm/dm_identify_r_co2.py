"""
DM_Identify_RCo2 — KNX 03.05.02 §3.4.3 (PDF p. 73).

Spec text (verbatim from spec):

    This Management Procedure shall use the point-to-point connection-oriented communication mode.
    DM_Identify_RCo2 (destination_address)
        server IA                   Individual Address of the Management Server

        device descriptor type 0    device descriptor of the Management Server
        manufacturer id             identification of the manufacturer of the Management
                                    Server
        hardware type               hardware type of the Management Server

    Used Application Layer Services for Management
    - A_Connect
    - A_DeviceDescriptor_Read
    - A_PropertyValue_Read

    Sequence
    If no Transport Layer connection exists between the Management Server and the Management Client,
    the Management Client shall execute the procedure DM_Connect_RCo prior to this procedure.
    NOTE DM_Connect_RCo already returns the value of the Device Descriptor Type 0 of the Management Server. This result
    is part of the return of this procedure NM_Identify_RCo2.

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Network / Management Server
        C->>S: A_PropertyValue_Read-PDU (destination_address = server IA, object_index = 0, Property_id = PID_MANUFACTURER_ID, nr_of_elem = 1, start_index = 1)
        S->>C: A_PropertyValue_Response-PDU (source_address = server IA, object_index = PID_MANUFACTURER_ID, nr_of_elem = 1, start_index = 1, data = manufacturer id)
        C->>S: A_PropertyValue_Read-PDU (destination_address = server IA, object_index = 0, Property_id = PID_HARDWARE_TYPE, nr_of_elem = 1, start_index = 1)
        S->>C: A_PropertyValue_Response-PDU (source_address = server IA, object_index = PID_HARDWARE_TYPE, nr_of_elem = 1, start_index = 1, data = hardware type)
    ```

    Exception handling
    The default error handling applies. If any of these services fails (time-out, negative response, no
    response) then the request shall be repeated up to three times. On further failure, the Management
    Procedure and the encompassing Configuration Procedure shall be interrupted.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dm_identify_r_co2(xknx: XKNX) -> None:
    """DM_Identify_RCo2 — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DM_Identify_RCo2 (KNX 03.05.02 §3.4.3) — implementation pending"
    )
