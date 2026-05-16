"""
NM_DomainAddress_Scan2 — KNX 03.05.02 §2.14.1.2.2 (PDF p. 28).

Spec text (verbatim from spec):

    Use
    This Management Procedure shall be used by a Management Client to scan for the presence of any
    devices with a 6 octet Domain Address that lies within a given range.
    It returns whether or not there are any devices with a Domain Address in the scanned range. The
    devices respond with their Individual Address in the Source Address field of the responses, so the
    Individual Addresses are known by this as well. Additionally, on KNX RF, as the devices shall
    respond in system broadcast communication mode, the AET shall be 0 and the response shall contain
    the KNX Serial Number of the responding device. This is actually the key data retrieved by this
    procedure.
    The MaC shall not execute this Management Procedure with values of any DoA in which the MSB
    differs from 00h.
    Used Application Layer Services for management
    • A_DomainAddressSelective_Read
      (please note that this service responds with the A_DomainAddress_Response-PDU).
    Parameters of the Management Procedure
    NM_DomainAddress_Scan2(/* [in] */ mpp_DoA_start, /* [in] */ mpp_DoA_end,
    /* [out] */ mmp_KNX_SN[],/* [out] */ mmp_IA[], /* [out] */ mpp_DoA_response[])
        mpp_DoA_start:                         This shall be lower limit of the range of Domain Addresses in
                                               which the presence of devices shall be searched.
        mpp_DoA_end:                           This shall be upper limit of the range of Domain Addresses in
                                               which the presence of devices shall be searched.
        mpp_KNX_SN[]:                          This shall be the collection of all KNX Serial Number values that
                                               have been used by the responding devices.
        mpp_IA[]:                              This shall be the collection of all Individual Address values that
                                               have been used by the responding devices.
        mpp_DoA_response[]:                    This shall be the DoA with which the Management Server has
                                               responded. There can be 0, 1 or multiple answers with the same
                                               of different DoA-values.

    The A_DomainAddressSelective_Read-PDU shall be transmitted with priority System.
    Management                                                                  Management
    Client                                                                      Server (device)

                        A_DomainAddressSelective_Read-PDU
                 (type = 01h, domain_address_start = mmp_DoA_start
                        domain_address_end = mpp_DoA_end)

                                           If the Management Server finds the conditions for replying to the message fulfilled,
                                                                                              then it shall transmit a response.
                          A_DomainAddress_Response-PDU
                        (mpp_DoA_response= domain_address)

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def nm_domain_address_scan2(xknx: XKNX) -> None:
    """NM_DomainAddress_Scan2 — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "NM_DomainAddress_Scan2 (KNX 03.05.02 §2.14.1.2.2) — implementation pending"
    )
