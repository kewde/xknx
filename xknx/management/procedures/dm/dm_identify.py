"""
DM_Identify — KNX 03.05.02 §3.4 (PDF p. 72).

Spec text (verbatim from spec):

    3.4.1        General
    This Management Procedure shall be used to retrieve data from the Management Server in order to be
    able to uniquely identify this Management Server and differentiate it from other Management Servers.

    3.4.2 DM_Identify_R
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

    3.4.3        DM_Identify_RCo2
    This Management Procedure shall use the point-to-point connection-oriented communication mode.
    DM_Identify_RCo2                              (destination_address)
       server IA                                   Individual Address of the Management Server

             device descriptor type 0               device descriptor of the Management Server
             manufacturer id                        identification of the manufacturer of the Management
                                                    Server
             hardware type                          hardware type of the Management Server

    Used Application Layer Services for Management
         •      A_Connect
         •      A_DeviceDescriptor_Read
         •      A_PropertyValue_Read
    Sequence
    If no Transport Layer connection exists between the Management Server and the Management Client,
    the Management Client shall execute the procedure DM_Connect_RCo prior to this procedure.
    NOTE          DM_Connect_RCo already returns the value of the Device Descriptor Type 0 of the Management Server. This result
    is part of the return of this procedure NM_Identify_RCo2.
    Management                                                                       Network /                   remark
    Client                                                                           Management
                                                                                     Server
                               A_PropertyValue_Read-PDU
                             (destination_address = server IA,
                                     object_index = 0,
                        Property_id = PID_MANUFACTURER_ID,
                             nr_of_elem = 1, start_index = 1)

                             A_PropertyValue_Response-PDU
                                (source_address = server IA
                       object_index = PID_MANUFACTURER_ID,
                              nr_of_elem = 1, start_index = 1,
                                  data = manufacturer id)

                                A_PropertyValue_Read-PDU
                              (destination_address = server IA,
                                      object_index = 0,
                          Property_id = PID_HARDWARE_TYPE,
                              nr_of_elem = 1, start_index = 1)

                            A_PropertyValue_Response-PDU
                               (source_address = server IA
                        object_index = PID_HARDWARE_TYPE,
                   nr_of_elem = 1, start_index = 1, data = hardware type)

    Exception handling
    The default error handling applies. If any of these services fails (time-out, negative response, no
    response) then the request shall be repeated up to three times. On further failure, the Management
    Procedure and the encompassing Configuration Procedure shall be interrupted.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dm_identify(xknx: XKNX) -> None:
    """DM_Identify — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DM_Identify (KNX 03.05.02 §3.4) — implementation pending"
    )
