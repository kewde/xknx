"""
DM_SearchRequestExtended_Unicast — KNX 03.05.02 §6.2 (PDF p. 183).

Spec text (verbatim from spec):

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Client
        participant S as Server (device)
        C->>S: SEARCH_REQUEST_EXTENDED (UDP or TCP, control endpoint, SRPs)
        Note over S: Evaluates all SRPs from the request according the specification of the Search Request Parameters in [10]. If the result of the evaluation is to create a response:
        S->>C: SEARCH_RESPONSE_EXTENDED (DIBs)
        Note over C: The client shall wait for UNICAST_SEARCH_RESPONSE_EXTENDED_TIME_OUT (10 s)
    ```

    6.3 DMP_KNXnet/IP_Connect
    This procedure shall be used to connect to a KNXnet/IP server using a specific connection type.

    DMP_KNXnet/IP_Connect( /* [in] */ dmp_HPAIControlEndpoint,
                           /* [in] */ dmp_HPAIDataEndpoint, /* [in] */ dmp_CRI,
                           /* [out] */ dmp_CommChannelID, /* [out] */ dmp_Status,
                           /* [out] */ dmp_HPAIServerDataEndpoint, /* [out] */ dmp_CRD)

    Parameters of the Management Procedure
        dmp_HPAIClientControlEndpoint  This Management Procedure Parameter shall contain the
                                       HPAI of the Control Endpoint of the Management Client.
        dmp_HPAIClientDataEndpoint     This Management Procedure Parameter shall contain the
                                       HPAI of the Data Endpoint of the Management Client.
        dmp_CRI                        This Management Procedure Parameter shall contain the
                                       Connection Request Information from the Management
                                       Client.
        dmp_CommChannelID              This Management Procedure Parameter shall return the
                                       communication channel ID that is chosen by the
                                       Management Server.
        dmp_Status                     This Management Procedure Parameter shall return the
                                       status of the request.
        dmp_HPAIServerDataEndpoint     This Management Procedure Parameter shall contain the
                                       HPAI of the Data Endpoint of the Management Server.
        dmp_CRD                        This Management Procedure Parameter shall contain the
                                       Connection Response Data Block from the Management
                                       Server.

    Variables
    None.

    Precondition
    Through KNXnet/IP Discovery, it is confirmed that the KNXnet/IP device supports the requested
    connection type.
    NOTE 22 To this, the KNXnet/IP Client sends a DESCRIPTION_REQUEST to the control endpoint of the device to which it
    wants to establish a KNXnet/IP Tunnelling Connection. The device shall respond with a DESCRIPTION_RESPONSE frame
    holding the "DIB supported service families". If the device supports KNXnet/IP Tunnelling, one of the DIBs will report a
    Supported Service family 04h, this is, KNXnet/IP Tunnelling.

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as KNXnet/IP Client
        participant S as KNXnet/IP Server
        C->>S: CONNECT_REQUEST (HPAI Control Endpoint = dmp_HPAIClientControlEndpoint, HPAI Data Endpoint = dmp_HPAIClientDataEndpoint, CRI = dmp_CRI)
        S->>C: CONNECT_RESPONSE (dmp_CommChannelID = communication channel ID, dmp_Status = status, dmp_HPAIServerDataEndpoint = HPAI Data Endpoint, dmp_CRD = CRD)
    ```

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dm_search_request_extended_unicast(xknx: XKNX) -> None:
    """DM_SearchRequestExtended_Unicast — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DM_SearchRequestExtended_Unicast (KNX 03.05.02 §6.2) — implementation pending"
    )
