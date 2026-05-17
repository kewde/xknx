"""
DMP_LoadStateMachineRead_R_IO — KNX 03.05.02 §3.33.3 (PDF p. 147).

Spec text (verbatim from spec):

    This method shall use either the connection oriented or the connectionless communication mode.
    The control and state of the Load State Machine shall be located in Interface Objects of the
    Management Server and shall be accessible via Property services.
    The Management Client shall search the according Interface Object in the Management Server.

    Used Application Layer Services for Management
    - A_PropertyDescription_Read
    - A_PropertyValue_Read

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        opt Property of management control is unknown to the Management Client
            C->>S: A_PropertyDescription_Read-PDU (object_index = X, PID = PID_LOAD_STATE_CONTROL)
            S->>C: A_PropertyDescription_Response-PDU (object_index = X, PID = PID_LOAD_STATE_CONTROL, type = PDT_CONTROL, ...)
            Note right of S: A_Disconnect.ind ⇒ error, Property does not exist ⇒ error
        end
        C->>S: A_PropertyValue_Read-PDU (object_index = X, PID = PID_LOAD_STATE_CONTROL, start_index = 1, element_count = 1)
        S->>C: A_PropertyValue_Response-PDU (object_index = X, PID = PID_LOAD_STATE_CONTROL, start_index = 1, element_count = 1, data = loadstate)
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


async def dmp_load_state_machine_read_r_io(xknx: XKNX) -> None:
    """DMP_LoadStateMachineRead_R_IO — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_LoadStateMachineRead_R_IO (KNX 03.05.02 §3.33.3) — implementation pending"
    )
