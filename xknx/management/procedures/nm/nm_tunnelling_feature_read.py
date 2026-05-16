"""
NM_TunnellingFeature_Read — KNX 03.05.02 §6.6 (PDF p. 188).

Spec text (verbatim from spec):

    Tunnelling                                                                     Tunnelling
    Client                                                                         Server (device)

                             TUNNELLING_FEATURE_GET
                                  (Feature Identifier)

                                                         In case of a UDP connection, the Tunnelling Server shall confirm the
                                                         Tunnelling Feature service with TUNNELLING_ACK just like other
                                                       KNXnet/IP Tunnelling services (see clause “Tunnelling Feature services”
                                                                                                                      in [12]).
                                 UDP: TUNNELLING_ACK

    UDP: If the Tunnelling Client does not receive a TUNNELLING_ACK within the
    TUNNELLING_REQUEST_TIME_OUT (1 s) then it shall repeat the
    TUNNELLING_FEATURE_GET 1 time.
                                                                          The Tunnelling Server shall within 3 s respond with a
                                                      TUNNELLING_FEATURE_RESPONSE, repeating the Feature Identifier
                                                      and including the Return Code and the Feature Value if the Return Code is
                                                                                                                       positive.
                        TUNNELLING_FEATURE_RESPONSE
                     (Feature Identifier, Return Code, Feature Value)

    UDP: In case of a UDP connection, the Tunnelling Client shall confirm the reception of the
    TUNNELLING_FEATURE_RESPONSE with a TUNNELLING_ACK.
                                 UDP: TUNNELLING_ACK

                            UDP: If the Tunnelling Server does not receive a TUNNELLING_ACK within the TUNNELLING_-
                           REQUEST_TIME_OUT (1 s) then it shall repeat the TUNNELLING_FEATURE_RESPONSE 1 time.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def nm_tunnelling_feature_read(xknx: XKNX) -> None:
    """NM_TunnellingFeature_Read — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "NM_TunnellingFeature_Read (KNX 03.05.02 §6.6) — implementation pending"
    )
