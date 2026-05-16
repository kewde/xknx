"""
DMP_ProgModeSwitch_RCo — KNX 03.05.02 §3.13.2 (PDF p. 94).

Spec text (verbatim from spec):

    This Management Procedure shall use the connection oriented communication mode.
    The Programming Mode shall be realised as “Programming Mode – Realisation Type 2” as specified
    in [05].
    NOTE         This means that the state of the Programming Mode is located at memory address 60h.

    Used Application Layer Services for Management
        •     A_Memory_Read
        •     A_Memory_Write

    Sequence
    Management                                                                     Management                     remark
    Client                                                                         Server

                                     A_Memory_Read-PDU
                                    (Addr = 60h, Length = 1)

                                 A_Memory_Response-PDU                                           A_Disconnect.ind ⇒ error,
                             (Addr = 60h, Length = 1, Data = DD)                                 different or no data received
                                                                                                 ⇒ error
                                   A_Memory_Write-PDU                                            In the data (DD) bit 0 has to
                             (Addr = 60h, Length = 1, Data = DD)                                 be set according to the mode.
                                                                                                 The parity (bit 7) has to be
                                                                                                 calculated.

    Exception handling
    The general exception handling shall apply.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dmp_prog_mode_switch_r_co(xknx: XKNX) -> None:
    """DMP_ProgModeSwitch_RCo — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_ProgModeSwitch_RCo (KNX 03.05.02 §3.13.2) — implementation pending"
    )
