"""
DM_Delay — KNX 03.05.02 §3.8 (PDF p. 90).

Spec text (verbatim from spec):

    3.8.1        Use
    This device Management Procedure shall be used to wait a specified time before starting the next
    action.
    DM_Delay            (flags, delay time)
          delay time                     Time in milliseconds
          flags                          All bits are reserved. These shall be set to 0. This shall be tested
                                         by the Management Client.

    3.8.2        Procedure: DMP_Delay
    Used Application Layer Services for Management
    None.
    Sequence
    Management                                                              Management                remark
    Client                                                                  Server

                  delay for specified time

    Exception handling
    The general exception handling shall apply.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dm_delay(xknx: XKNX) -> None:
    """DM_Delay — see module docstring for the verbatim spec text."""
    raise NotImplementedError("DM_Delay (KNX 03.05.02 §3.8) — implementation pending")
