"""
DMP_DownloadLoadablePart_RCo_IO — KNX 03.05.02 §3.31.4 (PDF p. 141).

Spec text (verbatim from spec):

    3.31.4.1 Normal conditions
    This method shall use the connection oriented or connectionless remote communication.
    Used Application Layer Services for Management
         •     A_PropertyValue_Write
         •     A_PropertyValue_Read

    Complete Download Sequence for one loadable part 15)
    Managemen                                                                         Management                 remark
       t Client                                                                       Server

                                A_PropertyValue_Write-PDU                                          Unload
                      (object_index, Property_id = 5, start_index = 01h,
                             nr_of_elem = 01h,Data = 04 00 …)
     This part is
      optional               A_PropertyValue_Response –PDU                                         Load State Machine shall changes to
                      (object_index, Property_id=5, start_index = 01h,                             Unload (00h)
                                nr_of_elem = 01h, data = 00)

              If data is equal 04 (unloading) read Property and verify value                       Retry read Property for 30 Seconds.
              if data is equal 00 (unloaded) continue
              else break with error

    15) The optional state Unloading is not used.

                               A_PropertyValue_Write-PDU                                        Start loading
                     (object_index, Property_id = 5, start_index = 01h,
                            nr_of_elem = 01h, data = 01 00 …)

                             A_PropertyValue_Response –PDU                                      Load State Machine shall change to
                      (object_index, Property_id=5, start_index = 01h,                          Loading.
                                nr_of_elem = 01h, data = 02)

                                 if data is not equal 02 break with error
      This part is             A_PropertyValue_Write-PDU                                        Additional load controls
    optional and     (object_index, Property_id = 5, start_index = 01h,
    may repeated
     for different          nr_of_elem = 01h, data = 03 … …)
      additional
    load controls            A_PropertyValue_Response –PDU                                      Load State Machine shall stay in the
                      (object_index, Property_id=5, start_index = 01h,                          state Loading.
                                nr_of_elem = 01h, data = 02)

                                  if data is not equal 02 break with error
                     Load the loadable data via Property access or memory access
                               A_PropertyValue_Write-PDU                                        Load complete
                     (object_index, Property_id = 5, start_index = 01h,                         Time-out?
                           nr_of_elem = 01h, data = 02 00 … …)

                             A_PropertyValue_Response –PDU                                      Load State Machine shall change to
                      (object_index, Property_id=5, start_index = 01h,                          the state Loaded.
                                nr_of_elem = 01h, data = 01)

                                 if data is not equal 01 break with error

    3.31.4.2 Error and exception handling
    The general exception handling shall apply.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dmp_download_loadable_part_r_co_io(xknx: XKNX) -> None:
    """DMP_DownloadLoadablePart_RCo_IO — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "DMP_DownloadLoadablePart_RCo_IO (KNX 03.05.02 §3.31.4) — implementation pending"
    )
