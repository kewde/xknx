"""
DMP_PeiTypeRead_R_IO — KNX 03.05.02 §3.15.3 (PDF p. 98).

Spec text (verbatim from spec):

    This Management Procedure shall use the connection oriented or connectionless communication
    mode.
    The value shall be read via the Interface Objects.
    Used Application Layer Services for Management
        •     A_PropertyDescription_Read
        •     A_PropertyValue_Read

    Sequence
    Management                                                            Management                remark
    Client                                                                Server
    if Property of management control is unknown to the Management Client
                          A_PropertyDescription_Read-PDU
                (object_index = DeviceObject, PID = PID_PEI_TYPE)

                        A_PropertyDescription_Response-PDU                             A_Disconnect.ind ⇒ error,
                 (object_index = DeviceObject, PID = PID_PEI_TYPE,                     Property does not exist ⇒
                                     type = .. , ...)                                  error

    endif
                              A_PropertyValue_Read-PDU
                 (object_index = DeviceObject, PID = PID_PEI_TYPE,
                        start_index = 01H, element_count = 01h)

                           A_PropertyValue_Response-PDU                                A_Disconnect.ind ⇒ error,
                 (object_index = DeviceObject, PID = PID_PEI_TYPE,                     no data received ⇒ error
                        start_index = 01H, element_count = 01h,
                                    data = PEI-Type)

    endfor

    Exception handling
    The general exception handling shall apply.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dmp_pei_type_read_r_io(xknx: XKNX) -> None:
    """DMP_PeiTypeRead_R_IO — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_PeiTypeRead_R_IO (KNX 03.05.02 §3.15.3) — implementation pending"
    )
