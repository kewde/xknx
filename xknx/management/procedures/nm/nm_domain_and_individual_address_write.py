"""
NM_DomainAndIndividualAddress_Write — KNX 03.05.02 §2.9 (PDF p. 19).

Spec text (verbatim from spec):

    Use
    This Network Management Procedure shall be used to set the Domain Address and the Individual
    Address of one single device that is in Programming Mode.
    This procedure shall ensure that no other device has the same Individual Address and shall wait until
    there is exactly one device in which Programming Mode is active. It shall verify whether the
    programming is successful and shall switch deactivate the Programming Mode in the device into by
    executing a restart of the device.
    For this procedure the Management Server has to provide a free Domain Address.
    Used Application Layer Services for Management
          •   A_Connect
          •   A_DeviceDescriptor_Read
          •   A_DomainAddress_Read
          •   A_DomainAddress_Write
          •   A_IndividualAddress_Write
          •   A_Restart

    Parameters of the Management Procedure
    NM_DomainAndIndividualAddress_Write(/* [in] */ DoA_new, /* [in] */ IA_new)
       DoA_new:     The Domain Address to be assigned to the device.
       IA_new:      The new Individual Address to be assigned to the device.
    Variables
         IA_current:       The current IA of the device in which Programming Mode is active prior to the
                           assignment of IA_new.
         DoA_current:      The current IA of the device that in which Programming Mode is active prior to
                           the assignment of IA_new.
    Sequence
    Management                                                              Network /                   remark
    Client                                                                  Management
                                                                            Server
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
    Exception handling
    to 1.: If an A_Disconnect-PDU is received instead of an A_DeviceDescriptor_Response-PDU, then a
           device with this Individual Address exists but it may either already have another Transport
           Layer connection open and not accept any further Transport Layer connections, or does not
           support connection oriented communication mode.
           ⇒ The Management Client shall continue with the Management Procedure in every case.

    to 2.: The Management Client shall always wait until the time-out has elapsed. It shall collect all
           responses during this time-out.
           This Management Procedure shall wait until Programming Mode is active in only exactly one
           device 3).
            The following cases may occur at this point.
            •    A device with the Individual Address exists, but it is not the one in which Programming
                 Mode is active.
                 ⇒ The Management Client shall not continue with the Management Procedure.
            •    A device with the Individual Address exists, and it is the one in which Programming Mode
                 is active.
                 ⇒ The Management Client shall continue with the Management Procedure.
            •    No device with the Individual Address exists.
                 ⇒ The Management Client shall continue with the Management Procedure.
    to 4.: If no A_DeviceDescriptor_Response-PDU is received, then the programming of the Individual
           Address may have failed or the system (Router) has not been configured correctly.

Inputs (from spec):
    (see body)
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
