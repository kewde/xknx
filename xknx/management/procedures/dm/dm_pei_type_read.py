"""
DM_PeiTypeRead — KNX 03.05.02 §3.15 (PDF p. 97).

Spec text (verbatim from spec):

    3.15.1 Use
    This device Management Procedure shall read the current PEI type of the device and store the value in
    the specified data block.
    A DM_Connect shall be executed before executing this Management Procedure.
    DM_PeiTypeRead                              (flags, dataBlockStartAddress, data)
            flags                       bit 0   location of data
                                                   0: in data block
                                                   1: -
                                        All other bits are reserved. These shall be set to 0. This shall be
                                        tested by the Management Client.
            dataBlockStartAddress       specifies the address where the data are located in the data block.
            data                        the data read by this Management Procedure

    3.15.2 Procedure: DMP_PeiTypeRead_RCo_ADC
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

    3.15.3 Procedure: DMP_PeiTypeRead_R_IO
    This Management Procedure shall use the connection oriented or connectionless communication
    mode.
    The value shall be read via the Interface Objects.
    Used Application Layer Services for Management
        •     A_PropertyDescription_Read
        •     A_PropertyValue_Read

    Sequence
    Management                                                            Management                remark
    Client                                                                Server
    if Property of management control is unknown to the Management Client
                          A_PropertyDescription_Read-PDU
                (object_index = DeviceObject, PID = PID_PEI_TYPE)

                        A_PropertyDescription_Response-PDU                             A_Disconnect.ind ⇒ error,
                 (object_index = DeviceObject, PID = PID_PEI_TYPE,                     Property does not exist ⇒
                                     type = .. , ...)                                  error

    endif
                              A_PropertyValue_Read-PDU
                 (object_index = DeviceObject, PID = PID_PEI_TYPE,
                        start_index = 01H, element_count = 01h)

                           A_PropertyValue_Response-PDU                                A_Disconnect.ind ⇒ error,
                 (object_index = DeviceObject, PID = PID_PEI_TYPE,                     no data received ⇒ error
                        start_index = 01H, element_count = 01h,
                                    data = PEI-Type)

    endfor

    Exception handling
    The general exception handling shall apply.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dm_pei_type_read(xknx: XKNX) -> None:
    """DM_PeiTypeRead — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DM_PeiTypeRead (KNX 03.05.02 §3.15) — implementation pending"
    )
