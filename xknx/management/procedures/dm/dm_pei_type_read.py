"""
DM_PeiTypeRead — KNX 03.05.02 §3.15 (PDF p. 97).

Spec text (verbatim from spec):

    3.15.1 Use
    This device Management Procedure shall read the current PEI type of the device and store the value in
    the specified data block.
    A DM_Connect shall be executed before executing this Management Procedure.

    DM_PeiTypeRead (flags, dataBlockStartAddress, data)
        flags                  bit 0 location of data
                                   0: in data block
                                   1: -
                               All other bits are reserved. These shall be set to 0. This shall be
                               tested by the Management Client.
        dataBlockStartAddress  specifies the address where the data are located in the data block.
        data                   the data read by this Management Procedure

    3.15.2 Procedure: DMP_PeiTypeRead_RCo_ADC
    This Management Procedure shall use the connection oriented communication mode.
    The value shall be read via the service A_ADC_Read.

    Used Application Layer Services for Management
    - A_ADC_Read

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        C->>S: A_ADC_Read-PDU (AD-channel = 4, count = 1)
        S->>C: A_ADC_Response-PDU (AD-channel, Data)
        Note right of S: A_Disconnect.ind ⇒ error, no data received ⇒ error
    ```

    The formula to calculate the PEI type is:

        PEI_Type = (10 · ADC_Value + 60) / 128

    Exception handling
    The general exception handling shall apply.

    3.15.3 Procedure: DMP_PeiTypeRead_R_IO
    This Management Procedure shall use the connection oriented or connectionless communication
    mode.
    The value shall be read via the Interface Objects.

    Used Application Layer Services for Management
    - A_PropertyDescription_Read
    - A_PropertyValue_Read

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        opt Property of management control is unknown to the Management Client
            C->>S: A_PropertyDescription_Read-PDU (object_index = DeviceObject, PID = PID_PEI_TYPE)
            S->>C: A_PropertyDescription_Response-PDU (object_index = DeviceObject, PID = PID_PEI_TYPE, type = .., ...)
            Note right of S: A_Disconnect.ind ⇒ error, Property does not exist ⇒ error
        end
        C->>S: A_PropertyValue_Read-PDU (object_index = DeviceObject, PID = PID_PEI_TYPE, start_index = 01H, element_count = 01h)
        S->>C: A_PropertyValue_Response-PDU (object_index = DeviceObject, PID = PID_PEI_TYPE, start_index = 01H, element_count = 01h, data = PEI-Type)
        Note right of S: A_Disconnect.ind ⇒ error, no data received ⇒ error
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


async def dm_pei_type_read(xknx: XKNX) -> None:
    """DM_PeiTypeRead — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DM_PeiTypeRead (KNX 03.05.02 §3.15) — implementation pending"
    )
