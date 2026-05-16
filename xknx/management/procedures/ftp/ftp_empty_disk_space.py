"""
FTP_EmptyDiskSpace — KNX 03.05.02 §8.10 (PDF p. 200).

Spec text (verbatim from spec):

    Use
    This Management Procedure shall be used to read the size of the available free disk or memory space
    of the File Server.
    Used Application Layer messages for management
    • A_FunctionPropertyCommand-PDU(destination_address, object_index, Property_id, data)
    • A_FunctionPropertyState_Response-PDU(destination_address, object_index, Property_id,
      return_code, data)

    Variables in FTP_EmptyDiskSpace
          Server IA                          Individual Address of the FTP Server
          File Server OI                     Object Index of the File Server Object in the Management Server.
          Client IA                          Individual Address of the FTP Client.
          File handle                        File handle retrieved from the FTP server

    Sequence
    Management                                                                    Management                 remark
    Client                                                                        Server
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

                             A_FunctionPropertyCommand-PDU
                     (Server IA, File Server OI, PID_FILE_COMMAND,
                                data = Get Empty Disk Space)

                           A_FunctionPropertyState_Response-PDU
                  (Client IA, File Server OI, PID_FILE_COMMAND, Return
                                      Code, Return Value)

    Management                                                            Management              remark
    Client                                                                Server
    if the Return Code is “Command Successful”, the command was executed correctly
    else an error shall be reported.
    The File handle shall be released.

    The Empty Disk Space is returned with the Return Code “Command successful”.

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
