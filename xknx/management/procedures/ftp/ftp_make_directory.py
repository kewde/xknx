"""
FTP_MakeDirectory — KNX 03.05.02 §8.8 (PDF p. 199).

Spec text (verbatim from spec):

    Use
    This Management Procedure shall be used to create a directory on a File Server.
    The procedure is identical to the procedure FTP_Delete in 8.6 except that the command “Make
    Directory” shall be used instead of the command “Delete”.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def ftp_make_directory(xknx: XKNX) -> None:
    """FTP_MakeDirectory — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "FTP_MakeDirectory (KNX 03.05.02 §8.8) — implementation pending"
    )
