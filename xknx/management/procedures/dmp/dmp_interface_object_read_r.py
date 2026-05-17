"""
DMP_InterfaceObjectRead_R — KNX 03.05.02 §3.27.2 (PDF p. 123).

Spec text (verbatim from spec):

    This Management Procedure shall use the connection oriented or connectionless communication
    mode.

    Used Application Layer Services for Management
    - A_PropertyDescription_Read
    - A_PropertyValue_Read

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        opt Property of management control is unknown to the Management Client
            C->>S: A_PropertyDescription_Read-PDU (object_index = OO, PID = PP)
            S->>C: A_PropertyDescription_Response-PDU (object_index = OO, PID = PP, type = .. , ...)
            Note right of S: A_Disconnect.ind ⇒ error, Property does not exist ⇒ error
        end
        loop for each data block, until all data are transmitted
            C->>S: A_PropertyValue_Read-PDU (object_index = OO, PID = PP, start_index = SSSS, element_count = EE)
            S->>C: A_PropertyValue_Response-PDU (object_index = OO, PID = PP, start_index = SSSS, element_count = EE, data = XX, ..)
            Note right of S: A_Disconnect.ind ⇒ error, no data received ⇒ error
        end
    ```

    Exception handling
    The general exception handling shall apply.
    The Management Client shall not interpret the value of the Property Index contained in the
    A_PropertyDescription_Response-PDU at the level of this Management Procedure. Possibly, error
    handling in case an unexpected value of the Property Index can be handled at the level of the
    Configuration Procedure in which this Management Procedure is used.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from xknx.exceptions import ManagementConnectionError
from xknx.telegram import apci

if TYPE_CHECKING:
    from xknx.management.management import P2PConnection

# nr_of_elem field is 4 bits (KNX 03.03.07 v02.01.01 §3.4.4 Figure 46), max value 2^4 - 1
MAX_ELEMENTS_PER_REQUEST = (1 << 4) - 1


async def dmp_interface_object_read_r(
    connection: P2PConnection,
    object_index: int,
    property_id: int,
    count: int = 1,
    start_index: int = 1,
) -> bytes:
    """
    Read property value(s) from an interface object.

    DMP_InterfaceObjectRead_R — KNX 03.05.02 §3.27.2. Requires an established
    connection (DM_Connect must be executed first).

    :param connection: Active P2P connection to the device
    :param object_index: Index of the interface object (0-255)
    :param property_id: Property identifier (1-255)
    :param count: Number of elements to read
    :param start_index: Start element index (1-based, 1-4095)
    :return: The property data read from device
    :raises ManagementConnectionError: If device returns error (nr_of_elem = 0)
    """
    if count <= 0:
        return b""

    data = bytearray()
    remaining = count
    current_index = start_index

    while remaining > 0:
        chunk_count = min(remaining, MAX_ELEMENTS_PER_REQUEST)
        response = await connection.request(
            payload=apci.PropertyValueRead(
                object_index=object_index,
                property_id=property_id,
                count=chunk_count,
                start_index=current_index,
            ),
            expected=apci.PropertyValueResponse,
        )
        # KNX 03.03.07 v02.01.01 §3.4.4.1: "If the remote application process has a problem,
        # e.g., object or Property does not exist or the data does not fit in a PDU
        # or the requester has not the required access rights, then the nr_of_elem
        # of the A_PropertyValue_Response-PDU shall be zero and shall contain no data."
        response_count = response.payload.count
        if response_count == 0:
            raise ManagementConnectionError(
                f"Property read failed: object {object_index} PID {property_id} "
                f"index {current_index} returned nr_of_elem=0"
            )
        if response_count != chunk_count:
            raise ManagementConnectionError(
                f"Property read failed: object {object_index} PID {property_id} "
                f"index {current_index} requested {chunk_count} elements, "
                f"got {response_count}"
            )
        data.extend(response.payload.data)
        current_index += response_count
        remaining -= response_count

    return bytes(data)
