"""
DMP_RunStateMachineVerify_R_IO — KNX 03.05.02 §3.35.3 (PDF p. 154).

Spec text (verbatim from spec):

    This method shall use either the connection oriented or the connectionless communication mode.
    The control and state of the Run State Machine shall be located in Interface Objects of the
    Management Server and shall be accessible via Property services.
    The Management Client shall search the according Interface Object in the Management Server.
    Used Application Layer Services for Management
        •     A_PropertyDescription_Read
        •     A_PropertyValue_Read

    Sequence
    Management                                                            Management                remark
    Client                                                                Server
    if Property of run control is unknown to the Management Client
                         A_PropertyDescription_Read-PDU
                                   (object_index = X,
                       PID = PID_RUN_STATE_CONTROL)

                        A_PropertyDescription_Response-PDU                             A_Disconnect.ind ⇒ error,
                                 (object_index = X,                                    Property does not exist ⇒
                        PID = PID_RUN_STATE_CONTROL,                                   error
                             type = PDT_CONTROL...)

    endif
                             A_PropertyValue_Read-PDU
                                   (object_index = X,
                        PID = PID_RUN_STATE_CONTROL,
                          start_index = 1, element_count = 1)

                          A_PropertyValue_Response-PDU                                 A_Disconnect.ind ⇒ error,
                                  (object_index = X,                                   Wrong state ⇒ error
                        PID = PID_RUN_STATE_CONTROL,
                 start_index = 1, element_count = 1, data = runstate)

    Exception handling
    To be completed.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dmp_run_state_machine_verify_r_io(xknx: XKNX) -> None:
    """DMP_RunStateMachineVerify_R_IO — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_RunStateMachineVerify_R_IO (KNX 03.05.02 §3.35.3) — implementation pending"
    )
