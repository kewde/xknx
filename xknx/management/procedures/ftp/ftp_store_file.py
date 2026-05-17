"""
FTP_StoreFile — KNX 03.05.02 §8.3 (PDF p. 195).

Spec text (verbatim from spec):

    Use
    This Management Procedure shall be used to write a file in FTP (raw) mode to a File Server.

    Used Application Layer messages for management
    - A_FunctionPropertyCommand-PDU(destination_address, object_index, Property_id, data)
    - A_FunctionPropertyState_Response-PDU(destination_address, object_index, Property_id,
      return_code, data)
    - A_PropertyValue_Write-PDU(destination_address, object_index, Property_id, nr_of_elem,
      start_index, data)
    - A_PropertyValue_Response-PDU(destination_address, object_index, Property_id, nr_of_elem,
      start_index, data)
    - A_FileStream_InfoReport-PDU(destination_address, file_handle, file_block_sequence_number,
      file_block)

    Variables in FTP_StoreFile
        Server IA           Individual Address of the FTP Server
        File Server OI      Object Index of the File Server Object in the Management Server.
        Client IA           Individual Address of the FTP Client.
        File Path           The path to the file to be stored in the File Server.
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
        C->>S: A_FunctionPropertyCommand-PDU (Server IA, File Server OI, PID_FILE_COMMAND, data = Store File)
        S->>C: A_FunctionPropertyState_Response-PDU (Client IA, File Server OI, PID_FILE_COMMAND, Return Code)
        alt the Return Code is "Command Successful", the server is ready to accept a file
            loop until the whole file is transmitted
                Note left of C: The Management Client (File Client) shall transmit the file in consecutive A_FileStream_InfoReport-PDUs. Each APDU shall have an APDU-length of 14 or longer as given in PID_MAX_APDU_LENGTh. The last APDU may have a shorter length.
                C->>S: A_FileStream_InfoReport-PDU (Server IA, file handle, file_block_sequence_number, file_block)
            end
            Note left of C: mark end of file. The field file_block is not present.
            C->>S: A_FileStream_InfoReport-PDU (Server IA, file handle, file_block_sequence_number)
        else if the Return Code is an Error Code, report this error.
        end
        Note over C,S: The File handle shall be released.
    ```

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def ftp_store_file(xknx: XKNX) -> None:
    """FTP_StoreFile — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "FTP_StoreFile (KNX 03.05.02 §8.3) — implementation pending"
    )
