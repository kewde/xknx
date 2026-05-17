"""
DMP_MemWrite_LEmi1 — KNX 03.05.02 §3.16.4 (PDF p. 102).

Spec text (verbatim from spec):

    This Management Procedure shall use the local communication with EMI 1.

    Used EMI-services for Management
    - PC_Get_Value
    - PC_Set_Value

    Parameters of the Management Procedure
    DMP_MemWrite_LEmi1(/* [in] */ DmpStartAddr, /* [in]*/ DmpEndAddr, /* [in]*/ DmpData,
                       /* [out] */ DmpError)
        DmpStartAddr    The start address in the memory of the device into which the Data
                        shall be written.
        DmpEndAddr      The end address in the memory of the device into which the Data shall
                        be written.
        DmpData         The Data to be written in the device.
        DmpError        Possible error indication.

    Service parameters
        SrvDataIn       The data that shall be written in the device in one call of the service
                        PC_Set_Value.
        SrvDataOut      The data as read back from the device for each call of the service
                        PC_Set_Value.
        SrvDBLen        The length of the datablock written in one call of the service
                        PC_Set_Value. This shall be 12 octets for all datablocks except for the
                        last one, which may be smaller.
        SrvDBAddr       The start address in the memory of the device where the current
                        datablock shall be written.

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        loop for each datablock (≤12 octet), until all data are transmitted
            C->>S: PC_Set_Value.req message (Length = SrvDBLen, Address = SrvDBAddr, Data = SrvDBIn)
            alt verify = enabled
                C->>S: PC_Get_Value.req message (Length = SrvDBLen, Address = SrvDBAddr)
                S->>C: PC_Get_Value.con message (Length = SrvDBLen, Address = SrvDBAddr, Data = SrvDBOut)
                Note right of S: If SrvDBOut differs from SrvDBIn or if no data received ⇒ error
            else verify = disabled
                Note over C: delay for programming the memory in the device
            end
        end
    ```

    Note 13: The delay time depends on the Management Server and on the amount of written octets (see [08]).

    Exception handling
    The general exception handling shall apply.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dmp_mem_write_l_emi1(xknx: XKNX) -> None:
    """DMP_MemWrite_LEmi1 — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_MemWrite_LEmi1 (KNX 03.05.02 §3.16.4) — implementation pending"
    )
