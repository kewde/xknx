"""
DMP_MemRead_RCo — KNX 03.05.02 §3.18.2 (PDF p. 106).

Spec text (verbatim from spec):

    This Management Procedure shall use the connection oriented communication mode.

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
    - A_Memory_Read

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        loop for each data block (data size ≤ maximal size), until all data are transmitted
            C->>S: A_Memory_Read-PDU (Addr, Length)
            S->>C: A_Memory_Response-PDU (Addr, Length, Data)
            Note right of S: A_Disconnect.ind ⇒ error, no data received ⇒ error
        end
    ```

    Exception handling
    The general exception handling shall apply.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from xknx.telegram import apci

if TYPE_CHECKING:
    from xknx.management.management import P2PConnection

DEFAULT_MAX_CHUNK_SIZE = 12


async def dmp_mem_read_r_co(
    connection: P2PConnection,
    address: int,
    count: int,
    max_chunk_size: int = DEFAULT_MAX_CHUNK_SIZE,
) -> bytes:
    """
    Read a contiguous block of memory from a KNX device.

    DMP_MemRead_RCo — KNX 03.05.02 §3.18.2. Requires an established
    connection (DM_Connect must be executed first).

    :param connection: Active P2P connection to the device
    :param address: Start address in device memory (0-65535)
    :param count: Number of bytes to read
    :param max_chunk_size: Max bytes per request (default 12 for standard frames)
    :return: The data read from device memory
    """
    if count <= 0:
        return b""

    data = bytearray()
    remaining = count
    current_address = address

    while remaining > 0:
        chunk_size = min(remaining, max_chunk_size)
        response = await connection.request(
            payload=apci.MemoryRead(address=current_address, count=chunk_size),
            expected=apci.MemoryResponse,
        )
        data.extend(response.payload.data)
        current_address += chunk_size
        remaining -= chunk_size

    return bytes(data)
