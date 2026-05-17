"""
DMP_LCRouteTableStateWrite_RCo — KNX 03.05.02 §3.45.2 (PDF p. 170).

Spec text (verbatim from spec):

    This Management Procedure shall use the connection oriented communication mode.
    The Verify Mode of the Management Server shall not be used.

    Used Application Layer Services for Management
    - A_RouterStatus_Write
    - A_RouterStatus_Read

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        C->>S: A_RouterStatus_Write-PDU (RouteTableState)
        opt verify = enabled
            C->>S: A_RouterStatus_Read-PDU ()
            S->>C: A_RouterStatus_Response-PDU (RouteTableState)
            Note right of S: A_Disconnect.ind ⇒ error, different or no data received ⇒ error
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


async def dmp_lc_route_table_state_write_r_co(xknx: XKNX) -> None:
    """DMP_LCRouteTableStateWrite_RCo — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_LCRouteTableStateWrite_RCo (KNX 03.05.02 §3.45.2) — implementation pending"
    )
