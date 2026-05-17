"""
DM_MemVerify — KNX 03.05.02 §3.17 (PDF p. 103).

Spec text (verbatim from spec):

    3.17.1 Use
    This device Management Procedure shall read a contiguous block of memory and compare it with the
    specified data. The data shall be located either in the management control or in the data block. Only
    the data that are specified in the data block shall be compared. If the deviceStartAddress is higher than
    the deviceEndAddress this Management Procedure is skipped.
    A DM_Connect shall be executed before executing this Management Procedure.

    13) The delay time shall depend on the Management Server and on the amount of written octets (see [08]).

    DM_MemVerify (flags, dataBlockStartAddress, deviceStartAddress, deviceEndAddress, data)
        flags                  bit 0 location of data
                                   0: in data block
                                   1: in management control
                               All other bits are reserved. These shall be set to 0. This shall be
                               tested by the Management Client.
        dataBlockStartAddress  specifies the address where the data are located in the data block.
                               If the data are located in the Management Procedure, this field is
                               set to 0.
        deviceStartAddress     address of first memory octet that is compared by this
                               Management Procedure
        deviceEndAddress       address of the last octet that is compared by this Management
                               Procedure
        data                   the data that are compared by this Management Procedure. The
                               data can be located in the data block or in the Management
                               Procedure.

    3.17.2 Procedure: DMP_MemVerify_RCo
    This Management Procedure shall use the connection oriented communication mode.

    Preconditions
    This Management Procedure shall transfer the data in datablocks and transmit these in subsequent
    A_Memory_Read-PDUs and/or A_Memory_Write-PDUs, as specified below, all of which except
    possibly the last PDU, shall have a data field (ASDU) with a size equal to the maximum size that can
    be transported over the communication path consisting of the Management Client, the Management
    Server and Couplers and Routers in between these two.
    - If the Management Server does not support the L_Data_Extended frame format, then this
      maximal size shall be 12 octets.
    - If the Management Server supports L_Data_Extended frames, then the maximal size shall be
      adapted in function of the capabilities of the Management Server and possible Couplers and
      Routers in the communication path to the Management Client. This is specified in [06].

    Used Application Layer Services for Management
    - A_Memory_Read

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        loop for each data block (data size ≤ maximal size), until all data are transmitted
            C->>S: A_Memory_Read-PDU (Addr, Length)
            S->>C: A_Memory_Response-PDU (Addr, Length, Data)
            Note right of S: A_Disconnect.ind ⇒ error, different or no data received ⇒ error
        end
    ```

    Exception handling
    The general exception handling shall apply.

    3.17.3 Procedure: DMP_MemVerify_LEmi1
    This Management Procedure shall use the local communication with EMI 1.

    Used Application Layer Services for Management
    - PC_Get_Value

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        loop for each data block (≤12 octet), until all data are transmitted
            C->>S: PC_Get_Value-PDU (Addr, Length)
            S->>C: PC_Get_Value-PDU (Addr, Length, Data)
            Note right of S: different or no data received ⇒ error
        end
    ```

    Exception handling
    The general exception handling shall apply.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dm_mem_verify(xknx: XKNX) -> None:
    """DM_MemVerify — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DM_MemVerify (KNX 03.05.02 §3.17) — implementation pending"
    )
