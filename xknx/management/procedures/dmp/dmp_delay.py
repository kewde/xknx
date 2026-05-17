"""
DMP_Delay — KNX 03.05.02 §3.8.2 (PDF p. 90).

Spec text (verbatim from spec):

    Used Application Layer Services for Management
    None.

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        Note over C: delay for specified time
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


async def dmp_delay(xknx: XKNX) -> None:
    """DMP_Delay — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_Delay (KNX 03.05.02 §3.8.2) — implementation pending"
    )
