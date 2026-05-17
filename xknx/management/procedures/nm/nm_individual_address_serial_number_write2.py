"""
NM_IndividualAddress_SerialNumber_Write2 — KNX 03.05.02 §2.6 (PDF p. 16).

Spec text (verbatim from spec):

    Use
    NOTE  The beginning of the procedure is identical to the link sequence of PB-Mode. A central Management Client shall
    react to the Start_Link command by sending a Stop_Link. The device shall stop the link sequence.

    At this point the Management Client shall know the KNX Serial Number of the device and shall
    assign the Individual Address with A_IndividualAddressSerialNumber_Write. Finally the Device
    Descriptor shall be read.

    ```mermaid
    sequenceDiagram
        participant S as Sensor
        participant C as Central Unit
        Note left of S: sensor in config mode
        S->>C: CC_Config_Link (Start_Link, manufacturer code, Number of objects)
        Note right of C: enter config mode
        C->>S: CC_Config_Link (Stop_Link)
        Note left of S: leaves config mode
        Note right of C: stop link sequence
        Note right of C: write Individual Address
        C->>S: A_IndividualAddressSerialNumber_Write-PDU (serial_number, new_address)
        C->>S: A_IndividualAddressSerialNumber_Read-PDU (serial_number)
        S->>C: A_IndividualAddressSerialNumber_Response-PDU (serial_number)
        Note right of C: read DD2 (point-to-point)
        C->>S: A_DeviceDescriptor_Read-PDU (descriptor_type = 2)
        S->>C: A_DeviceDescriptor_Response-PDU (descriptor_type = 2, device_descriptor)
        Note right of C: See note a)
    ```

    Notes
    a) In the context of this Management Procedure NM_IndividualAddress_SerialNumber_Write2, the
       A_DeviceDescriptor_Read-service is only applied to check whether the Sensor can be addressed
       using its new Individual Address. The Management Client is only interested in whether it
       receives a response or not; the contents, this is, the value of descriptor_type and device_descriptor
       should not be evaluated at this point.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def nm_individual_address_serial_number_write2(xknx: XKNX) -> None:
    """NM_IndividualAddress_SerialNumber_Write2 — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "NM_IndividualAddress_SerialNumber_Write2 (KNX 03.05.02 §2.6) — implementation pending"
    )
