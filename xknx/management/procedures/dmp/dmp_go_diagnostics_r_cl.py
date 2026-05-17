"""
DMP_GO_DIAGNOSTICS_RCl — KNX 03.05.02 §5.1 (PDF p. 179).

Spec text (verbatim from spec):

    This Management Procedure shall be used to perform Group Object Diagnostics to the GOs of the
    MaS.
    This Management Procedure shall be used in point-to-point connectionless communication mode. If
    the MaS supports connections, then it shall additionally be supported connection-oriented.

    DMP_GO_DIAGNOSTICS_RCl (/* [in] */ dmp_command, /* [in] */ dmp_group_object_number,
                             /* [in] */ command_data, /* [out] */ command_result_data)
    - dmp_command:                the command that shall be executed
    - dmp_group_object_number:    indication of the Group Object to which the command shall
                                  be executed
                                  S-Mode  the Group Object number
                                  E-Mode  the Group Object index

    - dmp_command_data:           command specific data
    - dmp_command_result_data:    Return Code and possible additional command result data

    Used Application Layer services
    - A_FunctionPropertyCommand

    ```mermaid
    sequenceDiagram
        participant C as MaC
        participant S as MaS
        Note over C,S: In function of the command that will be used, the MaC may have to set the Operation Mode to "Diagnostic Mode". Please refer to the specification of the GO Diagnostic commands for which commands require prior setting the Operation Mode to "Diagnostic Mode".
        C->>S: A_FunctionPropertyCommand-PDU (object_index = 00h, PID = PID_OPERATION_MODE, data = 1)
        Note right of S: If the MaS accepts the command then it shall set its Operation Mode to "Diagnostic Mode" and respond to the MaS with Return Code E_OM_CURRENT_OPERATION_MODE and the Time Left.
        Note right of S: If the MaS does not accept the command then it shall respond with the Return Code E_OM_ERROR and the Time Left.
        S->>C: A_FunctionPropertyState_Response-PDU (object_index = 00h, PID = PID_OPERATION_MODE, Return Code, Operation Mode, Time Left)
        Note over C,S: If the MaS responds with a negative Return Code, then the MaC shall abandon the procedure.
        Note over C,S: If the MaS responds with a positive Return Code, then the MaC shall continue the procedure.
        Note over C,S: If the MaS responds with a Time Left ≠ 255 s, then the MaC shall retrigger the Operation Mode as needed before this Operation Mode expires automatically at the MaS.
        Note over C,S: The MaS may now access Group Object Diagnostics.
        Note left of C: The MaC may have to retrigger PID_OPERATION_MODE during this sequence.
        C->>S: A_FunctionPropertyCommand-PDU (object_index = Group Object Table.index 18), PID = PID_GO_DIAGNOSTICS, data = dmp_command + dmp_group_object_number + dmp_command_data)
        Note right of S: If the MaS supports Group Object Diagnostics in the addressed Interface Object, then it shall respond.
        S->>C: A_FunctionPropertyState_Response-PDU (object_index = Group Object Table.index PID = PID_GO_DIAGNOSTICS, data = dmp_return_code + dmp_command + dmp_group_object_number + dmp_command_result_data)
        Note over C,S: Depending on the specific command, the MaS or the user may further have to do the following.
    ```

    - It may have to interpret the data returned in the dmp_command_result_-
      data.
        EXAMPLE 13 For the command "Get local GO value".
    - It may additionally have to monitor the bus and the communication
      partners of the addressed GO.
        EXAMPLE 14 For the commands "Send A_GroupValue_Write" and "Send
        local GO value on bus" the MaC may verify whether the MaS effectively
        sends a Frame on the bus, whether this is received by the communication
        partners and how these react.
    - It may need subsequent commands to complete an entire operation.
        EXAMPLE 15 The command "Read GO value from bus" may not return
        the final result. This may have to be read over a next command "Get local
        GO value".
    At the end, if the user does not perform any further GO Diagnostics, the MaC
    shall set the Operation Mode of the MaS back to "Normal Operation" if this
    was set to "Diagnostic Mode" before.
    NOTE 20 These Device Management Procedures are specified for a single MaS.
    The MaC shall reset however all involved MaS.

    ```mermaid
    sequenceDiagram
        participant C as MaC
        participant S as MaS
        C->>S: A_FunctionPropertyCommand-PDU (object_index = 00h, PID = PID_OPERATION_MODE, data = 0)
        Note right of S: If the MaS accepts the command then it shall set its Operation Mode to "Normal Mode" and respond to the MaS with Return Code E_OM_CURRENT_OPERATION_MODE and the Time Left.
        Note right of S: If the MaS does not accept the command then it shall respond with the Return Code E_OM_ERROR and the Time Left. The MaC shall in that case after that time retry to set the Operation Mode back to "Normal mode".
        Note over C,S: 18) In an E-Mode MaS, the Property shall not be addressed in the Group Object Table but in the E-Mode Channel Object or Adjusted E-Mode Channel Object in which the GO resides that shall be diagnosed.
        S->>C: A_FunctionPropertyState_Response-PDU (object_index = 00h, PID = PID_OPERATION_MODE, Return Code, Operation Mode, Time Left)
    ```

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dmp_go_diagnostics_r_cl(xknx: XKNX) -> None:
    """DMP_GO_DIAGNOSTICS_RCl — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_GO_DIAGNOSTICS_RCl (KNX 03.05.02 §5.1) — implementation pending"
    )
