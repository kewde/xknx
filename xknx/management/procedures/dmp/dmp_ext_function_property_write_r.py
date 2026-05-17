"""
DMP_ExtFunctionProperty_Write_R — KNX 03.05.02 §3.30.2 (PDF p. 131).

Spec text (verbatim from spec):

    This Management Procedure shall use the connection oriented or connectionless communication
    mode.

    Used Application Layer Services for Management
    - A_FunctionPropertyExtCommand

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        C->>S: A_ FunctionPropertyExtCommand-PDU (object_type = OT, object_instance = OI, PID = PP, data = command)
        S->>C: A_FunctionPropertyExtState_Response-PDU (object_type = OT, object_instance = OI, PID = PP, return_code = RC, data = output data)
        Note right of S: The Management Server shall execute the Function Property and return the result and error indication to the Management Client
    ```

    Exception handling
    The error shall be Function Property specific and is specified in [05]. The handling of this error
    depends on the Configuration Procedure in which this Management Procedure is used.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dmp_ext_function_property_write_r(xknx: XKNX) -> None:
    """DMP_ExtFunctionProperty_Write_R — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_ExtFunctionProperty_Write_R (KNX 03.05.02 §3.30.2) — implementation pending"
    )
