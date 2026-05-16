"""
DMP_InterfaceObjectWrite_R — KNX 03.05.02 §3.25.2 (PDF p. 116).

Spec text (verbatim from spec):

    This Management Procedure shall use the connection oriented or connectionless communication
    mode.

    Used Application Layer Services for Management
        •     A_PropertyDescription_Read
        •     A_PropertyValue_Write

    Sequence
    Management                                                            Management                 remark
    Client                                                                Server
    if Property of management control is unknown to the Management Client
                        A_PropertyDescription_Read-PDU
                         (object_index = OO, PID = PH)

                       A_PropertyDescription_Response-PDU                              A_Disconnect.ind ⇒ error,
                     (object_index = OO, PID = PP, type = .. , ...)                    Property does not exist ⇒
                                                                                       error
    endif
    for each data block, until all data are transmitted
                            A_PropertyValue_Write-PDU
                 (object_index = OO, PID = PP, start_index = SSSS,
                                  element_count = EE,
                                      data = DD, ..)

                           A_PropertyValue_Response-PDU                                A_Disconnect.ind ⇒ error,
                 (object_index = OOH, PID = PP, start_index = SSSS,                    if verify = enabled and
                                 element_count = EE,                                   different or no data received
                                    data = XX, ..)                                     ⇒ error

    endfor

    Exception handling
    The general exception handling shall apply.
    The Management Client shall not interpret the value of the Property Index contained in the
    A_PropertyDescription_Response-PDU at the level of this Management Procedure. Possibly, error
    handling in case an unexpected value of the Property Index can be handled at the level of the
    Configuration Procedure in which this Management Procedure is used.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dmp_interface_object_write_r(xknx: XKNX) -> None:
    """DMP_InterfaceObjectWrite_R — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_InterfaceObjectWrite_R (KNX 03.05.02 §3.25.2) — implementation pending"
    )
