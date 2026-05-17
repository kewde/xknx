"""
DM_RunStateMachineWrite — KNX 03.05.02 §3.34 (PDF p. 148).

Spec text (verbatim from spec):

    3.34.1 Use
    This device Management Procedure shall be used to write to the Run State Machine of a Management
    Server The data shall be located in the Management Procedure. Depending on the flag, the resulting
    state is verified immediately.

                          event     resulting state
                          Restart   Ready or Running
                          Stop      Terminated

    A DM_Connect shall be executed before executing this Management Procedure.

    DM_RunStateMachineWrite (flags, stateMachineType, stateMachineNr, event)
        flags             bit 0: location of data
                              0: -
                              1: in management control
                          bit 1: verify the resulting state enabled / disabled
                              0: disabled
                              1: enabled
                          All other bits are reserved. These shall be set to 0. This shall be
                          tested by the Management Client.
        stateMachineType  type of the object that contains the state machine:

                          type   state machine
                          0003   application program

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dm_run_state_machine_write(xknx: XKNX) -> None:
    """DM_RunStateMachineWrite — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DM_RunStateMachineWrite (KNX 03.05.02 §3.34) — implementation pending"
    )
