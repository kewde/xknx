"""
Result type for the §2.6 Discovery of maximal frame length procedure.

KNX 03_05_03 Configuration Procedures v02.01.01, §2.6 (PDF p. 31-33).

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

from xknx.telegram.address import IndividualAddress


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
            Per KNX 03_05_01 §4.3.7 the value is bounded to 15..254. When
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
