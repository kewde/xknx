"""
NM_SearchRequestExtended_Multicast — KNX 03.05.02 §6.1 (PDF p. 183).

Spec text (verbatim from spec):

    Client                                                                             Server (device)

                             SEARCH_REQUEST_EXTENDED
                              (UDP, discovery endpoint, SRPs)

                                                       Evaluates all SRPs from the request according the specification of the Seach
                                                                                                          Request Parameters in [10]
                                                                              If the result of the evaluation is to create a response:.
                            SEARCH_RESPONSE_EXTENDED
                                      (DIBs)

    Collect all responses until either all expected responses
    have arrived, or a timeout of 3 seconds elapsed.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def nm_search_request_extended_multicast(xknx: XKNX) -> None:
    """NM_SearchRequestExtended_Multicast — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "NM_SearchRequestExtended_Multicast (KNX 03.05.02 §6.1) — implementation pending"
    )
