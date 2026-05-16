"""
DMP_ExtRunStateMachineVerify_RCo_IO — KNX 03.05.02 §3.35.4 (PDF p. 155).

Spec text (verbatim from spec):

    This Management Procedure shall use the connection oriented communication mode.
    Used Application Layer Services for Management
        •   A_FunctionPropertyExtState_Read
    Sequence
    Management                                                              Management
    Client                                                                  Server

                      A_ FunctionPropertyExtState_Read-PDU
                 (object_type = OT, object_instance = OI, PID = PP)

                    A_FunctionPropertyExtState_Response-PDU                              The Management Server
                 (object_type = OT, object_instance = OI, PID = PP,                      shall return the result and
                                  data = run state)                                      error indication to the
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


async def dmp_ext_run_state_machine_verify_r_co_io(xknx: XKNX) -> None:
    """DMP_ExtRunStateMachineVerify_RCo_IO — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_ExtRunStateMachineVerify_RCo_IO (KNX 03.05.02 §3.35.4) — implementation pending"
    )
