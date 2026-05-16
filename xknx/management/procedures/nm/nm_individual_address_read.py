"""
NM_IndividualAddress_Read — KNX 03.05.02 §2.2 (PDF p. 11).

Spec text (verbatim from spec):

    Use
    This Network Management Procedure shall be used to read out the Individual Addresses of all the
    devices that are in Programming Mode.
    This procedure shall work independently of the configuration of the Individual Address of the Routers.
    When applicable this procedure shall be preceded by the configuration of the Domain Address.
    Used Application Layer Services for Management
       • A_IndividualAddress_Read
    Parameters of the Management Procedure
    NM_IndividualAddress_Read(/* [out] */ individual_addresses[])
          individual_addresses[]:     The collection of all the Individual Addresses of the devices that are
                                      in Programming Mode.
    Service parameters
       None.
    Variables
          IAn:     The IA of one device n that responds to the A_IndividualAddress_Read-PDU. The
                   Management Client shall collect all IAn of the individual responses and report these via
                   individual_addresses[].
    Sequence
    Management                                                             Network /                  remark
    Client                                                                 Management
                                                                           Server
                           A_IndividualAddress_Read-PDU
                                         ()

                         A_IndividualAddress_Response-PDU                               the devices, one or more, that are
                               (source_address = IAn)...                                in Programming Mode shall
                                                                                        respond
                                               …                                        time-out: 3 s

    1)   The Management Server functionality has to be implemented.

    Exception handling
    The Management Client shall always wait until the time-out has elapsed. It shall collect all responses
    IAn during this time-out.
         -   If no A_IndividualAddress_Response-PDU is received, no device is in Programming Mode.
         -   If one A_IndividualAddress_Response-PDU is received, exactly one device is in
             Programming Mode.
         -   If more than one response is received, several devices are in Programming Mode.
         -   If two or more responses with the same Individual Address are received, there is more than
             one device with the same Individual Addresses.
    The Management Client shall not evaluate Layer-2 repetitions.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from xknx.exceptions import ManagementConnectionError
from xknx.telegram import apci
from xknx.telegram.address import IndividualAddress

if TYPE_CHECKING:
    from xknx import XKNX

logger = logging.getLogger("xknx.management.procedures")


async def nm_individual_address_read(
    xknx: XKNX,
    timeout: float | None = 3,
    raise_if_multiple: bool = False,
) -> list[IndividualAddress]:
    """
    Request individual addresses of all devices that are in programming mode.

    :param xknx: XKNX object
    :param timeout: specifies the timeout in seconds, the KNX specification requires a timeout of 3s
    :param raise_if_multiple: if true, ManagementConnectionError is raised when multiple devices are in programming mode
    :returns: list of individual address of devices in programming mode
    """
    addresses = []
    # initialize queue or event handler gathering broadcasts
    async with xknx.management.broadcast() as bc_context:
        await xknx.management.send_broadcast(apci.IndividualAddressRead())
        async for result in bc_context.receive(timeout=timeout):
            if isinstance(result.payload, apci.IndividualAddressResponse):
                addresses.append(result.source_address)
                if raise_if_multiple and (len(addresses) > 1):
                    raise ManagementConnectionError(
                        "More than one KNX device is in programming mode."
                    )
    return addresses
