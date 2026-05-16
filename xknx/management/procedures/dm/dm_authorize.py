"""
DM_Authorize — KNX 03.05.02 §3.5 (PDF p. 74).

Spec text (verbatim from spec):

    Use
    This device Management Procedure shall be used to obtain access authorization. The authorization
    shall be executed only when it is required by the Management Server.
    Whether or not a Management Server supports authorisation can directly be retrieved from the Device
    Descriptor Type 0 (mask version). In [14] it is specified for which Profiles authorisation is mandatory.
    DM_Connect shall be executed before executing this Management Procedure.
    DM_Authorize (flags, keys)
       flags                                 All bits are reserved. These shall be set to 0. This shall be tested
                                             by the Management Client.
              key                            key for authorization

    3.5.1           Procedure: DMP_Authorize_RCo
    This Management Procedure shall use the connection oriented communication mode.
    Used Application Layer Services for Management
          •     A Authorize
    Sequence
    Management                                                                        Management                    remark
    Client                                                                            Server

    if authorization is required (key != FFFF FFFFH)
                               A_Authorize_Request-PDU (key)

                          A_Authorize_Response-PDU (key, level)                                     A_Disconnect.ind ⇒
                                                                                                    error: connection was broken
                                                                                                    down
    endif

    Exception handling
    The general exception handling shall apply.

    3.5.2 DM_Authorize2_RCo
    Use
    This device Management Procedure DM_Authorize2_RCo shall be used to obtain access
    authorization. It shall assume that the Management Client has an access key provided by its user. If the
    Management Client does not have an access key, it shall not be executed.
    Opposite to the Management Procedure DM_Authorize_RCo, this Management Procedure
    DM_Authorize2_RCo does not presume that the device has been locked with the key that is provided
    to the procedure. Therefore, it authorizes subsequently with the key FFFFFFFFh and with the key
    client_key and continues with the key that gives the maximal access rights.
    NOTE         This is the case when the ETS User enters a key to be used to lock the devices and uninitialised devices fresh from
    the factory are used.

    DM_Connect shall be executed before executing this Management Procedure.

    Use
     •        ProfilesSystem 2
                      BIM M112
     • Conditions Write access, i.e. modifying memory- or Property contents
                      A key must be available
    Used Application Layer Services for Management
          •      A_Authorize_Request

    Sequence
                                   Client                                              Server
     The Management Server (device) shall according the specification of
     A_Auhorize in [03] have granted the access rights associated to the key
     FFFFFFFFh. This level is however unknown to the Management Client.
     Therefore, the client re-authorizes explicitly with key FFFFFFFFh to obtain the
     free access level.
                                                       A_Authorize_Request-PDU
                                                           (key = FFFFFFFFh)

                                                   A_Authorize_Response-PDU
                                                      (level = free_level)

     If the free access level is not the highest level (lowest numerical value,
     maximum access rights)
                                                         A_Authorize_Request-PDU
                                                             (key = client_key)

                                                   A_Authorize_Response-PDU
                                                      (level = client_level)

     The level obtained now with access_key is compared to the one obtained for free
     access. If free access gave higher access level (lower numerical value), a new
     authorisation with free access level is done.
         if client_level > free_level
                                                       A_Authorize_Request-PDU
                                                          (key = FFFFFFFFh)

                                                   A_Authorize_Response-PDU
                                                      (level = FFFFFFFFh)

        endif
     endif
    Error and exception handling
    Failure of any of the contained Application Layer Services shall lead to failure of the entire
    Configuration Procedure.
    The general exception handling shall apply.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dm_authorize(xknx: XKNX) -> None:
    """DM_Authorize — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DM_Authorize (KNX 03.05.02 §3.5) — implementation pending"
    )
