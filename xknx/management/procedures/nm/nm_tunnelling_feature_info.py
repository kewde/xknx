"""
NM_TunnellingFeature_Info — KNX 03.05.02 §6.8 (PDF p. 189).

Spec text (verbatim from spec):

    Tunnelling                                                                      Tunnelling
    Client                                                                          Server (device)

                                                    If the value changes of an Interface Feature that is available to the connected
                                                           Tunnelling Client through TUNNELLING_FEATURE_INFO and that
                                                       Tunnelling Client has enabled the Interface Feature Info service (Interface
                                                                Feature 8), then the Tunnelling Server shall spontaneously send a
                                                   TUNNELLING_FEATURE_INFO to the Tunnelling Client, with the Feature
                                                                                                 Identifier and the Feature Value.
                             TUNNELLING_FEATURE_INFO
                             (Feature Identifier, Feature Value)

    UDP: In case of a UDP connection, the Tunnelling Client shall confirm the reception of the
    TUNNELLING_FEATURE_INFO with a TUNNELLING_ACK.
                                 UDP: TUNNELLING_ACK

                             UDP: If the Tunnelling Server does not receive a TUNNELLING_ACK within the TUNNELLING_-
                                REQUEST_TIME_OUT (1 s) then it shall repeat the TUNNELLING_FEATURE_INFO 1 time.

    7 RF Management Procedures

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def nm_tunnelling_feature_info(xknx: XKNX) -> None:
    """NM_TunnellingFeature_Info — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "NM_TunnellingFeature_Info (KNX 03.05.02 §6.8) — implementation pending"
    )
