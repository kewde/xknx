"""
Discovery of maximal frame length — KNX 03.05.03 §2.6.

Contains the result type and the procedures that implement the three-step
discovery algorithm:

    §2.6.2.1  Local cEMI peer's PID_MAX_APDU_LENGTH (caller-supplied).
    §2.6.2.2  Target device's PID_MAX_APDU_LENGTH via DMP_InterfaceObjectRead_R.
    §2.6.2.3  Each in-between coupler's effective limit, with DD0 short-
              circuit on Coupler 1.0/1.1 masks and Device-Object fallback
              when the Router Object value is absent.

KNX 03.05.03 Configuration Procedures v02.01.01 §2.6 (PDF p. 31-33).

§2.6.1 Goal:
    This clause specifies the Configuration Procedures to discover the
    maximal frame size that can be used between a Management Client and a
    Management Server. L_Data_Standard frames shall always be capable of
    supporting APDUs of up to 14 octets. L_Data_Extended frames are capable
    of transferring larger APDUs; therefore this procedure focuses on
    discovering the maximal frame size that can be used with L_Data_Extended
    frames.
"""

from __future__ import annotations

from dataclasses import dataclass
import logging
from typing import TYPE_CHECKING

from xknx.exceptions import (
    ManagementConnectionRefused,
    ManagementConnectionTimeout,
)
from xknx.management.interface_object import nm_interface_object_scan
from xknx.profile.const import (
    ResourceDevicePropertyId,
    ResourceObjectType,
    ResourceRouterPropertyId,
)
from xknx.telegram import apci
from xknx.telegram.address import (
    IndividualAddress,
    IndividualAddressableType,
)

if TYPE_CHECKING:
    from collections.abc import Sequence

    from xknx import XKNX
    from xknx.management.management import P2PConnection

logger = logging.getLogger("xknx.management.procedures")

NON_EXTENDED_FRAME_MASK_VERSIONS: frozenset[int] = frozenset({0x0910, 0x0911})
"""Device Descriptor Type 0 mask versions that do not support L_Data_Extended.

KNX 03.05.01 §4.1.2 — Coupler 1.0 (TP1) and Coupler 1.1 (TP1) predate the
extended-frame extension; §2.6.2.3 short-circuits to ``extended_frames =
False`` when any in-between coupler reports either DD0 value.
"""


@dataclass(frozen=True, slots=True)
class MaxApduResult:
    """
    Outcome of the §2.6 Discovery of maximal frame length procedure.

    Attributes:
        extended_frames: True when every hop on the path (local, target, and
            all in-between couplers) reports support for L_Data_Extended
            frames with APDU > 15. False if any hop falls back to standard
            frames; in that case ``max_frame_length`` is 15.
        max_frame_length: Minimum APDU length usable end-to-end, in octets.
            Per KNX 03.05.01 §4.3.7 the value is bounded to 15..254. When
            ``extended_frames`` is False this is 15 (L_Data_Standard floor).
        local_length: Local device's reported ``PID_MAX_APDU_LENGTH``. Per
            §2.6.2.1 this is read from the local Device Object via cEMI
            local-management services.
        target_length: Target device's reported ``PID_MAX_APDU_LENGTH``, or
            None if the property is absent. Per §2.6.2.2 this is read via
            ``DMP_InterfaceObjectReadR(object_index=0, PID=56)``.
        coupler_lengths: Per-coupler APDU lengths gathered during §2.6.2.3
            (in-between router walk), in path order. Empty when the path
            has no in-between couplers or when ``extended_frames`` is False.

    """

    extended_frames: bool
    max_frame_length: int
    local_length: int
    target_length: int | None
    coupler_lengths: tuple[tuple[IndividualAddress, int], ...]


