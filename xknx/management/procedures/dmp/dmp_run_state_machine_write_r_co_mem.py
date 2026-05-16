"""
DMP_RunStateMachineWrite_RCo_Mem — KNX 03.05.02 §3.34.2 (PDF p. 149).

Spec text (verbatim from spec):

    This Management Procedure shall use the connection oriented communication mode.
    The control and state of the Run State Machine shall be located in the memory of the Management
    Server and shall be accessible as Memory Mapped Resource.
    The Verify Mode of the Management Server shall not be used.
    This Management Procedure shall support only one state machine of each type.
    This Management Procedure shall only be used with device model for mask version 070nh (BIM
    M112). The address of the run control shall be 0103h. The address (AAAA) of the run state depends on
    the Run State Machine.
                                                                    address of run state
                                       state machine
                                                                         (AAAA)
                                    application program                     0101h
                                        PEI program                         0102h

    This Management Procedure shall not be used for further developments of Management Servers.
    Used Application Layer Services for Management
        •       A_Memory_Write
        •       A_Memory_Read

    Sequence
    Management                                                             Management                remark
    Client                                                                 Server
                                A_Memory_Write-PDU
                        (addr = 0103h, length = 01h, data = RE)

    repeat
                                A_Memory_Read-PDU
                              (addr = AAAA, length = 01h)

                             A_Memory_Response-PDU                                      A_Disconnect.ind ⇒ error,
                     (addr = AAAA, length = 01h, data = run state)                      Wrong state ⇒ error

    until runstate is correct (for max. 3 times)

    Exception handling
    The general exception handling shall apply.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dmp_run_state_machine_write_r_co_mem(xknx: XKNX) -> None:
    """DMP_RunStateMachineWrite_RCo_Mem — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_RunStateMachineWrite_RCo_Mem (KNX 03.05.02 §3.34.2) — implementation pending"
    )
