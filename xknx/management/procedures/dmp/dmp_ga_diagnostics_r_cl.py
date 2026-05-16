"""
DMP_GA_DIAGNOSTICS_RCl — KNX 03.05.02 §5.2 (PDF p. 181).

Spec text (verbatim from spec):

    This Management Procedure shall be used to perform Group Object Diagnostics to the GAs of the
    MaS.
    This Management Procedure shall be used in point-to-point connectionless communication mode. If
    the MaS supports connections, then it shall additionally be supported connection-oriented.
    DMP_GA_DIAGNOSTICS_RCl (/* [in] */ dmp_command, /* [in] */ dmp_flags,
                             /* [in] */ dmp_group_address, /* [in] */ command_data,
                             /* [out] */ command_result_data)
          •   dmp_command:                       the command that shall be executed
          •   dmp_flags                          the flags that shall be included in the command
          •   dmp_group_address:                 indication of the Group Address to which the command shall
                                                 be executed
          •   dmp_command_data:                  command specific data
                                                 EXAMPLE 16 The value to be sent on the GA (WriteServiceID
                                                 01h) or nothing (WriteServiceID 03h).
          •   dmp_command_result_data: Return Code and possible additional command result data

    Used Application Layer services
          -   A_FunctionPropertyCommand
    MaC                                                                      MaS
    NOTE 21         The GO Diagnostic commands that address Group Addresses do not require
    Diagnostic Mode to be enabled. The MaC may set this.
                The MaS may now access Group Object Diagnostics.
                         A_FunctionPropertyCommand-PDU
                    (object_index = Group Object Table.index 19),
                          PID = PID_GO_DIAGNOSTICS,
                        data = dmp_command + dmp_flags +
                     dmp_group_address+ dmp_command_data)

                If the MaS supports Group Object Diagnostics in the addressed Interface Object, then it shall
                                                                                                   respond.
                       A_FunctionPropertyState_Response-PDU
                       (object_index = Group Object Table.index
                           PID = PID_GO_DIAGNOSTICS,
                      data = dmp_return_code + dmp_command)

    Depending on the specific command, the MaS or the user may further have to
    do the following.
    19) In an E-Mode MaS, the Property shall not be addressed in the Group Object Table but in the E-Mode
       Channel Object or Adjusted E-Mode Channel Object in which the GO resides that shall be diagnosed.

    MaC                                                                       MaS
    •     The MaC may have to interpret the data returned in the dmp_command_-
          result_data.
               This mainly concerns negative Return Codes.
    •     The MaC may additionally have to monitor the bus and the
          communication partners of the addressed GO.
          EXAMPLE 17 For the WriteServiceID 01h Send A_GroupValue_Write and the
          WriteServiceID 03h Send A_GroupValue_Read, the Return Code gives no indication of
          success or failure of the transmission of a Telegram on the bus.
          EXAMPLE 18 For the WriteServiceID 03h Send A_GroupValue_Read, the Return
          Code gives no indication about the number and contents of any
          A_GroupValue_Response-PDUs that have as a result been sent on the bus by other
          devices.
    •     The MaC may need subsequent commands to complete an entire
          operation.
          The MaS shall in the above also provide the message to the internal GOs
          (see the specification of the WriteServiceID 01h - Send
          A_GroupValue_Write in [05]). The result of this is not contained in the
          Return Code back to the MaC.
          For the WriteServiceID “Send A_GroupValue_Write” if the MaC wants
          to know if the internal GOs are updated, then it shall read one or more
          values with the ReadServiceID “Get local GO value”. The MaC shall
          however do this at first after 100 ms after the WriteServiceID. If the MaC
          is not satisfied with the response, then it shall wait at least 1 s and may
          repeat the request still two times more, each time waiting 1 s.
          For the WriteServiceID 03h “Send A_GroupValue_Read” the MaC may
          check whether any GO-value in the MaS has changed with a
          ReadServiceID 01h “Get local GO value”.

    6 KNXnet/IP Management Procedures

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dmp_ga_diagnostics_r_cl(xknx: XKNX) -> None:
    """DMP_GA_DIAGNOSTICS_RCl — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_GA_DIAGNOSTICS_RCl (KNX 03.05.02 §5.2) — implementation pending"
    )
