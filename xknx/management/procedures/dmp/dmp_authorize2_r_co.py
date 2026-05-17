"""
DMP_Authorize2_RCo — KNX 03.05.02 §3.5.2 (PDF p. 74).

NOTE: The spec names this "DM_Authorize2_RCo" but it follows the DMP pattern
(connection-oriented procedure implementation), so we treat it as DMP here.

Spec text (verbatim from spec):

    Use
    This device Management Procedure DM_Authorize2_RCo shall be used to obtain access
    authorization. It shall assume that the Management Client has an access key provided by its user. If the
    Management Client does not have an access key, it shall not be executed.
    Opposite to the Management Procedure DM_Authorize_RCo, this Management Procedure
    DM_Authorize2_RCo does not presume that the device has been locked with the key that is provided
    to the procedure. Therefore, it authorizes subsequently with the key FFFFFFFFh and with the key
    client_key and continues with the key that gives the maximal access rights.
    NOTE  This is the case when the ETS User enters a key to be used to lock the devices and uninitialised
    devices fresh from the factory are used.

    DM_Connect shall be executed before executing this Management Procedure.

    Use
    - Profiles: System 2, BIM M112
    - Conditions: Write access, i.e. modifying memory- or Property contents
    - A key must be available

    Used Application Layer Services for Management
    - A_Authorize_Request

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        Note over C,S: The Management Server (device) shall according the specification of A_Authorize in [03] have granted the access rights associated to the key FFFFFFFFh. This level is however unknown to the Management Client. Therefore, the client re-authorizes explicitly with key FFFFFFFFh to obtain the free access level.
        C->>S: A_Authorize_Request-PDU (key = FFFFFFFFh)
        S->>C: A_Authorize_Response-PDU (level = free_level)
        opt free access level is not the highest level (lowest numerical value, maximum access rights)
            C->>S: A_Authorize_Request-PDU (key = client_key)
            S->>C: A_Authorize_Response-PDU (level = client_level)
            Note over C,S: The level obtained now with access_key is compared to the one obtained for free access. If free access gave higher access level (lower numerical value), a new authorisation with free access level is done.
            opt client_level > free_level
                C->>S: A_Authorize_Request-PDU (key = FFFFFFFFh)
                S->>C: A_Authorize_Response-PDU (level = FFFFFFFFh)
            end
        end
    ```

    Error and exception handling
    Failure of any of the contained Application Layer Services shall lead to failure of the entire
    Configuration Procedure.
    The general exception handling shall apply.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from xknx.management.procedures.dmp.dmp_authorize_r_co import (
    FREE_ACCESS_KEY,
    dmp_authorize_r_co,
)

if TYPE_CHECKING:
    from xknx.management.management import P2PConnection


async def dmp_authorize2_r_co(connection: P2PConnection, client_key: int) -> int:
    """
    Authorize with a KNX device, comparing free access vs client key.

    DMP_Authorize2_RCo — KNX 03.05.02 §3.5.2. Tries free access first,
    then client key, and uses whichever gives better (lower) access level.

    NOTE: The spec names this "DM_Authorize2_RCo" but it follows the DMP pattern.

    :param connection: Active P2P connection to the device
    :param client_key: 4-byte client authorization key
    :return: Best access level obtained (0 = highest, 15 = lowest)
    """
    free_level = await dmp_authorize_r_co(connection, FREE_ACCESS_KEY)

    if free_level == 0:
        return free_level

    client_level = await dmp_authorize_r_co(connection, client_key)

    if client_level > free_level:
        await dmp_authorize_r_co(connection, FREE_ACCESS_KEY)
        return free_level

    return client_level
