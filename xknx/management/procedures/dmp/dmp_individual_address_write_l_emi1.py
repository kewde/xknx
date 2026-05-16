"""
DMP_IndividualAddressWrite_LEmi1 — KNX 03.05.02 §3.10.2 (PDF p. 91).

Spec text (verbatim from spec):

    This Management Procedure shall use the local communication with EMI 1.

    Used EMI-services for Management
     • PC_Get_Value
     • PC_Set_Value

    Parameters of the Management Procedure
    DMP_IndividualAddressWrite_LEmi1(/* [in] */ IAnew, /* [out] */ IAresult)
        IAnew:                                 The Individual Address that shall be written in the device.
        IAresult:                              The Individual Address as read back from the device after writing
                                               IAnew

    Sequence
    Management                                                            Management                 remark
    Client                                                                Server

                             PC_Set_Value.req message
                     (Length = 2, Address = 0117h, Data = IAnew)

                               PC_Get_Value.req message
                             (Length = 2, Address = 0117h,)

                             PC_Get_Value.con message                                  If IAresult differs from IAnew
                    (Length = 2, Address = 0117h, Data = IAresult)                     or if no data received ⇒ error

    Exception handling
    The general exception handling shall apply.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dmp_individual_address_write_l_emi1(xknx: XKNX) -> None:
    """DMP_IndividualAddressWrite_LEmi1 — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_IndividualAddressWrite_LEmi1 (KNX 03.05.02 §3.10.2) — implementation pending"
    )
