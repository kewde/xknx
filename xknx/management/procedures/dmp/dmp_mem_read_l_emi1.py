"""
DMP_MemRead_LEmi1 — KNX 03.05.02 §3.18.3 (PDF p. 106).

Spec text (verbatim from spec):

    This Management Procedure shall use the local communication with EMI 1.

    Used EMI-services for Management
    - PC_Get_Value

    Parameters of the Management Procedure
    DMP_MemRead_LEmi1(/* [in] */ DmpStartAddr, /* [in] */ DmpEndAddr, /* [out] */ DmpData,
    /* [out] */ DmpError)
        DmpStartAddress:    The start address of the memory of the device from which the Data
                            shall be read.
        DmpEndAddress:      The end address of the memory of the device from which the Data
                            shall be read.
        DmpData:            The contents of the memory as returned by the device.
        DmpError:           Possible error indication.

    Service parameters
        SrvDataOut:     The data as read from the device for each call of the service
                        PC_Get_Value.
        SrvDBLen:       The length of the datablock that shall be in one call of the service
                        PC_Get_Value. This shall be 12 octets for all datablocks except for the
                        last one, which may be smaller.
        SrvDBAddr:      The start address in the memory of the device from which the current
                        datablock shall be read.

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        loop for each data block (≤12 octet), until all data are transmitted
            C->>S: PC_Get_Value.req message (Length = SrvDBLen, Addr = SrvDBAddr)
            S->>C: PC_Get_Value.con (Length = SrvDBLen, Addr = SrvDBAddr, Data = SrvDataOut)
            Note right of S: no data received ⇒ error
        end
    ```

    Exception handling
    The general exception handling shall apply.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dmp_mem_read_l_emi1(xknx: XKNX) -> None:
    """DMP_MemRead_LEmi1 — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_MemRead_LEmi1 (KNX 03.05.02 §3.18.3) — implementation pending"
    )
