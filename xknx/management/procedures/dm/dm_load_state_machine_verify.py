"""
DM_LoadStateMachineVerify — KNX 03.05.02 §3.32 (PDF p. 143).

Spec text (verbatim from spec):

    3.32.1 Use
    This device Management Procedure shall be used to verify the state of a Load State Machine of a
    Management Server. The state shall be located in the Management Procedure.
    A DM_Connect shall be executed before executing this Management Procedure.
    DM_LoadStateMachineVerify (flags, stateMachineType, stateMachineNr, state)
          flags                    bit 0 :   location of data
                                                   0: -
                                                   1: in management control
                                   All other bits are reserved. These shall be set to 0. This shall be tested by
                                   the Management Client.
          stateMachineType         type of the object that contains the state machine:

                                                    type       state machine
                                                    0001       address table
                                                    0002       association table
                                                    0003       application program

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dm_load_state_machine_verify(xknx: XKNX) -> None:
    """DM_LoadStateMachineVerify — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DM_LoadStateMachineVerify (KNX 03.05.02 §3.32) — implementation pending"
    )
