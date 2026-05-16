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

    DM_MemWrite                                      (flags, dataBlockStartAddress, deviceStartAddress,
                                                     deviceEndAddress, data)
              flags                          bit 0     location of data
                                                         0: in data block
                                                         1: in Management Procedure
                                             bit 1 verify enabled / disabled
                                                         0: disabled
                                                         1: enabled
                                             All other bits are reserved. These shall be set to 0. This shall be
                                             tested by the Management Client.
              dataBlockStartAddress          specifies the address where the data are located in the data block.
                                             If the data are located in the Management Procedure, this field is
                                             set to 0.
              deviceStartAddress             address of first memory octet that is written by this Management
                                             Procedure
              deviceEndAddress               address of the last octet that is written by this Management
                                             Procedure
              data                           the data that are transferred by this Management Procedure. The
                                             data can be located in the data block or in the Management
                                             Procedure.
    Data Format
     code            flags dataBlockStartAddress        deviceStartAddress       deviceEndAddress         reserved /
                                                                                                             data
      20h            FFh       BBBB BBBB                    SSSS SSSS               EEEE EEEE             00h / DDh
    1 octet 1 octet                4 octet                     4 octet                 4 octet             18 octet

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
         -    If the Management Server does not support the L_Data_Extended frame format, then this
              maximal size shall be 12 octets.
         -    If the Management Server supports L_Data_Extended frames, then the maximal size shall be
              adapted in function of the capabilities of the Management Server and possible Couplers and
              Routers in the communication path to the Management Client. This is specified in [06].
    Used Application Layer Services for Management
          •      A_Memory_Write
          •      A_Memory_Read

    Sequence
    Management                                                              Management                 remark
    Client                                                                  Server
    for each datablock (data size ≤ maximal size), until all data are transmitted
                                A_Memory_Write-PDU
                                 (Addr, Length, Data)

             if verify = enabled
                                   A_Memory_Read-PDU
                                      (Addr, Length)

                                A_Memory_Response-PDU                                    A_Disconnect.ind ⇒
                                  (Addr, Length, Data)                                   error,
                                                                                         different or no data received
                                                                                         ⇒ error
             else
                     delay for programming the memory in the device 12
             endif
    endfor

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
         -    If the Management Server does not support the L_Data_Extended frame format, then this
              maximal size shall be 12 octets.
         -    If the Management Server supports L_Data_Extended frames, then the maximal size shall be
              adapted in function of the capabilities of the Management Server and possible Couplers and
              Routers in the communication path to the Management Client. This is specified in [06].
    Used Application Layer Services for Management
        •     A_Memory_Write

    12) The delay time depends on the Management Server and on the amount of written octets (see [08]).

    Sequence
    Management                                                            Management                 remark
    Client                                                                Server
    if Verify Mode is not active
             if Property of device control is unknown to the Management Client
                          A_PropertyDescription_Read-PDU
                             (object_index = DeviceObject,
                          PID = PID_DEVICE_CONTROL)

                        A_PropertyDescription_Response-PDU                             A_Disconnect.ind ⇒ error,
                             (object_index = DeviceObject,                             Property does not exist ⇒
                     PID = PID_DEVICE_CONTROL, type = .. , ...)                        error

             endif
                               A_PropertyValue_Read-PDU
                              (object_index = DeviceObject,
                           PID = PID_DEVICE_CONTROL,
                        start_index = 01h, element_count = 01h)

                           A_PropertyValue_Response-PDU                                A_Disconnect.ind ⇒ error,
                             (object_index = DeviceObject,                             if no data received ⇒ error
                           PID = PID_DEVICE_CONTROL,
                        start_index = 01h, element_count = 01h,
                                     data = DDh, ..)

                              A_PropertyValue_Write-PDU                                In the data (DD) bit 2
                             (object_index = DeviceObject,                             (Verify Mode) has to be set.
                           PID = PID_DEVICE_CONTROL,
                        start_index = 01h, element_count = 01h,
                                     data = DDh, ..)

                           A_PropertyValue_Response-PDU                                A_Disconnect.ind ⇒ error,
                             (object_index = DeviceObject,                             if verify = enabled and
                           PID = PID_DEVICE_CONTROL,                                   different or no data received
                        start_index = 01h, element_count = 01,                         ⇒ error
                                     data = XX, ..)

    endif
    for each data block (data size ≤ maximal size), until all data are transmitted
                               A_Memory_Write-PDU
                                 (Addr, Length, Data)

                                  A_Memory_Response                                    A_Disconnect.ind ⇒
                                  (Addr, Length, Data)                                 error,
                                                                                       if verify = enabled and
                                                                                       different or no data received
                                                                                       ⇒ error
    endfor

    Exception handling
    The general exception handling shall apply.

    3.16.4 Procedure: DMP_MemWrite_LEmi1
    This Management Procedure shall use the local communication with EMI 1.
    Used EMI-services for Management
        •     PC_Get_Value
        •     PC_Set_Value

    Parameters of the Management Procedure
    DMP_MemWrite_LEmi1(/* [in] */ DmpStartAddr, /* [in]*/ DmpEndAddr, /* [in]*/ DmpData,
    /* [out] */ DmpError)
        DmpStartAddr:                          The start address in the memory of the device into which the Data
                                               shall be written.
        DmpEndAddr:                            The end address in the memory of the device into which the Data shall
                                               be written.
        DmpData:                               The Data to be written in the device.
        DmpError:                              Possible error indication.

    Service parameters
        SrvDataIn:                             The data that shall be written in the device in one call of the service
                                               PC_Set_Value.
        SrvDataOut:                            The data as read back from the device for each call of the service
                                               PC_Set_Value.
        SrvDBLen:                              The length of the datablock written in one call of the service
                                               PC_Set_Value. This shall be 12 octets for all datablocks except for the
                                               last one, which may be smaller.
        SrvDBAddr:                             The start address in the memory of the device where the current
                                               datablock shall be written.

    Sequence
    Management                                                              Management                 remark
    Client                                                                  Server
    for each datablock (≤12 octet), until all data are transmitted
                             PC_Set_Value.req message
                    (Length = SrvDBLen, Address = SrvDBAddr,
                                   Data = SrvDBIn)

             if verify = enabled
                               PC_Get_Value.req message
                      (Length = SrvDBLen, Address = SrvDBAddr)

                             PC_Get_Value.con message                                    If SrvDBOut differs from
                     (Length = SrvDBLen, Address = SrvDBAddr;                            SrvDBIn or if no data
                                  Data = SrvDBOut)                                       received ⇒ error

             else
                  delay for programming the memory in the device 13)
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


async def dm_mem_write(xknx: XKNX) -> None:
    """DM_MemWrite — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DM_MemWrite (KNX 03.05.02 §3.16) — implementation pending"
    )
