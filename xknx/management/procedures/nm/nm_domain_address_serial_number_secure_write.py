"""
NM_DomainAddressSerialNumber_Secure_Write — KNX 03.05.02 §2.13 (PDF p. 25).

Spec text (verbatim from spec):

    Use
    This Network Management Procedure shall be used to write the Domain Address of one single secure
    device of which the KNX Serial Number is known.
    All timeouts are counted from the time when the sending of the preceding message is confirmed
    locally.
    NOTE 2           This is relevant mainly for the use case where the MaC is connected via satellite to a Tunnelling
    Server in the installation.
    NM_DomainAddressSerialNumber_Secure_Write(/* [in] */ SerNo, /* [in] */ Key, /* [in] */ DoANew)
               SerNo:           The KNX Serial Number of the device.
               Key              The current Tool Key, or the FDSK for ex-factory devices, of the device.
               DoANew:          The Domain Address to be assigned to the device. In case of IP devices this
                                is either a 4 octet DoA consisting of the KNXnet/IP routing multicast
                                address, or a 21 octet DoA consisting of the KNXnet/IP routing multicast
                                address,the routing security version, and the security Backbone Key.
         1. If there is a KNXnet/IP Router between the MaC and the MaS, the MaC shall set the IP System
            Broadcast Routing Mode of the router to “Enable” by sending an
            A_FunctionPropertyCommand(…) or A_FunctionPropertyExtCommand(…).
         2. If the current Data Security sequence number of the device is not known, the MaC executes
            DM_SecureSync_SBC (4.1) firstly.
         3. The MaC sends an A_DomainAddressSerialNumber_Write with SerNo and DoANew, as S-
            A_Data, with the SBC bit in SCF field set to 1, encrypted with the Tool Key.
            If the MaC is on the same IP network, the Frame shall be sent as IP system broadcast;
            otherwise, the Frame will be transformed to an IP system broadcast by the KNXnet/IP Router.
         4. The MaS now shall execute a timer synchronisation procedure using the new routing multicast
            address and Backbone Key. This can in general not be observed by the MaC 4) so the MaC shall
            wait for the maximum time needed for the timer synchronisation.
         5. To verify, the MaC shall wait for another 1 second and then repeatedly send an
            A_IndividualAddressSerialNumber_Read with SerNo on broadcast until the MaS responds
            with A_IndividualAddressSerialNumber_Response or the timeout elapses (see [01]
            clause 4.3.5.3.4 “A_DomainAddressSerialNumber_Write”).
    Error handling
    If no A_IndividualAddressSerialNumber_Response in step 5 is received within the timeout, the MaC
    shall firstly repeat from step 4 after a delay of 1 second.
    If this entire Management Procedure fails, the MaC (ETS) shall not automatically repeat it. This may
    only be repeated after indication or confirmation by the user.

    4)   E.g. if the MaC is on TP1

    2.14 Procedures with A_DomainAddressSelective_Read
    The Management Client (this is the local of Application Layer user) shall apply the A_Domain-
    AddressSelective_Read.req primitive to read the KNX PL110 - or KNX RF DoA of one or more
    devcies without using a specific Domain Address.
    The type of network Resources that shall be read shall be indicated by field Type in the ASDU. The
    following network Resources can be read.
         -    Type 0: The Domain Address of one or more KNX PL110 MaS.
         -    Type 1: The Domain Address of one or more KNX RF MaS.
    This service is particularly used to check the existence of any open media devices with the specified
    Domain Address in possibly neighbouring installations.
    There is no common general behaviour specified for the MaS. The reaction of the MaS has to be
    specified case per case. In case the MaS receives an A_DomainAddressSelective_Read-PDU with a
    value of the field Type that it does not support, or with further service parameters for which no
    reaction is specified, then the MaS shall not react.

    2.14.1.1 Type 00h – single octet DoA
    The ASDU of the A_DomainAddressSelective_Read-PDU shall contain the following fields.
     -    type:                         This shall be the type of call of the A_DomainAddressSelective_Read-
                                        service. This field shall have the value 00h.
     -    start_address:                This shall be the start_address of the range of Individual Addresses to
                                        which the Management Server shall compare its own Individual Address.
     -    range:                        This shall be the range of Individual Addresses, starting from
                                        start_address and ending at start_address + range to which a
                                        Management Server shall compare its own Individual Address.

                            octet 8           octet 9              octet 10           octet 11     octet 12
                                                                start_address      start_address
                           type = 00       domain_addres                                            range
                                                                    (high)              (low)
                      7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0

                      0 0 0 0 0 0 0 0

                    Figure 1 - A_DomainAddressSelective_Read-SDU – Type 00h (example)

    The Management Server shall ignore the A_DomainAddressSelective_Read.ind primitive with Type
    00h , if its Domain Address does not match with the argument domain_address, or its Individual
    Address is lower than the argument start_address or its Individual Address is higher than the
    (start_address + range).
    If Management Server accepts the A_DomainAddressSelective_Read.ind primitive it shall respond to
    the Application Layer with an A_DomainAddress_Read.res primitive after a wait time:
    (individual_address - start_address) x Tmedia 5). If the received argument range is lower than FFh and
    the Management Server receives during the waiting time an A_DomainAddress_Response-PDU then
    it shall terminate the transmission of its own response.
    The A_DomainAddress_Response-PDU shall contain the fields Type and domain_address as show in
    Figure 2.

    5)   Tmedia is specified in [05].

                                         octet 6                 octet 7               octet 8                    octet 9
                                                              APCI                    type = 00h          domain_address
                               7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0
                                                   APCI
                                                   APCI
                                                   APCI
                                                   APCI
                                                   APCI
                                                   APCI
                                                   APCI
                                                   APCI
                                                   APCI
                                                   APCI

                                                   1 1 1 1 1 0 0 0 1 0

              Figure 2 - A_DomainAddress_Response-PDU for a type 0 (1 octet DoA) (example)

    2.14.1.2 Type 01h – six octet DoA

    2.14.1.2.1 General requirements
    The ASDU of the A_DomainAddressSelective_Read-PDU shall contain the following fields.
    -   type:                                This shall be the type of call of the A_DomainAddressSelective_Read-
                                             service. This field shall have the value 01h.
    -   domain_address_start: This shall be the start_address of the range of Domain Addresses to
                              which the Management Server shall compare its own Domain Address.
    -   domain_address_end: This shall be the end_address of the range of Domain Addresses to
                            which the Management Server shall compare its own Domain Address.

          octet 8              octet 9                           octet 14               octet 15                            octet 20          octet 21
         type = 01h                       domain_address_start                                     domain_address_end                         reserved
    7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0                       7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0                          7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0

    0 0 0 0 0 0 0 1                                                                                                                      0 0 0 0 0 0 0 0

                      Figure 3 - A_DomainAddressSelective_Read-SDU – Type 01h (example)

    The Management Server shall only accept the A_DomainAddressSelective_Read.ind primitive with
    Type 01h if its Domain Address is within the range domain_address_start to domain_address_end;
    else, it shall ignore the service.
    If Management Server accepts the A_DomainAddressSelective_Read.ind primitive it shall respond to
    the Application Layer with an A_DomainAddress_Read.res primitive after a random wait time from
    0 s to 2 s.
    EXAMPLE 1              To have an equal spreading of the responses, this random wait time may for instance be based on the least
    significant octet to the KNX Serial Number of the Management Server device.

    The A_DomainAddress_Response-PDU shall contain the fields Type and domain_address as show in
    Figure 4.
                           octet 6                  octet 7                 octet 8                                           octet 13
                                                   APCI                                          domain_address
                      7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0                                  …              7 6 5 4 3 2 1 0
                                     APCI
                                     APCI
                                     APCI
                                     APCI
                                     APCI
                                     APCI
                                     APCI
                                     APCI
                                     APCI
                                     APCI

                                     1 1 1 1 1 0 0 0 1 0

              Figure 4 - A_DomainAddress_Response-PDU for a type 1 (6 octet DoA) (example)

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def nm_domain_address_serial_number_secure_write(xknx: XKNX) -> None:
    """NM_DomainAddressSerialNumber_Secure_Write — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "NM_DomainAddressSerialNumber_Secure_Write (KNX 03.05.02 §2.13) — implementation pending"
    )
