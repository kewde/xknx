"""
Generic Interface Object management primitives — KNX 03.05.02.

This module hosts the management procedures that operate on Interface
Objects in a generic, spec-section-agnostic way. Higher-level procedures
(§2.6 max-APDU discovery, future §3.5 downloads, etc.) consume these
primitives instead of re-implementing the scan/read loops themselves.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from xknx.profile.const import ResourceGenericPropertyId
from xknx.telegram import apci

if TYPE_CHECKING:
    from xknx.management.management import P2PConnection

# Logger name preserved from the pre-split location so log output is
# bit-identical to the unrefactored module.
logger = logging.getLogger("xknx.management.procedures")

INTERFACE_OBJECT_SCAN_LIMIT = 256
"""Safety cap on object_index iteration in :func:`nm_interface_object_scan`.

KNX 03.05.02 §3.28.2 does not impose a hard bound; the loop is
expected to terminate when ``A_PropertyDescription_Response`` reports
``PID = 0``. This cap guards against misbehaving devices that always echo a
non-zero PID.
"""


async def nm_interface_object_scan(
    connection: P2PConnection, object_type: int
) -> int | None:
    """
    Find the first Interface Object of ``object_type`` on the connected peer.

    Implements ``DMP_InterfaceObjectScan_R`` from KNX 03.05.02 §3.28.2
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
    KNX 03.05.01 §4.2.1. The Device Object always carries object_type
    ``0x0000``; the Router Object ``0x0006``.

    Termination conditions:
        - First match found → return that ``object_index``.
        - ``A_PropertyDescription_Response`` carries ``PID = 0`` → no more
          Interface Objects on the peer → return ``None``.
        - Safety cap :data:`INTERFACE_OBJECT_SCAN_LIMIT` reached → return
          ``None``.

    Note: a coupler with multiple Router Object instances (multi-line
    coupler, per KNX 03.05.01 §4.5.9.1) exposes one instance per outgoing
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
