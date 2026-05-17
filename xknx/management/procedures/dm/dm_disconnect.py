"""
DM_Disconnect — KNX 03.05.02 §3.3 (PDF p. 71).

Spec text (verbatim from spec):

    3.3.1 Use
    This device Management Procedure shall be used to close a connection to the Management Server,
    which was built up with DM_Connect.
    A DM_Connect shall be executed before executing this Management Procedure.
    DM_Disconnect (flags)
        flags    All other bits are reserved. These shall be set to 0. This shall be
                 tested by the Management Client.

    3.3.2 Procedure: DMP_Disconnect_RCo
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

    3.3.4 Procedure: DMP_Disconnect_LEmi1
    Use
    This Management Procedure shall use the local communication with EMI 1.
    Used EMI-services for Management
     None

    Parameters of the Management Procedure
    DMP_Disconnect_LEmi1()
    Sequence
    None.

    Exception handling
    The general exception handling shall apply.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dm_disconnect(xknx: XKNX) -> None:
    """DM_Disconnect — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DM_Disconnect (KNX 03.05.02 §3.3) — implementation pending"
    )
