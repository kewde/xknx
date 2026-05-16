"""
DMP_ExtFunctionProperty_Write_R — KNX 03.05.02 §3.30.2 (PDF p. 131).

Spec text (verbatim from spec):

    This Management Procedure shall use the connection oriented or connectionless communication
    mode.
    Used Application Layer Services for Management
        •   A_FunctionPropertyExtCommand

    Sequence
    Management                                                             Management
    Client                                                                 Server

                       A_ FunctionPropertyExtCommand-PDU
                  (object_type = OT, object_instance = OI, PID = PP,
                                  data = command)

                                                                                        The Management Server
                     A_FunctionPropertyExtState_Response-PDU                            shall execute the Function
                  (object_type = OT, object_instance = OI, PID = PP,                    Property and return the
                         return_code = RC, data = output data)                          result and error indication
                                                                                        to the Management Client

    Exception handling
    The error shall be Function Property specific and is specified in [05]. The handling of this error
    depends on the Configuration Procedure in which this Management Procedure is used.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dmp_ext_function_property_write_r(xknx: XKNX) -> None:
    """DMP_ExtFunctionProperty_Write_R — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_ExtFunctionProperty_Write_R (KNX 03.05.02 §3.30.2) — implementation pending"
    )
