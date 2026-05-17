"""
NM_TunnellingFeature_Read — KNX 03.05.02 §6.6 (PDF p. 188).

Spec text (verbatim from spec):

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Tunnelling Client
        participant S as Tunnelling Server (device)
        C->>S: TUNNELLING_FEATURE_GET (Feature Identifier)
        Note over S: In case of a UDP connection, the Tunnelling Server shall confirm the Tunnelling Feature service with TUNNELLING_ACK just like other KNXnet/IP Tunnelling services (see clause "Tunnelling Feature services" in [12]).
        opt UDP
            S->>C: TUNNELLING_ACK
        end
        Note over C: UDP: If the Tunnelling Client does not receive a TUNNELLING_ACK within the TUNNELLING_REQUEST_TIME_OUT (1 s) then it shall repeat the TUNNELLING_FEATURE_GET 1 time.
        Note over S: The Tunnelling Server shall within 3 s respond with a TUNNELLING_FEATURE_RESPONSE, repeating the Feature Identifier and including the Return Code and the Feature Value if the Return Code is positive.
        S->>C: TUNNELLING_FEATURE_RESPONSE (Feature Identifier, Return Code, Feature Value)
        Note over C: UDP: In case of a UDP connection, the Tunnelling Client shall confirm the reception of the TUNNELLING_FEATURE_RESPONSE with a TUNNELLING_ACK.
        opt UDP
            C->>S: TUNNELLING_ACK
        end
        Note over S: UDP: If the Tunnelling Server does not receive a TUNNELLING_ACK within the TUNNELLING_REQUEST_TIME_OUT (1 s) then it shall repeat the TUNNELLING_FEATURE_RESPONSE 1 time.
    ```

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
