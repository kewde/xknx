"""
DM_RunStateMachineRead — KNX 03.05.02 §3.36 (PDF p. 155).

Spec text (verbatim from spec):

    3.36.1 Use
    This device Management Procedure shall be used to read the state of a Run State Machine of a
    Management Server The state shall be located in the Management Procedure.
    A DM_Connect shall be executed before executing this Management Procedure.
    DM_RunStateMachineRead                     (dataBlockStartAddress, flags, stateMachineType,
                                               stateMachineNr, state)
    flags                                      bit 0:        location of data
                                               0: in data block
                                               1: -
                                               All other bits are reserved. These shall be set to 0. This shall be
                                               tested by the Management Client.
    dataBlockStartAddress                      specifies the address where the data are stored in the data block.
    stateMachineType                           type of the object that contains the state machine
                                                      state machine                 type
                                                   application program              0003
                                                       PEI program                  0004

    stateMachineNr                             index to the state machine. For this index only the state
                                               machines of this type are relevant. This index starts counting
                                               from 0.

    3.36.2 Procedure: DMP_RunStateMachineRead_RCo_Mem
    This Management Procedure shall use the connection oriented communication mode.
    The control and state of the Run State Machine shall be located in the memory of the Management
    Server and shall be accessible as Memory Mapped Resource.
    This Management Procedure shall support only one state machine of each type.
    This Management Procedure shall only be used with device model for mask version 070nh (BIM
    M112). The address (AAAA) of the run state depends on the Run State Machine.
                                       state machine              address of run state
                                    application program                   0101h
                                        PEI program                       0102h

    This Management Procedure shall not be used for further developments of Management Servers.
    Used Application Layer Services for Management
        •     A_Memory_Read

    Sequence
    Management                                                             Management                remark
    Client                                                                 Server

                                A_Memory_Read-PDU
                              (addr = AAAA, length = 01h)

                             A_Memory_Response-PDU                                      A_Disconnect.ind ⇒ error,
                     (addr = AAAA, length = 01h, data = runstate)

    Exception handling
    To be completed.

    3.36.3 Procedure: DMP_RunStateMachineRead_R_IO
    This method shall use either the connection oriented or the connectionless communication mode.
    The control and state of the Run State Machine shall be located in Interface Objects of the
    Management Server and shall be accessible via Property services.
    The Management Client shall search the according Interface Object in the Management Server.
    Used Application Layer Services for Management
        •     A_PropertyDescription_Read
        •     A_PropertyValue_Read

    Sequence
    Management                                                            Management                 remark
    Client                                                                Server
    if Property of run control is unknown to the Management Client
                         A_PropertyDescription_Read-PDU
                                   (object_index = X,
                       PID = PID_RUN_STATE_CONTROL)

                        A_PropertyDescription_Response-PDU                             A_Disconnect.ind ⇒ error,
                                       ( = X,                                          Property does not exist ⇒
                        PID = PID_RUN_STATE_CONTROL,                                   error
                             type = PDT_CONTROL, ...)

    endif
                             A_PropertyValue_Read-PDU
                                   (object_index = X,
                        PID = PID_RUN_STATE_CONTROL,
                          start_index = 1, element_count = 1)

                          A_PropertyValue_Response-PDU                                 A_Disconnect.ind ⇒ error,
                                  (object_index = X,
                        PID = PID_RUN_STATE_CONTROL,
                 start_index = 1, element_count = 1, data = runstate)

    Exception handling
    The general exception handling shall apply.

    3.36.4 Procedure: DMP_ExtRunStateMachineRead_RCo_IO
    This Management Procedure shall use the connection oriented communication mode.
    Used Application Layer Services for Management
        •   A_FunctionPropertyExtState_Read
    Sequence
    Management                                                            Management
    Client                                                                Server

                      A_ FunctionPropertyExtState_Read-PDU
                 (object_type = OT, object_instance = OI, PID = PP)

                    A_FunctionPropertyExtState_Response-PDU                             The Management Server
                 (object_type = OT, object_instance = OI, PID = PP,                     shall return the result and
                                  data = run state)                                     error indication to the
                                                                                        Management Client

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
