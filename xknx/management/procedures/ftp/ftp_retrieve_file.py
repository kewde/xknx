"""
FTP_RetrieveFile — KNX 03.05.02 §8.2 (PDF p. 193).

Spec text (verbatim from spec):

    Use
    This Management Procedure shall be used to read a file in FTP (raw) mode from a File Server.
    Used Application Layer messages for management
    • A_FunctionPropertyCommand-PDU(destination_address, object_index, Property_id, data)
    • A_FunctionPropertyState_Response-PDU(destination_address, object_index, Property_id,
      return_code, data)
    • A_PropertyValue_Write-PDU(destination_address, object_index, Property_id, nr_of_elem,
      start_index, data)
    • A_PropertyValue_Response-PDU(destination_address, object_index, Property_id, nr_of_elem,
      start_index, data)
    • A_FileStream_InfoReport-PDU(destination_address, file_handle, file_block_sequence_number,
      file_block)

    Variables in FTP_RetrieveFile
          Server IA                       Individual Address of the FTP Server
          File Server OI                  Object Index of the File Server Object in the Management Server.
          Client IA                       Individual Address of the FTP Client.
          File Path                       The path to the file to be retrieved from the File Server.
          File handle                     File handle retrieved from the FTP server

    Sequence
    Management                                                                   Management                  remark
    Client                                                                       Server
    repeat
       get file handle from File Server Object
                             A_FunctionPropertyCommand-PDU                                       The File Server shall execute
                     (Server IA, File Server OI, PID_FILE_COMMAND,                               the command “Get File
                                    data = Get File handle)                                      handle” and return the File
                                                                                                 handle.
                          A_FunctionPropertyState_Response-PDU
                 (Client IA, File Server OI, PID_FILE_COMMAND, Return
                                     Code, Return Value)

         If the Return Code is “Object busy”, take the Return Value as Object Index of the
         next free File Server Object.
         If this object index is > 0, set File Server OI to this value and repeat, else report
         “Server Busy”.
    until a valid file handle is received or no more File Server Objects are available.
    if the Return Code is “Command Successful”
    File handle = Return Value
    write file path into File Server Object Property PID_FILE_PATh (this needs not to be
    done if the file path is transferred within the File Command).
                                   DMP_InterfaceObject_Write_R
                           (Server IA, File Server OI, PID_FILE_PATh)

                             A_FunctionPropertyCommand-PDU
                     (Server IA, File Server OI, PID_FILE_COMMAND,
                                      data = Retrieve File)

                          A_FunctionPropertyState_Response-PDU
                 (Client IA, File Server OI, PID_FILE_COMMAND, Return
                                             Code)

    if the Return Code is “Command Successful”, a file exists and will be transferred to the client
                                                                                                                    repeat
                                                            The Management Server (File Server) shall transmit the file
                                                                     in consecutive A_FileStream_InfoReport-PDUs.
                                                                       Each APDU shall have an APDU-length of 14
                                                                  or longer as given in PID_MAX_APDU_LENGTh.
                                                                           The last APDU may have a shorter length.
                             A_FileStream_InfoReport-PDU
                  (Client IA, file handle, file_block_sequence_number,
                                        file_block)

                                                                                          until the whole file is transmitted
                                                                                                             mark end of file
                                                                                      The field file_block is not present.
                             A_FileStream_InfoReport-PDU
                  (Client IA, file handle, file_block_sequence_number)

    else if the Return Code is an Error Code, report this error.
    The File handle shall be released.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def ftp_retrieve_file(xknx: XKNX) -> None:
    """FTP_RetrieveFile — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "FTP_RetrieveFile (KNX 03.05.02 §8.2) — implementation pending"
    )
