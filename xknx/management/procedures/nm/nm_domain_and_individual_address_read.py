"""
NM_DomainAndIndividualAddress_Read — KNX 03.05.02 §2.8 (PDF p. 19).

Spec text (verbatim from spec):

    Use
    This Network Management Procedure shall be used to read the Domain Address and the Individual
    Address of one or more devices in which the Programming Mode is active.

    Used Application Layer Services for Management
     • A_DomainAddress_Read
     • A_IndividualAddress_Read

    Parameters of the Management Procedure
    NM_DomainAndIndividualAddress_Read(/* [out] */ individual_addresses[],
       /* [out] */ domain_addresses)
      individual_addresses[]: The collection of all the Individual Addresses of the devices in which
                               Programming Mode is active.
      domain_addresses[]:      The collection of all theDomain Addresses of the devices in which
                               Programming Mode is active.

    Variables
          IAn:
             The IA of one device n that responds to the A_DomainAddress_Read-PDU. The
             Management Client shall collect all IAn of the individual responses and report these via
             individual_addresses[].
       DoAn: The DoAn of one device n that responds to the A_DomainAddress_Read-PDU. The
             Management Client shall collect all DoAn of the individual responses and report these
             via domain_addresses[].

    Sequence
    Management                                                            Network /    remark
    Client                                                                Management
                                                                          Server
                          A_DomainAddress_Read-PDU
                                     ()
                    comm_mode = comm_mode = system broadcast

                          A_DomainAddress_Response-PDU
                    (source_address = IAn, domain_address= DoAn)
                           comm_mode = system broadcast

                            A_IndividualAddress_Read-PDU
                                          ()
                            comm_mode = system broadcast

                          A_IndividualAddress_Response-PDU
                                (source_address = IAn)
                            comm_mode = system broadcast

Inputs (from spec):
    [out] individual_addresses[], [out] domain_addresses[]
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def nm_domain_and_individual_address_read(xknx: XKNX) -> None:
    """NM_DomainAndIndividualAddress_Read — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "NM_DomainAndIndividualAddress_Read (KNX 03.05.02 §2.8) — implementation pending"
    )
