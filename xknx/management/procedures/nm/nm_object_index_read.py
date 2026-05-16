"""
NM_ObjectIndex_Read — KNX 03.05.02 §2.23.4 (PDF p. 60).

Spec text (verbatim from spec):

    This Network Management Procedure shall allow discovery of the index of a certain Interface Object
    Type in one device. The service request shall be handled via point-to-point communication mode.
    This Network Management Procedure shall be used by a Management Client to find the Object
    Index(es) of one Object Type in one device.
    NM_ObjectIndex_Read (/* [in] */ ASAP, /* [in] */ comm_mode_req, /* [in] */ object_type,
       /* [in] */ PID, /* [in] */ test_info, /* [out] */ test_result, /* [in] */ comm_mode_res)
            ASAP                                 PPPP = Individual Address of the Device in which the index of an
                                                 Interface Object Type shall be discovered
            comm_mode_req                        point-to-point, connectionless
            object_type:                         nm_object_type: Interface Object Type of which the presence in the
                                                 Management Server is to be discovered
            PID:                                 PID_OBJECT_INDEX = 29 (see [05])
            test_info:                           Octet 11:        start_instance of object_type
                                                 Octet 12:        number_of_instances
            test_result:                         Octet 13 … N: Object Index(es) of target object_type
            comm_mode_res:                       point-to-point, connectionless

    Used Application Layer services for Management
        •      A_NetworkParameter_Read

    Sequence
    Management                                                            Network /               remark
    Client                                                                Management
                                                                          Server

                            A_NetworkParameter_Read.req
                   (ASAP = PPPP, comm_mode_req = point-to-point
                     connectionless, object_type = nm_object_type,
                         PID = 29, test_info = start_instance +
                                 number_of_instances)

                             A_NetworkParameter_Read.res                               Only one response shall be
                        (object_type = nm_object_type, PID = 29,                       given to one read request. If
                                                                                       one response is not enough to
                    test_info = start_instance + number_of_instances,                  deliver all indexes, than the
                              test_result = Object Index(es))                          Management Client shall
                                                                                       read again with a higher start
                                                                                       instance within the test_info.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def nm_object_index_read(xknx: XKNX) -> None:
    """NM_ObjectIndex_Read — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "NM_ObjectIndex_Read (KNX 03.05.02 §2.23.4) — implementation pending"
    )
