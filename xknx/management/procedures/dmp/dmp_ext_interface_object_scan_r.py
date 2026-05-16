"""
DMP_ExtInterfaceObjectScan_R — KNX 03.05.02 §3.28.4 (PDF p. 128).

Spec text (verbatim from spec):

    This Management Procedure shall use the connection oriented - or connectionless communication
    mode.
    Used Application Layer Services for Management
          •      A_PropertyExtDescription_Read
          •      A_PropertyExtValue_Read
    Sequence
    Management                                                            Management
    Client                                                                Server
    If Property of management control is unknown to the Management Client
                        A_PropertyExtDescription_Read-PDU
                      (object_type = 0, object_instance = 1, PID =
                                PID_IO_LIST, type = 0)

                       A_PropertyExtDescription_Response-PDU                             A_Disconnect.ind ⇒ error,
                      (object_type = 0, object_instance = 1, PID =                       Property does not exist ⇒
                              PID_IO_LIST, type = 0, …)                                  error

    endif

    Management                                                              Management
    Client                                                                  Server
    io_list = new[]{}
    for each data block, until all data are transmitted
                          A_PropertyExtValue_Read-PDU
                     (object_type = 0, object_instance = 0, PID =
                 PID_IO_LIST, start_index = SSSS, nr_of_elem = EE)

                        A_PropertyExtValue_Response-PDU                                  A_Disconnect.ind ⇒ error,
                     (object_type = 0, object_instance = 0, PID =                        no data received ⇒ error
                 PID_IO_LIST, start_index = SSSS, nr_of_elem = EE,
                                 data = object_types)

            io_list.Add(object_types)
    endfor
    Calculate Object Informations from io_list (object_index, object_type, object_instance)
    foreach (object_index, object_type, object_instance) in io_list
            Property_index = 0
            repeat if Property scan is enabled
                        A_PropertyExtDescription_Read-PDU
                        (object_type, object_instance, PID = 0,
                               Property_index, type = 0)

                      A_PropertyExtDescription_Response-PDU
                  (object_type, object_instance, PID, Property_index,
                                      type = 0, …)

                      Property_index ++
             Until PID = 0
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


async def dmp_ext_interface_object_scan_r(xknx: XKNX) -> None:
    """DMP_ExtInterfaceObjectScan_R — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_ExtInterfaceObjectScan_R (KNX 03.05.02 §3.28.4) — implementation pending"
    )
