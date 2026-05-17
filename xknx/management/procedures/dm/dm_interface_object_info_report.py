"""
DM_InterfaceObjectInfoReport — KNX 03.05.02 §3.29 (PDF p. 129).

Spec text (verbatim from spec):

    3.29.1 Use
    This Management Procedure shall be used by a Management Server to report the value of an Interface
    Object Property to any interested communication partner.
    Used Application Layer Services for Management
    - A_NetworkParameter_InfoReport

    Parameters of the Management Procedure
    DMP_InterfaceObjectInfoReport_RCl (/* [in] */ mpp_ASAP, /* [in] */ mpp_comm_mode,
           /* [in] */ mpp_hop_count_type, /* [in] */ mpp_object_type, /* [in] */ mpp_PID,
           /* [in] */ mpp_priority, /* [in] */ mpp_test_info, /* [in] */ mpp_test_result)
        mpp_ASAP:              The parameter ASAP shall only be evaluated if the parameter
                               mpp_comm_mode equals point-to-point connectionless. It shall in this
                               case contain the Individual Address of the communication partner to
                               which the A_NetworkParameter_InfoReport-PDU shall be sent.
        mpp_comm_mode:         Communication mode that shall be used by the Management Server
                               for transmission of the A_NetworkParameter_InfoReport-PDU. It can
                               be
                               − point-to-all-points connectionless (this is broadcast), or
                               − point-to-point connectionless.
        mpp_hop_count_type:    Value of the hop_count that shall be used to transmit the
                               A_NetworkParameter_InfoReport-PDU.
                               NOTE 17 This value shall be fixed in function of the specific Property of which the value
                               shall be reported via this Management Procedure..
        mpp_object_type:       Value that shall be used by the Management Server for the subfield
                               object_type of the field parameter_type of the
                               A_NetworkParameter_InfoReport-PDU.
        mpp_PID:               Value that shall be used by the Management Server for the subfield
                               PID of the field parameter_type of the
                               A_NetworkParameter_InfoReport-PDU.
        mpp_priority:          The priority that shall be used for the transmission of the
                               A_NetworkParameter_InfoReport-PDU.
        mpp_test_info:         This shall be the contents of the field tests_info of the
                               A_NetworkParameter_InfoReport-PDU.
        mpp_test_result:       This shall be the contents of the field tests_result of the
                               A_NetworkParameter_InfoReport-PDU.

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        Note right of S: This procedure shall be initiated by the Management Server. According the Management Procedure Parameter mpp_comm_mode, it shall send the A_NetworkParameter_InfoReport-PDU
        Note right of S: * on broadcast communication mode
        Note right of S: * or on point-to-point connectionless communication mode to the Individual Address given in mpp_ASAP
        Note right of S: as given below. The priority shall be as requested in mpp_priority. The hop_count_type shall be requested as in the Parameter mpp_hop_count_type.
        S->>C: A_NetworkParameter_InfoReport-PDU (object_type = mpp_object_type, property_id = mpp_PID, test_info = mpp_tests_info, test_result = mpp_test_result)
    ```

    Example use (informative)
    EXAMPLE 12 The A_NetworkParameter_InfoReport is used in Flexible E-Mode Channels (see [06]) to report a human
    localisation action of an E-Mode Channel, using PID_LOCALISATION_REPORT ([05]) as follows:

         /* Report on a localisation action on E-Mode Channel n. */
    DMP_InterfaceObjectInfoReport_RCl(mpp_ASAP = Controller.IA, mpp_Obj.Type = E-Mode Device Object,
         mpp_Prop.ID = PID_LOCALISATION_REPORT, mpp_Test_Info = 00h,
         mpp_Test_Result = Channel Number)

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dm_interface_object_info_report(xknx: XKNX) -> None:
    """DM_InterfaceObjectInfoReport — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DM_InterfaceObjectInfoReport (KNX 03.05.02 §3.29) — implementation pending"
    )
