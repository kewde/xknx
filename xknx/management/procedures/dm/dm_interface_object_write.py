"""
DM_InterfaceObjectWrite — KNX 03.05.02 §3.25 (PDF p. 116).

Spec text (verbatim from spec):

    3.25.1 Use
    This device Management Procedure shall write to the specified Property value of an Interface Object.
    The data shall be located either in the management control or in the data block. Depending on the flag
    the data shall be verified immediately. The Interface Object can be addressed via the Object Type and
    index (e.g. first Interface Object of type ´polling master´) or via the Object Index independent of the
    type.
    Remark
    Existing implementations of Interface Object Servers in existing Management Servers may have fixed
    Object Indexes for the Interface Objects for Device- and Network Management. This restriction shall
    not be implemented in new developments. New developments of Management Clients shall instead
    obtain the object_index by a preceding DM_InterfaceObjectScan-procedure if the object_index is not
    known.
    A DM_Connect shall be executed before executing this Management Procedure.
    DM_InterfaceObjectWrite (flags, dataBlockStartAddress, object_type, object_index, PID,
                             start_index, noElements, data)
    flags                      bit 0:    location of data
                                         0: in data block
                                         1: in management control
                               bit 1:    verify enabled / disabled
                                         0: disabled
                                         1: enabled
                               bit 2:    address mode
                                         0: address via Object Type / index
                                         1: address via object index
                               All other bits are reserved. These shall be set to 0. This shall be
                               tested by the Management Client.
    dataBlockStartAddress      specifies the address where the data are located in the data
                               block. If the data are located in the Management Procedure, this
                               field is set to 0.
    object_type                type of the Interface Object
    object_index               index of the Interface Object of one type. This index starts
                               counting from 0.
    PID                        ID of the Property
    start_index                start element of the Property
    noElements                 number of elements that are transferred
    data                       the data that are transferred by this Management Procedure. The
                               data can be located in the data block or in the Management
                               Procedure.

    3.25.2 Procedure: DMP_InterfaceObjectWrite_R
    This Management Procedure shall use the connection oriented or connectionless communication
    mode.

    Used Application Layer Services for Management
    - A_PropertyDescription_Read
    - A_PropertyValue_Write

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        opt Property of management control is unknown to the Management Client
            C->>S: A_PropertyDescription_Read-PDU (object_index = OO, PID = PH)
            S->>C: A_PropertyDescription_Response-PDU (object_index = OO, PID = PP, type = .. , ...)
            Note right of S: A_Disconnect.ind => error, Property does not exist => error
        end
        Note over C,S: for each data block, until all data are transmitted
        C->>S: A_PropertyValue_Write-PDU (object_index = OO, PID = PP, start_index = SSSS, element_count = EE, data = DD, ..)
        S->>C: A_PropertyValue_Response-PDU (object_index = OOH, PID = PP, start_index = SSSS, element_count = EE, data = XX, ..)
        Note right of S: A_Disconnect.ind => error, if verify = enabled and different or no data received => error
        Note over C,S: endfor
    ```

    Exception handling
    The general exception handling shall apply.
    The Management Client shall not interpret the value of the Property Index contained in the
    A_PropertyDescription_Response-PDU at the level of this Management Procedure. Possibly, error
    handling in case an unexpected value of the Property Index can be handled at the level of the
    Configuration Procedure in which this Management Procedure is used.

    3.25.3 Procedure: DMP_ReducedInterfaceObjectWrite_R
    Prior to this procedure the procedure DMP_Connect_RCl can be executed to identify the remote
    device.

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        Note over C,S: for each data block, until all data is transmitted
        C->>S: A_PropertyValue_Write-PDU (objectNr = OO, PID = PP, start_index = SSSS, element_count = EE, data = DD, ..)
        S->>C: A_PropertyValue_Reponse-PDU (objectNr = 00, PID = PP, start_index = SSSS, element_count = EE, data = XX, …)
        Note right of S: A_Disconnect.ind => error, if verify = enabled and different or no data received => error
        Note over C,S: endfor
    ```

    3.25.4 Procedure: DMP_ExtInterfaceObjectWriteCon_R
    This Management Procedure shall use the connection oriented or connectionless communication
    mode.
    Used Application Layer Services for Management
    - A_PropertyExtDescription_Read
    - A_PropertyExtValue_WriteCon

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        opt Property of management control is unknown to the Management Client
            C->>S: A_PropertyExtDescription_Read-PDU (object_type = OT, object_instance = OI, PID = PP, type = 0)
            S->>C: A_PropertyExtDescription_Response-PDU (object_type = OT, object_instance = OI, PID = PP, type = 0, …)
            Note right of S: A_Disconnect.ind => error, Property does not exist => error
        end
        Note over C,S: for each data block, until all data are transmitted
        C->>S: A_PropertyExtValue_WriteCon-PDU (object_type = OT, object_instance = OI, PID = PP, start_index = SSSS, nr_of_elem = EE, data = DD,…)
        S->>C: A_PropertyExtValue_WriteConRes-PDU (object_type = OT, object_instance = OI, PID = PP, start_index = SSSS, nr_of_elem = EE, return_code = RR)
        Note right of S: A_Disconnect.ind => error, RR ≠ 0 => error
        Note over C,S: endfor
    ```

    Exception handling
    The general exception handling shall apply.
    The MaC shall not interpret the value of the Property Index contained in the A_Property_-
    Description_Response-PDU at the level of this Management Procedure. Possibly, error handling in
    case an unexpected value of the Property Index can be handled at the level of the Configuration
    Procedure in which this Management Procedure is used.

    3.25.5 Procedure: DMP_ExtInterfaceObjectWriteUnCon_R
    This Management Procedure shall use the connection oriented - or connectionless communication
    mode.
    Used Application Layer Services for Management
    - A_PropertyExtDescription_Read
    - A_PropertyExtValue_WriteUnCon

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        opt Property of management control is unknown to the Management Client
            C->>S: A_PropertyExtDescription_Read-PDU (object_type = OT, object_instance = OI, PID = PP, type = 0)
            Note right of S: A_Disconnect.ind => error, Property does not exist => error
            S->>C: A_PropertyExtDescription_Response-PDU (object_type = OT, object_instance = OI, PID = PP, type = 0, …)
            Note right of S: A_Disconnect.ind => error, Property does not exist => error
        end
        Note over C,S: for each data block, until all data are transmitted
        C->>S: A_PropertyExtValue_WriteUnCon-PDU (object_type = OT, object_instance = OI, PID = PP, start_index = SSSS, nr_of_elem = EE, data = DD,…)
        Note right of S: A_Disconnect.ind => error
        Note over C,S: endfor
    ```

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

from xknx.management.procedures.dmp.dmp_interface_object_write_r import (
    dmp_interface_object_write_r,
)

__all__ = ["dmp_interface_object_write_r"]
