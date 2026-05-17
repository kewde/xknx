"""
DM_InterfaceObjectScan — KNX 03.05.02 §3.28 (PDF p. 126).

Spec text (verbatim from spec):

    3.28.1 Use
    This device Management Procedure shall scan for the available the Interface Objects in one
    Management Server and return the description of each found Interface Object.
    A DM_Connect shall be executed before executing this Management Procedure.
    DM_InterfaceObjectScan (flags, dataBlockStartAddress, object_index, data)
    flags                      bit 0:    location of data
                                         0: in data block
                                         1: no data returned
                               bit 2:    scan all properties
                                         0: read only the type of the Interface Object
                                         1: scan all the properties of the Interface Object
                               bit 3:    scan Interface Objects
                                         0: read only the data of one object
                                         1: scan all Interface Objects
                               All other bits are reserved. These shall be set to 0. This shall be
                               tested by the Management Client.
    dataBlockStartAddress      specifies the address where the data are located in the data
                               block. If the data are located in the Management Procedure, this
                               field is set to 0.
    object_index               index of the Interface Object. If Interface Object scan is enabled
                               the value shall be 0.
    data                       the data that are read by this Management Procedure. The data
                               are stored in the data block.
    For each found Interface Object the following data is returned - the end of the list is marked by
    Interface Object nr. 0:
        - object_index
        - object_type
        - PropertyCount
    For each found Property the following data shall be returned:
        - PropertyIndex
        - PID
        - Data Type
        - Number of elements
        - Access rights / write enable

    3.28.2 Procedure: DMP_InterfaceObjectScan_R
    This Management Procedure shall use the connection oriented or connectionless communication
    mode.
    Used Application Layer Services for Management
    - A_PropertyDescription_Read
    - A_PropertyValue_Read

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        Note over C,S: object_index = 0;
        Note over C,S: repeat if Interface Object scan is enabled
        C->>S: A_PropertyDescription_Read-PDU (object_index, PID = 0, Property_index = 0)
        S->>C: A_PropertyDescription_Response-PDU (object_index, Property_index = 0, PID)
        opt Interface Object exists (Property ID <> 0)
            C->>S: A_PropertyValue_Read-PDU (object_index, PID = 01h, start_index = 01h, element_count = 01h)
            S->>C: A_PropertyValue_Response-PDU (object_index, PID = 01h, start_index = 01h, element_count = 01h, data = object_type)
            Note right of S: A_Disconnect.ind => error, no data received => error
        end
        Note over C,S: Property_index = 0;
        Note over C,S: repeat if Property scan is enabled
        C->>S: A_PropertyDescription_Read-PDU (object_index, PID = 0, Property_index = 0)
        S->>C: A_PropertyDescription_Response-PDU (object_index, Property_index = 0, PID)
        Note over C,S: Property_index ++
        Note over C,S: until PID = 0
        Note over C,S: object_index ++
        Note over C,S: until PID = 0
    ```

    3.28.3 Procedure: DMP_ReducedInterfaceObjectScan_R
    Use
    This Management Procedure shall scan the Interface Objects in a device with Reduced Interface
    Objects. Prior to this Management Procedure the Management Procedure DMP_Connect_RCl can be
    executed to identify the remote device.

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        Note over C,S: objectNr = 0;
        Note over C,S: repeat if Interface Object scan is enabled
        C->>S: A_PropertyValue_Read-PDU (object_index = objectNr, PID = 01h, start_index = 01h, element_count = 01h)
        Note right of S: PID 01h is the Object Type
        S->>C: A_PropertyValue_Response-PDU (object_index = objectNr, PID = 01h, start_index = 01h, element_count = 01h, data = object_type)
        Note right of S: A_Disconnect.ind => error, no data received => error
        Note over C,S: endif
        Note over C,S: objectNr ++
        Note over C,S: until PID = 0
    ```

    Exception handling
    The general exception handling shall apply.

    3.28.4 Procedure: DMP_ExtInterfaceObjectScan_R
    This Management Procedure shall use the connection oriented - or connectionless communication
    mode.
    Used Application Layer Services for Management
    - A_PropertyExtDescription_Read
    - A_PropertyExtValue_Read

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        opt Property of management control is unknown to the Management Client
            C->>S: A_PropertyExtDescription_Read-PDU (object_type = 0, object_instance = 1, PID = PID_IO_LIST, type = 0)
            S->>C: A_PropertyExtDescription_Response-PDU (object_type = 0, object_instance = 1, PID = PID_IO_LIST, type = 0, …)
            Note right of S: A_Disconnect.ind => error, Property does not exist => error
        end
        Note over C,S: io_list = new[]{}
        Note over C,S: for each data block, until all data are transmitted
        C->>S: A_PropertyExtValue_Read-PDU (object_type = 0, object_instance = 0, PID = PID_IO_LIST, start_index = SSSS, nr_of_elem = EE)
        S->>C: A_PropertyExtValue_Response-PDU (object_type = 0, object_instance = 0, PID = PID_IO_LIST, start_index = SSSS, nr_of_elem = EE, data = object_types)
        Note right of S: A_Disconnect.ind => error, no data received => error
        Note over C,S: io_list.Add(object_types)
        Note over C,S: endfor
        Note over C,S: Calculate Object Informations from io_list (object_index, object_type, object_instance)
        Note over C,S: foreach (object_index, object_type, object_instance) in io_list
        Note over C,S: Property_index = 0
        Note over C,S: repeat if Property scan is enabled
        C->>S: A_PropertyExtDescription_Read-PDU (object_type, object_instance, PID = 0, Property_index, type = 0)
        S->>C: A_PropertyExtDescription_Response-PDU (object_type, object_instance, PID, Property_index, type = 0, …)
        Note over C,S: Property_index ++
        Note over C,S: Until PID = 0
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


async def dm_interface_object_scan(xknx: XKNX) -> None:
    """DM_InterfaceObjectScan — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DM_InterfaceObjectScan (KNX 03.05.02 §3.28) — implementation pending"
    )
