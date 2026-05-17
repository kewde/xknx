"""
DMP_ExtInterfaceObjectWriteCon_R — KNX 03.05.02 §3.25.4 (PDF p. 118).

Spec text (verbatim from spec):

    This Management Procedure shall use the connection oriented or connectionless communication
    mode.

    Used Application Layer Services for Management
    - A_PropertyExtDescription_Read
    - A_PropertyExtValue_WriteCon

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        opt Property of management control is unknown to the Management Client
            C->>S: A_PropertyExtDescription_Read-PDU (object_type = OT, object_instance = OI, PID = PP, type = 0)
            S->>C: A_PropertyExtDescription_Response-PDU (object_type = OT, object_instance = OI, PID = PP, type = 0, …)
            Note right of S: A_Disconnect.ind ⇒ error, Property does not exist ⇒ error
        end
        loop for each data block, until all data are transmitted
            C->>S: A_PropertyExtValue_WriteCon-PDU (object_type = OT, object_instance = OI, PID = PP, start_index = SSSS, nr_of_elem = EE, data = DD,…)
            S->>C: A_PropertyExtValue_WriteConRes-PDU (object_type = OT, object_instance = OI, PID = PP, start_index = SSSS, nr_of_elem = EE, return_code = RR)
            Note right of S: A_Disconnect.ind ⇒ error, RR ≠ 0 ⇒ error
        end
    ```

    Exception handling
    The general exception handling shall apply.
    The MaC shall not interpret the value of the Property Index contained in the A_Property_-
    Description_Response-PDU at the level of this Management Procedure. Possibly, error handling in
    case an unexpected value of the Property Index can be handled at the level of the Configuration
    Procedure in which this Management Procedure is used.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dmp_ext_interface_object_write_con_r(xknx: XKNX) -> None:
    """DMP_ExtInterfaceObjectWriteCon_R — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_ExtInterfaceObjectWriteCon_R (KNX 03.05.02 §3.25.4) — implementation pending"
    )
