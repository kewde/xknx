"""
DMP_LoadStateMachineWrite_RCo_Mem — KNX 03.05.02 §3.31.2 (PDF p. 133).

Spec text (verbatim from spec):

    Use
    This Management Procedure shall use the connection oriented communication mode.
    The control and state of the Load State Machine shall be located in the memory of the Management
    Server and shall be accessible as Memory Mapped Resource.
    The Verify Mode of the Management Server shall not be used.
    This Management Procedure shall support only one state machine of each type.
    This Management Procedure shall only be used with device model for mask version 070nh (BIM
    M112). The address of the management control is 0104h. The address (AAAA) of the load state
    depends on the Load State Machine.

        state machine          address of load state (AAAA)
        address table          B6EAh
        association table      B6EBh
        application program    B6ECh
        PEI program            B6EDh

    This Management Procedure shall not be used for further developments of Management Servers.

    Used Application Layer Services for Management
    - A_Memory_Write
    - A_Memory_Read

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        C->>S: A_Memory_Write (addr =0104h, length = 0Bh, data = depends on event)
        loop repeat until loadstate is correct (for max. 3 times)
            C->>S: A_Memory_Read (addr = AAAA, length = 01h)
            S->>C: A_Memory_Response (addr = AAAA, length = 01h, data = loadstate)
            Note right of S: A_Disconnect.ind ⇒ error, Wrong state ⇒ error
        end
    ```

    The transmitted data depend on the event.
    - LoadEvent: Unload
    data
        state machine / event   reserved
        L4                      00h
        1 octet                 10 octets

    - LoadEvent: Load
    data
        state machine / event   reserved
        L1                      00h
        1 octet                 10 octets

    - LoadEvent: LoadComplete
    data
        state machine / event   reserved
        L2                      00h
        1 octet                 10 octets

    - LoadEvent: AllocAbsDataSeg (segment type 0)
    data
        state machine / event   segment type    segment ID  start address   length              access attributes   memory type     memory attributes   reserved
        L3                      00h             00h         SSSS            EEEE - SSSS +1      AA                  TT              MM                  00h
        1 octet                 1 octet         1 octet     2 octets        2 octets            1 octet             1 octet         1 octet             1 octet

        Access Attributes   contains the access level of the segment
                            bit 0…3 write access level
                            bit 4…7 read access level
        Memory type         contains the type of the memory of the segment
                            bit 0…2 memory type

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dmp_load_state_machine_write_r_co_mem(xknx: XKNX) -> None:
    """DMP_LoadStateMachineWrite_RCo_Mem — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_LoadStateMachineWrite_RCo_Mem (KNX 03.05.02 §3.31.2) — implementation pending"
    )
