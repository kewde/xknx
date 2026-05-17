"""
DMP_Authorize_RCo — KNX 03.05.02 §3.5.1 (PDF p. 74).

Spec text (verbatim from spec):

    This Management Procedure shall use the connection oriented communication mode.

    Used Application Layer Services for Management
    - A Authorize

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        opt authorization is required (key != FFFF FFFFH)
            C->>S: A_Authorize_Request-PDU (key)
            S->>C: A_Authorize_Response-PDU (key, level)
            Note right of S: A_Disconnect.ind ⇒ error: connection was broken down
        end
    ```

    Exception handling
    The general exception handling shall apply.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from xknx.telegram import apci

if TYPE_CHECKING:
    from xknx.management.management import P2PConnection

FREE_ACCESS_KEY = 0xFFFFFFFF


async def dmp_authorize_r_co(connection: P2PConnection, key: int) -> int:
    """
    Authorize with a KNX device to obtain access rights.

    DMP_Authorize_RCo — KNX 03.05.02 §3.5.1. Requires an established
    connection (DM_Connect must be executed first).

    :param connection: Active P2P connection to the device
    :param key: 4-byte authorization key (0xFFFFFFFF for free access)
    :return: Access level granted by the device (0 = highest, 15 = lowest)
    """
    response = await connection.request(
        payload=apci.AuthorizeRequest(key=key),
        expected=apci.AuthorizeResponse,
    )
    return response.payload.level
