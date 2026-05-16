"""
DMP_UserMemRead_RCo — KNX 03.05.02 §3.21.2 (PDF p. 113).

Spec text (verbatim from spec):

    This Management Procedure shall use the connection oriented communication mode.
    Preconditions
    This Management Procedure shall transfer the data in datablocks and transmit these in subsequent
    A_Memory_Read-PDUs, as specified below, all of which except possibly the last PDU, shall have a
    data field (ASDU) with a size equal to the maximum size that can be transported over the
    communication path consisting of the Management Client, the Management Server and Couplers and
    Routers in between these two.
         -    If the Management Server does not support the L_Data_Extended frame format, then this
              maximal size shall be 11 octets.
         -    If the Management Server supports L_Data_Extended frames, then the maximal size shall be
              adapted in function of the capabilities of the Management Server and possible Couplers and
              Routers in the communication path to the Management Client. This is specified in [06].
    Used Application Layer Services for Management
          •   A_UserMemory_Read

    Sequence
    Management                                                            Management                remark
    Client                                                                Server
    for each data block (data size ≤ maximal size), until all data are transmitted
                             A_UserMemory_Read-PDU
                                    (Addr, Length)

                             A_UserMemory_Response-PDU                                 A_Disconnect.ind ⇒ error,
                                 (Addr, Length, Data)                                  no data received ⇒ error

    endfor

    Exception handling
    The general exception handling shall apply.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dmp_user_mem_read_r_co(xknx: XKNX) -> None:
    """DMP_UserMemRead_RCo — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_UserMemRead_RCo (KNX 03.05.02 §3.21.2) — implementation pending"
    )
