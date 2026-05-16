"""
NM_DomainAndIndividualAddress_Write2 — KNX 03.05.02 §2.10 (PDF p. 23-24).

Spec pseudocode (verbatim from spec):

    1. Wait until Programming Mode is active in the device.
       Repeat until one A_IndividualAddress_Response-PDU is received.
                           A_IndividualAddress_Read-PDU
                                         ()
                           comm_mode = system broadcast

                         A_IndividualAddress_Response-PDU
                          (source_address = NmpIACurrent)

          The Management client shall store the KNX Serial Number of the device.
          If more than one response is received:
          ⇒ Programming Mode is active in more than one device
       end repeat

    2. Set Domain Address
                             A_DomainAddress_Write-PDU
                           (domain_address = NmpDoANew)
                            comm_mode = system broadcast

                                                  The device shall store and use the received Domain Address NmpDoANew.

    3. Set Individual Address
       if NmpIANew ≠ NmpIACurrent
                           A_IndividualAddress_Write-PDU
                            (new_address = NmpIANew)
                           comm_mode = system broadcast

                                                               The device shall store the received Individual Address.
       endif

    4. verify
                         A_DeviceDescriptor_Read-PDU
                        (destination address = NmpIANew,
                                descriptor_type = 0)
                     comm_mode = point-to-point connectionless

                        A_DeviceDescriptor_Response-PDU
                        (descriptor_type, device_descriptor)
                     comm_mode = point-to-point connectionless
    See note a)
                                     A_Restart-PDU
                                           ()

                                                                            The device shall quit Programming Mode.

Inputs (from spec):
    [in] NmpDoANew, [in] NmpIANew, [out] NmpIACurrent
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def nm_domain_and_individual_address_write2(xknx: XKNX) -> None:
    """NM_DomainAndIndividualAddress_Write2 — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "NM_DomainAndIndividualAddress_Write2 (KNX 03.05.02 §2.10) — implementation pending"
    )
