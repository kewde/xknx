"""
DMP_Connect_RCo — KNX 03.05.02 §3.2.1 (PDF p. 67).

Spec text (verbatim from spec):

    This Management Procedure shall use the connection oriented communication mode.
    Used Application Layer Services for Management
          •      A_Connect
          •      A_DeviceDescriptor_Read
    Sequence
    Management                                                              Network /                  remark
    Client                                                                  Management
                                                                            Server
                                    A_Connect-PDU
                            (destination_address = IA_target)

    if negative A_Connect.Lcon ⇒ error: no connection established
    else (this is, a positive A_Connect.Lcon is received)
                                                                                  If the device that occupies the IA_target
                                                                            does not support Transport Layer connections,
                                                                                        it shall send a T_Disconnect-PDU.

                                      A_Disconnect-PDU
                                             ()

    if A_Disconnect-PDU is received ⇒ error: the device refuses the connection-oriented connection
    else (no A_Disconnect-PDU is received)
                                                             If a device that occupies IA_target is present on the network,
                                                                            and does support Transport Layer connections,
                                                                                  it shall have no other reaction on the bus
                                                   than the Layer-2 acknowledge that initiates the above A_Connect.Lcon
        The A_DeviceDescriptor_Read-PDU shall use DD0.
                              A_DeviceDescriptor_Read-PDU
                              (destination_address = IA_test,
                                 descriptor_type = 0000h)

                            A_DeviceDescriptor_Response-PDU
                            (descriptor_type, device_descriptor)

    If the Management Client receives an A_DeviceDescriptor_Response-PDU it shall conclude that the Transport Layer connection has
    been established successfully.
    If no A_DeviceDescriptor_Response-PDU is received after time-out ⇒ error: no connection established
    endif

    Exception handling
    There are several error situations when building up a connection oriented communication.
    -   If the T_Connect.req telegram is not acknowledged by a Link Layer acknowledge (negative
        A_Connect.Lcon) then the Management Server with the Individual Address does not exist or the
        system is not configured correctly. (e.g. coupler, Domain Address ...)
    -   If a T_Disconnect-telegram is sent out by the Management Server but no
        A_DeviceDescriptor_Response, the device with the Individual Address exists. The reason for this
        may either be that the Management Server is already using another connection, doesn't support
        connection oriented mode, or the time-out has elapsed.
    -   If a T_Disconnect-telegram is sent out by the transport layer of the Management Client, then the
        system may not be configured correctly, or the Management Server doesn't exist.
    -   If more than one A_DeviceDescriptor_Response-PDU is received, there is more than one device
        with the target address.
    If the above indicates the network may be configured incorrectly, than the network topology shall be
    checked. In all other cases, the DM_Connect may be repeated several times. If this procedure is not
    successful, the depending procedures shall be aborted.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dmp_connect_r_co(xknx: XKNX) -> None:
    """DMP_Connect_RCo — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_Connect_RCo (KNX 03.05.02 §3.2.1) — implementation pending"
    )
