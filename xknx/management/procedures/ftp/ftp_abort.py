"""
FTP_Abort — KNX 03.05.02 §8.11 (PDF p. 201).

Spec text (verbatim from spec):

    Use
    This Management Procedure shall be used to stop any running transmission from a File Server. This is
    the only command that is sent without requesting a File handle. The valid File handle has been given
    to the client for the previous command (Retrieve File, List Directory or Get File) which has to be
    stopped by the Abort command.

    Used Application Layer messages for management
    - A_FunctionPropertyCommand-PDU(destination_address, object_index, Property_id, data)
    - A_FunctionPropertyState_Response-PDU(destination_address, object_index, Property_id,
      return_code)

    Variables in FTP_Abort
        Server IA           Individual Address of the FTP Server
        File Server OI      Object Index of the File Server Object in the Management Server.
        Client IA           Individual Address of the FTP Client.

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        C->>S: A_FunctionPropertyCommand-PDU (Server IA, File Server OI, PID_FILE_COMMAND, data = Abort)
        S->>C: A_FunctionPropertyState_Response-PDU (Client IA, File Server OI, PID_FILE_COMMAND, Return Code)
        Note over C,S: if the Return Code is "Command Successful", the command was executed correctly else an error shall be reported.
    ```

    8.12 hTTP_GetFile
    Use
    This Management Procedure shall be used to read a file in hTTP mode from a File Server.
    The procedure shall be identical to 8.2 "FTP_RetrieveFile".
    The Content-Type shall be returned with the Return Code "Command successful".

    8.13 hTTP_PostFile
    Use
    This Management Procedure shall be used to write a file in hTTP mode to a File Server.
    The procedure shall be identical to 8.3 "FTP_StoreFile".
    the specification of the S-A_Sync-service in [03]
    the requirements on the challenge in the specification of the S-A_Sync-service in [03]
    "Sequence Number for Tool Access" in [05]
    PID_SECURITY_INDIVIDUAL_ADDRESS_TABLE in [05]

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def ftp_abort(xknx: XKNX) -> None:
    """FTP_Abort — see module docstring for the verbatim spec text."""
    raise NotImplementedError("FTP_Abort (KNX 03.05.02 §8.11) — implementation pending")
