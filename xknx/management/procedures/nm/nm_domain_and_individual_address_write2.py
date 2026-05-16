"""
NM_DomainAndIndividualAddress_Write2 — KNX 03.05.02 §2.10 (PDF p. 22).

Spec text (verbatim from spec):

    Use
    This procedure NM_DomainAndIndividualAddress_Write2 differs from the above procedure
    NM_DomainAndIndividualAddress_Write in the following.
         -   It shall not check whether the Individual Address that shall be assigned is already present in
             the network. As a result, it does not need the service A_Connect.
         -   After assignment of the Individual Address it reads out the Device Descriptor
             connectionless.
         -   The Management Server is not restarted at the end of the procedure. As a result, it does not
             need the service A_Restart.
    Used Application Layer Services for Management
       • A_IndividualAddress_Read
       • A_DomainAddress_Write
       • A_IndividualAddress_Write
       • A_DeviceDescriptor_Read
    Parameters of the Management Procedure
    NM_DomainAndIndividualAddress_Write2(/* [in] */ NmpDoANew, /* [in] */ NmpIANew,
          /* [out] */ NmpIACurrent)
      NmpDoANew:          The Domain Address to be assigned to the device
      NmpIANew:           The new Individual Address to be assigned to the device.
      NmpIACurrent:       Individual Address used by the device before the start of the Management
                          Procedure.

    3)   The user of the Management Client should get an information, how many devices are in Programming Mode
         (none or more than one)

    Sequence
    Management                                                              Management                remark
    Client                                                                  Server
                                                                            (Device)
                                                                                            Enter Programming Mode
                                                                                              (Manufacturer specific)
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

    Notes
    a)    In the context of this Management Procedure NM_DomainAndIndividualAddress_Write2, the
          A_DeviceDescriptor_Read-service is only applied to check whether the Management Server
          (device) can be addressed using its new Individual Address. The Management Client is only
          interested in whether it receives a response or not; the contents, this is, the value of
          descriptor_type and device_descriptor should not be evaluated at this point.

Inputs (from spec):
    (see body)
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
