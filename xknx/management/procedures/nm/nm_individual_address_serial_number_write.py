"""
NM_IndividualAddress_SerialNumber_Write — KNX 03.05.02 §2.5 (PDF p. 15).

Spec text (verbatim from spec):

    Use
    This Network Management Procedure shall be used to write the Individual Address of one single
    device of which the KNX Serial Number is known.
    The procedure shall ensure that the assigned Individual Address is unique. The procedure shall check
    if the programming has been successful.
    If applicable this procedure shall be preceded by the configuration of the Individual Addresses of the
    installed Routers and the Domain Addresses.
    The KNX Serial Number of the device to be programmed must be known in advance. Either by the
    mechanism NM_SerialNumberDefaultIA_Scan or by any other means.

    If the Individual Address of more than one device has to be programmed, this Network Management
    Procedure NM_IndividualAddress_SerialNumber_Write has to be repeated for each device, using that
    device’s KNX Serial Number.

    Used Application Layer Services for Management
    - A_IndividualAddressSerialNumber_Write
    - A_IndividualAddressSerialNumber_Read

    Parameters of the Management Procedure
    NM_IndividualAddress_SerialNumber_Write(/* [in] */ SN_device, /* [in] */ IA_new,
        /* [out] */ DoA_Device)
        SN_Device:  KNX Serial Number of device to which the Individual Address will be
                    assigned.
        IA_new:     Individual Address to be programmed.
        DoA_Device: The Domain Address of the device if the device is on an open medium
                    supporting a Domain Address.

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        Note over C,S: 1.Set Individual Address of Server
        C->>S: A_IndividualAddressSerialNumber_Write-PDU (serial_number = SN_Device, new_address = IA_new)
        Note right of S: The server shall set its Individual Address according to the received value
        Note over C,S: 2. Verify
        C->>S: A_IndividualAddressSerialNumber_Read-PDU (serial_number = SN_Device)
        S->>C: A_IndividualAddressSerialNumber_Response-PDU (source_address = IA_new, serial number = SN_Device, domain_address = DoA_Device)
        Note right of S: Different or no answer received ⇒ Error
    ```

    NOTE - Opposite to the procedures NM_IndividualAddress_Write and
    NM_DomainAndIndividualAddress_Write, both requiring that the Programming Mode be active in the device and using the
    service A_IndividualAddress_Write, this procedure does not reset the device after assigning the Individual Address.

    Exception handling
    The default exception handling shall apply.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from xknx.exceptions import ManagementConnectionError
from xknx.management.procedures.nm.nm_individual_address_serial_number_read import (
    nm_individual_address_serial_number_read,
)
from xknx.telegram import apci
from xknx.telegram.address import IndividualAddress, IndividualAddressableType

if TYPE_CHECKING:
    from xknx import XKNX

logger = logging.getLogger("xknx.management.procedures")


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
