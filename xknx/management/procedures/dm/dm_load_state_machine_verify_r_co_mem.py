"""
DM_LoadStateMachineVerify_RCo_Mem — KNX 03.05.02 §3.32.2 (PDF p. 143).

Spec text (verbatim from spec):

    This Management Procedure shall use the connection oriented communication mode.
    The control and state of the Load State Machine shall be located in the memory of the Management
    Server and shall be accessible as Memory Mapped Resource.
    This Management Procedure shall support only one state machine of each type.
    This Management Procedure shall only be used with device model for mask version 070nh (BIM
    M112). The address of the management control shall be 0104h. The address (AAAA) of the load state
    depends on the Load State Machine.
                                                                 address of load state
                                      state machine
                                                                       (AAAA)
                             address table                                B6EAh
                             association table                            B6EBh
                             application program                          B6ECh
                             PEI program                                  B6EDh

    This Management Procedure shall not be used for further developments of Management Servers.

    Used Application Layer Services for Management
        •     A_Memory_Read

    Sequence
    Management                                                            Management                remark
    Client                                                                Server

                                A_Memory_Read-PDU
                              (addr = AAAA, length = 01h)

                              A_Memory_Response-PDU                                    A_Disconnect.ind ⇒ error,
                     (addr = AAAA, length = 01h, data = loadstate)                     different state ⇒ error

    Exception handling
    The general exception handling shall apply.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dm_load_state_machine_verify_r_co_mem(xknx: XKNX) -> None:
    """DM_LoadStateMachineVerify_RCo_Mem — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DM_LoadStateMachineVerify_RCo_Mem (KNX 03.05.02 §3.32.2) — implementation pending"
    )
