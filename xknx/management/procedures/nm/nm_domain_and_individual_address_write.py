"""
NM_DomainAndIndividualAddress_Write — KNX 03.05.02 §2.9 (PDF p. 20-22).

Spec pseudocode (verbatim from spec):

    1. Verify whether the Individual Address IA_new is already occupied
       on the network.
                                     A_Connect-PDU
                             (destination_address = IA_new)

    if negative A_Connect.Lcon ⇒ IA_new is not occupied; continue with 2.
    else (this is, a positive A_Connect.Lcon is received)
                                                                                 If the device that occupies the IA IA_new
                                                                             does not support Transport Layer connections,
                                                                                         it shall send a T_Disconnect-PDU.
                                   A_Disconnect-PDU
                             (destination_address = IA_new)

    If an A_Disconnect-PDU is received then IA_new shall be regarded as occupied; end procedure.
    else (no A_Disconnect-PDU is received)
                                                              If a device that occupies IA_new is present on the network,
                                                                           and does support Transport Layer connections,
                                                                                  it shall have no other reaction on the bus
                                                 than the Layer-2 acknowledge that initiates the above A_Connect.Lcon
        The A_DeviceDescriptor_Read-PDU shall use DD0.
                             A_DeviceDescriptor_Read-PDU
                             (destination_address = IA_new,
                                descriptor_type = 0000h)

                          A_DeviceDescriptor_Response-PDU
                          (descriptor_type, device_descriptor)

    If the Management Client receives an A_DeviceDescriptor_Response-PDU it shall
    conclude that the Individual Address IA_new is occupied.
        The Management Client shall accept any value of descriptor_type, also values ≠ 0.
    If no A_DeviceDescriptor_Response-PDU is received after time-out
    ⇒ IA_new is not occupied
    endif
                                   A_Disconnect-PDU
                             (destination_address = IA_new)

    2. wait until Programming Mode is active in the device:
    repeat until one A_IndividualAddress_Response-PDU is received
                              A_DomainAddress_Read-PDU
                                         ()

                          A_DomainAddress_Response-PDU                               one or more responses may be
                            (source_address = IA_current,                            received from different devices
                           domain_addres= DoA_current)                               time-out: 1 s

                                               …

    if more than one response is received ⇒ than Programming Mode is active in more than one device
    end repeat

    3.set Domain Address and Individual Address
    if Domain Address DoA_current != DoA_new
                              A_DomainAddress_Write-PDU
                              (domain_address = DoA_new)

    endif
    if IA_current != IA_new
                           A_IndividualAddress_Write-PDU
                              (new_address = IA_new)

    endif

    4. verify and inactivate programming mode
                                      A_Connect-PDU
                              (destination_address = IA_new)

                            A_DeviceDescriptor_Read-PDU
                              (descriptor_type = 0000h)

                          A_DeviceDescriptor_Response-PDU
                          (descriptor_type, device_descriptor)

                                     A_Restart-PDU
                                           ()

    Abort the connection of the Management Client side Transport Layer.

Inputs (from spec):
    [in] DoA_new, [in] IA_new
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def nm_domain_and_individual_address_write(xknx: XKNX) -> None:
    """NM_DomainAndIndividualAddress_Write — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "NM_DomainAndIndividualAddress_Write (KNX 03.05.02 §2.9) — implementation pending"
    )
