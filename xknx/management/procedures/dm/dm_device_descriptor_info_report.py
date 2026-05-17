"""
DM_DeviceDescriptor_InfoReport — KNX 03.05.02 §3.2.7 (PDF p. 70).

Spec text (verbatim from spec):

    Use
    This Management Procedure shall be used to spontaneously send a Device Descriptor value. This
    procedure is typically spontaneously executed by the Manegement Server (device) and not by the
    Management Client!
    On KNX RF, the A_DeviceDescriptor_InfoReport-PDU shall betransmitted in a RF
    AddrExtensionType = 0; the frame shall then contain the KNX Serial Number of the sender.
    Used Application Layer Services for Management
    - A_DeviceDescriptor_InfoReport

    Parameters of the Management Procedure
    DM_DeviceDescriptor_InfoReport (/* [in] */ DM_DDType, /* [in] */ DM_DD)
        DM_DDType    type of the Device Descriptor
        DM_DD        the Device Descriptor of the device
    This Management Procedure shall use the system broadcast communication mode.

    Sequence

    ```mermaid
    sequenceDiagram
        participant S as Management Server
        participant C as Management Client
        Note right of C: Set client in teaching mode.
        S->>C: A_DeviceDescriptor_InfoReport-PDU (descriptor_type = DM_DDType, device_descriptor = DM_DD)
    ```

    Error and exception handling
    Not applicable.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dm_device_descriptor_info_report(xknx: XKNX) -> None:
    """DM_DeviceDescriptor_InfoReport — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DM_DeviceDescriptor_InfoReport (KNX 03.05.02 §3.2.7) — implementation pending"
    )
