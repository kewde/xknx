"""
DMP_PeiTypeRead_RCo_ADC — KNX 03.05.02 §3.15.2 (PDF p. 97).

Spec text (verbatim from spec):

    This Management Procedure shall use the connection oriented communication mode.
    The value shall be read via the service A_ADC_Read.
    Used Application Layer Services for Management
        •      A_ADC_Read

    Sequence
    Management                                                             Management                 remark
    Client                                                                 Server
                                 A_ADC_Read-PDU
                              (AD-channel = 4, count = 1)

                                A_ADC_Response-PDU                                      A_Disconnect.ind ⇒
                                  (AD-channel, Data)                                    error,
                                                                                        no data received ⇒ error

    The formula to calculate the PEI type is:

                                                        10 ⋅ ADC _ Value + 60
                                       PEI _ Type =
                                                                128
    Exception handling
    The general exception handling shall apply.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dmp_pei_type_read_r_co_adc(xknx: XKNX) -> None:
    """DMP_PeiTypeRead_RCo_ADC — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_PeiTypeRead_RCo_ADC (KNX 03.05.02 §3.15.2) — implementation pending"
    )
