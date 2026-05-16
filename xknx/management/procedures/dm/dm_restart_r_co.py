"""
DM_Restart_RCo — KNX 03.05.02 §3.7.3 (PDF p. 87).

Spec text (verbatim from spec):

    Use
    This method shall use the point-to-point connection oriented remote communication.
    The Management Client shall prior to calling this Management Procedure with a Master Reset verify
    that this feature is effectively supported by the Management Server. If not, the procedure shall only be
    called with a Basic Restart 11).
    A DM_Connect shall be executed before executing this Management Procedure.
    After reception of the A_Restart-PDU this Transport Layer connection breaks down with the
    execution of the A_Restart service; nevertheless an explicit DM_Disconnect procedure shall follow.
    Used Application Layer services for Management
     • A_Restart

    Parameters of the Management Procedure
    DM_Restart_RCo (/* [in] */ mpp_RestartType, /* [in] */ mpp_EraseCode,
                   /* [in] */ mpp_ChannelNumber, /* [out] *mpp_ErrorCode,
                   /* [out] */ mpp_ProcessTime)
          mpp_RestartType:            This Management Procedure Parameter shall indicate whether a Basic
                                      Restart or a Master Reset shall be executed.

    11) Existing implementations may not check bit 0 of octet 7 and may not react as expected. They may ignore the
       service entirely, only perform a Basic Restart if a Master Reset is called or exhibit another behaviour.

          mpp_EraseCode:                  This Management Procedure Parameter shall indicate which
                                          Resource(s) shall be reset to its (their) default value. This is void in
                                          case only a Basic Restart is executed.
          mpp_ChannelNumber:              The number of the application channel that shall be reset or 00h.
          mpp_ErrorCode                   This Management Procedure Parameter shall contain the Error Code
                                          returned by the Management Client.
          mpp_ProcessTime                 This Management Procedure Parameter shall return to the Management
                                          Client the Process Time needed by the Management Server. The
                                          Management Client shall consider this mpp_ProcessTime as time-out
                                          after which communication attempts following a Master Reset shall be
                                          considered without success.

    Variables
    None.

    Sequence
    Management                                                                       Management                   remark
    Client                                                                           Server

    The Management Client shall send an A_Restart-PDU to the Management
    Server in point-to-point connection-oriented communication mode; the fields of
    the A_Restart-PDU shall be set according the values of the Parameters of this
    Management Procedure. Reserved and unused fields shall be set to 0.

                                       A_Restart-PDU
                             (restart_type = mpp_RestartType,
                               erase_code = mpp_EraseCode,
                         channel_number = mpp_ChannelNumber)

                                                 The Management Server shall confirm with an A_Restart_Response-PDU if a Master
                                                 Reset is requested. It shall then execute a Basic Restart or Master Reset as requested.
                                  A_Restart_Response-PDU
                              (restart_type = mpp_RestartType,
                                mpp_ErrorCode = error_code,
                             mpp_ProcessTime = process_time))

                                                               The Management Server shall reset the related Resource as indicated in the
                                                                   A_Restart-PDU (1). The Management Server shall additionally restart.
                             It is recommended that the execution of the Basic Restart includes closing the Transport Layer connection.
                                                                                                           This is however not required.
                                                Additionally, it may be that the reset of the Management Server’s communication system
                             leads to the effect that the handling of the T_Disconnect in the Management Server’s communication stack
                                                             “down” is not completed and that no T_Disconnect –frame is sent on the bus.
    (5)                                T_Disconnect-PDU
                                              ()

    abort the connection of the client side Transport Layer
                                       T_Disconnect-PDU
                                              ()

    Exception handling
            The general exception handling shall be applicable.
     (1) If the Management Server receives an A_Restart-PDU with a reserved field with a value
         different from 0, then this service request shall be ignored.
     (2) If the Management Server receives an A_Restart-PDU but the Management Client does not
         have the required access rights (KNX Authorization) then it shall respond with an
         A_Restart_Response-PDU with Error Code = 01h “Access Denied”.
     (3) If the Management Server receives an A_Restart-PDU with an Erase Code that it does not
         support then it shall respond with an A_Restart_Response-PDU with Error Code = 02h
         “Unsupported Erase Code”.
     (4) The Management Server shall respond with the Error Code 03h = “Invalid Channel Number”
         in any of the following cases.
             - It receives an A_Restart-PDU with a Channel Number that is not 00h with an Erase
                Code for which the Channel Number.
             - It receives an A_Restart-PDU with an Erase Code that allows the Channel Number to be
                different from 00h; the Channel Number is different from 00h but the Management
                Server does not support application channels.
             - It receives an A_Restart-PDU with an Erase Code that allows the Channel Number to be
                different from 00h; the Channel Number is different from 00h and the Management
                Server does support application channels but does not have a channel with the requested
                channel number.
     (5) All telegrams sent out by the Management Server shall be ignored, except negative
         TL-confirmations.
         In particular, the recommended T_Disconnect-PDU from the Management Server may or may
         not be sent on the bus. The Management Client shall take that into account.
         1 Regardless of whether or not a T_Disconnect-PDU is received from the Management
              Server, the Management Client shall issue a T_Disconnect-PDU to the Management
              Server.
         2 The Management Client shall wait for a possible T_Disconnect-PDU for
              6 seconds.(See NOTE 16)
              -     If after this time no T_Disconnect-PDU is received, then this shall not be regarded as
                    a protocol error.
              -     If the Management Client receives a T_Disconnect-PDU then it shall ignore this
                    message. This T_Disconnect-PDU may be received before or after the “own”
                    mandatory T_Disconnect-PDU from the Management Client specified under 1.
              In both cases, at first after this time-out has elapsed, the Management Client shall
              continue the possible further configuration of the Management Server: the configuration
              shall not be continued while this time-out has not elapsed.
                NOTE 16        This is because a possible subsequent T_Connect-PDU from the MaC and the awaited
                T_Disconnect-PDU from the MaS may miss each other on the network. Cause and consequence are then
                unclear to both MaS and MaC, which will leave the TL state machines in an unpredictable state.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dm_restart_r_co(xknx: XKNX) -> None:
    """DM_Restart_RCo — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DM_Restart_RCo (KNX 03.05.02 §3.7.3) — implementation pending"
    )
