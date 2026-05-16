"""
NM_IndividualAddress_Write — KNX 03.05.02 §2.3 (PDF p. 12).

Spec text (verbatim from spec):

    Use
    This Network Management Procedure shall be used to write the Individual Address of one single
    device that is in Programming Mode.
    The procedure shall wait until exactly one device is in Programming Mode. It shall check that no other
    device has the same Individual Address. The procedure shall check if the programming is successful
    and shall deactivate the Programming Mode by executing a restart of the device.
    When applicable this procedure shall be preceded by the configuration of the Individual Addresses of
    the installed Routers and the Domain Addresses.
    Used Application Layer Services for Management
       • A_IndividualAddress_Read
       • A_IndividualAddress_Write
       • A_DeviceDescriptor_Read
       • A_Restart
       • A_Connect
    Parameters of the Management Procedure
    NM_IndividualAddress_Write(/* [in] */ IA_new)
        IA_new: The new IA that shall be assigned to the device in Programming Mode.
    Service parameters
       None.
    Variables
          IA_current: The current IA of the device that is in Programming Mode prior to the assignment
                      of IA_new.

    Sequence
    Management                                                               Network /                  remark
    Client                                                                   Management
                                                                             Server
    1. Verify whether the Individual Address IA_new is already occupied
       on the network.
                                    A_Connect-PDU
                            (destination_address = IA_new)

    if negative A_Connect.Lcon ⇒ IA_new is not occupied; end procedure.
    else (this is, a positive A_Connect.Lcon is received)
                                                                                  If the device that occupies the IA IA_new
                                                                              does not support Transport Layer connections,
                                                                                          it shall send a T_Disconnect-PDU.
                                   A_Disconnect-PDU
                                          ()

    if A_Disconnect-PDU is received then IA_new shall be regarded as occupied; end procedure.
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
    a)
    If the Management Client receives an A_DeviceDescriptor_Response-PDU it shall
    conclude that the Individual Address IA_new is occupied.
    If no A_DeviceDescriptor_Response-PDU is received after time-out ⇒ IA_new is not
    occupied
    endif
                                  A_Disconnect-PDU
                            (destination_address = IA_new)

    2. wait until device is in Programming Mode:
    repeat until one A_IndividualAddress_Response-PDU is received
                           A_IndividualAddress_Read-PDU
                                         ()

                         A_IndividualAddress_Response-PDU                                 one or more responses may be
                            (source_address = IA_current)                                 received from different devices
                                                                                          time-out: 1 s
                                               ...

    if more than one response is received ⇒ more than one device in Programming Mode
    end repeat

    3.set Individual Address
    if IA_new!= IA_current
                           A_IndividualAddress_Write-PDU
                              (new_address = IA_new)

    endif
    4. verify and deactivate programming mode:
                                       A_Connect-PDU
                               (destination_address = IA_new)

                            A_DeviceDescriptor_Read-PDU
                               (descriptor_type = 00h)

                          A_DeviceDescriptor_Response-PDU
                          (descriptor_type, device_descriptor)
    b)
                                      A_Restart-PDU
                                            ()

    Abort the connection of the client side Transport Layer.

    Exception handling
    to 1.: If an A_Disconnect-PDU is received instead of an A_DeviceDescriptor_Response-PDU, than a
           device with this Individual Address exists but it may either already have another Transport
           Layer connection open and not accept any further Transport Layer connections, or does not
           support connection oriented communication mode.
           The Management Client shall continue with the Management Procedure in every case.
    a)    The Management Client shall accept any value of descriptor_type, also values ≠ 0, and any value
          of device_descriptor.
    to 2.: The Management Client shall always wait until the time-out has elapsed. It shall collect all the
           responses during this time-out.
           This procedure shall wait until exactly one device is in Programming Mode 2).
            Following case may occur at this point:
            •    A device with the Individual Address IA_new to be assigned exists, but it is not the one
                 that is in Programming Mode.
                 ⇒ The Management Client shall not continue with the Management Procedure.
            •    A device with the Individual Address IA_new to be assigned exists, and it is the one that is
                 in Programming Mode.
                 ⇒ The Management Client shall continue with the Management Procedure.
            •    No device with the Individual Address IA_new to be assigned exists.
                 ⇒ The Management Client shall continue with the Management Procedure.
    to 4.: If no A_DeviceDescriptor_Response-PDU is received, than the programming of the Individual
           Address may have failed, or the system (Router) is not configured correctly.

    2)   The user of the Management Client should get an information in how many devices are Programming Mode
         is active (none or more than one).

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from xknx.exceptions import ManagementConnectionError, ManagementConnectionTimeout
from xknx.management.procedures.nm.nm_individual_address_check import (
    nm_individual_address_check,
)
from xknx.management.procedures.nm.nm_individual_address_read import (
    nm_individual_address_read,
)
from xknx.telegram import Telegram, apci, tpci
from xknx.telegram.address import IndividualAddress, IndividualAddressableType

if TYPE_CHECKING:
    from xknx import XKNX

logger = logging.getLogger("xknx.management.procedures")


async def nm_individual_address_write(
    xknx: XKNX, individual_address: IndividualAddressableType
) -> None:
    """
    Write the individual address of a single device in programming mode.

    :param xknx: XKNX object
    :param individual_address: address to be written to KNX device
    """
    logger.debug("Writing individual address %s to device.", individual_address)

    # check if the address is already occupied on the network
    individual_address = IndividualAddress(individual_address)
    address_found = await nm_individual_address_check(xknx, individual_address)

    if address_found:
        logger.debug(
            "Individual address %s already present on the bus", individual_address
        )

    # check which devices are in programming mode
    dev_pgm_mode = await nm_individual_address_read(
        xknx, raise_if_multiple=True
    )  # raises exception if more than one device in programming mode
    if not dev_pgm_mode:
        logger.debug("No device in programming mode detected.")
        raise ManagementConnectionError("No device in programming mode detected.")

    # check if new and received addresses match
    if address_found:
        if individual_address != dev_pgm_mode[0]:
            logger.debug(
                "Device with address %s found and it is not in programming mode. Exiting to prevent address conflict.",
                individual_address,
            )
            raise ManagementConnectionError(
                f"A device was found with {individual_address}, cannot continue with programming."
            )
        # device in programming mode's address matches address that we want to write, so we can abort the operation safely
        logger.debug("Device already has requested address, no write operation needed.")
    else:
        await xknx.management.send_broadcast(
            payload=apci.IndividualAddressWrite(address=individual_address),
        )
        logger.debug("Wrote new address %s to device.", individual_address)

    async with xknx.management.connection(
        address=IndividualAddress(individual_address)
    ) as connection:
        logger.debug(
            "Checking if device exists at %s and restarting it.", individual_address
        )

        try:
            await connection.request(
                payload=apci.DeviceDescriptorRead(descriptor=0),
                expected=apci.DeviceDescriptorResponse,
            )
        except ManagementConnectionTimeout as ex:
            # if nothing is received (-> timeout) IA is free
            raise ManagementConnectionError(
                f"No device answered to connection attempt after write address operation. {ex}"
            ) from None

        logger.debug("Restating device, exiting programming mode.")
        # A_Restart will not be ACKed by the device, so it is manually sent to avoid timeout and retry
        seq_num = next(connection.sequence_number)
        telegram = Telegram(
            destination_address=connection.address,
            source_address=xknx.current_address,
            payload=apci.Restart(),
            tpci=tpci.TDataConnected(sequence_number=seq_num),
        )
        await xknx.cemi_handler.send_telegram(telegram)
