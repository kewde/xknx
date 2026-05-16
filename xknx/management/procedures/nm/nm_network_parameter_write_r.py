"""
NM_NetworkParameter_Write_R — KNX 03.05.02 §2.22.1 (PDF p. 46).

Spec text (verbatim from spec):

    Use
    This Management Procedure shall be used by a Management Server to report the value of a parameter
    related to network configuration to any interested communication partner.
    Used Application Layer Services for Management
     • A_NetworkParameter_Write

    Parameters of the Management Procedure
    NM_NetworkParameter_Write_R(/* [in] */ ASAP, /* [in] */ comm_mode,
    /* [in] */ hop_count_type_req, /* [in] */ object_type, /* [in] */ PID, /* [in] */ priority, /* [in] */ value)
        ASAP:                                  The parameter ASAP shall only be evaluated if the parameter
                                               comm_mode equals point-to-point connectionless. It shall in this case
                                               contain the Individual Address of the communication partner to which
                                               the A_NetworkParameter_Write-PDU shall be sent.
        comm_mode:                             Communication mode that shall be used by the Management Server
                                               for transmission of the A_NetworkParameter_Write-PDU. It can be
                                               − point-to-all-points connectionless (this is broadcast), or
                                               − point-to-point connectionless.
        hop_count_type_req:                    Value of the hop_count that shall be used to transmit the
                                               A_NetworkParameter_Write-PDU.
                                               NOTE       This value shall be fixed in function of the specific Property of which the value
                                               shall be reported via this Management Procedure as specified in [05].

        object_type:                           Value that shall be used by the Management Server for the subfield
                                               object_type of the field parameter_type of the
                                               A_NetworkParameter_Write-PDU.
        PID:                                   Value that shall be used by the Management Server for the subfield
                                               PID of the field parameter_type of the
                                               A_NetworkParameter_Write-PDU.
        priority:                              The priority that shall be used for the transmission of the
                                               A_NetworkParameter_Write-PDU.
        value:                                 This shall be the contents of the field value of the
                                               A_NetworkParameter_Write-PDU.

    The A_NetworkParameter_Write-PDU shall be transmitted with priority System.
    Sequence
    Management                                                                         Management                remark
    Client                                                                             Server

                         A_NetworkParameter_Write-PDU
                 (ASAP, comm_mode, hop_count_type_req, , priority,
                          object_type, PID, priority, value)

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def nm_network_parameter_write_r(xknx: XKNX) -> None:
    """NM_NetworkParameter_Write_R — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "NM_NetworkParameter_Write_R (KNX 03.05.02 §2.22.1) — implementation pending"
    )