def _derive_in_between_couplers(
    source: IndividualAddress, target: IndividualAddress
) -> list[IndividualAddress]:
    """
    Enumerate the couplers on the path from ``source`` to ``target``.

    A KNX Individual Address has three parts: ``area`` (4 bit), ``main``
    (4 bit, the trunk/line subdivision), and ``line`` (8 bit, the device
    number on the line). Line and area couplers sit at addresses with
    ``line = 0``:

        - Line Coupler  at  ``area.main.0`` — between trunk and line.
        - Area Coupler  at  ``area.0.0``    — between backbone and area.

    The enumeration is destination-side only: source-side couplers are
    not queried because the source on a Management Client is the
    KNXnet/IP interface itself, whose ``PID_MAX_APDU_LENGTH`` is taken
    from the local DIB and not via §2.6.2.3.

    Rules:
        - Same area, same main → no in-between couplers.
        - Same area, different main → destination line coupler at
          ``target_area.target_main.0``.
        - Different area → destination area coupler at
          ``target_area.0.0`` plus, when ``target.main != 0`` (target
          not on the area trunk), the destination line coupler at
          ``target_area.target_main.0``.

    Callers may override this with an explicit coupler list when the
    topology does not match these defaults (e.g. mixed-medium installs).
    """
    if source.area == target.area and source.main == target.main:
        return []
    couplers: list[IndividualAddress] = []
    if source.area != target.area:
        couplers.append(IndividualAddress(target.area << 12))
        if target.main != 0:
            couplers.append(IndividualAddress((target.area << 12) | (target.main << 8)))
    else:
        couplers.append(IndividualAddress((target.area << 12) | (target.main << 8)))
    return couplers


async def nm_read_max_apdu_length(connection: P2PConnection) -> int | None:
    """
    Read ``PID_MAX_APDU_LENGTH`` from the Device Object of the connected peer.

    Implements the §2.6.2.2 atom of KNX 03.05.03 (PDF p. 32) using the
    ``DMP_InterfaceObjectRead_R`` procedure from KNX 03.05.02 §3.27.2
    (PDF p. 124):

        if Property of management control is unknown to the Management Client
            A_PropertyDescription_Read-PDU (object_index, PID)
            A_PropertyDescription_Response-PDU (object_index, PID, type, ...)
        endif
        for each data block, until all data are transmitted
            A_PropertyValue_Read-PDU
                (object_index, PID, start_index, element_count)
            A_PropertyValue_Response-PDU
                (object_index, PID, start_index, element_count, data)
        endfor

    The data type of ``PID_MAX_APDU_LENGTH`` is known a priori
    (PDT_UNSIGNED_INT, KNX 03.05.01 §4.3.7, PDF p. 46-47) so the optional
    A_PropertyDescription_Read step is skipped.

    Returns the value in octets, or ``None`` when the property is absent on
    the device (peer responds with ``count = 0``). Per §4.3.7.1 valid
    values are in the range 15..254; this helper does not enforce that
    range — callers interpret values per §2.6 semantics.
    """
    response = await connection.request(
        payload=apci.PropertyValueRead(
            object_index=0,
            property_id=ResourceDevicePropertyId.PID_MAX_APDU_LENGTH,
            count=1,
            start_index=1,
        ),
        expected=apci.PropertyValueResponse,
    )
    payload = response.payload
    assert isinstance(payload, apci.PropertyValueResponse)
    if payload.count == 0 or not payload.data:
        return None
    return int.from_bytes(payload.data, byteorder="big")


