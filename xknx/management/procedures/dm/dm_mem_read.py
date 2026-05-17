"""
DM_MemRead — KNX 03.05.02 §3.18 (PDF p. 105).

Spec text (verbatim from spec):

    3.18.1 Use
    This device Management Procedure shall read a contiguous block of memory and store it in the data
    block. If the deviceStartAddress if higher than the deviceEndAddress this Management Procedure
    shall be skipped.
    A DM_Connect shall be executed before executing this Management Procedure.

    DM_MemRead (flags, dataBlockStartAddress, deviceStartAddress, deviceEndAddress, data)
        flags                  bit 0 location of data
                                   0: in data block
                                   1: -
                               All other bits are reserved. These shall be set to 0. This shall be
                               tested by the Management Client.
        dataBlockStartAddress  specifies the address where the data are located in the data block.
                               If the data are located in the Management Procedure, this field is
                               set to 0
        deviceStartAddress     address of first memory octet that is read by this Management
                               Procedure
        deviceEndAddress       address of the last octet that is read by this Management
                               Procedure
        data                   the data that are read by this Management Procedure. The data are
                               stored in the data block.

    3.18.2 Procedure: DMP_MemRead_RCo
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
            Note right of S: A_Disconnect.ind ⇒ error, no data received ⇒ error
        end
    ```

    Exception handling
    The general exception handling shall apply.

    3.18.3 Procedure: DMP_MemRead_LEmi1
    This Management Procedure shall use the local communication with EMI 1.

    Used EMI-services for Management
    - PC_Get_Value

    Parameters of the Management Procedure
    DMP_MemRead_LEmi1(/* [in] */ DmpStartAddr, /* [in] */ DmpEndAddr, /* [out] */ DmpData, /* [out] */ DmpError)
        DmpStartAddress  The start address of the memory of the device from which the Data
                         shall be read.
        DmpEndAddress    The end address of the memory of the device from which the Data
                         shall be read.
        DmpData          The contents of the memory as returned by the device.
        DmpError         Possible error indication.

    Service parameters
        SrvDataOut  The data as read from the device for each call of the service PC_Get_Value.
        SrvDBLen    The length of the datablock that shall be in one call of the service
                    PC_Get_Value. This shall be 12 octets for all datablocks except for the
                    last one, which may be smaller.
        SrvDBAddr   The start address in the memory of the device from which the current
                    datablock shall be read.

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        loop for each data block (≤12 octet), until all data are transmitted
            C->>S: PC_Get_Value.req message (Length = SrvDBLen, Addr = SrvDBAddr)
            S->>C: PC_Get_Value.con (Length = SrvDBLen, Addr = SrvDBAddr, Data = SrvDataOut)
            Note right of S: no data received ⇒ error
        end
    ```

    Exception handling
    The general exception handling shall apply.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from xknx.management.procedures.dmp.dmp_mem_read_r_co import dmp_mem_read_r_co

__all__ = ["dmp_mem_read_r_co"]
