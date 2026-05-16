"""
NM_Coupler_Scan_LocalSubnetwork — KNX 03.05.02 §2.23.5 (PDF p. 63).

Spec text (verbatim from spec):

    NOTE 7       This procedure was named NM_Coupler_Scan before.

    2.23.5.1 Procedure
    This Network Management Procedure shall allow detecting a Coupler in the local Subnetwork in
    which the MaC is installed. The service request and the service response shall be handled via point-to-
    all-points, connectionless (broadcast) communication mode.
    NM_Coupler_Scan_LocalSubnetwork (/* [in] */ ASAP, /* [in] */ comm_mode_req,
                     /* [in] */ hop_count_type_req, /* [in] */ object_type, /* [in] */ PID,
                     /* [in] */ test_info, /* [in] */ comm_mode_res, /* [in] */ hop_count_type_res,
                     /* [out] */ test_result)
        ASAP:                                  not applicable: the communication mode of the request is broadcast
        comm_mode_req                          point-to-all-points, connectionless (broadcast)
        hop_count_type_req:                    Value of the hop_count that shall be used by the Management Client
                                               for the transmission of the A_NetworkParameter_Read-PDU.
                                               0: to find the presence of any Coupler in the local Subnetwork.
        object_type:                           6 = Router Object
        PID:                                   01 = PID_OBJECT_TYPE
        test_info:                             octet 11:         00h
        comm_mode_res:                         point-to-all-points, connectionless (broadcast)
                                               • The response shall be sent on the Medium Interface of the
                                                    Coupler on which the request has arrived.
                                               • The response may additionally be sent on further Medium
                                                    Interfaces of the Coupler. This is the recommended behaviour.
        hop_count_type_res:                    Network Layer parameter
        test_result:                           octet 12 a 13:    0006h = Object Type of the Router Object

    Used Application Layer services for Management
        •      A_NetworkParameter_Read
    Sequence
    Management                                                                        Network /                      remark
    Client                                                                            Management
                                                                                      Server

                            A_NetworkParameter_Read-PDU
                     (comm_mode_req = point-to-point connectionless,
                              object_type = Router Object,
                       PID = PID_OBJECT_TYPE, test_info = 00h)

                                                           If the MaS is a Coupler, then it shall at least send a response on the
                                                           Medium Interface on which the request has arrived; it should send
                                                           additional responses on the other Medium Interface(s)
                                                           The response(s) shall contain Object Type of the Router Object.
                                                           If the MaS is not a Coupler, then it shall not respond.

                                A_NetworkParameter_Response-PDU
                        (comm_mode_res = point-to-all-points connectionless
                               object_type = Router Object, PID = 01h,
                       test_info = 00h, test_result = Object Type of the Router
                                           Object = 0006h).

      2.23.5.2 Management Server support
      •       The MaS shall verify that the test_info equals 0. If this is not the case, the MaS shall ignore the
              request.
      •       If the MaS (Coupler) implements more than one Router Object, then it shall only give one single
              response, on the Medium Interface 7) on which the request is received.

      2.23.5.3 Management Client support
      •       The MaC shall take into account that the requirements to the MaS do not require that the MaS
              (Coupler) be used as a Router (Line Coupler or Backbone Coupler), this is, this Management
              Procedure will be responded upon as well by the Coupler implementations configured as KNX
              TP1 Bridge or as KNX TP1 Repeater.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def nm_coupler_scan_local_subnetwork(xknx: XKNX) -> None:
    """NM_Coupler_Scan_LocalSubnetwork — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "NM_Coupler_Scan_LocalSubnetwork (KNX 03.05.02 §2.23.5) — implementation pending"
    )
