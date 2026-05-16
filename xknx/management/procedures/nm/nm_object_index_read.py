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

    2.23.4.1 Management Server support
    If a Management Server receives this request, it shall answer with the total number of instances of
    object_type that are present in the Management Server device. Further, it shall answer with the
    requested number of Object Indexes.
    The indexes in the response shall be sorted in ascending order. The numbering of instances shall with
    ‘1’, i.e. an Object Instance ‘0’ shall never exist. Instances of the same Object Type shall be numbered
    in ascending order of their indexes, i.e. instance 1 shall be the Interface Object with the lowest index
    of object_type, instance 2 shall be the interface with the next higher Object Index of the same
    object_type etc.
    If a Management Server receives this request that is in point-to-point communication mode it shall
    answer with only one response. If not all requested indexes can be delivered in one response due to
    e.g. max. frame length, then the Management Server shall deliver as many indexes as fit in the frame
    with number_of_instances set to the number of instances delivered with the response. The
    Management Client can detect the total number of instances by setting start_instance and number of
    instances each to ‘0’ in the request, refer to case (d) in the table below (2.23.4.3).

    2.23.4.2 Management Client support
    If a Management Client does not know whether the Management Server supports long frames or not, it
    shall send a request only for 9 or less Object Instances at once. The response shall then fit in a short
    frame.
    If a Management Client wants to know the indexes of all Object Instances and not all of them fit in
    one frame, then it shall repeat the procedure. It shall then send the repeated request with an adjusted
    test_info (higher value for the start_instance, adjusted value for number_of_instances). The
    Management Client can detect the total number of instances with an own request, i.e. start_instance
    and number of instances each set to ‘0’ in the request, refer to case (d) in the table below (2.23.4.3).
    The responsibility and control of this lies entirely with the Management Client; there are no
    requirements towards the Management Server.
    See also 2.23.4.3 for error and exception handling.

    2.23.4.3 Error and exception handling
    Management Server
    The following table gives an overview about the behaviour of the Management Server in the normal
    cases (a), (b) as well as in various exception cases. The left columns specify the possible combinations
    of the test_info in the A_NetworkParameter_Read-PDU of NM_ObjectIndex_Read. The right 4
    columns specify how the Management Server shall answer with test_info and test_result in the
    A_NetworkParameter_Response-PDU of NM_ObjectIndex_Read.
                                         Table 3 – Management Server side error handling

                 test_info in Read-PDU                        test_result in Response-PDU                                          Remark

                 start_        number_of_            start_         number_of_              Object
     case       instance        instances           instance         instances             Index(es)

                                                                    as requested in
     (a)           1                >0                  1                               As many indexes       This is the most typical case.
                                                                      Read_PDU
                                                                                        as requested with
                                                                                          number_of_-         This allows reading with an offset, in case more
                                                  as requested in   as requested in         instances         instances of the Object Type are available in the
     (b)           >1               >0
                                                    Read_PDU          Read_PDU                                Management Server than what can be reported in
                                                                                                              a single A_NetworkParameter_Response-PDU.
                                                                                                              This is a “lazy client” style: the Management
                                                                                                              Client does not specify the number of instances it
                                                                      = number of                             wants, either because it expects that the number
                                                  as requested in                      All indexes starting   will fit in an L_Data_Standard frame, or expects
     (c)           >0                0                              delivered Object
                                                    Read_PDU                           from start_instance    that it can handle a possible L_Data_Extended
                                                                         Indexes                              frame, or is ready to send more requests if the
                                                                                                              Server would signal the availability of potential
                                                                                                              other instances.
                                                                        current                               This is a standard exception allowing the Client
                                                                                                              to firstly detect the total number of instances and
     (d)           0                 0                  0           total_number_                             then have a systematic discovery without any of
                                                                     of_instances                             the risks of case (c).
                                                                                                              This is an error by the Management Client: 0 is
                                                                                                              not a valid start_instance. The Server does not
     (e)           0                 x                  0                  0                  none            give information in the response but possibly
                                                                                                              adjusts the number_of_instances in the response.
                 > current                                                                                    This is an error by the Management Client, which
                                                                                                              it may make if it has not discovered the total
     (f)      total_number_          x                  0                  0                                  number of instances: the start_index has a value
               of_instances                                                                                   larger than the number of instances.

                                 requested                           = number of         indexes starting     The Management Client attempts to read more
                                                  as requested in                                             instances than what is available. The
     (g)           >0         number exceeds                        delivered object   from start_instance
                                                    Read_PDU                                                  Management Server returns all instances it has
                              highest instance                          indexes         until last instance   and corrects the number_of_instances.

                                                                      = number of        Indexes starting     The Management Client attempts to read more
                              > number fitting                      delivered object           from           instances than what the Management Server can
                                                  as requested in
     (h)           >0           in response                            indexes, as      start_instance, as    hold in its response frame. The Management
                                                    Read_PDU                                                  Server returns as many as possible and corrects
                                   frame                             many as fit in     many as fit in the
                                                                        the frame             frame           the number_of_instances.
                                 0, but total                                            Indexes starting
                                  number of                          = number of               from           This is a combination of (c) and (h): again, the
                                                  as requested in
     (i)           >0            instances >                        delivered object    start_instance, as    Management Server returns the maximal set of
                                                    Read_PDU                                                  instances and corrects the number_of_instances.
                              number fitting in                         indexes         many as fit in the
                               response frame                                                 frame

    Management Client
    If no response is received, the Management Client shall wait until the time-out has expired. This
    time-out shall be 3 s 6). If no response is received, the Management Client shall assume that the
    requested Object Type is not present in the Management Server device.
    NOTE 6      It is assumed here that a Management Client uses the NM_ObjectIndex_Read-Procedure only for devices
    supporting the NM_ObjectIndex_Read-Procedure as Management Servers. The support of NM_ObjectIndex_Read by
    Management Servers shall be defined in the corresponding device Profiles, see also [14].

    6)     3 s is the Application Layer time-out typically used for confirmed AL-services with response on point-to-
           point connectionless communication mode.

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
