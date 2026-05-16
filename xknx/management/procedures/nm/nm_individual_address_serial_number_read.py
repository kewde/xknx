"""
NM_IndividualAddress_SerialNumber_Read — KNX 03.05.02 §2.4 (PDF p. 15).

Spec text (verbatim from spec):

    Use
    This Network Management Procedure shall be used to read the Individual Address of one single
    device of which the KNX Serial Number is known.
    The KNX Serial Number of the device (SN_Device) must be known in advance.
    If the Individual Address of more than one device has to be read, this Network Management Procedure
    “NM_IndividualAddress_SerialNumber_Read” has to be repeated for each device, using each device’s
    KNX Serial Number.
    Used Application Layer Services for Management
       • A_IndividualAddressSerialNumber_Read
    Parameters of the Management Procedure
    NM_IndividualAddress_SerialNumber_Read(/* [in] */ SN_Device, /* [out] */ DoA_current,
        /* [out] */ IA_current)
       SN_Device:        KNX Serial Number of the device of which the Individual Address is to be read.
       DoA_Device: The Domain Address of the device of which the Individual Address is read;
                         it is contained in the response if the device is on Powerline.
       IA_Device:        The Individual Address of the device, in the response.
    Sequence
    Management                                                            Management                remark
    Client                                                                Server
    1.Get the Individual Address of the Management Server.
                   A_IndividualAddressSerialNumber_Read-PDU
                           (serial_number = SN_Device)

                 A_IndividualAddressSerialNumber_Response-PDU
                           (source_address = IA_current,
                            serial_number = SN_Device,
                         domain_address = DoA_Device)
                                                                                       No answer received ⇒ Error

    The Individual Address is contained as the Source Address of the
    A_IndividualAddressSerialNumber_Response-PDU.
    Exception handling
    If no answer is received, there is no device present in the network with the given KNX Serial Number.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from xknx.telegram import apci
from xknx.telegram.address import IndividualAddress

if TYPE_CHECKING:
    from xknx import XKNX

logger = logging.getLogger("xknx.management.procedures")


async def nm_individual_address_serial_number_read(
    xknx: XKNX,
    serial: bytes,
    timeout: float = 3,
) -> IndividualAddress | None:
    """Read individual address from device with specified serial number."""
    # initialize queue or event handler gathering broadcasts
    async with xknx.management.broadcast() as bc_context:
        await xknx.management.send_broadcast(
            payload=apci.IndividualAddressSerialRead(serial=serial)
        )
        async for result in bc_context.receive(timeout=timeout):
            if (
                isinstance(result.payload, apci.IndividualAddressSerialResponse)
                and result.payload.serial == serial
            ):
                return result.source_address

    return None
