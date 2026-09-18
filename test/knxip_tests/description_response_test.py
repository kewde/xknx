"""Unit test for KNX/IP DescriptionResponse objects."""

import pytest

from xknx.exceptions import CouldNotParseKNXIP
from xknx.knxip import (
    DescriptionResponse,
    DIBDeviceInformation,
    DIBServiceFamily,
    DIBSuppSVCFamilies,
    KNXIPFrame,
)


class TestKNXIPDescriptionResponse:
    """Test class for KNX/IP DescriptionResponse objects."""

    def test_description_response(self) -> None:
        """Test parsing and streaming DescriptionResponse KNX/IP packet."""
        raw = bytes.fromhex(
            "06 10 02 04 00 48 36 01 02 00 10 00 00 00 00 08"
            "2d 40 83 4d e0 00 17 0c 00 0a b3 27 4a 32 4b 4e"
            "58 2f 49 50 2d 52 6f 75 74 65 72 00 00 00 00 00"
            "00 00 00 00 00 00 00 00 00 00 00 00 0c 02 02 02"
            "03 02 04 02 05 02 07 01",
        )
        knxipframe, rest = KNXIPFrame.from_knx(raw)
        assert not rest
        assert knxipframe.header.total_length == 72
        assert knxipframe.to_knx() == raw

        assert isinstance(knxipframe.body, DescriptionResponse)
        assert len(knxipframe.body.dibs) == 2
        # Specific testing of parsing and serializing of
        # DIBDeviceInformation and DIBSuppSVCFamilies is
        # done within knxip_dib_test.py
        assert isinstance(knxipframe.body.dibs[0], DIBDeviceInformation)
        assert isinstance(knxipframe.body.dibs[1], DIBSuppSVCFamilies)
        assert knxipframe.body.device_name == "KNX/IP-Router"
        assert knxipframe.body.dibs[1].supports(DIBServiceFamily.CORE, version=2)
        assert knxipframe.body.dibs[1].supports(
            DIBServiceFamily.DEVICE_MANAGEMENT, version=2
        )
        assert knxipframe.body.dibs[1].supports(DIBServiceFamily.ROUTING, version=2)
        assert knxipframe.body.dibs[1].supports(DIBServiceFamily.TUNNELING, version=2)
        assert knxipframe.body.dibs[1].supports(
            DIBServiceFamily.REMOTE_CONFIGURATION_DIAGNOSIS
        )
        assert not knxipframe.body.dibs[1].supports(DIBServiceFamily.OBJECT_SERVER)

        description_response = DescriptionResponse()
        description_response.dibs.append(knxipframe.body.dibs[0])
        description_response.dibs.append(knxipframe.body.dibs[1])
        knxipframe2 = KNXIPFrame.init_from_body(description_response)

        assert knxipframe2.to_knx() == raw

    def test_unknown_device_name(self) -> None:
        """Test device_name if no DIBDeviceInformation is present."""
        description_response = DescriptionResponse()
        assert description_response.device_name == "UNKNOWN"

    def test_description_response_zero_length_dib(self) -> None:
        """
        Test a DIB declaring length 0 raises instead of hanging the parser.

        A DIB header is itself two octets, so a declared length of 0x00 is
        nonsensical; previously it made the DIB loop advance by 0 bytes and
        spin forever (synchronously blocking the asyncio event loop). It
        shall raise CouldNotParseKNXIP and terminate.
        """
        # DIB body of a single DIB whose declared length byte is 0x00 and whose
        # type code 0x02 (SUPP_SVC_FAMILIES) routes to DIBSuppSVCFamilies.
        with pytest.raises(CouldNotParseKNXIP):
            DescriptionResponse().from_knx(bytes.fromhex("00 02"))

        # End-to-end via the frame layer: valid 6-byte DESCRIPTION_RESPONSE
        # header (total_length 8) wrapping the 2-byte malformed body "00 02".
        raw = bytes.fromhex("06 10 02 04 00 08 00 02")
        with pytest.raises(CouldNotParseKNXIP):
            KNXIPFrame.from_knx(raw)
