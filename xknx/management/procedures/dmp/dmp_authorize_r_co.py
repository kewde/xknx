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

if TYPE_CHECKING:
    from xknx import XKNX


async def dmp_authorize_r_co(xknx: XKNX) -> None:
    """DMP_Authorize_RCo — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_Authorize_RCo (KNX 03.05.02 §3.5.1) — implementation pending"
    )
