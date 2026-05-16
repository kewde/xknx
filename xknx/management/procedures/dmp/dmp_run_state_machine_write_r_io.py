"""
DMP_RunStateMachineWrite_R_IO — KNX 03.05.02 §3.34.3 (PDF p. 150).

Spec text (verbatim from spec):

    This method shall use either the connection oriented or the connectionless communication mode.
    The control and state of the Run State Machine shall be located in Interface Objects of the
    Management Server and shall be accessible via Property services.
    The Management Client shall search the according Interface Object in the Management Server.
    Used Application Layer Services for Management
        •     A_PropertyDescription_Read
        •     A_PropertyValue_Write

    Sequence
    Management                                                             Management                remark
    Client                                                                 Server
    if Property of run control is unknown to the Management Client
                         A_PropertyDescription_Read-PDU
                                   (object_index = X,
                       PID = PID_RUN_STATE_CONTROL)

                          A_PropertyDescription_Response-PDU                            A_Disconnect.ind ⇒ error,
                                    (object_index = X,                                  Property does not exist ⇒
                          PID = PID_RUN_STATE_CONTROL,                                  error
                               type = PDT_CONTROL, ...)

    endif
                                A_PropertyValue_Write-PDU
                                     (object_index = X,
                           PID = PID_RUN_STATE_CONTROL,
                       start_index = 1, element_count = 1, data = EE)

                            A_PropertyValue_Response-PDU                                A_Disconnect.ind ⇒ error,
                                    (object_index = X,                                  Wrong state ⇒ error
                          PID = PID_RUN_STATE_CONTROL,
                   start_index = 1, element_count = 1, data = runstate)

    Exception handling
    The transmitted data depend on the event and are specified in the clauses 3.34.3.1 to 3.34.3.4 below.

    3.34.3.1 Run Control: Restart (Write)
     01h         00h     00h    00h     00h      00h    00h      00h      00h   00h
     8 bit                                     9 octets

    This command shall restart the executable part related to the Interface Object in which this Run
    Control Property is located.

    3.34.3.2 Run Control: Stop (Write)
     02h         00h     00h    00h     00h      00h    00h      00h      00h   00h
     8 bit                                     9 octets

    This command shall stop the executable part related to the Interface Object in which this Run Control
    Property is located.

    3.34.3.3 Run Control: No Operation (Write)
     00h         00h     00h    00h     00h      00h    00h      00h      00h   00h
     8 bit                                     9 octets

    This command shall have no effect.

    3.34.3.4 Run State (Read from Run Control)
     State
     8 bit

    This state value shall be the Run State of the Run State Machine.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dmp_run_state_machine_write_r_io(xknx: XKNX) -> None:
    """DMP_RunStateMachineWrite_R_IO — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_RunStateMachineWrite_R_IO (KNX 03.05.02 §3.34.3) — implementation pending"
    )
