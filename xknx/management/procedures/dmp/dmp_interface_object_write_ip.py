"""
DMP_InterfaceObjectWrite_IP — KNX 03.05.02 §6.4 (PDF p. 185).

Spec text (verbatim from spec):

    Used KNXnet/IP Services
    • DEVICE_CONFIGURATION_REQUEST
      with cEMI-services
      - M_PropWrite.req
      - M_PropWrite.con
    • DEVICE_CONFIGURATION_ACK
    Preconditions
    It is assumed that any type of KNXnet/IP connection exists to the Management Server with
    Communication Channel ID dmp_CommChannelID.
    Parameters of the Management Procedure
    DMP_InterfaceObjectWrite_IP(/* [in] */ mpp_Obj.Type, /* [in] */ mpp_Obj.Inst,
    /* [in] */ mpp_Prop.ID, /* [in] */ mpp_Prop.Value, /* [in] */ mpp_Prop.StartIndex,
    /* [in] */ = mpp_Prop.NrOfElem, /* [out] */ = mpp_ErrorCode)
         mpp_Obj.Type:             This Management Procedure Parameter shall hold the Object Type of
                                   the Interface Object in which the Property shall be written.
         mpp_Obj.Inst:             This Management Procedure Parameter shall hold the Instance of the
                                   Interface Object in which the Property shall be written.
         mpp_Prop.ID:              This Management Procedure Parameter shall hold the Property
                                   Identifier of the Property that shall be written.
         mpp_Prop.Value:           This Management Procedure Parameter shall hold the value of the
                                   Property that is shall be written.
         mpp_Prop.StartIndex:      This Management Procedure Parameter shall hold the start index
                                   within the Property value from which index onwards the Property
                                   value shall be written.
         mpp_Prop.NrOfElem:        This Management Procedure Parameter shall hold the number of
                                   Property array elements that shall be written.
         mpp_ErrorCode:            This Management Procedure Parameter shall return the Error Code
                                   that may be returned by the Management Server.

    Variables
          mpp_Obj.NoE                This shall hold the number of elements of the Property Value that is
                                     written in one call of the cEMI service M_PropWrite.req.
          mpp_Obj.SIx:               This shall hold the start index within the Property Value from which
                                     the Property elements are written.

    Sequence
              KNXnet/IP                                                                 KNXnet/IP
                    Client                                                              Server
     The Management Client writes the Property Value
     with a DEVICE_CONFIGURATION_REQUEST.
     For each data block until all data are transferred
                                        DEVICE_CONFIGURATION_REQUEST
                                  (CommunicationChannel ID = dmp_CommChannelID,
                                cEMI-Frame = (M_PropWrite.req(IOT = mpp_Obj.Type,
                                          OI = mpp.Obj.Inst, PID = mpp_Prop.ID,
                                        NoE = mpp_Obj.NoE, SIx = mpp_Obj.SIx)

                                                 The Management Server confirms the reception of the request
                                                              with a DEVICE_CONFIGURATION_ACK.
                                         DEVICE_CONFIGURATION_ACK
                                                   (Status)

                                                 The Management Server now responds with the Property Value
                                                         with a new DEVICE_CONFIGURATION_REQUEST.
                                     DEVICE_CONFIGURATION_REQUEST
                                 (CommunicationChannel ID = dmp_CommChannelID,
                                cEMI-Frame = M_PropWrite.con(IOT = mpp_Obj.Type,
                                      OI = mpp_Obj.Inst, PID = mpp_Prop.ID,
                                     NoE = mpp_Obj.NoE, SIx = mpp_Obj.SIx,
                                          mpp_ErrorCode = Error Code))

     The Management Client confirms the reception of the response
     with a DEVICE_CONFIGURATION_ACK.
                                      DEVICE_CONFIGURATION_ACK
                                                      (Status)

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dmp_interface_object_write_ip(xknx: XKNX) -> None:
    """DMP_InterfaceObjectWrite_IP — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_InterfaceObjectWrite_IP (KNX 03.05.02 §6.4) — implementation pending"
    )
