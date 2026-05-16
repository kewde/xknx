"""
DMP_ExtLoadStateMachineWrite_RCo_IO — KNX 03.05.02 §3.31.5 (PDF p. 142).

Spec text (verbatim from spec):

    This Management Procedure shall use the connection oriented communication mode.
    Used Application Layer Services for Management
        •     A_FunctionPropertyExtCommand
    Sequence
    Management                                                                     Management
    Client                                                                         Server

                          A_ FunctionPropertyExtCommand-PDU
                     (object_type = OT, object_instance = OI, PID = PP,
                                     data = command)

                                                                                                 The Management Server
                        A_FunctionPropertyExtState_Response-PDU                                  shall execute the Control
                     (object_type = OT, object_instance = OI, PID = PP,                          Property and return the
                                     data = load state)                                          result and error indication
                                                                                                 to the Management Client

    The format of command shall be identical to the one specified for
    DMP_LoadStateMachineWrite_RCo_IO in 3.31.3.
    Exception handling
    The general exception handling shall apply.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dmp_ext_load_state_machine_write_r_co_io(xknx: XKNX) -> None:
    """DMP_ExtLoadStateMachineWrite_RCo_IO — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_ExtLoadStateMachineWrite_RCo_IO (KNX 03.05.02 §3.31.5) — implementation pending"
    )
