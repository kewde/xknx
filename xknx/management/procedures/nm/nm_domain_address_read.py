"""
NM_DomainAddress_Read — KNX 03.05.02 §2.7 (PDF p. 17).

Spec text (verbatim from spec):

    Use
    This Network Management Procedure shall be used to read out the Domain Addresses of all the
    devices in which Programming Mode is active.
    This procedure works independently of the configuration of the Domain Address and the Individual
    Address of the Router.
    Used Application Layer Services for Management
       • A_DomainAddress_Read
    Parameters of the Management Procedure
    NM_DomainAddress_Read (/* [out] */ individual_addresses[], /* [out] */ domain_addresses[])
          individual_addresses[]:     The collection of all the Individual Addresses of the devices in which
                                      Programming Mode is active.
          domain_addresses[]:         The collection of all theDomain Addresses of the devices in which
                                      Programming Mode is active.
    Variables
          IAn:    The IA of one device n that responds to the A_DomainAddress_Read-PDU. The
                  Management Client shall collect all IAn of the individual responses and report these via
                  individual_addresses[].

       DoAn: The DoAn of one device n that responds to the A_DomainAddress_Read-PDU. The
             Management Client shall collect all DoAn of the individual responses and report these
             via domain_addresses[].
    Sequence
    Management                                                             Network /                  remark
    Client                                                                 Management
                                                                           Server
                             A_DomainAddress_Read-PDU
                                        ()

                          A_DomainAddress_Response-PDU                                  one or more responses may be
                    (source_address =IAn, domain_address = DoAn)                        received from different devices
                                                                                        time-out: 3 s
                                               …

    Exception handling
    The Management Client shall always wait until the time-out has elapsed. It shall collect all responses
    during this time-out.
         -    If no A_DomainAddress_Response is received, there is no device in which Programming
              Mode is active.
         -    If one A_DomainAddress_Response is received, there is exactly one device in which
              Programming Mode is active.
         -    If more than one response is received, there are several devices in which Programming Mode
              is active.
         -    If two or more responses with the same Domain Address and Individual Addresses are
              received, there is more than one device with the same Domain Address and the same
              Individual Addresses.
    The Management Client shall not evaluate Layer-2 repetitions.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def nm_domain_address_read(xknx: XKNX) -> None:
    """NM_DomainAddress_Read — see module docstring for the verbatim spec text."""
    raise NotImplementedError(
        "NM_DomainAddress_Read (KNX 03.05.02 §2.7) — implementation pending"
    )
