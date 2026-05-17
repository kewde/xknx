"""
DMP_DownloadLoadablePart_RCo_IO — KNX 03.05.02 §3.31.4 (PDF p. 141).

Spec text (verbatim from spec):

    3.31.4.1 Normal conditions
    This method shall use the connection oriented or connectionless remote communication.

    Used Application Layer Services for Management
    - A_PropertyValue_Write
    - A_PropertyValue_Read

    Complete Download Sequence for one loadable part 15)

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        C->>S: A_PropertyValue_Write-PDU (object_index, Property_id = 5, start_index = 01h, nr_of_elem = 01h,Data = 04 00 …)
        Note right of S: Unload
        Note left of C: This part is optional
        S->>C: A_PropertyValue_Response –PDU (object_index, Property_id=5, start_index = 01h, nr_of_elem = 01h, data = 00)
        Note right of S: Load State Machine shall changes to Unload (00h)
        Note over C,S: If data is equal 04 (unloading) read Property and verify value if data is equal 00 (unloaded) continue else break with error
        Note right of S: Retry read Property for 30 Seconds.
        Note over C,S: 15) The optional state Unloading is not used.
        C->>S: A_PropertyValue_Write-PDU (object_index, Property_id = 5, start_index = 01h, nr_of_elem = 01h, data = 01 00 …)
        Note right of S: Start loading
        S->>C: A_PropertyValue_Response –PDU (object_index, Property_id=5, start_index = 01h, nr_of_elem = 01h, data = 02)
        Note right of S: Load State Machine shall change to Loading.
        Note over C,S: if data is not equal 02 break with error
        Note left of C: This part is optional and may repeated for different additional load controls
        C->>S: A_PropertyValue_Write-PDU (object_index, Property_id = 5, start_index = 01h, nr_of_elem = 01h, data = 03 … …)
        Note right of S: Additional load controls
        S->>C: A_PropertyValue_Response –PDU (object_index, Property_id=5, start_index = 01h, nr_of_elem = 01h, data = 02)
        Note right of S: Load State Machine shall stay in the state Loading.
        Note over C,S: if data is not equal 02 break with error
        Note over C,S: Load the loadable data via Property access or memory access
        C->>S: A_PropertyValue_Write-PDU (object_index, Property_id = 5, start_index = 01h, nr_of_elem = 01h, data = 02 00 … …)
        Note right of S: Load complete Time-out?
        S->>C: A_PropertyValue_Response –PDU (object_index, Property_id=5, start_index = 01h, nr_of_elem = 01h, data = 01)
        Note right of S: Load State Machine shall change to the state Loaded.
        Note over C,S: if data is not equal 01 break with error
    ```

    3.31.4.2 Error and exception handling
    The general exception handling shall apply.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dmp_download_loadable_part_r_co_io(xknx: XKNX) -> None:
    """DMP_DownloadLoadablePart_RCo_IO — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_DownloadLoadablePart_RCo_IO (KNX 03.05.02 §3.31.4) — implementation pending"
    )
