"""
DMP_LCSlaveMemWrite_Rco — KNX 03.05.02 §3.38.2 (PDF p. 161).

Spec text (verbatim from spec):

    This Management Procedure shall use the connection oriented communication mode.
    The Verify Mode of the Management Server shall not be used.
    Preconditions
    This Management Procedure shall transfer the data in data blocks and transmit these in subsequent
    A_RouterMemory_Read_Read-PDUs and/or A_RouterMemory_Write-PDUs, as specified below, all
    of which except possibly the last PDU, shall have a data field (ASDU) with a size equal to the
    maximum size that can be transported over the communication path consisting of the Management
    Client, the Management Server and Couplers and Routers in between these two.
           -   If the Management Server does not support the L_Data_Extended Frame format, then this
               maximal size shall be 11 octets.
           -   If the Management Server supports L_Data_Extended Frames, then the maximal size shall
               be adapted in function of the capabilities of the Management Server and possible Couplers
               and Routers in the communication path to the Management Client. This is specified in [06].
    Used Application Layer Services for Management
           •   A_RouterMemory_Write
           •   A_RouterMemory_Read

    Sequence
    Management                                                            Management                 remark
    Client                                                                Server
    for each data block (data size≤ maximal size), until all data are transmitted
                           A_RouterMemory_Write-PDU
                                 (Addr, Length, Data)

             if verify = enabled
                             A_RouterMemory_Read-PDU
                                   (Addr, Length)

                           A_RouterMemory_Response-PDU                                 A_Disconnect.ind ⇒
                                (Addr, Length, Data)                                   error,
                                                                                       if verify = enabled and
                                                                                       different or no data received
                                                                                       ⇒ error
             else
                 delay for programming the memory in the device 16)
             endif
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


async def dmp_lc_slave_mem_write_rco(xknx: XKNX) -> None:
    """DMP_LCSlaveMemWrite_Rco — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_LCSlaveMemWrite_Rco (KNX 03.05.02 §3.38.2) — implementation pending"
    )
