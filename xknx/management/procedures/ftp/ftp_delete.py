"""
FTP_Delete — KNX 03.05.02 §8.6 (PDF p. 198).

Spec text (verbatim from spec):

    Use
    This Management Procedure shall be used to delete a file on a File Server.

    Used Application Layer messages for management
    - A_FunctionPropertyCommand-PDU(destination_address, object_index, Property_id, data)
    - A_FunctionPropertyState_Response-PDU(destination_address, object_index, Property_id,
      return_code, data)
    - A_PropertyValue_Write-PDU(destination_address, object_index, Property_id, nr_of_elem,
      start_index, data)
    - A_PropertyValue_Response-PDU(destination_address, object_index, Property_id, nr_of_elem,
      start_index, data)

    Variables in FTP_Delete
        Server IA           Individual Address of the FTP Server
        File Server OI      Object Index of the File Server Object in the Management Server.
        Client IA           Individual Address of the FTP Client.
        File Path           The path to the file to be deleted from the File Server.
        File handle         File handle retrieved from the FTP server

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        loop until a valid file handle is received or no more File Server Objects are available.
            Note over C,S: get file handle from File Server Object
            C->>S: A_FunctionPropertyCommand-PDU (Server IA, File Server OI, PID_FILE_COMMAND, data = Get File handle)
            Note right of S: The File Server shall execute the command "Get File handle" and return the File handle.
            S->>C: A_FunctionPropertyState_Response-PDU (Client IA, File Server OI, PID_FILE_COMMAND, Return Code, Return Value)
            Note over C,S: If the Return Code is "Object busy", take the Return Value as Object Index of the next free File Server Object. If this object index is > 0, set File Server OI to this value and repeat, else report "Server Busy".
        end
        Note over C,S: if the Return Code is "Command Successful" File handle = Return Value write file path into File Server Object Property PID_FILE_PATh (this needs not to be done if the file path is transferred within the File Command).
        C->>S: DMP_InterfaceObject_Write_R (Server IA, File Server OI, PID_FILE_PATh)
        C->>S: A_FunctionPropertyCommand-PDU (Server IA, File Server OI, PID_FILE_COMMAND, data = Delete)
        S->>C: A_FunctionPropertyState_Response-PDU (Client IA, File Server OI, PID_FILE_COMMAND, Return Code)
        Note over C,S: if the Return Code is "Command Successful", the command was executed correctly else an error shall be reported. The File handle shall be released.
    ```

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def ftp_delete(xknx: XKNX) -> None:
    """FTP_Delete — see module docstring for the verbatim spec text."""
    raise NotImplementedError("FTP_Delete (KNX 03.05.02 §8.6) — implementation pending")
