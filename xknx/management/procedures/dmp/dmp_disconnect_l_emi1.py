"""
DMP_Disconnect_LEmi1 — KNX 03.05.02 §3.3.4 (PDF p. 71).

Spec text (verbatim from spec):

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


async def dmp_disconnect_l_emi1(xknx: XKNX) -> None:
    """DMP_Disconnect_LEmi1 — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_Disconnect_LEmi1 (KNX 03.05.02 §3.3.4) — implementation pending"
    )
