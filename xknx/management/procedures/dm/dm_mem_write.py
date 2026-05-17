"""
DM_MemWrite — KNX 03.05.02 §3.16 (PDF p. 98).

Spec text (verbatim from spec):

    3.16.1 Use
    This device Management Procedure shall write a contiguous block of data to the specified memory
    addresses.
    The data shall be located either in the management control or in the data block. Only the data that is
    specified in the data block shall be written. Depending on the flag the data shall be verified
    immediately. If the deviceStartAddress is higher than the deviceEndAddress this Management
    Procedure shall be skipped.
    A DM_Connect shall be executed before executing this Management Procedure.

    DM_MemWrite (flags, dataBlockStartAddress, deviceStartAddress, deviceEndAddress, data)
        flags                  bit 0 location of data
                                   0: in data block
                                   1: in Management Procedure
                               bit 1 verify enabled / disabled
                                   0: disabled
                                   1: enabled
                               All other bits are reserved. These shall be set to 0. This shall be
                               tested by the Management Client.
        dataBlockStartAddress  specifies the address where the data are located in the data block.
                               If the data are located in the Management Procedure, this field is
                               set to 0.
        deviceStartAddress     address of first memory octet that is written by this Management
                               Procedure
        deviceEndAddress       address of the last octet that is written by this Management
                               Procedure
        data                   the data that are transferred by this Management Procedure. The
                               data can be located in the data block or in the Management
                               Procedure.

    Data Format
    code   flags  dataBlockStartAddress  deviceStartAddress  deviceEndAddress  reserved / data
    20h    FFh    BBBB BBBB              SSSS SSSS           EEEE EEEE         00h / DDh
    1 octet 1 octet 4 octet              4 octet             4 octet           18 octet

    3.16.2 Procedure: DMP_MemWrite_RCo
    Use
    This Management Procedure shall use the connection oriented communication mode.
    The Verify Mode of the Management Server shall not be used.

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
    - A_Memory_Write
    - A_Memory_Read

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        loop for each datablock (data size ≤ maximal size), until all data are transmitted
            C->>S: A_Memory_Write-PDU (Addr, Length, Data)
            alt verify = enabled
                C->>S: A_Memory_Read-PDU (Addr, Length)
                S->>C: A_Memory_Response-PDU (Addr, Length, Data)
                Note right of S: A_Disconnect.ind ⇒ error, different or no data received ⇒ error
            else
                Note over C,S: delay for programming the memory in the device 12
            end
        end
    ```

    Exception handling
    The general exception handling shall apply.

    3.16.3 Procedure: DMP_MemWrite_RCoV
    This Management Procedure shall use the connection oriented communication mode.
    The Verify Mode of the Management Server shall be used.

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
    - A_Memory_Write

    12) The delay time depends on the Management Server and on the amount of written octets (see [08]).

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        opt Verify Mode is not active
            opt Property of device control is unknown to the Management Client
                C->>S: A_PropertyDescription_Read-PDU (object_index = DeviceObject, PID = PID_DEVICE_CONTROL)
                S->>C: A_PropertyDescription_Response-PDU (object_index = DeviceObject, PID = PID_DEVICE_CONTROL, type = .., ...)
                Note right of S: A_Disconnect.ind ⇒ error, Property does not exist ⇒ error
            end
            C->>S: A_PropertyValue_Read-PDU (object_index = DeviceObject, PID = PID_DEVICE_CONTROL, start_index = 01h, element_count = 01h)
            S->>C: A_PropertyValue_Response-PDU (object_index = DeviceObject, PID = PID_DEVICE_CONTROL, start_index = 01h, element_count = 01h, data = DDh, ..)
            Note right of S: A_Disconnect.ind ⇒ error, if no data received ⇒ error
            C->>S: A_PropertyValue_Write-PDU (object_index = DeviceObject, PID = PID_DEVICE_CONTROL, start_index = 01h, element_count = 01h, data = DDh, ..)
            Note right of C: In the data (DD) bit 2 (Verify Mode) has to be set.
            S->>C: A_PropertyValue_Response-PDU (object_index = DeviceObject, PID = PID_DEVICE_CONTROL, start_index = 01h, element_count = 01, data = XX, ..)
            Note right of S: A_Disconnect.ind ⇒ error, if verify = enabled and different or no data received ⇒ error
        end
        loop for each data block (data size ≤ maximal size), until all data are transmitted
            C->>S: A_Memory_Write-PDU (Addr, Length, Data)
            S->>C: A_Memory_Response (Addr, Length, Data)
            Note right of S: A_Disconnect.ind ⇒ error, if verify = enabled and different or no data received ⇒ error
        end
    ```

    Exception handling
    The general exception handling shall apply.

    3.16.4 Procedure: DMP_MemWrite_LEmi1
    This Management Procedure shall use the local communication with EMI 1.

    Used EMI-services for Management
    - PC_Get_Value
    - PC_Set_Value

    Parameters of the Management Procedure
    DMP_MemWrite_LEmi1(/* [in] */ DmpStartAddr, /* [in]*/ DmpEndAddr, /* [in]*/ DmpData, /* [out] */ DmpError)
        DmpStartAddr  The start address in the memory of the device into which the Data
                      shall be written.
        DmpEndAddr    The end address in the memory of the device into which the Data shall
                      be written.
        DmpData       The Data to be written in the device.
        DmpError      Possible error indication.

    Service parameters
        SrvDataIn   The data that shall be written in the device in one call of the service
                    PC_Set_Value.
        SrvDataOut  The data as read back from the device for each call of the service
                    PC_Set_Value.
        SrvDBLen    The length of the datablock written in one call of the service
                    PC_Set_Value. This shall be 12 octets for all datablocks except for the
                    last one, which may be smaller.
        SrvDBAddr   The start address in the memory of the device where the current
                    datablock shall be written.

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        loop for each datablock (≤12 octet), until all data are transmitted
            C->>S: PC_Set_Value.req message (Length = SrvDBLen, Address = SrvDBAddr, Data = SrvDBIn)
            alt verify = enabled
                C->>S: PC_Get_Value.req message (Length = SrvDBLen, Address = SrvDBAddr)
                S->>C: PC_Get_Value.con message (Length = SrvDBLen, Address = SrvDBAddr, Data = SrvDBOut)
                Note right of S: If SrvDBOut differs from SrvDBIn or if no data received ⇒ error
            else
                Note over C,S: delay for programming the memory in the device 13)
            end
        end
    ```

    Exception handling
    The general exception handling shall apply.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from xknx.management.procedures.dmp.dmp_mem_write_r_co import dmp_mem_write_r_co

__all__ = ["dmp_mem_write_r_co"]
