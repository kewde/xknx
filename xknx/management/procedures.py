"""Package for management procedures as described in KNX-Standard 3.5.2."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from xknx.exceptions import (
    ManagementConnectionError,
    ManagementConnectionRefused,
    ManagementConnectionTimeout,
)
from xknx.profile.const import ResourceDevicePropertyId, ResourceGenericPropertyId
from xknx.telegram import Telegram, apci, tpci
from xknx.telegram.address import (
    IndividualAddress,
    IndividualAddressableType,
)

if TYPE_CHECKING:
    from xknx import XKNX
    from xknx.management.management import P2PConnection

logger = logging.getLogger("xknx.management.procedures")

INTERFACE_OBJECT_SCAN_LIMIT = 256
"""Safety cap on object_index iteration in :func:`nm_interface_object_scan`.

The KNX spec (03_05_02 §3.28.2) does not impose a hard bound; the loop is
expected to terminate when ``A_PropertyDescription_Response`` reports
``PID = 0``. This cap guards against misbehaving devices that always echo a
non-zero PID.
"""


async def nm_interface_object_scan(
    connection: P2PConnection, object_type: int
) -> int | None:
    """
    Find the first Interface Object of ``object_type`` on the connected peer.

    Implements ``DMP_InterfaceObjectScan_R`` from KNX 03_05_02 §3.28.2
    (PDF p. 127). Verbatim spec pseudocode:

        object_index = 0;
        repeat if Interface Object scan is enabled
            A_PropertyDescription_Read-PDU
                (object_index, PID = 0, Property_index = 0)
            A_PropertyDescription_Response-PDU
                (object_index, Property_index = 0, PID)
            if Interface Object exists (Property ID <> 0)
                A_PropertyValue_Read-PDU
                    (object_index, PID = 01h, start_index = 01h,
                     element_count = 01h)
                A_PropertyValue_Response-PDU
                    (object_index, PID = 01h, start_index = 01h,
                     element_count = 01h, data = object_type)
            endif
            ...
            object_index ++
        until PID = 0

    ``PID_OBJECT_TYPE`` (PID 1) is mandatory on every Interface Object per
    KNX 03_05_01 §4.2.1. The Device Object always carries object_type
    ``0x0000``; the Router Object ``0x0006``.

    Termination conditions:
        - First match found → return that ``object_index``.
        - ``A_PropertyDescription_Response`` carries ``PID = 0`` → no more
          Interface Objects on the peer → return ``None``.
        - Safety cap :data:`INTERFACE_OBJECT_SCAN_LIMIT` reached → return
          ``None``.

    Note: a coupler with multiple Router Object instances (multi-line
    coupler, per KNX 03_05_01 §4.5.9.1) exposes one instance per outgoing
    line. This helper returns the first instance found by ascending
    ``object_index``; callers that need a specific routing direction must
    select the instance themselves.
    """
    for object_index in range(INTERFACE_OBJECT_SCAN_LIMIT):
        description = await connection.request(
            payload=apci.PropertyDescriptionRead(
                object_index=object_index, property_id=0, property_index=0
            ),
            expected=apci.PropertyDescriptionResponse,
        )
        description_payload = description.payload
        assert isinstance(description_payload, apci.PropertyDescriptionResponse)
        if description_payload.property_id == 0:
            return None
        value = await connection.request(
            payload=apci.PropertyValueRead(
                object_index=object_index,
                property_id=ResourceGenericPropertyId.PID_OBJECT_TYPE,
                count=1,
                start_index=1,
            ),
            expected=apci.PropertyValueResponse,
        )
        value_payload = value.payload
        assert isinstance(value_payload, apci.PropertyValueResponse)
        if value_payload.count == 0 or not value_payload.data:
            continue
        if int.from_bytes(value_payload.data, byteorder="big") == object_type:
            return object_index
    return None


async def nm_read_max_apdu_length(connection: P2PConnection) -> int | None:
    """
    Read ``PID_MAX_APDU_LENGTH`` from the Device Object of the connected peer.

    Implements the §2.6.2.2 atom of KNX 03_05_03 (Configuration Procedures,
    PDF p. 32) using the ``DMP_InterfaceObjectRead_R`` procedure
    (KNX 03_05_02 §3.27.2, PDF p. 124):

        if Property of management control is unknown to the Management Client
            A_PropertyDescription_Read-PDU (object_index, PID)
            A_PropertyDescription_Response-PDU (object_index, PID, type, ...)
        endif
        for each data block, until all data are transmitted
            A_PropertyValue_Read-PDU
                (object_index, PID, start_index, element_count)
            A_PropertyValue_Response-PDU
                (object_index, PID, start_index, element_count, data)
        endfor

    The data type of ``PID_MAX_APDU_LENGTH`` is known a priori
    (PDT_UNSIGNED_INT, KNX 03_05_01 §4.3.7, PDF p. 46-47) so the optional
    A_PropertyDescription_Read step is skipped.

    Returns the value in octets, or ``None`` when the property is absent on
    the device (peer responds with ``count = 0``). Per §4.3.7.1 valid
    values are in the range 15..254; this helper does not enforce that
    range — callers interpret values per §2.6 semantics.
    """
    response = await connection.request(
        payload=apci.PropertyValueRead(
            object_index=0,
            property_id=ResourceDevicePropertyId.PID_MAX_APDU_LENGTH,
            count=1,
            start_index=1,
        ),
        expected=apci.PropertyValueResponse,
    )
    payload = response.payload
    assert isinstance(payload, apci.PropertyValueResponse)
    if payload.count == 0 or not payload.data:
        return None
    return int.from_bytes(payload.data, byteorder="big")


async def dm_restart(xknx: XKNX, individual_address: IndividualAddressableType) -> None:
    """
    Restart the device.

    :param xknx: XKNX object
    :param individual_address: address of device to reset
    """
    async with xknx.management.connection(
        address=IndividualAddress(individual_address)
    ) as connection:
        logger.debug("Requesting a Basic Restart of %s.", individual_address)
        # A_Restart will not be ACKed by the device, so it is manually sent to avoid timeout and retry
        seq_num = next(connection.sequence_number)
        telegram = Telegram(
            destination_address=connection.address,
            source_address=xknx.current_address,
            payload=apci.Restart(),
            tpci=tpci.TDataConnected(sequence_number=seq_num),
        )
        await xknx.cemi_handler.send_telegram(telegram)


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


async def nm_individual_address_read(
    xknx: XKNX,
    timeout: float | None = 3,
    raise_if_multiple: bool = False,
) -> list[IndividualAddress]:
    """
    Request individual addresses of all devices that are in programming mode.

    :param xknx: XKNX object
    :param timeout: specifies the timeout in seconds, the KNX specification requires a timeout of 3s
    :param raise_if_multiple: if true, ManagementConnectionError is raised when multiple devices are in programming mode
    :returns: list of individual address of devices in programming mode
    """

    addresses = []
    # initialize queue or event handler gathering broadcasts
    async with xknx.management.broadcast() as bc_context:
        await xknx.management.send_broadcast(apci.IndividualAddressRead())
        async for result in bc_context.receive(timeout=timeout):
            if isinstance(result.payload, apci.IndividualAddressResponse):
                addresses.append(result.source_address)
                if raise_if_multiple and (len(addresses) > 1):
                    raise ManagementConnectionError(
                        "More than one KNX device is in programming mode."
                    )
    return addresses


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


# for backwards compatibility
nm_invididual_address_write = nm_individual_address_write


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


async def nm_individual_address_serial_number_write(
    xknx: XKNX, serial: bytes, individual_address: IndividualAddressableType
) -> None:
    """Write individual address to device with specified serial number."""
    individual_address = IndividualAddress(individual_address)
    await xknx.management.send_broadcast(
        payload=apci.IndividualAddressSerialWrite(
            address=individual_address,
            serial=serial,
        )
    )
    logger.debug(
        "Wrote new address %s to device with serial number %s.",
        individual_address,
        serial,
    )

    address = await nm_individual_address_serial_number_read(xknx=xknx, serial=serial)

    if address is None:
        raise ManagementConnectionError(f"No reply received from {serial!r}.")

    if address != individual_address:
        raise ManagementConnectionError(
            f"Failed to write serial address {individual_address} to device with serial {serial!r}. Detected {address}"
        )

    logger.debug(
        "New address %s validated on device with serial number %s.",
        individual_address,
        serial,
    )
