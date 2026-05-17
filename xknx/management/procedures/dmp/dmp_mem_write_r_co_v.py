"""
DMP_MemWrite_RCoV — KNX 03.05.02 §3.16.3 (PDF p. 100).

Spec text (verbatim from spec):

    This Management Procedure shall use the connection oriented communication mode.
    The Verify Mode of the Management Server shall be used.

    Preconditions
    This Management Procedure shall transfer the data in datablocks and transmit these in subsequent
    A_Memory_Read-PDUs and/or A_Memory_Write-PDUs, as specified below, all of which except
    possibly the last PDU, shall have a data field (ASDU) with a size equal to the maximum size that can
    be transported over the communication path consisting of the Management Client, the Management
    Server and Couplers and Routers in between these two.
    - If the Management Server does not support the L_Data_Extended frame format, then this
      maximal size shall be 12 octets.
    - If the Management Server supports L_Data_Extended frames, then the maximal size shall be
      adapted in function of the capabilities of the Management Server and possible Couplers and
      Routers in the communication path to the Management Client. This is specified in [06].

    Used Application Layer Services for Management
    - A_Memory_Write

    Note 12: The delay time depends on the Management Server and on the amount of written octets (see [08]).

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        opt Verify Mode is not active
            opt Property of device control is unknown to the Management Client
                C->>S: A_PropertyDescription_Read-PDU (object_index = DeviceObject, PID = PID_DEVICE_CONTROL)
                S->>C: A_PropertyDescription_Response-PDU (object_index = DeviceObject, PID = PID_DEVICE_CONTROL, type = .., ...)
                Note right of S: A_Disconnect.ind ⇒ error, Property does not exist ⇒ error
            end
            C->>S: A_PropertyValue_Read-PDU (object_index = DeviceObject, PID = PID_DEVICE_CONTROL, start_index = 01h, element_count = 01h)
            S->>C: A_PropertyValue_Response-PDU (object_index = DeviceObject, PID = PID_DEVICE_CONTROL, start_index = 01h, element_count = 01h, data = DDh, ..)
            Note right of S: A_Disconnect.ind ⇒ error, if no data received ⇒ error
            C->>S: A_PropertyValue_Write-PDU (object_index = DeviceObject, PID = PID_DEVICE_CONTROL, start_index = 01h, element_count = 01h, data = DDh, ..)
            Note right of S: In the data (DD) bit 2 (Verify Mode) has to be set.
            S->>C: A_PropertyValue_Response-PDU (object_index = DeviceObject, PID = PID_DEVICE_CONTROL, start_index = 01h, element_count = 01h, data = XX, ..)
            Note right of S: A_Disconnect.ind ⇒ error, if verify = enabled and different or no data received ⇒ error
        end
        loop for each data block (data size ≤ maximal size), until all data are transmitted
            C->>S: A_Memory_Write-PDU (Addr, Length, Data)
            S->>C: A_Memory_Response (Addr, Length, Data)
            Note right of S: A_Disconnect.ind ⇒ error, if verify = enabled and different or no data received ⇒ error
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


async def dmp_mem_write_r_co_v(xknx: XKNX) -> None:
    """DMP_MemWrite_RCoV — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_MemWrite_RCoV (KNX 03.05.02 §3.16.3) — implementation pending"
    )
