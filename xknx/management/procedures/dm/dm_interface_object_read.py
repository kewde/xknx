"""
DM_InterfaceObjectRead — KNX 03.05.02 §3.27 (PDF p. 122).

Spec text (verbatim from spec):

    3.27.1 Use
    This device Management Procedure shall read the Property value of an Interface Object and store it in
    the data block. The Interface Object can be addressed via the Object Type and Object Index (e.g. first
    Interface Object of type ´polling master´) or via the Object Index independent of the type.
    Remark
    Existing implementations of Interface Object Servers in existing Management Servers may have fixed
    Object Indexes for the Interface Objects for Device- and Network Management. This restriction shall
    not be implemented in new developments. New developments of Management Clients shall instead
    obtain the object_index by a preceding DM_InterfaceObject_Scan-procedure if the object_index is not
    known.
    A DM_Connect shall be executed before executing this Management Procedure.

    DM_InterfaceObjectRead                     (flags, dataBlockStartAddress, object_type, object_index, PID,
                                               start_index, noElements, data)
    flags                                      bit 0:        location of data
                                               0: in data block
                                               1: -
                                               bit 2:        address mode
                                               0: address via Object Type / index
                                               1: address via object index
                                               All other bits are reserved. These shall be set to 0. This shall be
                                               tested by the Management Client.
    dataBlockStartAddress                      specifies the address where the data are located in the data
                                               block. If the data are located in the Management Procedure, this
                                               field is set to 0.
    object_type                                type of the Interface Object
    object_index                               index of the Interface Object of one type. This index starts
                                               counting from 0.
    PID                                        ID of the Property
    start_index                                start element of the Property
    noElements                                 number of elements that are read
    data                                       the data that are read by this Management Procedure. The data
                                               are stored in the data block.

    3.27.2 Procedure: DMP_InterfaceObjectRead_R
    This Management Procedure shall use the connection oriented or connectionless communication
    mode.
    Used Application Layer Services for Management
           •   A_PropertyDescription_Read
           •   A_PropertyValue_Read

    Sequence
    Management                                                            Management                 remark
    Client                                                                Server
    if Property of management control is unknown to the Management Client
                        A_PropertyDescription_Read-PDU
                          (object_index = OO, PID = PP)

                       A_PropertyDescription_Response-PDU                               A_Disconnect.ind ⇒ error,
                     (object_index = OO, PID = PP, type = .. , ...)                     Property does not exist ⇒
                                                                                        error
    endif
    for each data block, until all data are transmitted
                            A_PropertyValue_Read-PDU
                 (object_index = OO, PID = PP, start_index = SSSS,
                                  element_count = EE)

                           A_PropertyValue_Response-PDU                                 A_Disconnect.ind ⇒ error,
                  (object_index = OO, PID = PP, start_index = SSSS,                     no data received ⇒ error
                                 element_count = EE,
                                    data = XX, ..)

    endfor

    Exception handling
    The general exception handling shall apply.
    The Management Client shall not interpret the value of the Property Index contained in the
    A_PropertyDescription_Response-PDU at the level of this Management Procedure. Possibly, error
    handling in case an unexpected value of the Property Index can be handled at the level of the
    Configuration Procedure in which this Management Procedure is used.

    3.27.3 Procedure: DMP_ReducedInterfaceObjectRead_R
    Prior to this procedure the procedure DMP_Connect_RCl can be executed to identify the remote
    device.
    Sequence
    Management                                                             Management                remark
    Client                                                                 Server

    for each data block, until all data is transmitted
                            A_PropertyValue_Read-PDU
                    (objectNr = OO, PID = PP, start_index = SSSS,
                                 element_count = EE)

                           A_PropertyValue_Response-PDU                                 A_Disconnect.ind ⇒ error,
                    (objectNr = OO, PID = PP, start_index = SSSS,                       no data received ⇒ error
                          element_count = EE, data = XX, ..)

    endfor

    3.27.4 Procedure: DMP_ExtInterfaceObjectRead_R
    This Management Procedure shall use the connection oriented - or connectionless communication
    mode.
    Used Application Layer Services for Management
        • A_PropertyExtDescription_Read
        • A_PropertyExtValue_Read
    Sequence
    Management                                                            Management
    Client                                                                Server
    If Property of management control is unknown to the Management Client
                       A_PropertyExtDescription_Read-PDU
                 (object_type = OT, object_instance = OI, PID = PP,
                                     type = 0)

                     A_PropertyExtDescription_Response-PDU                             A_Disconnect.ind ⇒ error,
                 (object_type = OT, object_instance = OI, PID = PP,                    Property does not exist ⇒
                                    type = 0, …)                                       error

    endif
    for each data block, until all data are transmitted
                           A_PropertyExtValue_Read-PDU
                 (object_type = OT, object_instance = OI, PID = PP,
                        start_index = SSSS, nr_of_elem = EE)

                         A_PropertyExtValue_Response-PDU                               A_Disconnect.ind ⇒ no
                  (object_type = OT, object_instance = OI, PID = PP,                   data received ⇒ error
                 start_index = SSSS, nr_of_elem = EE, data = XX,…)

    endfor

    Exception handling
    The general exception handling shall apply.
    The MaC shall not interpret the value of the Property Index contained in the A_Property_-
    Description_Response-PDU at the level of this Management Procedure. Possibly, error handling in
    case an unexpected value of the Property Index can be handled at the level of the Configuration
    Procedure in which this Management Procedure is used.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dm_interface_object_read(xknx: XKNX) -> None:
    """DM_InterfaceObjectRead — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DM_InterfaceObjectRead (KNX 03.05.02 §3.27) — implementation pending"
    )
