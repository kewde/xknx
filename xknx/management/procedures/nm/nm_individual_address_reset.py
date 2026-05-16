"""
NM_IndividualAddress_Reset — KNX 03.05.02 §2.18 (PDF p. 33).

Spec pseudocode (verbatim from spec):

    repeat
       reset Individual Address of all devices in which the Programming Mode is active
                            A_IndividualAddress_Write-PDU
                                   (newaddress= FFFFh)

       reset all devices with Individual Address FFFFh (deactivate Programming Mode)
                                       A_Connect-PDU
                                              ()
                                 destination_address= FFFFh

                                         A_Restart-PDU
                                               ()
                                  destination_address = FFFFh

                                       A_Disonnect-PDU
                                               ()
                                  destination_address = FFFFh

       verify, that all devices are reset
                               A_IndividualAddress_Read-PDU
                                             ()

                              A_IndividualAddress_Response-PDU                                one or more responses may be
                                              ()                                              received from different devices

                                                ...

    until no A_IndividualAddress_Response-PDU is received

    Do not evaluate any local confirmation, or received telegrams, except the
    A_IndividualAddress_Read.Lcon and the A_IndividualAddress_Response-PDU.

Inputs (from spec):
    None (procedure resets all devices in Programming Mode)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def nm_individual_address_reset(xknx: XKNX) -> None:
    """NM_IndividualAddress_Reset — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "NM_IndividualAddress_Reset (KNX 03.05.02 §2.18) — implementation pending"
    )
