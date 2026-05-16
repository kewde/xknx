"""
NM_Router_Scan — KNX 03.05.02 §2.15 (PDF p. 30).

Spec pseudocode (verbatim from spec):

    for (SNA_Current = 0; SNA_Current = 255; SNA_Current = SNA_Current+1)
                                   A_Connect-PDU                                       collect all received
                      (destination_address.SNA = SNA_Current;                          A_Disconnect-PDUs
                            destination_address.DA = 00h)

                                      delay for 0,1 s
                                        collect
                                  A_Disconnect-PDU
                      (destination_address.SNA = SNA_Current;
                            destination_address.DA = 00h)

    endfor
                                         collect                                       time-out: 6s after last sent
                                   A_Disconnect-PDU                                    A_Connect
                            (destination_address.SNA = any;
                             destination_address.DA = 00h)

Inputs (from spec):
    None (implicit variables: SNA_Current)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def nm_router_scan(xknx: XKNX) -> None:
    """NM_Router_Scan — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "NM_Router_Scan (KNX 03.05.02 §2.15) — implementation pending"
    )
