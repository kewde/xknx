"""Unit test for KNX/IP SearchResponse objects."""

from xknx.knxip import (
    HPAI,
    DIBDeviceInformation,
    DIBGeneric,
    DIBServiceFamily,
    DIBSuppSVCFamilies,
    KNXIPFrame,
    SearchResponse,
)


class TestKNXIPSearchResponse:
    """Test class for KNX/IP SearchResponse objects."""

    def test_search_response(self) -> None:
        """Test parsing and streaming SearchResponse KNX/IP packet."""
        raw = bytes.fromhex(
            "06 10 02 02 00 50 08 01 C0 A8 2A 0A 0E 57 36 01"
            "02 00 11 00 00 00 11 22 33 44 55 66 E0 00 17 0C"
            "01 02 03 04 05 06 47 69 72 61 20 4B 4E 58 2F 49"
            "50 2D 52 6F 75 74 65 72 00 00 00 00 00 00 00 00"
            "00 00 00 00 0C 02 02 01 03 02 04 01 05 01 07 01"
        )
        knxipframe, rest = KNXIPFrame.from_knx(raw)
        assert knxipframe.header.total_length == 80
        assert not rest
        assert knxipframe.to_knx() == raw

        assert isinstance(knxipframe.body, SearchResponse)
        assert knxipframe.body.control_endpoint == HPAI("192.168.42.10", 3671)
        assert len(knxipframe.body.dibs) == 2
        # Specific testing of parsing and serializing of
        # DIBDeviceInformation and DIBSuppSVCFamilies is
        # done within knxip_dib_test.py
        assert isinstance(knxipframe.body.dibs[0], DIBDeviceInformation)
        assert isinstance(knxipframe.body.dibs[1], DIBSuppSVCFamilies)
        assert knxipframe.body.device_name == "Gira KNX/IP-Router"
        assert knxipframe.body.dibs[1].supports(DIBServiceFamily.ROUTING)
        assert knxipframe.body.dibs[1].supports(DIBServiceFamily.TUNNELING)
        assert not knxipframe.body.dibs[1].supports(DIBServiceFamily.OBJECT_SERVER)

        search_response = SearchResponse(
            control_endpoint=HPAI(ip_addr="192.168.42.10", port=3671)
        )
        search_response.dibs.append(knxipframe.body.dibs[0])
        search_response.dibs.append(knxipframe.body.dibs[1])
        knxipframe2 = KNXIPFrame.init_from_body(search_response)

        assert knxipframe2.to_knx() == raw

    def test_unknown_device_name(self) -> None:
        """Test device_name if no DIBDeviceInformation is present."""
        search_response = SearchResponse()
        assert search_response.device_name == "UNKNOWN"

    def test_search_response_with_unknown_dib_type_code(self) -> None:
        """
        Test parsing SearchResponse containing an out-of-enum DIB type code.

        Core-V1 SearchRequests send no SRP, so a device may include any DIBs in
        its response. A reserved / vendor / future DIB type code (not a
        DIBTypeCode enum member) shall not abort parsing of the whole frame; the
        mandatory DIBs must be preserved so the gateway stays discoverable.
        """
        # KNX/IP header (06 10 02 02) + total length 0x0054 (84 bytes) followed by
        # HPAI control endpoint (8 bytes) + DIBDeviceInformation (54 bytes) +
        # DIBSuppSVCFamilies (12 bytes) + unknown DIB with reserved type code
        # 0x09 (4 bytes).
        raw = bytes.fromhex(
            "06 10 02 02 00 54 08 01 C0 A8 2A 0A 0E 57 36 01 02 00 11 00 23 42"
            "13 37 13 37 13 37 E0 00 17 0C 00 01 02 03 04 05 47 69 72 61 20 4B"
            "4E 58 2F 49 50 2D 52 6F 75 74 65 72 00 00 00 00 00 00 00 00 00 00"
            "00 00 0C 02 02 01 03 02 04 01 05 01 07 01 04 09 AA BB"
        )
        knxipframe, rest = KNXIPFrame.from_knx(raw)
        assert not rest
        assert isinstance(knxipframe.body, SearchResponse)
        assert knxipframe.body.control_endpoint == HPAI("192.168.42.10", 3671)
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
