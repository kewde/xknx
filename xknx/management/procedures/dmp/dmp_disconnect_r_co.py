"""
DMP_Disconnect_RCo — KNX 03.05.02 §3.3.2 (PDF p. 71).

Spec text (verbatim from spec):

    This method shall use the connection oriented remote communication.

    Used Application Layer Services for Management
    - A_Disconnect

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        C->>S: A_Disconnect_Req ()
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


async def dmp_disconnect_r_co(xknx: XKNX) -> None:
    """DMP_Disconnect_RCo — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_Disconnect_RCo (KNX 03.05.02 §3.3.2) — implementation pending"
    )
