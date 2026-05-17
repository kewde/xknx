"""
DM_SetKey_RCo — KNX 03.05.02 §3.6.1 (PDF p. 76).

Spec text (verbatim from spec):

    This Management Procedure shall use the connection oriented communication mode.

    Used Application Layer Services for Management
    - A_Key_Write

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        C->>S: A_Key_Write(key, level)
        S->>C: A_Key_Response(level)
        Note right of S: A_Disconnect.ind ⇒ error, requested level != returned level ⇒ operation failed
    ```

    Exception handling
    If the level returned in A_Key_Response is not the same as in the A_Key_Write, the operation was not
    successful. Possibly an authorization is required.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dm_set_key_r_co(xknx: XKNX) -> None:
    """DM_SetKey_RCo — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DM_SetKey_RCo (KNX 03.05.02 §3.6.1) — implementation pending"
    )
