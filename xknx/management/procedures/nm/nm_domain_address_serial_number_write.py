"""
NM_DomainAddressSerialNumber_Write — KNX 03.05.02 §2.12 (PDF p. 25).

Spec text (verbatim from spec):

    Use
    This Network Management Procedure shall be used to write the Domain Address of one single device
    of which the KNX Serial Number is known.
    All timeouts are counted from the time when the sending of the preceding message is confirmed
    locally.
    NOTE 1           This is relevant mainly for the use case where the MaC is connected via satellite to a Tunnelling
    Server in the installation.

    NM_DomainAddressSerialNumber_Write(/* [in] */ SerNo, /* [in] */ DoANew)
               SerNo:      The KNX Serial Number of the device.
               DoANew: The Domain Address to be assigned to the device. In case of IP devices this is a
                       4 octet DoA consisting of the KNXnet/IP routing multicast address (21 octet
                       DoA can be loaded only with the secure procedure in 2.13).

    Procedure:
          1.    If there is a KNXnet/IP Router between the MaC and the MaS, the MaC sets the IP System
                Broadcast Routing Mode of the router to "Enable" by sending an
                A_FunctionPropertyCommand(…) or A_FunctionPropertyExtCommand(…).
          2.    The MaC sends an A_DomainAddressSerialNumber_Write with SerNo and DoANew. If the
                MaC is on the same IP network, the Frame shall be sent as IP system broadcast; otherwise
                the Frame will be transformed to an IP system broadcast by the KNXnet/IP Router.
          3.    To verify, the MaC waits 1 second and then sends repeatedly an
                A_IndividualAddressSerialNumber_Read with SerNo on broadcast until the MaS responds
                with A_IndividualAddressSerialNumber_Response-PDU or the timeout elapses (see [01]
                clause 4.3.5.3.4 "A_DomainAddressSerialNumber_Write").
          4.    If the IP System Broadcast Routing Mode of a router has been set to "Enable" in step 1, set it
                back to "Disable" by sending an A_FunctionPropertyCommand(…) or
                A_FunctionPropertyExtCommand(…).

    Error handling
    If no A_IndividualAddressSerialNumber_Response-PDU in 3 is received within the timeout (see [01]
    clause 4.3.5.3.4 "A_DomainAddressSerialNumber_Write"), the MaC first repeats from 2 after a delay
    of 1 second.
    If this entire Management Procedure fails, the MaC (ETS) shall not automatically repeat it. This may
    only be repeated after indication or confirmation by the user.

Inputs (from spec):
    [in] SerNo, [in] DoANew
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def nm_domain_address_serial_number_write(xknx: XKNX) -> None:
    """NM_DomainAddressSerialNumber_Write — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "NM_DomainAddressSerialNumber_Write (KNX 03.05.02 §2.12) — implementation pending"
    )
