"""
NM_SerialNumberDefaultIA_Scan — KNX 03.05.02 §2.24 (PDF p. 65).

Spec text (verbatim from spec):

    Use
    This Network Management Procedure shall be used to obtain the KNX Serial Number of each device
    of which the Individual Address (IA) is the default Individual Address for the given medium
    (Subnetwork address as specified in [05], this is, with the Device Address FFh..

    Used Application Layer Services for Management
    - A_PropertyValue_Read

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Network / Management Server
        C->>S: A_PropertyValue_Read-PDU (destination_address = default IA, object_index = 0, Property_id = 11, nr_of_elem = 1, start_index = 1)
        S->>C: A_PropertyValue_Response-PDU (source_address = default IA, object_index = 0, Property_id = 11, nr_of_elem = 1, start_index = 1, data = KNX Serial Number)
        Note right of S: Responses may be received from none, one or more devices.
        Note right of S: Time-out: 7 sec
        Note right of S: If no response is received, no device has the default Individual Address.
        Note over C,S: …
        S->>C: A_PropertyValue_Response-PDU (source_address = default IA, object_index = 0, Property_id = 11, nr_of_elem = 1, start_index = 1, data = KNX Serial Number)
    ```

    Exception handling
    The general exception handling applies.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def nm_serial_number_default_ia_scan(xknx: XKNX) -> None:
    """NM_SerialNumberDefaultIA_Scan — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "NM_SerialNumberDefaultIA_Scan (KNX 03.05.02 §2.24) — implementation pending"
    )
