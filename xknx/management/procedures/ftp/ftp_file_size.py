"""
FTP_FileSize — KNX 03.05.02 §8.9 (PDF p. 200).

Spec text (verbatim from spec):

    Use
    This Management Procedure shall be used to read the size of a specified file.
    The procedure is identical to the procedure FTP_Delete in 8.6 except that the command “Get File
    Size” shall be used instead of the command “Delete”.
    The File Size shall be returned with the Return Code “Command successful”.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def ftp_file_size(xknx: XKNX) -> None:
    """FTP_FileSize — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "FTP_FileSize (KNX 03.05.02 §8.9) — implementation pending"
    )
