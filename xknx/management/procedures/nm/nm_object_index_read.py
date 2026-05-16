"""
NM_ObjectIndex_Read — KNX 03.05.02 §2.23.4 (PDF p. 61-62).

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

    Sequence:
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

    Management Server support
    If a Management Server receives this request, it shall answer with the total number of instances of
    object_type that are present in the Management Server device. Further, it shall answer with the
    requested number of Object Indexes.
    The indexes in the response shall be sorted in ascending order. The numbering of instances shall with
    '1', i.e. an Object Instance '0' shall never exist. Instances of the same Object Type shall be numbered
    in ascending order of their indexes, i.e. instance 1 shall be the Interface Object with the lowest index
    of object_type, instance 2 shall be the interface with the next higher Object Index of the same
    object_type etc.
    If a Management Server receives this request that is in point-to-point communication mode it shall
    answer with only one response. If not all requested indexes can be delivered in one response due to
    e.g. max. frame length, then the Management Server shall deliver as many indexes as fit in the frame
    with number_of_instances set to the number of instances delivered with the response. The
    Management Client can detect the total number of instances by setting start_instance and number of
    instances each to '0' in the request, refer to case (d) in the table below (2.23.4.3).

    Management Client support
    If a Management Client does not know whether the Management Server supports long frames or not, it
    shall send a request only for 9 or less Object Instances at once. The response shall then fit in a short
    frame.
    If a Management Client wants to know the indexes of all Object Instances and not all of them fit in
    one frame, then it shall repeat the procedure. It shall then send the repeated request with an adjusted
    test_info (higher value for the start_instance, adjusted value for number_of_instances). The
    Management Client can detect the total number of instances with an own request, i.e. start_instance
    and number of instances each set to '0' in the request, refer to case (d) in the table below (2.23.4.3).
    The responsibility and control of this lies entirely with the Management Client; there are no
    requirements towards the Management Server.
    See also 2.23.4.3 for error and exception handling.

Inputs (from spec):
    [in] ASAP, [in] comm_mode_req, [in] object_type, [in] PID, [in] test_info, [out] test_result, [in] comm_mode_res
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
