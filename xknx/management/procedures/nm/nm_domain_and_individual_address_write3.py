"""
NM_DomainAndIndividualAddress_Write3 — KNX 03.05.02 §2.11 (PDF p. 23).

Spec text (verbatim from spec):

    [spec text unavailable]

Inputs (from spec):
    (none specified in spec)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def nm_domain_and_individual_address_write3(xknx: XKNX) -> None:
    """NM_DomainAndIndividualAddress_Write3 — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "NM_DomainAndIndividualAddress_Write3 (KNX 03.05.02 §2.11) — implementation pending"
    )
