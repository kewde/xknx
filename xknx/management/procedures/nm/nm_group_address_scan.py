"""
NM_GroupAddress_Scan — KNX 03.05.02 §2.23.3 (PDF p. 59).

Spec text (verbatim from spec):

    Use
    This Network Management Procedure shall allow testing whether a Group Address is used within the
    range start_address to start_address+range-1. To check for a single Group Address, the range shall be
    set to 1. The service request shall be handled via broadcast communication mode.
    This Network Management Procedure shall be used by a Management Client to find if a Group
    Address is used in the network or not. In general, it shall be used to find a free Group Address before
    assigning it in a subsequent Management Procedure to one or more Management Servers (devices).
    Used Application Layer Services for Management
          •    A_NetworkParameter_Read

    Parameters of the Management Procedure
    NM_GroupAddress_Scan (/* [in] */ GAchecked, /* [in] */ rangedchekced, /* [out] */ test_result)
      Service parameters
              object_type:                1 (Group Address Table)
              PID:                        PID_TABLE = 23 (List of Group Addresses)
              comm_mode response:         point-to-point, connectionless

    Sequence
    Management                                                            Network /                remark
    Client                                                                Management
                                                                          Server

                           A_NetworkParameter_Read-PDU
                         (object_type = 1, PID = PID_TABLE
                     range = rangechecked, start_address = GAChecked)

                        A_NetworkParameter_Response-PDU                                If Group Addresses are
                         (object_type = 1, PID = PID_TABLE                             supported and the investigated
                                                                                       Group Address is linked to one
                     range = rangechecked, start_address = GAChecked)                  or more Group Objects, one
                                                                                       single response is sent by the
                                                                                       device.

    Management Server support
    If a Management Server (device) supports Group Addresses (multicast communication mode) and
    supports this service, it shall support this service without any limitation. When thus receiving this
    request, the Management Server shall test the contained Group Address(es) against all the Group
    Addresses it was assigned to, independent of their value, usage or status.
    •     Number of Responses
    If the number of Group Addresses supported by the Management Server, within the range GAChecked to
    GAChecked+rangechecked-1
    =0        then the Management Server device shall send no answer
    ≠0        then the device shall send 1 single response
              even
              - if one Group Address is assigned to more than one Group Object, or
              - if more than one Group Address within the indicated range is supported, or
              - if the Group Address appears in the Group Address Table of the receiver but no associations
                    to it exist in the Group Association Table.

    •    Response
    There is no test-result field in the response PDU. The response shall be sent using point-to-point
    connectionless communication mode.
    NOTE        The field test_info (= range and Group Address) from the request shall be repeated in the response.

    Management Client support
    •    Error Handling
    The Management Client shall wait until the time-out has expired. This time-out is the sum of the
    maximum delay time in the device, in function of the medium and the frame transmission times. If no
    response is received, the Management Client shall assume that no Group Address in the range
    GAchecked to GAchecked + rangechecked-1 is used in the network. If one or more responses are received, the
    Management Client shall conclude that at least one Group Address in the range the GAchecked GAchecked
    + rangechecked-1 is be occupied.
    •    Usability of this Management Procedure
    The support of the A_NetworkParameter_Read service is not mandatory for all Profiles. This means
    that if a Group Address is checked in a range that is typically used by devices of a Profile that does not
    require the support of this service, the result of this procedure may be less reliable.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def nm_group_address_scan(xknx: XKNX) -> None:
    """NM_GroupAddress_Scan — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "NM_GroupAddress_Scan (KNX 03.05.02 §2.23.3) — implementation pending"
    )
