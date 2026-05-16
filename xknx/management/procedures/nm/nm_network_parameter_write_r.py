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

    2.22.2 Overview of accepted usage of A_NetworkParameter_Write
      •   NM_NetworkParameter_Write_R
          Abstract procedure to report or set the value of a network parameter.
          This is only a model, not a real Management Procedure. Do not use this like this in real life.
          intended sender:            not specified (abstract procedure)
          intended receiver:          not specified (abstract procedure)
          specification:              clause 2.22.1
          test:                       Chapter 8/3/7 “AIL and Management Tests” ([13] clause 2.19.1)
          ASAP:                       not specified (abstract procedure)
          comm_mode request           not specified (abstract procedure)
          hop_count_type_req:         not specified (abstract procedure)
          object_type:                not specified (abstract procedure)
          PID:                        not specified (abstract procedure)
          priority:                   system
          value:                      not specified (abstract procedure)

      •   NM_IndividualAddress_Check_LocalSubNetwork
          The procedure shall be used by a Management Client to check whether a given Individual
          Address is occupied on the Subnetwork where it is itself located (the “local” Subnetwork)
          intended sender:          E-Mode Client (device, controller)
          intended receiver:        E-Mode device
          specification:            clause 2.22.3
          test:                     No test specifications are available.
          ASAP:                     IA that is tested
          comm_mode request         point-to-point connectionless
          hop_count_type_req:       0
          object_type:              0000h = Device Object
          PID:                      61 = PID_ADDR_CHECK
          priority:                 system
          value:                    00h

      •   NM_IndividualAddress_SerialNumber_Report
          This Management Procedure shall be used by a Management Server in order to announce its
          (new) Individual Address.
          intended sender:          E-Mode device
          intended receiver:        Other E-Mode devices
          specification:            clause 2.22.4
          test:                     No test specifications are available. (Subnetwork Address
                                    Assignment is optional for all Profiles.)
          ASAP:                     not applicable (broadcast)
          comm_mode request         broadcast
          hop_count_type_req:       Network Layer parameter
          object_type:              0000h = Device Object
          PID:                      60 = PID_ADDR_REPORT
          priority:                 system
          value:                    KNX Serial Number of the sender

      •   SNA update on IA change
          SNA update on power-up
          SNA heart beat
          SNA update on SNA inconsistency
          “SNA update on IA change” is a procedure executed by the Router, in which it shall update the
          SNA on its secondary side if the Router’s own Individual Address changes.
          intended sender:          Coupler
          intended receiver:        E-Mode devices
                                    Coupler Model 2.0
          specification:
          test:
                                                                               Spec            Test
                                                                             Ch. 3/5/3       Part 9/3
                                      Procedure                                [06]            [15]
                                      SNA update on IA change               §1.3.4      §4.7.5.3
                                      SNA update on power-up                §1.3.5      §4.7.5.3 (nr. 5)
                                      SNA heart beat                        §1.3.6      §4.7.5.3 (nr. 6)
                                      SNA update on SNA inconsistency §1.3.7            §4.7.5.5
                                                                                        §4.7.5.6

                                        NOTE 4      This is actually always the same “Management Procedure” (actually only
                                        a single Telegram) that is triggered for different reasons.
                                        NOTE 5     §4.7.5.1 in [15] tests the SNA Read.

          ASAP:                         not applicable (broadcast communication mode)
          comm_mode request             broadcast
          hop_count_type_req:           0
          object_type:                  0000h = Device Object
          PID:                          57 = PID_SUBNET_ADDR
          priority:                     system
          value:                        Router.SNA

      •   PB-Mode Configuration Procedures
          This makes intense use of A_NetworkParameter_Write.
          This is not documented here in further detail.

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
