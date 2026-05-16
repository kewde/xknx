"""
NM_DomainAddressSerialNumber_Secure_Write — KNX 03.05.02 §2.13 (PDF p. 26).

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

    Procedure:
         1. If there is a KNXnet/IP Router between the MaC and the MaS, the MaC shall set the IP System
            Broadcast Routing Mode of the router to "Enable" by sending an
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
            clause 4.3.5.3.4 "A_DomainAddressSerialNumber_Write").

    Error handling
    If no A_IndividualAddressSerialNumber_Response in step 5 is received within the timeout, the MaC
    shall firstly repeat from step 4 after a delay of 1 second.
    If this entire Management Procedure fails, the MaC (ETS) shall not automatically repeat it. This may
    only be repeated after indication or confirmation by the user.

Inputs (from spec):
    [in] SerNo, [in] Key, [in] DoANew
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
