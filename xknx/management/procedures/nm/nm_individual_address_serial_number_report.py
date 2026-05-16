"""
NM_IndividualAddress_SerialNumber_Report — KNX 03.05.02 §2.22.4 (PDF p. 52).

Spec text (verbatim from spec):

    Use
    This Management Procedure shall be used by a Management Server in order to announce its (new)
    Individual Address. The Management Server shall be identified by its KNX Serial Number.
    The communication mode shall be broadcast. The hop_count_type shall be the default Network Layer
    value. The priority shall be set to "system".
    NOTE      Most E-Mode devices that support this Management Procedure will have a KNX Serial Number and may report.

    Used Application Layer messages for Management
     • A_NetworkParameter_Write

    Parameters of the Management Procedure
    NM_IndividualAddress_SerialNumber_Report(Device_SN)
          Device_SN                            KNX Serial Number of the device that reports its Individual Address

    Sequence:
       Management                                                                 Management
            Client                                                                Server          remark
                              A_NetworkParameter_Write-PDU
                                      (comm_mode = broadcast,
                               hop_count_type = default NL parameter,
                                   object_type = 0 = Device Object,
                     Property_id = PID_ADDR_REPORT = 60, priority = system,
                                         value = Device_SN)

Inputs (from spec):
    [in] Device_SN
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def nm_individual_address_serial_number_report(xknx: XKNX) -> None:
    """NM_IndividualAddress_SerialNumber_Report — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "NM_IndividualAddress_SerialNumber_Report (KNX 03.05.02 §2.22.4) — implementation pending"
    )
