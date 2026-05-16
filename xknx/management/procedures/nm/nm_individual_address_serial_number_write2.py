"""
NM_IndividualAddress_SerialNumber_Write2 — KNX 03.05.02 §2.6 (PDF p. 17).

Spec text (verbatim from spec):

    Use
    NOTE         The beginning of the procedure is identical to the link sequence of PB-Mode. A central Management Client shall react to the Start_Link command by sending a Stop_Link. The device shall stop the link sequence.

    At this point the Management Client shall know the KNX Serial Number of the device and shall assign the Individual Address with A_IndividualAddressSerialNumber_Write. Finally the Device Descriptor shall be read.

    Sequence diagram shows:
    - Sensor in config mode sends CC_Config_Link (Start_Link, manufacturer code, Number of objects)
    - Central Unit enters config mode and sends CC_Config_Link (Stop_Link)
    - Sensor leaves config mode, stops link sequence
    - Central Unit writes Individual Address with A_IndividualAddressSerialNumber_Write-PDU (serial_number, new_address)
    - Central Unit sends A_IndividualAddressSerialNumber_Read-PDU (serial_number)
    - Management Server responds with A_IndividualAddressSerialNumber_Response-PDU (serial_number)
    - Central Unit reads DD2 (point-to-point) with A_DeviceDescriptor_Read-PDU (descriptor_type = 2)
    - Management Server responds with A_DeviceDescriptor_Response-PDU (descriptor_type = 2, device_descriptor)

    Notes
    a)    In the context of this Management Procedure NM_IndividualAddress_SerialNumber_Write2, the
          A_DeviceDescriptor_Read-service is only applied to check whether the Sensor can be addressed
          using its new Individual Address. The Management Client is only interested in whether it
          receives a response or not; the contents, this is, the value of descriptor_type and device_descriptor
          should not be evaluated at this point.

Inputs (from spec):
    [Implicit: serial_number, new_address; verification uses A_DeviceDescriptor_Read with descriptor_type = 2]
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
