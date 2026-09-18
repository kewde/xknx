"""Unit test for KNX/IP SRP objects."""

import pytest

from xknx.exceptions import ConversionError, CouldNotParseKNXIP
from xknx.knxip import (
    DIBServiceFamily,
    DIBTypeCode,
    KNXIPFrame,
    SearchRequestParameterType,
)
from xknx.knxip.srp import SRP


class TestKNXIPSRP:
    """Test class for KNX/IP SRP objects."""

    def test_basic(self) -> None:
        """Test SRP with mac contains mac address."""
        srp: SRP = SRP.with_mac_address(bytes([1, 2, 3, 4, 5, 6]))
        assert len(srp) == SRP.SRP_HEADER_SIZE + 6
        assert srp.type == SearchRequestParameterType.SELECT_BY_MAC_ADDRESS

        srp: SRP = SRP.with_service(DIBServiceFamily.TUNNELING, 2)
        assert len(srp) == SRP.SRP_HEADER_SIZE + 2
        assert srp.type == SearchRequestParameterType.SELECT_BY_SERVICE

        srp: SRP = SRP.with_programming_mode()
        assert len(srp) == SRP.SRP_HEADER_SIZE
        assert srp.type == SearchRequestParameterType.SELECT_BY_PROGRAMMING_MODE

        dibs: list[DIBTypeCode] = [
            DIBTypeCode.SUPP_SVC_FAMILIES,
            DIBTypeCode.ADDITIONAL_DEVICE_INFO,
        ]
        srp: SRP = SRP.request_device_description(dibs)
        assert len(srp) == SRP.SRP_HEADER_SIZE + len(dibs)
        assert srp.type == SearchRequestParameterType.REQUEST_DIBS

    def test_invalid_payload_raises(self) -> None:
        """Test SRP with invalid data size raises."""
        with pytest.raises(ConversionError):
            SRP.with_mac_address(bytes([1, 2, 3, 4, 5, 6, 7, 8]))

        with pytest.raises(ConversionError):
            SRP(SearchRequestParameterType.SELECT_BY_SERVICE, True)

        with pytest.raises(ConversionError):
            SRP(SearchRequestParameterType.REQUEST_DIBS, True)

    def test_invalid_payload_from_knx_raises(self) -> None:
        """Test from_knx with invalid data size raises."""
        # size is too big
        with pytest.raises(CouldNotParseKNXIP):
            SRP.from_knx(bytes.fromhex("08 82"))

        # too small
        with pytest.raises(CouldNotParseKNXIP):
            SRP.from_knx(bytes.fromhex("08"))

    def test_unknown_type_raises_couldnotparse(self) -> None:
        """
        Test from_knx with an unknown SRP type raises CouldNotParseKNXIP, not ValueError.

        The parser masks the type byte with `& 0x7F` (accepting 0x00-0x7F) but
        SearchRequestParameterType only defines 0x00-0x04, so any value 0x05-0x7F
        is unknown to the enum. This used to raise a bare ValueError that escaped
        the transport's `except CouldNotParseKNXIP` and reached asyncio's
        call_exception_handler; it now raises CouldNotParseKNXIP like the other
        from_knx parsers (see KNXIPHeader.from_knx).
        """
        # Unknown type 0x10 (appears as 0x90 on the wire with the Mandatory bit set):
        with pytest.raises(CouldNotParseKNXIP):
            SRP.from_knx(bytes.fromhex("02 90"))

    def test_unknown_type_raises_couldnotparse_via_frame(self) -> None:
        """Test a SEARCH_REQUEST_EXTENDED with an unknown SRP type parses to CouldNotParseKNXIP."""
        # End-to-end through the frame parser. Header total_length is 0x10
        # (6-byte header + 10-byte body = 8-byte HPAI + 2-byte SRP) so the SRP
        # is not truncated as out-of-frame data:
        with pytest.raises(CouldNotParseKNXIP):
            KNXIPFrame.from_knx(bytes.fromhex("0610020b001008010000000000000210"))

    @pytest.mark.parametrize(
        ("srp", "expected_bytes"),
        [
            (
                SRP.with_mac_address(bytes([1, 2, 3, 4, 5, 6])),
                bytes.fromhex("08 82 01 02 03 04 05 06"),
            ),
            (
                SRP.with_service(DIBServiceFamily.TUNNELING, 2),
                bytes.fromhex("04 83 04 02"),
            ),
            (
                SRP.with_programming_mode(),
                bytes.fromhex("02 81"),
            ),
            (
                SRP.request_device_description(
                    [DIBTypeCode.SUPP_SVC_FAMILIES, DIBTypeCode.TUNNELING_INFO]
                ),
                bytes.fromhex("04 04 02 07"),
            ),
            (
                SRP.request_device_description([DIBTypeCode.SUPP_SVC_FAMILIES]),
                bytes.fromhex("04 04 02 00"),
            ),
        ],
    )
    def test_to_and_from_knx(self, srp: SRP, expected_bytes: bytes) -> None:
        """Test to and from KNX."""
        assert bytes(srp) == expected_bytes
        assert SRP.from_knx(expected_bytes) == srp
