"""
DM_FunctionProperty_Write_R — KNX 03.05.02 §3.30 (PDF p. 131).

Spec text (verbatim from spec):

    3.30.1 Use
    This Management Procedure shall use point-to-point connection-oriented or point-to-point
    connectionless communication mode. In case the point-to-point connection-oriented communication
    mode is used, a DMP_Connect_RCo shall be performed preceding this procedure.
    Used Application Layer Services for Management
    - A_FunctionPropertyCommand

    Parameters used during this Management Procedure
    - OI:      Object Index of the Interface Object in which the Function Property is located.
    - PID:     Property Identifier of the Function Property
    - command: The command that is requested of the Function Property. The coding shall be
               Function Property specific and is specified in [05]
    - error:   Error code returned by the Function Property Server.

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        C->>S: A_FunctionPropertyCommand-PDU (object_index = OI, Property_id = PID, data = command)
        Note right of S: The Management Server shall execute the Function Property and return the result and error indication to the Management Client.
        S->>C: A_FunctionPropertyState_Response-PDU (object_index = OI, Property_id = PID, return_code = error, data = command)
    ```

    Error handling
    The error shall be Function Property specific and is specified in [05]. The handling of this error
    depends on the Configuration Procedure in which this Management Procedure is used.

    3.30.2 Procedure: DMP_ExtFunctionProperty_Write_R
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


async def dm_function_property_write_r(xknx: XKNX) -> None:
    """DM_FunctionProperty_Write_R — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DM_FunctionProperty_Write_R (KNX 03.05.02 §3.30) — implementation pending"
    )
