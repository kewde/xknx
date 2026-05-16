"""
DM_GroupObjectLink_Write_RCl — KNX 03.05.02 §3.37.3 (PDF p. 159).

Spec text (verbatim from spec):

    Used Application Layer Services for Management
     • A_Link_Write
    Parameters of the Management Procedure
    DM_GroupObjectLink_Write_RCl(/* [in] */ GO.number, /* [in] */ GO.action, /* [in] */ GO.sending,
       /* [in] */ GO.value, /* [out] */ GO.sendingindex, /* [out] */ GO.GAList)
        GO.number:                             Number of the GO to which the GA shall be added or from which the
                                               GA shall be removed.
        GO.action                              This flag shall indicate whether the contained GA shall be added to the
                                               GO or be removed from the GO.
                                               0: add: The contained GA shall be added to the list of GA assigned
                                                          to the referred GO.
                                               1: delete: The contained GA shall be removed from the list of GAs
                                                          assigned to the referred GO.
        GO.sending:                            Indication whether the added GA shall be the sending GA or not. This
                                               flag shall not be interpreted if the GA is removed.
        GO.value:                              The value of the GA hat shall be linked to or unlinked from the GO.
        GO.sendingindex:                       The index of the sending Group Address for this Group Object as
                                               returned by the Management Server (device).
        GO.GAList                              The list of all Group Addresses associated to the Group Object as
                                               returned by the Management Server (device).

    Sequence
    Management                                                            Network /                   remark
    Client                                                                Management
                                                                          Server
                                 A_Link_Write-PDU
                         (group_object_number = GO.number,
                                  flags.d = GO.action
                                 flags.s = GO.sending
                              group_address = GO.value)

                                                                          The Management Server (device) shall add or
                                                                          delete the GA to or from the list of GAs assigned
                                                                          to the referred GO and set the sending flag, both
                                                                          according the flags.
                                                                          The Management Server shall reply with the list of
                                                                          GAs assigned to the referred GO (1); if it has a
                                                                          problem, it shall respond with a negative
                                                                          A_Link_Response-PDU.
                               A_Link_Response-PDU
                        (group_object_number = GO.number,
                 sending_addresss = GO.sendingindex, start_index = 1,
                          group_address_list = GO.GAList)

    Error and exception handling
     (1)   The Management Server shall reply with the list of GAs assigned to the GO starting with
           start_index 1, thus with the first GA assigned to the GO. The number of GAs in the
           A_Link_Response-PDU shall be in-between 0 and 6, in function of the number of GAs
           assigned to the GO. If more than 6 GA are assigned, the Management Server shall only
           respond with the 6 first ones. The Management Server shall only send one single
           A_Link_Response-PDU. This means that the Management Client may take into account that
           the received A_Link_Response-PDY does not contain the GA that has just been added.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dm_group_object_link_write_r_cl(xknx: XKNX) -> None:
    """DM_GroupObjectLink_Write_RCl — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DM_GroupObjectLink_Write_RCl (KNX 03.05.02 §3.37.3) — implementation pending"
    )
