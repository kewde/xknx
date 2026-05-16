"""
DMP_MemVerify_Extended_R — KNX 03.05.02 §3.23 (PDF p. 114).

Spec text (verbatim from spec):

    This Management Procedure shall use the connection oriented or connectionless communication
    mode.
    Preconditions
    This Management Procedure shall transfer the data in datablocks and transmit these in subsequent
    A_MemoryExtended_Read-PDUs and/or A_MemoryExtended_Write-PDUs, as specified below, all of
    which except possibly the last PDU, shall have a data field (ASDU) with a size equal to the maximum
    size that can be transported over the communication path consisting of the Management Client, the
    Management Server and Couplers and Routers in between these two.
    The usage of this procedure instead of the DMP_MemWrite_Extended_R procedure will produce the
    same amount of data on the bus. It still can be a useful procedure if the Server has no optimization in
    his write algorithm and writes Data no matter if the same data is already stored in the memory.
         -       If the Management Server does not support the L_Data_Extended Frame format, then this
                 maximal size shall be 10 octets.
         -       If the Management Server supports L_Data_Extended Frames, then the maximal size shall
                 be adapted in function of the capabilities of the Management Server and possible Couplers
                 and Routers in the communication path to the Management Client. This is specified in [06].
    Used Application Layer Services for Management
    •    A_MemoryExtended_Read
    •    A_MemoryExtended_Read_Response

    Management                                                            Management                 remark
    Client                                                                Server

    for each data block (data size ≤ maximal size), until all data are transmitted
                            A_MemoryExtended_Read -PDU
                                  (Addr, Length)

                       A_MemoryExtended_Read_Response-PDU                              A_Disconnect.ind ⇒
                            (Return Code, Addr, Data)                                  error,
                                                                                       negative Return Code
                                                                                       received ⇒ error
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


async def dmp_mem_verify_extended_r(xknx: XKNX) -> None:
    """DMP_MemVerify_Extended_R — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_MemVerify_Extended_R (KNX 03.05.02 §3.23) — implementation pending"
    )
