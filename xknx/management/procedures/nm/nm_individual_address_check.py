"""
NM_IndividualAddress_Check — KNX 03.05.02 §2.19 (PDF p. 33).

Spec text (verbatim from spec):

    NOTE         This procedure has also been named NM_IndividualAddress_Scan.

    Use
    This Network Management Procedure shall be used by a network Management Client to check
    whether a given Individual Address is occupied on the network or not.
    Used Application Layer Services for Management
          • A_Connect
          • A_DeviceDescriptor_Read
          • A_Disconnect

    Parameters of the Management Procedure
    NM_IndividualAddress_Check(/* [in] */ IA_test, /* [out] */ result, /* [out] */ DDType,
    /* [out] */ DDx)
         IA_test:      Individual Address of which the occupation on the network has to be tested.
         result:       Result back to the user of the Management Procedure to indicate whether the IA_test is
                       occupied on the network or not.
         DDType: The Device Descriptor Type as reported by the device
         DDx:          The Device Descriptor value according the format DDType as reported by the device.

    Sequence
    Management                                                                     Network /                   remark
    Client                                                                         Management
                                                                                   Server
                                      A_Connect-PDU
                               (destination_address = IA_test)

    if negative A_Connect.Lcon ⇒ IA_test occupied; end procedure.
    else (this is, a positive A_Connect.Lcon is received)
                                                                                          If the device that occupies the IA_test
                                                                                  does not support Transport Layer connections,
                                                                                              it shall send a T_Disconnect-PDU.
                                      A_Disconnect-PDU
                                             ()

    if A_Disconnect-PDU is received then IA_test shall be regarded as occupied; end procedure.
    else (no A_Disconnect-PDU is received)
                                                                If a device that occupies IA_test is present on the network,
                                                                             and does support Transport Layer connections,
                                                                                   it shall have no other reaction on the bus
                                                   than the Layer-2 acknowledge that initiates the above A_Connect.Lcon
        The A_DeviceDescriptor_Read-PDU shall use DD0.
                              A_DeviceDescriptor_Read-PDU
                              (destination_address = IA_test,
                                 descriptor_type = 0000h)

                            A_DeviceDescriptor_Response-PDU
                            (descriptor_type, device_descriptor)
    1), 2)
    If the Management Client receives an A_DeviceDescriptor_Response-PDU it shall conclude that the Individual Address IA_test is
    occupied.
    if no A_DeviceDescriptor_Response-PDU is received after time-out ⇒ IA_test is not occupied
    endif
    3)                          A_Disconnect-PDU
                          (destination_address = IA_test)

    Possible reactions
    1)   If the Network Management Server reacts on the connection oriented
         A_DeviceDescriptor_Read-PDU then the Management Client shall assume that the IA IA_test is
         occupied on the network and that the device that occupies this IA_test supports the
         connection-oriented Transport Layer.

    2)     The descriptor_type and the device_descriptor in the response by the device shall be reported
           back via DDType respectively DDx. The Device Descriptor Type may differ from 0 and the
           format of the Device Descriptor may be encoded accordingly as well.
    3)     If the Network Management Client receives an A_Disconnect-PDU and no A_Device-
           Descriptor_Response-PDU, then the Management Client shall assume that the IA_test is occupied
           on the network and that the device that occupies this IA_test does not support the
           connection-oriented Transport Layer.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from xknx.exceptions import ManagementConnectionRefused, ManagementConnectionTimeout
from xknx.telegram import apci
from xknx.telegram.address import IndividualAddress, IndividualAddressableType

if TYPE_CHECKING:
    from xknx import XKNX

logger = logging.getLogger("xknx.management.procedures")


async def nm_individual_address_check(
    xknx: XKNX, individual_address: IndividualAddressableType
) -> bool:
    """
    Check if the individual address is occupied on the network.

    :param xknx: XKNX object
    :param individual_address: address to check
    """
    try:
        async with xknx.management.connection(
            address=IndividualAddress(individual_address)
        ) as connection:
            try:
                response = await connection.request(
                    payload=apci.DeviceDescriptorRead(descriptor=0),
                    expected=apci.DeviceDescriptorResponse,
                )

            except ManagementConnectionTimeout as ex:
                # if nothing is received (-> timeout) IA is free
                logger.debug("No device answered to connection attempt. %s", ex)
                return False
            if isinstance(response.payload, apci.DeviceDescriptorResponse):
                # if response is received IA is occupied
                logger.debug("Device found at %s", individual_address)
                return True
            return False
    except ManagementConnectionRefused as ex:
        # if Disconnect is received immediately, IA is occupied
        logger.debug("Device does not support transport layer connections. %s", ex)
        return True
