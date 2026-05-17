"""
DM_LCSlaveMemVerify — KNX 03.05.02 §3.39 (PDF p. 162).

Spec text (verbatim from spec):

    3.39.1 Use
    This device Management Procedure shall read a contiguous block of slave memory in the
    Management Server (Coupler) and compare it with the specified data. The data shall be located either
    in the management control or in the data block. Only the data that are specified in the data block shall
    be compared. If the deviceStartAddress if higher than the deviceEndAddress this Management
    Procedure shall be skipped
    A DM_Connect shall be executed before executing this Management Procedure.
    This device Management Procedure shall not be used for further developments of Management
    Servers.

    16) The delay time depends on the Management Server and on the amount of written octets (see [08]).

    DM_LCSlaveMemVerify (flags, dataBlockStartAddress, deviceStartAddress,
                         deviceEndAddress, data)
    flags                      bit 0:    location of data
                                         0: in data block
                                         1: in management control
                               All other bits are reserved. These shall be set to 0. This shall be
                               tested by the Management Client.
    dataBlockStartAddress      specifies the address where the data are located in the data
                               block. If the data are located in the Management Procedure, this
                               field is set to 0.
    deviceStartAddress         address of first memory octet that is compared by this
                               Management Procedure
    deviceEndAddress           address of the last octet that is compared by this Management
                               Procedure
    data                       the data that are compared by this Management Procedure. The
                               data can be located in the data block or in the Management
                               Procedure.

    3.39.2 Procedure: DMP_LCSlaveMemVerify_RCo
    This Management Procedure shall use the connection oriented communication mode.
    Preconditions
    This Management Procedure shall transfer the data in data blocks and transmit these in subsequent
    A_RouterMemory_Read-PDUs and/or A_RouterMemory_Write-PDUs, as specified below, all of
    which except possibly the last PDU, shall have a data field (ASDU) with a size equal to the maximum
    size that can be transported over the communication path consisting of the Management Client, the
    Management Server and Couplers and Routers in between these two.
        - If the Management Server does not support the L_Data_Extended Frame format, then this
          maximal size shall be 11 octets.
        - If the Management Server supports L_Data_Extended Frames, then the maximal size shall
          be adapted in function of the capabilities of the Management Server and possible Couplers
          and Routers in the communication path to the Management Client. This is specified in [06].
    Used Application Layer Services for Management
    - A_RouterMemory_Read

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        Note over C,S: for each data block (data size≤ maximal size), until all data are transmitted
        C->>S: A_RouterMemory_Read-PDU (Addr, Length)
        S->>C: A_RouterMemory_Response-PDU (Addr, Length, Data)
        Note right of S: A_Disconnect.ind => error, different or no data received => error
        Note over C,S: endfor
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


async def dm_lc_slave_mem_verify(xknx: XKNX) -> None:
    """DM_LCSlaveMemVerify — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DM_LCSlaveMemVerify (KNX 03.05.02 §3.39) — implementation pending"
    )
