"""
DMP_InterfaceObjectRead_IP — KNX 03.05.02 §6.5 (PDF p. 186).

Spec text (verbatim from spec):

    Used KNXnet/IP Services
    • DEVICE_CONFIGURATION_REQUEST
      with cEMI-services
      - M_PropRead.req
      - M_PropRead.con
    • DEVICE_CONFIGURATION_ACK
    Preconditions
    It is assumed that any type of KNXnet/IP connection exists to the Management Server with
    Communication Channel ID dmp_CommChannelID.
    Parameters of the Management Procedure
    DMP_InterfaceObjectRead_IP(/* [in] */ mpp_Obj.Type, /* [in] */ mpp_Obj.Inst,
    /* [in] */ mpp_Prop.ID, /* [out] */ mpp_Prop.Value, /* [out] */ mpp_Prop.CurrentNr)
         mpp_Obj.Type:             This Management Procedure Parameter shall hold the Object Type of
                                   the Interface Object in which the Property shall be read.
         mpp_Obj.Inst:             This Management Procedure Parameter shall hold the Instance of the
                                   Interface Object in which the Property shall be read.
         mpp_Prop.ID:              This Management Procedure Parameter shall hold the Property
                                   Identifier of the Property that shall be read.
         mpp_Prop.Value:           This Management Procedure Parameter shall return the value of the
                                   Property that is read.
         mpp_Prop.CurrentNr:       This Management Procedure Parameter shall return the current
                                   number of elements of the Property that is read.

    Variables
        mpp_Obj.NoE                  This shall hold the number of elements of the Property Value that is
                                     read in one call of the cEMI service M_PropRead.req.
        mpp_Obj.SIx:                 This shall hold the start index within the Property Value from which
                                     the Property elements are read.

    Sequence
              KNXnet/IP                                                                      KNXnet/IP
                    Client                                                                   Server
     If the Management Client does not know the number of elements of the Property
     Value array then this has to be read on beforehand 20).
                                        DEVICE_CONFIGURATION_REQUEST
                                  (CommunicationChannel ID = dmp_CommChannelID,
                                 cEMI-Frame = (M_PropRead.req(IOT = mpp_Obj.Type,
                               OI = mpp.Obj.Inst, PID = mpp_Prop.ID, NoE = 1, SIx = 0)

                                                 The Management Server confirms the reception of the request
                                                              with a DEVICE_CONFIGURATION_ACK.
                                         DEVICE_CONFIGURATION_ACK
                                                   (Status)

                                            The Management Server now responds with the number of elements
                                                        with a new DEVICE_CONFIGURATION_REQUEST.
                                     DEVICE_CONFIGURATION_REQUEST
                               (CommunicationChannel ID = dmp_CommChannelID,
                               cEMI-Frame = M_Propread.con(IOT = mpp_Obj.Type,
                              OI = mpp_Obj.Inst, PID = mpp_Prop.ID, NoE = 1, SIx = 0,
                                              Data = mpp_Obj.NoE))

     The Management Client confirms the reception of the response
     with a DEVICE_CONFIGURATION_ACK.
                                      DEVICE_CONFIGURATION_ACK
                                                      (Status)

     The Management Client requests the Property Value
     with a DEVICE_CONFIGURATION_REQUEST.
                                    DEVICE_CONFIGURATION_REQUEST
                              (CommunicationChannel ID = dmp_CommChannelID,
                             cEMI-Frame = (M_PropRead.req(IOT = mpp_Obj.Type,
                                     OI = mpp.Obj.Inst, PID = mpp_Prop.ID,
                                    NoE = mpp_Obj.NoE, SIx = mpp_Obj.SIx)

                                                 The Management Server confirms the reception of the request
                                                              with a DEVICE_CONFIGURATION_ACK.
                                         DEVICE_CONFIGURATION_ACK
                                                   (Status)

    20) This first reading is thus optional. It should only occur if the Management Client does not know the number
       of elements of the Property Value. Specifically, this should be done when the Property Value may be an
       array of which the current number of elements is unknown. By this value and by the knowledge of the
       maximal Frame length in-between the Management Client and the Management Server (see “Discovery of
       maximal Frame length” in [4]), the Management Client may know how many read operations may be
       required and how much data can fit in one single response.

                                                   The Management Server now responds with the Property Value
                                                            with a new DEVICE_CONFIGURATION_REQUEST.
                                        DEVICE_CONFIGURATION_REQUEST
                                   (CommunicationChannel ID = dmp_CommChannelID,
                                   cEMI-Frame = M_Propread.con(IOT = mpp_Obj.Type,
                                         OI = mpp_Obj.Inst, PID = mpp_Prop.ID,
                                        NoE = mpp_Obj.NoE, SIx = mpp_Obj.SIx,
                                               Data = mpp_Prop.Value))

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


async def dmp_interface_object_read_ip(xknx: XKNX) -> None:
    """DMP_InterfaceObjectRead_IP — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_InterfaceObjectRead_IP (KNX 03.05.02 §6.5) — implementation pending"
    )
