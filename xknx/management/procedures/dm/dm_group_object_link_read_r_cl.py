"""
DM_GroupObjectLink_Read_RCl — KNX 03.05.02 §3.37.2 (PDF p. 158).

Spec text (verbatim from spec):

    Used Application Layer Services for Management
     • A_Link_Read

    Parameters of the Management Procedure
    DM_GroupObjectLink_Read_RCl(/* [in] */ GO.number, /* [out] */ GO.sendingindex,
       /* [out] */ GO.GAList)
        GO.number:                             Number of the Group Object from which the associated Group
                                               Addresses shall be read.
        GO.sendingindex:                       The index of the sending Group Address for this Group Object as
                                               returned by the Management Server (device).
        GO.GAList                              The list of all Group Addresses associated to the Group Object as
                                               returned by the Management Server (device)

       Variables
        start_index_loop:                      The Management Client shall start reading the Group Addresses
                                               associated to the Group Object in the Management Server starting
                                               from the 1st one in the list, with start_index =start_index°loop 1. If an
                                               response is received from the Management Server with 6 Group
                                               Addresses, then the request shall be repeated: start_index_loop shall
                                               be incremented by 6 and used as start_index for the next call of the
                                               A_Link_Read-service by the Management Client
        group_address_set:                     A set of 6 or less GAs returned by the Management Server (device) in
                                               one A_Link_Response-PDU.
                                               The Management Client collects all these responses of one or more
                                               iterations in GO.GAList

    Sequence
    Management                                                              Network /                remark
    Client                                                                  Management
                                                                            Server
    start_index = 1
    repeat
                                A_Link_Read-PDU
                 (group_object_number = GO.number, start_index = )

                               A_Link_Response-PDU
                         (group_object_number = GO.number,
                         sending_addresss = GO.sendingindex,
                                   start_address = ,
                        group_address_list = group_address_set)

       The Management Server adds the received group_address_set
       to the GO.GAList.
    until a negative response is returned (start_index = 0) or less than

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dm_group_object_link_read_r_cl(xknx: XKNX) -> None:
    """DM_GroupObjectLink_Read_RCl — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DM_GroupObjectLink_Read_RCl (KNX 03.05.02 §3.37.2) — implementation pending"
    )
