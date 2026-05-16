"""
DM_UserMemWrite — KNX 03.05.02 §3.19 (PDF p. 108).

Spec text (verbatim from spec):

    3.19.1 Use
    This device Management Procedure shall write a contiguous block of data to the specified memory
    addresses of the user memory in the Management Server. The data shall be located either in the
    management control or in the data block. Only the data that are specified in the data block shall be
    written. Depending on the flag the data shall be verified immediately. If the deviceStartAddress if
    higher than the deviceEndAddress this Management Procedure shall be skipped.
    A DM_Connect shall be executed before executing this Management Procedure.
    DM_UserMemWrite                             (flags, dataBlockStartAddress, deviceStartAddress,
                                                deviceEndAddress, data)
            flags                       bit 0     location of data
                                                    0: in data block
                                                    1: in Management Procedure
                                        bit 1 verify enabled / disabled
                                                    0: disabled
                                                    1: enabled
                                        All other bits are reserved. These shall be set to 0. This shall be
                                        tested by the Management Client.
            dataBlockStartAddress       specifies the address where the data are located in the data block.
                                        If the data are located in the Management Procedure, this field is
                                        set to 0.
            deviceStartAddress          address of first user memory octet that is written by this
                                        Management Procedure
            deviceEndAddress            address of the last user memory octet that is written by this
                                        Management Procedure
            data                        the data that are transferred by this Management Procedure. The
                                        data can be located in the data block or in the Management
                                        Procedure.

    3.19.2 Procedure: DMP_UserMemWrite_RCo
    This Management Procedure shall use the connection oriented communication mode.
    The Verify Mode of the Management Server shall not be used.
    Preconditions
    This Management Procedure shall transfer the data in datablocks and transmit these in subsequent
    A_Memory_Read-PDUs and/or A_Memory_Write-PDUs, as specified below, all of which except
    possibly the last PDU, shall have a data field (ASDU) with a size equal to the maximum size that can
    be transported over the communication path consisting of the Management Client, the Management
    Server and Couplers and Routers in between these two.
         -    If the Management Server does not support the L_Data_Extended frame format, then this
              maximal size shall be 11 octets.
         -    If the Management Server supports L_Data_Extended frames, then the maximal size shall be
              adapted in function of the capabilities of the Management Server and possible Couplers and
              Routers in the communication path to the Management Client. This is specified in [06].
    Used Application Layer Services for Management
        •      A_UserMemory_Write
        •      A_UserMemory_Read

    Sequence
    Management                                                            Management                 remark
    Client                                                                Server
    for each data block (data size ≤ maximal size), until all data are transmitted
                            A_UserMemory_Write-PDU
                                 (Addr, Length, Data)

             if verify = enabled
                              A_UserMemory_Read-PDU
                                   (Addr, Length)

                            A_UserMemory_Response-PDU                                  A_Disconnect.ind ⇒ error,
                                (Addr, Length, Data)                                   if verify = enabled and
                                                                                       different or no data received
                                                                                       ⇒ error
             else
                delay for programming the memory in the device 14)
             endif
    endfor

    Exception handling
    The general exception handling shall apply.

    3.19.3 Procedure: DMP_UserMemWrite_RCoV
    This Management Procedure shall use the connection oriented communication mode.
    The Verify Mode of the Management Server shall be used.
    Preconditions
    This Management Procedure shall transfer the data in datablocks and transmit these in subsequent
    A_UserMemory_Read-PDUs and/or A_UserMemory_Write-PDUs, as specified below, all of which
    except possibly the last PDU, shall have a data field (ASDU) with a size equal to the maximum size
    that can be transported over the communication path consisting of the Management Client, the
    Management Server and Couplers and Routers in between these two.
         -    If the Management Server does not support the L_Data_Extended frame format, then this
              maximal size shall be 11 octets.
         -    If the Management Server supports L_Data_Extended frames, then the maximal size shall be
              adapted in function of the capabilities of the Management Server and possible Couplers and
              Routers in the communication path to the Management Client. This is specified in [06].
    Used Application Layer Services for Management
        •     A_UserMemory_Write

    14) The delay time depends on the Management Server and on the amount of written octets (see [08]).

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
                 PID = PID_DEVICE_CONTROL, start_index = 01h,
                               element_count = 01h)

                          A_PropertyValue_Response-PDU                                 A_Disconnect.ind ⇒ error,
                            (object_index = DeviceObject,                              if no data received ⇒ error
                 PID = PID_DEVICE_CONTROL, start_index = 01h,
                         element_count = 01h, data = DD, ..)

                            A_PropertyValue_Write-PDU                                  In the data (DD) bit 2 (Verify
                            (object_index = DeviceObject,                              Mode) has to be set.
                 PID = PID_DEVICE_CONTROL, start_index = 01h,
                         element_count = 01h, data = DD, ..)

                          A_PropertyValue_Response-PDU                                 A_Disconnect.ind ⇒ error,
                            (object_index = DeviceObject,                              if verify = enabled and
                 PID = PID_DEVICE_CONTROL, start_index = 01h,                          different or no data received
                         element_count = 01h, data = XX, ..)                           ⇒ error

    endif
    for each data block (data size ≤ maximal size), until all data are transmitted
                            A_UserMemory_Write-PDU
                                 (Addr, Length, Data)

                            A_UserMemory_Response-PDU                                  A_Disconnect.ind ⇒ error,
                                (Addr, Length, Data)                                   if verify = enabled and
                                                                                       different or no data received
                                                                                       ⇒ error
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


async def dm_user_mem_write(xknx: XKNX) -> None:
    """DM_UserMemWrite — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DM_UserMemWrite (KNX 03.05.02 §3.19) — implementation pending"
    )
