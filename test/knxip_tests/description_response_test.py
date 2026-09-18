"""Unit test for KNX/IP DescriptionResponse objects."""

from xknx.knxip import (
    DescriptionResponse,
    DIBDeviceInformation,
    DIBGeneric,
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

    def test_description_response_with_unknown_dib_type_code(self) -> None:
        """
        Test parsing DescriptionResponse containing an out-of-enum DIB type code.

        A reserved / vendor / future DIB type code (not a DIBTypeCode enum member)
        shall not abort parsing of the whole frame; the mandatory DIBs (device
        info, supported service families) must be preserved so the gateway stays
        discoverable.
        """
        # KNX/IP header (06 10 02 04) + total length 0x004C (76 bytes) followed by
        # DIBDeviceInformation (54 bytes) + DIBSuppSVCFamilies (12 bytes) +
        # unknown DIB with reserved type code 0x09 (4 bytes).
        raw = bytes.fromhex(
            "06 10 02 04 00 4C 36 01 02 00 11 00 23 42 13 37 13 37 13 37 E0 00"
            "17 0C 00 01 02 03 04 05 47 69 72 61 20 4B 4E 58 2F 49 50 2D 52 6F"
            "75 74 65 72 00 00 00 00 00 00 00 00 00 00 00 00 0C 02 02 01 03 02"
            "04 01 05 01 07 01 04 09 AA BB"
        )
        knxipframe, rest = KNXIPFrame.from_knx(raw)
        assert not rest
        assert isinstance(knxipframe.body, DescriptionResponse)
        assert len(knxipframe.body.dibs) == 3
        # Mandatory DIBs are parsed and preserved
        assert isinstance(knxipframe.body.dibs[0], DIBDeviceInformation)
        assert isinstance(knxipframe.body.dibs[1], DIBSuppSVCFamilies)
        # Unknown DIB is stored opaquely as a generic DIB (raw int type code)
        assert isinstance(knxipframe.body.dibs[2], DIBGeneric)
        assert knxipframe.body.dibs[2].dtc == 0x09
        # Gateway remains visible despite the unknown DIB
        assert knxipframe.body.device_name == "Gira KNX/IP-Router"
        assert knxipframe.body.dibs[1].supports(DIBServiceFamily.CORE, version=1)
        assert knxipframe.body.dibs[1].supports(DIBServiceFamily.ROUTING)
