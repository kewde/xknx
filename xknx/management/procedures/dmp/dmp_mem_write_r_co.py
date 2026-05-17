"""
DMP_MemWrite_RCo — KNX 03.05.02 §3.16.2 (PDF p. 99).

Spec text (verbatim from spec):

    Use
    This Management Procedure shall use the connection oriented communication mode.
    The Verify Mode of the Management Server shall not be used.

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
    - A_Memory_Read

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        loop for each datablock (data size ≤ maximal size), until all data are transmitted
            C->>S: A_Memory_Write-PDU (Addr, Length, Data)
            alt verify = enabled
                C->>S: A_Memory_Read-PDU (Addr, Length)
                S->>C: A_Memory_Response-PDU (Addr, Length, Data)
                Note right of S: A_Disconnect.ind ⇒ error, different or no data received ⇒ error
            else verify = disabled
                Note over C: delay for programming the memory in the device
            end
        end
    ```

    Note 12: The delay time depends on the Management Server and on the amount of written octets (see [08]).

    Exception handling
    The general exception handling shall apply.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from xknx.exceptions import ManagementConnectionError
from xknx.telegram import apci

if TYPE_CHECKING:
    from xknx.management.management import P2PConnection

DEFAULT_MAX_CHUNK_SIZE = 12


async def dmp_mem_write_r_co(
    connection: P2PConnection,
    address: int,
    data: bytes,
    verify: bool = False,
    write_delay: float = 0,
    max_chunk_size: int = DEFAULT_MAX_CHUNK_SIZE,
) -> None:
    """
    Write a contiguous block of data to device memory.

    DMP_MemWrite_RCo — KNX 03.05.02 §3.16.2. Requires an established
    connection (DM_Connect must be executed first).

    :param connection: Active P2P connection to the device
    :param address: Start address in device memory (0-65535)
    :param data: Data to write
    :param verify: If True, read back and verify each chunk after writing
    :param write_delay: Delay in seconds after each write when verify=False.
        Required for device to finish programming. Value is device-dependent
        (see KNX spec [08]). Ignored when verify=True.
    :param max_chunk_size: Max bytes per request (default 12 for standard frames)
    :raises ManagementConnectionError: If verify is enabled and readback differs
    """
    if not data:
        return

    remaining = memoryview(data)
    current_address = address

    while remaining:
        chunk = bytes(remaining[:max_chunk_size])
        await connection._send_data(apci.MemoryWrite(address=current_address, data=chunk))  # noqa: SLF001

        if verify:
            response = await connection.request(
                payload=apci.MemoryRead(address=current_address, count=len(chunk)),
                expected=apci.MemoryResponse,
            )
            if response.payload.data != chunk:
                raise ManagementConnectionError(
                    f"Memory verify failed at address 0x{current_address:04X}: "
                    f"expected {chunk.hex()}, got {response.payload.data.hex()}"
                )
        elif write_delay > 0:
            await asyncio.sleep(write_delay)

        current_address += len(chunk)
        remaining = remaining[max_chunk_size:]
