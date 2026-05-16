"""
DMP_ExtInterfaceObjectWriteUnCon_R — KNX 03.05.02 §3.25.5 (PDF p. 119).

Spec text (verbatim from spec):

    This Management Procedure shall use the connection oriented - or connectionless communication
    mode.
    Used Application Layer Services for Management
        •    A_PropertyExtDescription_Read
        •    A_PropertyExtValue_WriteUnCon
    Sequence
    Management                                                            Management
    Client                                                                Server
    If Property of management control is unknown to the Management Client
                       A_PropertyExtDescription_Read-PDU                               A_Disconnect.ind ⇒ error,
                 (object_type = OT, object_instance = OI, PID = PP,                    Property does not exist ⇒
                                     type = 0)                                         error

                     A_PropertyExtDescription_Response-PDU                             A_Disconnect.ind ⇒ error,
                 (object_type = OT, object_instance = OI, PID = PP,                    Property does not exist ⇒
                                    type = 0, …)                                       error

    endif
    for each data block, until all data are transmitted
                        A_PropertyExtValue_WriteUnCon-PDU                              A_Disconnect.ind ⇒ error
                  (object_type = OT, object_instance = OI, PID = PP,
                 start_index = SSSS, nr_of_elem = EE, data = DD,…)

    endfor

    Exception handling
    The general exception handling shall apply.
    The MaC shall not interpret the value of the Property Index contained in the A_Property_-
    Description_Response-PDU at the level of this Management Procedure. Possibly, error handling in
    case an unexpected value of the Property Index can be handled at the level of the Configuration
    Procedure in which this Management Procedure is used.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dmp_ext_interface_object_write_un_con_r(xknx: XKNX) -> None:
    """DMP_ExtInterfaceObjectWriteUnCon_R — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_ExtInterfaceObjectWriteUnCon_R (KNX 03.05.02 §3.25.5) — implementation pending"
    )
