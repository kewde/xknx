"""
DM_LoadStateMachineRead — KNX 03.05.02 §3.33 (PDF p. 146).

Spec text (verbatim from spec):

    3.33.1 Use
    This device Management Procedure shall be used to read the state of a Load State Machine of a
    Management Server. The state shall be located in the Management Procedure.
    A DM_Connect shall be executed before executing this Management Procedure.

    DM_LoadStateMachineRead (dataBlockStartAddress, flags, stateMachineType, stateMachineNr, state)
        dataBlockStartAddress  specifies the address where the data are stored in the data block
        flags                  bit 0: location of data
                                   0: in data block
                                   1: -
                               All other bits are reserved. These shall be set to 0. This shall be
                               tested by the Management Client.
        stateMachineType       type of the object that contains the state machine:

                               type   state machine
                               0001   address table
                               0002   association table
                               0003   application program

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dm_load_state_machine_read(xknx: XKNX) -> None:
    """DM_LoadStateMachineRead — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DM_LoadStateMachineRead (KNX 03.05.02 §3.33) — implementation pending"
    )
