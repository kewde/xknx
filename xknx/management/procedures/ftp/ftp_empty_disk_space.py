"""
FTP_EmptyDiskSpace — KNX 03.05.02 §8.10 (PDF p. 200).

Spec text (verbatim from spec):

    Use
    This Management Procedure shall be used to read the size of the available free disk or memory space
    of the File Server.

    Used Application Layer messages for management
    - A_FunctionPropertyCommand-PDU(destination_address, object_index, Property_id, data)
    - A_FunctionPropertyState_Response-PDU(destination_address, object_index, Property_id,
      return_code, data)

    Variables in FTP_EmptyDiskSpace
        Server IA           Individual Address of the FTP Server
        File Server OI      Object Index of the File Server Object in the Management Server.
        Client IA           Individual Address of the FTP Client.
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
        Note over C,S: if the Return Code is "Command Successful" File handle = Return Value
        C->>S: A_FunctionPropertyCommand-PDU (Server IA, File Server OI, PID_FILE_COMMAND, data = Get Empty Disk Space)
        S->>C: A_FunctionPropertyState_Response-PDU (Client IA, File Server OI, PID_FILE_COMMAND, Return Code, Return Value)
        Note over C,S: if the Return Code is "Command Successful", the command was executed correctly else an error shall be reported. The File handle shall be released.
    ```

    The Empty Disk Space is returned with the Return Code "Command successful".

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def ftp_empty_disk_space(xknx: XKNX) -> None:
    """FTP_EmptyDiskSpace — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "FTP_EmptyDiskSpace (KNX 03.05.02 §8.10) — implementation pending"
    )
