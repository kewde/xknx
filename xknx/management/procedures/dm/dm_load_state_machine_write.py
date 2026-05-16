"""
DM_LoadStateMachineWrite — KNX 03.05.02 §3.31 (PDF p. 132).

Spec text (verbatim from spec):

    3.31.1 Use
    This device Management Procedure shall be used to write to the Load State Machine of a Management
    Server. The data are located in the Management Procedure. Depending on the flag the resulting state
    shall be verified immediately.
    The Load State Machines are specified in [05].
    A DM_Connect shall be executed before executing this Management Procedure.
    DM_LoadStateMachineWrite                   (flags, stateMachineType, stateMachineNr, event, eventData)
          flags                    bit 0 :   location of data
                                                   0: -
                                                   1: in management control
                                   bit 1 :   verify resulting state enabled / disabled
                                                   0: disabled
                                                   1: enabled
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


async def dm_load_state_machine_write(xknx: XKNX) -> None:
    """DM_LoadStateMachineWrite — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DM_LoadStateMachineWrite (KNX 03.05.02 §3.31) — implementation pending"
    )
