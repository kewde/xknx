"""
DMP_InterfaceObjectScan_R — KNX 03.05.02 §3.28.2 (PDF p. 126).

Spec text (verbatim from spec):

    This Management Procedure shall use the connection oriented or connectionless communication
    mode.
    Used Application Layer Services for Management
           •   A_PropertyDescription_Read
           •   A_PropertyValue_Read

    Sequence
    Management                                                            Management                remark
    Client                                                                Server
    object_index = 0;
    repeat if Interface Object scan is enabled
                          A_PropertyDescription_Read-PDU
                      (object_index, PID = 0, Property_index = 0)

                        A_PropertyDescription_Response-PDU
                        (object_index, Property_index = 0, PID)

                     if Interface Object exists (Property ID <> 0)
                              A_PropertyValue_Read-PDU
                     (object_index, PID = 01h, start_index = 01h,
                                 element_count = 01h)

                          A_PropertyValue_Response-PDU                                 A_Disconnect.ind ⇒ error,
                     (object_index, PID = 01h, start_index = 01h,                      no data received ⇒ error
                       element_count = 01h, data = object_type)

                     endif
    Property_index = 0;
            repeat if Property scan is enabled
                         A_PropertyDescription_Read-PDU
                     (object_index, PID = 0, Property_index = 0)

                        A_PropertyDescription_Response-PDU
                        (object_index, Property_index = 0, PID)

    Property_index ++
            until PID = 0
    object_index ++
    until PID = 0

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dmp_interface_object_scan_r(xknx: XKNX) -> None:
    """DMP_InterfaceObjectScan_R — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_InterfaceObjectScan_R (KNX 03.05.02 §3.28.2) — implementation pending"
    )
