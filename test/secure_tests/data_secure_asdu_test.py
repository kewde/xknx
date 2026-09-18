"""Tests for KNX Data Secure Security Control Field and Security AL Service enum."""

import pytest

from xknx.secure.data_secure_asdu import (
    SecurityAlgorithmIdentifier,
    SecurityALService,
    SecurityControlField,
)


class TestSecurityALService:
    """Test class for SecurityALService enum encoding."""

    @pytest.mark.parametrize(
        "service, value",
        [
            (SecurityALService.S_A_DATA, 0b000),
            (SecurityALService.S_A_SYNC_REQ, 0b010),
            (SecurityALService.S_A_SYNC_RES, 0b011),
        ],
    )
    def test_enum_value(self, service: SecurityALService, value: int) -> None:
        """Test the enum values match AN158 v07 (S-A_sync.req = 0b010)."""
        assert int(service) == value
        assert SecurityALService(value) is service

    @pytest.mark.parametrize("reserved", [0b001, 0b100, 0b101, 0b110, 0b111])
    def test_reserved_values_raise(self, reserved: int) -> None:
        """Test reserved/unsupported service values raise ValueError."""
        with pytest.raises(ValueError):
            SecurityALService(reserved)


class TestSecurityControlField:
    """Test class for SecurityControlField parsing and serialization."""

    @pytest.mark.parametrize(
        "raw, tool_access, algorithm, system_broadcast, service",
        [
            # S_A_DATA combinations
            (
                0x00,
                False,
                SecurityAlgorithmIdentifier.CCM_AUTHENTICATION,
                False,
                SecurityALService.S_A_DATA,
            ),
            (
                0x08,
                False,
                SecurityAlgorithmIdentifier.CCM_AUTHENTICATION,
                True,
                SecurityALService.S_A_DATA,
            ),
            (
                0x10,
                False,
                SecurityAlgorithmIdentifier.CCM_ENCRYPTION,
                False,
                SecurityALService.S_A_DATA,
            ),
            (
                0x18,
                False,
                SecurityAlgorithmIdentifier.CCM_ENCRYPTION,
                True,
                SecurityALService.S_A_DATA,
            ),
            (
                0x80,
                True,
                SecurityAlgorithmIdentifier.CCM_AUTHENTICATION,
                False,
                SecurityALService.S_A_DATA,
            ),
            (
                0x90,
                True,
                SecurityAlgorithmIdentifier.CCM_ENCRYPTION,
                False,
                SecurityALService.S_A_DATA,
            ),
            # S_A_SYNC_REQ - Calimero encryptedSyncReq wire SCF byte 0x92 (AN158 v07)
            (
                0x92,
                True,
                SecurityAlgorithmIdentifier.CCM_ENCRYPTION,
                False,
                SecurityALService.S_A_SYNC_REQ,
            ),
            (
                0x12,
                False,
                SecurityAlgorithmIdentifier.CCM_ENCRYPTION,
                False,
                SecurityALService.S_A_SYNC_REQ,
            ),
            # S_A_SYNC_RES - Calimero encryptedSyncRes wire SCF byte 0x93 (AN158 v07)
            (
                0x93,
                True,
                SecurityAlgorithmIdentifier.CCM_ENCRYPTION,
                False,
                SecurityALService.S_A_SYNC_RES,
            ),
            (
                0x13,
                False,
                SecurityAlgorithmIdentifier.CCM_ENCRYPTION,
                False,
                SecurityALService.S_A_SYNC_RES,
            ),
        ],
    )
    def test_from_knx(
        self,
        raw: int,
        tool_access: bool,
        algorithm: SecurityAlgorithmIdentifier,
        system_broadcast: bool,
        service: SecurityALService,
    ) -> None:
        """Test parsing an SCF byte."""
        scf = SecurityControlField.from_knx(raw)
        assert scf.tool_access is tool_access
        assert scf.algorithm is algorithm
        assert scf.system_broadcast is system_broadcast
        assert scf.service is service

    @pytest.mark.parametrize("raw", [0x00, 0x10, 0x92, 0x93])
    def test_to_knx_round_trip(self, raw: int) -> None:
        """Test that from_knx().to_knx() round-trips the SCF byte."""
        assert SecurityControlField.from_knx(raw).to_knx() == bytes([raw])

    @pytest.mark.parametrize(
        "raw",
        # service bits 0b001 are reserved per AN158 v07 (was mislabeled S_A_SYNC_REQ)
        # service bits 0b100..0b111 are reserved/unsupported as well
        [0x01, 0x11, 0x04, 0x05, 0x06, 0x07],
    )
    def test_from_knx_reserved_service_raises(self, raw: int) -> None:
        """Test reserved Security AL Service values raise ValueError on parse."""
        with pytest.raises(ValueError):
            SecurityControlField.from_knx(raw)
