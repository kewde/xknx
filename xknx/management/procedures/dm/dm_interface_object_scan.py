"""
DM_InterfaceObjectScan — KNX 03.05.02 §3.28 (PDF p. 126).

Spec text (verbatim from spec):

    3.28.1 Use
    This device Management Procedure shall scan for the available the Interface Objects in one
    Management Server and return the description of each found Interface Object.
    A DM_Connect shall be executed before executing this Management Procedure.
    DM_InterfaceObjectScan                     (flags, dataBlockStartAddress, object_index, data)
    flags                                      bit 0:        location of data
                                               0: in data block
                                               1: no data returned
                                               bit 2:        scan all properties
                                               0: read only the type of the Interface Object
                                               1: scan all the properties of the Interface Object
                                               bit 3:        scan Interface Objects
                                               0: read only the data of one object
                                               1: scan all Interface Objects
                                               All other bits are reserved. These shall be set to 0. This shall be
                                               tested by the Management Client.
    dataBlockStartAddress                      specifies the address where the data are located in the data
                                               block. If the data are located in the Management Procedure, this
                                               field is set to 0.
    object_index                               index of the Interface Object. If Interface Object scan is enabled
                                               the value shall be 0.
    data                                       the data that are read by this Management Procedure. The data
                                               are stored in the data block.
    For each found Interface Object the following data is returned - the end of the list is marked by
    Interface Object nr. 0:
         -    object_index
         -    object_type
         -    PropertyCount
    For each found Property the following data shall be returned:
         -   PropertyIndex
         -   PID
         -   Data Type
         -   Number of elements
         -   Access rights / write enable

    3.28.2 Procedure: DMP_InterfaceObjectScan_R
    This Management Procedure shall use the connection oriented or connectionless communication
    mode.
    Used Application Layer Services for Management
           •   A_PropertyDescription_Read
           •   A_PropertyValue_Read

    Sequence
    Management                                                            Management                remark
    Client                                                                Server
    object_index = 0;
    repeat if Interface Object scan is enabled
                          A_PropertyDescription_Read-PDU
                      (object_index, PID = 0, Property_index = 0)

                        A_PropertyDescription_Response-PDU
                        (object_index, Property_index = 0, PID)

                     if Interface Object exists (Property ID <> 0)
                              A_PropertyValue_Read-PDU
                     (object_index, PID = 01h, start_index = 01h,
                                 element_count = 01h)

                          A_PropertyValue_Response-PDU                                 A_Disconnect.ind ⇒ error,
                     (object_index, PID = 01h, start_index = 01h,                      no data received ⇒ error
                       element_count = 01h, data = object_type)

                     endif
    Property_index = 0;
            repeat if Property scan is enabled
                         A_PropertyDescription_Read-PDU
                     (object_index, PID = 0, Property_index = 0)

                        A_PropertyDescription_Response-PDU
                        (object_index, Property_index = 0, PID)

    Property_index ++
            until PID = 0
    object_index ++
    until PID = 0

    3.28.3 Procedure: DMP_ReducedInterfaceObjectScan_R
    Use
    This Management Procedure shall scan the Interface Objects in a device with Reduced Interface
    Objects. Prior to this Management Procedure the Management Procedure DMP_Connect_RCl can be
    executed to identify the remote device.
    Sequence
    Management                                                             Management                 remark
    Client                                                                 Server
    objectNr = 0;
    repeat if Interface Object scan is enabled
                              A_PropertyValue_Read-PDU                                  PID 01h is the Object Type
                          (object_index = objectNr, PID = 01h,
                        start_index = 01h, element_count = 01h)

                            A_PropertyValue_Response-PDU                                A_Disconnect.ind ⇒ error,
                 (object_index = objectNr, PID = 01h, start_index = 01h,                no data received ⇒ error
                        element_count = 01h, data = object_type)

                      endif
    objectNr ++
    until PID = 0

    Exception handling
    The general exception handling shall apply.

    3.28.4 Procedure: DMP_ExtInterfaceObjectScan_R
    This Management Procedure shall use the connection oriented - or connectionless communication
    mode.
    Used Application Layer Services for Management
          •      A_PropertyExtDescription_Read
          •      A_PropertyExtValue_Read
    Sequence
    Management                                                            Management
    Client                                                                Server
    If Property of management control is unknown to the Management Client
                        A_PropertyExtDescription_Read-PDU
                      (object_type = 0, object_instance = 1, PID =
                                PID_IO_LIST, type = 0)

                       A_PropertyExtDescription_Response-PDU                             A_Disconnect.ind ⇒ error,
                      (object_type = 0, object_instance = 1, PID =                       Property does not exist ⇒
                              PID_IO_LIST, type = 0, …)                                  error

    endif

    Management                                                              Management
    Client                                                                  Server
    io_list = new[]{}
    for each data block, until all data are transmitted
                          A_PropertyExtValue_Read-PDU
                     (object_type = 0, object_instance = 0, PID =
                 PID_IO_LIST, start_index = SSSS, nr_of_elem = EE)

                        A_PropertyExtValue_Response-PDU                                  A_Disconnect.ind ⇒ error,
                     (object_type = 0, object_instance = 0, PID =                        no data received ⇒ error
                 PID_IO_LIST, start_index = SSSS, nr_of_elem = EE,
                                 data = object_types)

            io_list.Add(object_types)
    endfor
    Calculate Object Informations from io_list (object_index, object_type, object_instance)
    foreach (object_index, object_type, object_instance) in io_list
            Property_index = 0
            repeat if Property scan is enabled
                        A_PropertyExtDescription_Read-PDU
                        (object_type, object_instance, PID = 0,
                               Property_index, type = 0)

                      A_PropertyExtDescription_Response-PDU
                  (object_type, object_instance, PID, Property_index,
                                      type = 0, …)

                      Property_index ++
             Until PID = 0
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


async def dm_interface_object_scan(xknx: XKNX) -> None:
    """DM_InterfaceObjectScan — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DM_InterfaceObjectScan (KNX 03.05.02 §3.28) — implementation pending"
    )
