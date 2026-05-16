"""
DMP_LoadStateMachineWrite_RCo_IO — KNX 03.05.02 §3.31.3 (PDF p. 137).

Spec text (verbatim from spec):

    This Management Procedure shall use the connection oriented communication mode.
    The control and state of the Load State Machine shall be located in Interface Objects of the
    Management Server and shall be accessible via Property services.
    The Management Client shall search the according Interface Object in the Management Server.
    Used Application Layer Services for Management
        •      A_PropertyDescription_Read
        •      A_PropertyValue_Write

    Sequence
    Management                                                            Management                remark
    Client                                                                Server
    if Property of management control is unknown to the Management Client
                        A_PropertyDescription_Read-PDU
                                (object_index = X,
                     PID = PID_LOAD_STATE_CONTROL)

                        A_PropertyDescription_Response-PDU                             A_Disconnect.ind ⇒ error,
                                  (object_index = X,                                   Property does not exist ⇒
                       PID = PID_LOAD_STATE_CONTROL,                                   error
                             type = PDT_CONTROL, ...)

    endif
                            A_PropertyValue_Write-PDU
                                  (object_index = X,
                       PID = PID_LOAD_STATE_CONTROL,
                         start_index = 1, element_count = 1,
                               data = depends on event)

                           A_PropertyValue_Response-PDU                                A_Disconnect.ind ⇒ error,
                                   (object_index = X,                                  Wrong state ⇒ error
                       PID = PID_LOAD_STATE_CONTROL,
                 start_index = 1, element_count = 1, data = loadstate)

    The transmitted data depend on the event.

    3.31.3.1 LoadEvent: Unload (write)
    data
      event                                              reserved
       04h                                                  00h
     1 octet                                              9 octets

    This command shall unload a loadable part. All data shall be declared as invalid. The Load State
    Machine shall change to Unloaded.

    3.31.3.2 LoadEvent: Start Loading (write)
    data
      event                                               reserved
       01h                                                    00h
     1 octet                                              9 octets

    This command shall start the loading of the loadable part. The Load State Machine shall change to
    Loading.

    3.31.3.3 LoadEvent: LoadCompleted (write)
    data
      event                                               reserved
       02h                                                    00h
     1 octet                                              9 octets

    This command shall complete the loading of the loadable part. The checksum shall be calculated; all
    data shall be declared as valid and the Load State Machine shall change to Loaded. In case of
    download of an executable part, this executable part shall be started if the other run conditions are
    fulfilled.

    3.31.3.4 Load Control: Additional Load Controls (Write)
          Type                                                                    If data less than 8 octets:
                           Subtype                 Data
       = Additional                                                                        Fill octets

             03h             xx       Data depending on the sub type           .. 00h 00h 00h 00h 00h 00h 00h

            1 octet        1 octet                                     8 octets

    Please refer to [14] for the requirements on which subtype shall be supported per Profile.
           • LoadEvent: AllocAbsDataSeg (segment type 0)
    data
                segment                                               access memory memory
      event                  start address           length                                     reserved
                  type                                               attributes type attributes
       03h         00h            SSSS          EEEE - SSSS +1            AA        TT        MM         00h
     1 octet     1 octet          2 octet           2 octet           1 octet     1 octet   1 octet    1 octet
    This load event shall serve for the absolute allocation of data or code.

     Access Attributes           contains the access level of the segment
                                         bit 0…3 write access level
                                         bit 4…7 read access level
     Memory type                 contains the type of the memory of the segment
                                         bit 0…2 memory type

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dmp_load_state_machine_write_r_co_io(xknx: XKNX) -> None:
    """DMP_LoadStateMachineWrite_RCo_IO — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_LoadStateMachineWrite_RCo_IO (KNX 03.05.02 §3.31.3) — implementation pending"
    )