async def nm_discover_max_apdu_length(
    xknx: XKNX,
    target: IndividualAddressableType,
    *,
    local_max_apdu_length: int = 254,
    couplers: Sequence[IndividualAddressableType] | None = None,
) -> MaxApduResult:
    """
    Discover the maximal APDU length usable between MaC and a target device.

    KNX 03.05.03 Configuration Procedures v02.01.01 §2.6 (PDF p. 31-33).

    §2.6.1 Goal:
        This clause specifies the Configuration Procedures to discover the
        maximal frame size that can be used between a Management Client and
        a Management Server. L_Data_Standard frames shall always be capable
        of supporting APDUs of up to 14 octets. L_Data_Extended frames are
        capable of transferring larger APDUs; therefore this procedure
        focuses on discovering the maximal frame size that can be used with
        L_Data_Extended frames.

    §2.6.2.1 1st step — in the local device::

        ExtendedFrames = false;
        MaxFrameLength(local) = 15;
        If EMI-Type = cEMI then
            M_PropRead(Device Object, Object Instance = 1,
                       Property_Id = 56, start_index = 1);
            If PID_MAX_APDU_LENGTH.Value > 15 then
                ExtendedFrames = true;
                MaxFrameLength(local) = PID_MAX_APDU_LENGTH.Value
            Endif
        Endif

    The local value is taken from ``local_max_apdu_length`` (default 254).
    Routing-mode KNXnet/IP always uses cEMI extended frames; in tunnel
    mode the caller may pass the value advertised by the tunnel's
    ``DIBTunnelingInfo`` if available.

    §2.6.2.2 2nd step — in the target device::

        If ExtendedFrames = true then
            MaxFrameLength(target) = 15;
            DMP_InterfaceObjectReadR(object_index = 0;
                PID = PID_MAX_APDU_LENGTH;
                start_index = 1; element_count = 1);
            If DeviceObject.PID_MAX_APDU_LENGTH is present then
                If PID_MAX_APDU_LENGTH.Value > 15 then
                    MaxFrameLength(target) = PID_MAX_APDU_LENGTH.Value
                    MaxFrameLength = min(MaxFrameLength(local),
                                         MaxFrameLength(target))
                Else
                    ExtendedFrames = false
                Endif
            Else
                ExtendedFrames = false
            Endif
        Endif

    §2.6.2.3 3rd step — in all in-between couplers::

        If ExtendedFrames = true then
            Repeat /* For all in-between Routers do */
                DMP_Connect_RCo(connection oriented; descriptor_type = 0)
                If(DD0 = 0910h or DD0 = 0911h) then
                    ExtendedFrames = false
                Else
                    RouterObject.index = DMP_InterfaceObjectScan_R();
                    PID_MAX_APDU_LENGTH.Value = DMP_InterfaceObjectReadR(
                        object_index = RouterObject.index;
                        PID = PID_MAX_APDU_LENGTH;
                        start_index = 1; element_count = 1)
                    If RouterObject.PID_MAX_APDU_LENGTH does not exist then
                        PID_MAX_APDU_LENGTH.Value = DMP_InterfaceObjectReadR(
                            object_index = 0; PID = PID_MAX_APDU_LENGTH;
                            start_index = 1; element_count = 1)
                    EndIf
                    If Property not present then
                        ExtendedFrames = false
                    Else
                        If PID_MAX_APDU_LENGTH.Value > 15 then
                            MaxFrameLength(thisRouter) = PID_MAX_APDU_LENGTH.Value
                            MaxFrameLength = min(MaxFrameLength,
                                                 MaxFrameLength(thisRouter))
                        Else
                            ExtendedFrames = false
                        Endif
                    Endif
                Endif
            Until ExtendedFrames = false OR no more in-between Routers
        Endif

    The set of in-between couplers is taken from ``couplers`` when
    provided, else derived from ``xknx.current_address`` and ``target``
    via :func:`_derive_in_between_couplers`. Each coupler is opened on a
    fresh management connection with ``rate_limit = 0`` so the multi-
    request scan does not stall on the inter-request throttle.

    §2.6.3 Error and exception handling:
        If the discovery would make assume a certain L_Data_Extended frame
        length is supported along the entire communication path and
        afterwards communication using this frame length fails, then the
        following fall back option shall be used. Failure of management
        with APDU-length > 55 shall firstly fall back to management with
        APDU-length = 55 and only if also this fails to management with
        L_Data_Standard frames.

    Note: this function performs discovery only. The §2.6.3 runtime
    fallback (55/standard) is the caller's responsibility — the
    discovered value can later be invalidated by an actual send failure.

    A timeout when reading from the target is treated as "target does
    not support extended frames" and the result reports
    ``extended_frames = False`` with ``target_length = None``.
    """
    if local_max_apdu_length <= 15:
        return MaxApduResult(
            extended_frames=False,
            max_frame_length=15,
            local_length=local_max_apdu_length,
            target_length=None,
            coupler_lengths=(),
        )

    target_ia = IndividualAddress(target)
    try:
        async with xknx.management.connection(target_ia) as target_conn:
            target_length = await nm_read_max_apdu_length(target_conn)
    except ManagementConnectionTimeout:
        logger.debug(
            "Discovery timed out reading PID_MAX_APDU_LENGTH from %s; "
            "treating target as non-extended-frame capable.",
            target_ia,
        )
        return MaxApduResult(
            extended_frames=False,
            max_frame_length=15,
            local_length=local_max_apdu_length,
            target_length=None,
            coupler_lengths=(),
        )

    if target_length is None or target_length <= 15:
        return MaxApduResult(
            extended_frames=False,
            max_frame_length=15,
            local_length=local_max_apdu_length,
            target_length=target_length,
            coupler_lengths=(),
        )

    coupler_ias: list[IndividualAddress]
    if couplers is None:
        coupler_ias = _derive_in_between_couplers(xknx.current_address, target_ia)
    else:
        coupler_ias = [IndividualAddress(c) for c in couplers]

    coupler_lengths: list[tuple[IndividualAddress, int]] = []
    for coupler_ia in coupler_ias:
        coupler_length = await _read_coupler_max_apdu_length(xknx, coupler_ia)
        if coupler_length is None:
            return MaxApduResult(
                extended_frames=False,
                max_frame_length=15,
                local_length=local_max_apdu_length,
                target_length=target_length,
                coupler_lengths=tuple(coupler_lengths),
            )
        coupler_lengths.append((coupler_ia, coupler_length))

    all_lengths = [
        local_max_apdu_length,
        target_length,
        *(length for _, length in coupler_lengths),
    ]
    return MaxApduResult(
        extended_frames=True,
        max_frame_length=min(all_lengths),
        local_length=local_max_apdu_length,
        target_length=target_length,
        coupler_lengths=tuple(coupler_lengths),
    )


