"""
DM_RunStateMachineRead — KNX 03.05.02 §3.36 (PDF p. 155).

Spec text (verbatim from spec):

    3.36.1 Use
    This device Management Procedure shall be used to read the state of a Run State Machine of a
    Management Server The state shall be located in the Management Procedure.
    A DM_Connect shall be executed before executing this Management Procedure.

    DM_RunStateMachineRead (dataBlockStartAddress, flags, stateMachineType, stateMachineNr, state)
        flags                  bit 0: location of data
                                   0: in data block
                                   1: -
                               All other bits are reserved. These shall be set to 0. This shall be
                               tested by the Management Client.
        dataBlockStartAddress  specifies the address where the data are stored in the data block.
        stateMachineType       type of the object that contains the state machine

                               state machine          type
                               application program    0003
                               PEI program            0004

        stateMachineNr         index to the state machine. For this index only the state
                               machines of this type are relevant. This index starts counting
                               from 0.

    3.36.2 Procedure: DMP_RunStateMachineRead_RCo_Mem
    This Management Procedure shall use the connection oriented communication mode.
    The control and state of the Run State Machine shall be located in the memory of the Management
    Server and shall be accessible as Memory Mapped Resource.
    This Management Procedure shall support only one state machine of each type.
    This Management Procedure shall only be used with device model for mask version 070nh (BIM
    M112). The address (AAAA) of the run state depends on the Run State Machine.

                               state machine          address of run state
                               application program    0101h
                               PEI program            0102h

    This Management Procedure shall not be used for further developments of Management Servers.

    Used Application Layer Services for Management
    - A_Memory_Read

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        C->>S: A_Memory_Read-PDU (addr = AAAA, length = 01h)
        S->>C: A_Memory_Response-PDU (addr = AAAA, length = 01h, data = runstate)
        Note right of S: A_Disconnect.ind ⇒ error
    ```

    Exception handling
    To be completed.

    3.36.3 Procedure: DMP_RunStateMachineRead_R_IO
    This method shall use either the connection oriented or the connectionless communication mode.
    The control and state of the Run State Machine shall be located in Interface Objects of the
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
        opt Property of run control is unknown to the Management Client
            C->>S: A_PropertyDescription_Read-PDU (object_index = X, PID = PID_RUN_STATE_CONTROL)
            S->>C: A_PropertyDescription_Response-PDU (object_index = X, PID = PID_RUN_STATE_CONTROL, type = PDT_CONTROL, ...)
            Note right of S: A_Disconnect.ind ⇒ error, Property does not exist ⇒ error
        end
        C->>S: A_PropertyValue_Read-PDU (object_index = X, PID = PID_RUN_STATE_CONTROL, start_index = 1, element_count = 1)
        S->>C: A_PropertyValue_Response-PDU (object_index = X, PID = PID_RUN_STATE_CONTROL, start_index = 1, element_count = 1, data = runstate)
        Note right of S: A_Disconnect.ind ⇒ error
    ```

    Exception handling
    The general exception handling shall apply.

    3.36.4 Procedure: DMP_ExtRunStateMachineRead_RCo_IO
    This Management Procedure shall use the connection oriented communication mode.

    Used Application Layer Services for Management
    - A_FunctionPropertyExtState_Read

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        C->>S: A_FunctionPropertyExtState_Read-PDU (object_type = OT, object_instance = OI, PID = PP)
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


async def dm_run_state_machine_read(xknx: XKNX) -> None:
    """DM_RunStateMachineRead — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DM_RunStateMachineRead (KNX 03.05.02 §3.36) — implementation pending"
    )
