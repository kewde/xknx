"""
DMP_ExtInterfaceObjectScan_R — KNX 03.05.02 §3.28.4 (PDF p. 128).

Spec text (verbatim from spec):

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
            Note right of S: A_Disconnect.ind ⇒ error, Property does not exist ⇒ error
        end
        Note over C,S: io_list = new[]{}
        loop for each data block, until all data are transmitted
            C->>S: A_PropertyExtValue_Read-PDU (object_type = 0, object_instance = 0, PID = PID_IO_LIST, start_index = SSSS, nr_of_elem = EE)
            S->>C: A_PropertyExtValue_Response-PDU (object_type = 0, object_instance = 0, PID = PID_IO_LIST, start_index = SSSS, nr_of_elem = EE, data = object_types)
            Note right of S: A_Disconnect.ind ⇒ error, no data received ⇒ error
            Note over C,S: io_list.Add(object_types)
        end
        Note over C,S: Calculate Object Informations from io_list (object_index, object_type, object_instance)
        loop foreach (object_index, object_type, object_instance) in io_list
            Note over C,S: Property_index = 0
            loop repeat if Property scan is enabled
                C->>S: A_PropertyExtDescription_Read-PDU (object_type, object_instance, PID = 0, Property_index, type = 0)
                S->>C: A_PropertyExtDescription_Response-PDU (object_type, object_instance, PID, Property_index, type = 0, …)
                Note over C,S: Property_index ++
                Note over C,S: Until PID = 0
            end
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


async def dmp_ext_interface_object_scan_r(xknx: XKNX) -> None:
    """DMP_ExtInterfaceObjectScan_R — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_ExtInterfaceObjectScan_R (KNX 03.05.02 §3.28.4) — implementation pending"
    )