async def _read_coupler_max_apdu_length(
    xknx: XKNX, coupler_ia: IndividualAddress
) -> int | None:
    """
    Probe one in-between coupler per KNX 03.05.03 §2.6.2.3.

    Returns the coupler's effective ``PID_MAX_APDU_LENGTH`` in octets, or
    ``None`` when the spec mandates that ``extended_frames`` be set to
    False for this coupler (DD0 is a non-extended mask, the property is
    absent on both Router Object and Device Object, the reported value is
    ≤ 15, or the connection times out).
    """
    try:
        async with xknx.management.connection(coupler_ia, rate_limit=0) as conn:
            descriptor = await conn.request(
                payload=apci.DeviceDescriptorRead(descriptor=0),
                expected=apci.DeviceDescriptorResponse,
            )
            descriptor_payload = descriptor.payload
            assert isinstance(descriptor_payload, apci.DeviceDescriptorResponse)
            if descriptor_payload.value in NON_EXTENDED_FRAME_MASK_VERSIONS:
                logger.debug(
                    "Coupler %s reports DD0=%04Xh — disables extended frames.",
                    coupler_ia,
                    descriptor_payload.value,
                )
                return None

            router_oi = await nm_interface_object_scan(
                conn, ResourceObjectType.OBJECT_ROUTER
            )
            router_length: int | None = None
            if router_oi is not None:
                response = await conn.request(
                    payload=apci.PropertyValueRead(
                        object_index=router_oi,
                        property_id=ResourceRouterPropertyId.PID_MAX_APDU_LENGTH_ROUTER,
                        count=1,
                        start_index=1,
                    ),
                    expected=apci.PropertyValueResponse,
                )
                router_payload = response.payload
                assert isinstance(router_payload, apci.PropertyValueResponse)
                if router_payload.count > 0 and router_payload.data:
                    router_length = int.from_bytes(router_payload.data, "big")

            # §2.6.2.3: "If the above fails, PID_MAX_APDU_LENGTH shall
            # alternatively be read from the Device Object."
            if router_length is None:
                router_length = await nm_read_max_apdu_length(conn)

            if router_length is None or router_length <= 15:
                return None
            return router_length
    except ManagementConnectionTimeout:
        logger.debug(
            "Discovery timed out probing coupler %s; treating as "
            "non-extended-frame capable.",
            coupler_ia,
        )
        return None
    except ManagementConnectionRefused:
        logger.debug(
            "Coupler %s refused the management connection; treating as "
            "non-extended-frame capable.",
            coupler_ia,
        )
        return None
