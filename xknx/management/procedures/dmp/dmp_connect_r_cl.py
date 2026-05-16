"""
DMP_Connect_RCl — KNX 03.05.02 §3.2.2 (PDF p. 68).

Spec text (verbatim from spec):

    This Management Procedure shall be used to read the Device Descriptor of one Management Server
    (device). It shall allow differentiating between requesting DD0 and DD2 and is capable of handling
    both DD-types expected and unexpected.
    This Management Procedure shall use the point-to-point connectionless communication mode.
    DMP_Connect_RCl (/* [in] */ nm_ASAP, /* [in] */ nm_desc_type_req,
                    /* [out] */ nm_desc_type_res, /* [out] */ nm_desc_value_res)
        nm_ASAP:                               The parameter shall contain the IA of the communication partner of
                                               which the Device Descriptor is to be read.
        nm_desc_type_req:                      This parameter shall contain the requested Device Descriptor Type; it
                                               can be DD0 or DD2.

        nm_desc_type_res:                      This result shall contain the DD-type with which the Management
                                               Server has responded. This may be different from nm_desc_type_req.
                                               Please refer to the exception handling.
        nm_desc_value_res:                     This result shall contain the Device Descriptor value responded by the
                                               Management Server.

    Used Application Layer services for Management
    •     A_DeviceDescriptor_Read

    Sequence
    Management                                                              Management               remark
    Client                                                                  Server

    The Management Client shall send the A_DeviceDescriptor_Read-PDU to the Management
    Server. The ASAP shall equal nm_ASAP.
                            A_DeviceDescriptor_Read-PDU
                         (descriptor_type = nm_desc_type_req)

                          A_DeviceDescriptor_Response-PDU
                         (descriptor_type = nm_desc_type_res,
                        device_descriptor = nm_desc_value_res)

    Exception handling
    There are several error situations when building up a connectionless communication.
    -     If no A_DeviceDescriptor_Response-PDU is received, the Management Server with the Individual
          Address does not exist or the network is not configured correctly.
    -     If more than one A_DeviceDescriptor_Response-PDU is received, there is more than one device
          with the target address.
    If the above indicates the network may be configured incorrectly, than the network topology shall be
    checked. In all other cases, the DM_Connect_RCl may be repeated several times. If this procedure is
    not successful, the depending procedures shall be aborted.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dmp_connect_r_cl(xknx: XKNX) -> None:
    """DMP_Connect_RCl — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_Connect_RCl (KNX 03.05.02 §3.2.2) — implementation pending"
    )
