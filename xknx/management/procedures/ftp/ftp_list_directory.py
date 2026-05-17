"""
FTP_ListDirectory — KNX 03.05.02 §8.4 (PDF p. 196).

Spec text (verbatim from spec):

    Use
    This Management Procedure shall be used to read a directory listing from a File Server.
    The procedure shall be identical to 8.2 "FTP_RetrieveFile".
    Every line of the directory listing shall start with a new A_FileStream_InfoReport-PDU. The number
    of octets transferred in a A_FileStream_InfoReport-PDU shall be either 14 or as specified in
    PID_MAX_APDU_LENGTh_OUT. It is although allowed that less octets than the maximum number
    are transferred. This makes it possible to start every directory line with a new
    A_FileStream_InfoReport-PDU.

    8.5      FTP_Rename (consisting of Rename From and Rename To)
    Use
    This Management Procedure shall be used to rename a file on a File Server. The procedure consists of
    a sequence of the commands Rename From and Rename To. The File handle requested from the File
    Server for the Rename From command shall also be used for the Rename To command i.e. no extra
    File handle is requested for the Rename To command. The File handle shall therefore not be released
    after the execution of the Rename From command. It shall be released after the execution of the
    Rename To command (or after the time-out of 6 s, if one or both commands are missing).
    This is to prevent the execution of a command other than Rename To after a Rename From coming
    from another File Client.

    Used Application Layer messages for management
    - A_FunctionPropertyCommand-PDU(destination_address, object_index, Property_id, data)
    - A_FunctionPropertyState_Response-PDU(destination_address, object_index, Property_id,
      return_code, data)
    - A_PropertyValue_Write-PDU(destination_address, object_index, Property_id, nr_of_elem,
      start_index, data)
    - A_PropertyValue_Response-PDU(destination_address, object_index, Property_id, nr_of_elem,
      start_index, data)

    Variables in FTP_Rename
        Server IA           Individual Address of the FTP Server
        File Server OI      Object Index of the File Server Object in the Management Server.
        Client IA           Individual Address of the FTP Client.
        File Path           The path to the file to be renamed from the File Server.
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
        Note right of S: Old File Path
        C->>S: A_FunctionPropertyCommand-PDU (Server IA, File Server OI, PID_FILE_COMMAND, data = Rename From)
        Note right of S: Rename From command
        S->>C: A_FunctionPropertyState_Response-PDU (Client IA, File Server OI, PID_FILE_COMMAND, Return Code)
        Note over C,S: if the Return Code is "Command Successful", the command Rename To shall be executed else an error shall be reported.
        Note over C,S: write file path into File Server Object Property PID_FILE_PATh (this needs not to be done if the file path is transferred within the File Command).
        C->>S: DMP_InterfaceObject_Write_R (Server IA, File Server OI, PID_FILE_PATh)
        Note right of S: New File Path
        C->>S: A_FunctionPropertyCommand-PDU (Server IA, File Server OI, PID_FILE_COMMAND, data = Rename To)
        Note right of S: Rename To command
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


async def ftp_list_directory(xknx: XKNX) -> None:
    """FTP_ListDirectory — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "FTP_ListDirectory (KNX 03.05.02 §8.4) — implementation pending"
    )
