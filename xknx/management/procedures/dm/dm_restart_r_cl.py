"""
DM_Restart_RCl — KNX 03.05.02 §3.7.2 (PDF p. 85).

Spec text (verbatim from spec):

    Use
    This method shall use the point-to-point connectionless communication mode.
    The Management Client shall prior to calling this Management Procedure with a Master Reset verify
    that this feature is effectively supported by the Management Server. If not, the procedure shall only be
    called with a Basic Restart 10).

    10) Existing implementations may not check bit 0 of octet 7 and may not react as expected. They may ignore the
       service entirely, only perform a Basic Restart if a Master Reset is called or exhibit another behaviour.

    Used Application Layer services for Management
    - A_Restart

    Parameters of the Management Procedure
    DM_Restart_RCl (/* [in] */ mpp_RestartType, /* [in] */ mpp_EraseCode,
                   /* [in] */ mpp_ChannelNumber, /* [out] */ mpp_ErrorCode,
                   /* [out] */ mpp_ProcessTime)
        mpp_RestartType    This Management Procedure Parameter shall indicate whether a Basic
                           Restart or a Master Reset shall be executed.
        mpp_EraseCode      This Management Procedure Parameter shall indicate which
                           Resource(s) shall be reset to its (their) default value. This is void in case
                           only a Basic Restart is executed.
        mpp_ChannelNumber  The number of the application channel that shall be reset or 00h.
        mpp_ErrorCode      This Management Procedure Parameter shall contain the Error Code
                           returned by the Management Client.
        mpp_ProcessTime    This Management Procedure Parameter shall return to the Management
                           Client the Process Time needed by the Management Server. The
                           Management Client shall consider this mpp_ProcessTime as time-out
                           after which communication attempts following a Master Reset shall be
                           considered without success.

    Variables
    None.

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        Note over C: The Management Client shall send an A_Restart-PDU to the Management Server in point-to-point connectionless communication mode; the fields of the A_Restart-PDU shall be set according the values of the Parameters of this Management Procedure. Reserved and unused fields shall be set to 0.
        C->>S: A_Restart-PDU (restart_type = mpp_RestartType, erase_code = mpp_EraseCode, channel_number = mpp_ChannelNumber)
        Note over S: The Management Server shall confirm with an A_Restart_Response-PDU if a Master Reset is requested. It shall then execute a Basic Restart or Master Reset as requested.
        S->>C: A_Restart_Response-PDU (restart_type = mpp_RestartType, mpp_ErrorCode = error_code, mpp_ProcessTime = process_time)
        Note over S: The Management Server shall reset the Resource(s) as indicated in the A_Restart-PDU. The Management Server shall additionally restart.
        Note over C: The Management Client shall interpret any error. If further Management Procedures follow, the Management Client has to poll the Management Server for at least the period given by the mpp_ProcessTime. If mpp_ProcessTime expires without reaction from the Management Server, then the Management Client shall try the subsequent Management Procedure one last time, before it may conclude that the Management Server does no longer respond.
    ```

    Exception handling
    The general exception handling shall be applicable.
    The following errors and exceptions shall be checked in the below given priority.
    (1) If the Management Server receives an A_Restart-PDU with a reserved field with a value
        different from 0, then this service request shall be ignored.
    (2) If the Management Server receives an A_Restart-PDU but the Management Client does not
        have the required access rights (KNX Authorization) then it shall respond with an
        A_Restart_Response-PDU with Error Code = 01h "Access Denied".
    (3) If the Management Server receives an A_Restart-PDU with an Erase Code that it does not
        support or that is specified as "reserved" then it shall respond with an A_Restart_Response-
        PDU with Error Code = 02h "Unsupported Erase Code".
    (4) The Management Server shall respond with the Error Code 03h = "Invalid Channel Number"
        in any of the following cases.
        - It receives an A_Restart-PDU with a Channel Number that is not 00h with an Erase
          Code for which the Channel Number shall be 00h.
        - It receives an A_Restart-PDU with an Erase Code that allows the Channel Number to be
          different from 00h; the Channel Number is different from 00h but the Management
          Server does not support application channels.
        - It receives an A_Restart-PDU with an Erase Code that allows the Channel Number to be
          different from 00h; the Channel Number is different from 00h and the Management
          Server does support application channels but does not have a channel with the requested
          channel number.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dm_restart_r_cl(xknx: XKNX) -> None:
    """DM_Restart_RCl — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DM_Restart_RCl (KNX 03.05.02 §3.7.2) — implementation pending"
    )
