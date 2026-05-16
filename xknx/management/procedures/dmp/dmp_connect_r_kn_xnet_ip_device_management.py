"""
DMP_Connect_R_KNXnetIPDeviceManagement — KNX 03.05.02 §3.2.6 (PDF p. 70).

Spec text (verbatim from spec):

    The Management Client establishes a KNXnet/IP Device Management connection to the KNX IP - or
    KNXnet/IP device. The device shall by this autonomously switch its cEMI communication mode to
    cEMI Transport Layer mode. Further discovery (Device Descriptor, manufacturer…) is then done by
    the classic Application Layer services transferred via cEMI T_Data_Connected and
    T_Data_Individual via KNXnet/IP DEVICE_CONFIGURATION_REQUEST frames.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dmp_connect_r_kn_xnet_ip_device_management(xknx: XKNX) -> None:
    """DMP_Connect_R_KNXnetIPDeviceManagement — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_Connect_R_KNXnetIPDeviceManagement (KNX 03.05.02 §3.2.6) — implementation pending"
    )
