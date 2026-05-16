"""
DM_Identify_R — KNX 03.05.02 §3.4.2 (PDF p. 72).

Spec text (verbatim from spec):

    Use
    This Device Management Procedure shall be used to identify devices with the value 0300h for Device
    Descriptor type 0. This method shall point-to-point connection oriented - or point-to-point
    connectionless remote communication mode.
    This procedure shall use a two-step device discovery.
          Step 1:      Read Device Descriptor Type 0
          Step 2:      Read PID_MGT_DESCRIPTOR_01
    Used Application Layer Services for Management
          •   A_DeviceDescriptor_Read
          •   A_PropertyValue_Read

    Sequence
    Management                                                            Management                  remark
    Client                                                                Server

                            A_DeviceDescriptor_Read-PDU
                                (descriptor_type = 0)

                           A_DeviceDescriptor_Response-PDU
                  (descriptor_type = 0 =DD0, device_descriptor = 0300h)

                                                                                       If DD0 ≠ 0300h then continue with
                                                                                       identified management
                              A_PropertyValue_Read-PDU                                 If DD0 = 0300h then
                         (object_index = 00h, Property_id = 48h,
                          start_index = 01h, nr_of_elem = 01h)

                             A_PropertyValue_Response-PDU
                         (object_index = 00h, Property_id = 48h,
                           start_index = 01h, nr_of_elem = 01h,
                    data = 01h 00h 00h 00h 00h 00h 00h 00h 00h 00h)

                                                                                       If data = 01000000000000000000h
                                                                                       or data = 01000001000000000000h
                                                                                       continue with specified management
                                                                                       model

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dm_identify_r(xknx: XKNX) -> None:
    """DM_Identify_R — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DM_Identify_R (KNX 03.05.02 §3.4.2) — implementation pending"
    )
