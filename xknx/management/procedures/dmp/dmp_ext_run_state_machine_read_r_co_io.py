"""
DMP_ExtRunStateMachineRead_RCo_IO — KNX 03.05.02 §3.36.4 (PDF p. 157).

Spec text (verbatim from spec):

    This Management Procedure shall use the connection oriented communication mode.

    Used Application Layer Services for Management
    - A_FunctionPropertyExtState_Read

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        C->>S: A_ FunctionPropertyExtState_Read-PDU (object_type = OT, object_instance = OI, PID = PP)
        S->>C: A_FunctionPropertyExtState_Response-PDU (object_type = OT, object_instance = OI, PID = PP, data = run state)
        Note right of S: The Management Server shall return the result and error indication to the Management Client
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


async def dmp_ext_run_state_machine_read_r_co_io(xknx: XKNX) -> None:
    """DMP_ExtRunStateMachineRead_RCo_IO — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_ExtRunStateMachineRead_RCo_IO (KNX 03.05.02 §3.36.4) — implementation pending"
    )
