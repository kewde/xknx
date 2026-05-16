"""
NM_NetworkParameter_Read_R — KNX 03.05.02 §2.23.1 (PDF p. 53-55).

Spec text (verbatim from spec):

    Precondition
    The use of the point-to-point connectionless communication mode for the response requires the
    preceding correct configuration of Individual Address in the communication path between requester
    and receiver(s). This shall be guaranteed by other preceding Management Procedures.

    Risks
    The MaC shall use this Management Procedure with care, considering the following criteria for the
    responses.
         a) The number of expected responding devices.
         b) The communication mode of the response: point-to-point connectionless or broadcast.
         c) The hop count of the response: 0, 6 or 7.
    Improper use of this service may lead to very high and high busload in the local Subnetwork, all over
    the KNX installation, in the communication path between requester and responder(s) and on the Main-
    and Backbone Lines. The resulting bandwidth may for a short - or longer time hamper the runtime
    communication and may also make that responses to this service are lost.
    Because of this, this service shall only be supported and be used as specified in the KNX
    Specifications.

    Use
    This Management Procedure shall be used by a Management Client to find if a system- or device
    parameter of a given type and value is used in the network or not.

    Used Application Layer Services for Management
          •    A_NetworkParameter_Read

    Parameters of the Management Procedure
    NM_NetworkParameter_Read_R(/* [in] */ ASAP, /* [in] */ hop_count_type_req,
       /* [in] */ object_type, /* [in] */ PID, /* [in] */ test_info, /* [in] */ comm_mode_req,
       /* [in] */ comm_mode_res, /* [in] */ hop_count_type_res, /* [out] */ result_data[])
        ASAP:                                  The parameter ASAP shall only be evaluated if the parameter
                                               comm_mode_req equals point-to-point connectionless. It shall in this
                                               case contain the Individual Address of the communication partner to
                                               which the A_NetworkParameter_Read-PDU shall be sent.
        hop_count_type_req:                    Value of the hop_count that shall be used by the Management Client
                                               for the transmission of the A_NetworkParameter_Read-PDU.
                                               NOTE      This value shall be fixed in function of the specific Property that shall be
                                               accessible via this Management Procedure as specified in [05].

        object_type:                           Value that shall be used by the Management Client for the subfield
                                               object_type of the field parameter_type of the
                                               A_NetworkParameter_Read-PDU.
        PID:                                   Value that shall be used by the Management Client for the subfield
                                               PID of the field parameter_type of the
                                               A_NetworkParameter_Read-PDU.
        test_info:                             Value that shall be used by the Management Client for the field
                                               test_info of the A_NetworkParameter_Read-PDU.

        comm_mode_req:                         Communication mode that shall be used by the Management Client for
                                               transmission of the A_NetworkParameter_Read-PDU. It can be
                                               − point-to-all-points connectionless (this is broadcast), or
                                               − point-to-point connectionless.
        comm_mode_res:                         Communication mode that shall be used by the Management Server(s)
                                               for transmission of the A_NetworkParameter_Response-PDU.
        hop_count_type_res:                    Value of the hop_count that shall be used by the Management
                                               Server(s) for the transmission of the A_NetworkParameter_-
                                               Response-PDU.
                                               NOTE      This value shall be fixed in function of the specific Property that shall be
                                               accessible via this Management Procedure as specified in [05].

        result_data[]:                         The collection of all test_result data collected by the Management
                                               Client as result of the Management Procedure

    Service parameters
        test_info:                             Value that shall be used by the Management Server(s) for the field
                                               test_info of the A_NetworkParameter_Read-PDU.
                                               NOTE      This value shall be fixed in function of the specific Property that shall be
                                               accessible via this Management Procedure as specified in [05].

    Sequence:
    Management                                                                         Management                remark
    Client                                                                             Server

                           A_NetworkParameter_Read-PDU
                   (hop_count_type, parameter_type, priority, test_info)

                          A_NetworkParameter_Response-PDU                                           if the parameter_type is
                       (ASAP, hop_count_type, individual_address,                                   supported and the test is
                                                                                                    positive, the Management
                      parameter_type, priority, test_info, test_result)                             Server shall respond


                                                …                                                   According the specification of
                                                                                                    the parameter_type in [05], the
                          A_NetworkParameter_Response-PDU                                           Management Server may send
                                                                                                    1 or multiple responses.
                       (ASAP, hop_count_type, individual_address,
                      parameter_type, priority, test_info, test_result)


    Multiple answers may be received if the parameter_type is supported more than
    once by one device or by more than one device.
    The Management Client shall collect the answers of test_result in
    dmp_result_data[] as result of this Management Procedure for further processing.

    Management Server support
    The remote Application Layer User, this is the management in the remote device, may respond with
    either no, one or several responses.
         0.      No response:
                 If the parameter_type is not supported or the test_info leads to a negative result, the device
                 shall not answer.

         1.   One response:
              If the parameter_type can, due to its nature, only be supported once by the device. This is the
              case for instance for a group address. This Link Layer parameter can be shared inside the
              device between multiple Group Objects, but is supported only once.
         2.   Several responses:
              If the parameter_type can be supported several times in the device. This can be the case for
              the Functional Block scan: a device can have the identical Functional Block supported more
              than once. E.g. a double-channel heating regulator, a double audio cassette-deck.

    Error handling
    Wait until the time-out has expired. This time-out is the sum of the following and has to be taken into
    account for each KNX device (Management Client, Management Server, Couplers…) and for each
    physical segment in the communication path between Management Client and Management Server.
    •    The maximum delay time in the device.
             This is the time that the Management Server in the device needs to handle this request. This
             may depend on the specific Network Parameter that is read.
    •    Random wait times in the device.
             In order to avoid a very high busload due to the usage of this procedure, in many cases it
             may be specified that the Management Server in the device delays its response by a random
             wait time, in order to spread in time the responses by many devices.
    •    Bus access times.
             This is the time that may be needed to access the bus, due to bus free detection and possible
             collision avoidance if other devices are transmitting.
    •    Medium times
            This is the actual time that the telegram occupies the medium and the short signalling
            difference between sender and receiver.
    •    Delay times in Couplers.
             This is the time that Repeaters, Line- and Backbone Couplers, Media Couplers and
             Interfaces may need to receive, evaluate and forward a telegram.
    Therefore, the time-out should be defined for each specific use case of this Management Procedure.
    If no response is received, the Management Client shall assume the system or device parameter for the
    checked value to be free.

Inputs (from spec):
    [in] ASAP, [in] hop_count_type_req, [in] object_type, [in] PID, [in] test_info, [in] comm_mode_req, [in] comm_mode_res, [in] hop_count_type_res, [out] result_data[]
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def nm_network_parameter_read_r(xknx: XKNX) -> None:
    """NM_NetworkParameter_Read_R — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "NM_NetworkParameter_Read_R (KNX 03.05.02 §2.23.1) — implementation pending"
    )
