"""Unit test for KNX/IP SearchRequest Extended objects."""

import logging

import pytest

from xknx.exceptions import CouldNotParseKNXIP
from xknx.io.transport.udp_transport import UDPTransport
from xknx.knxip import HPAI, KNXIPFrame, SearchRequestExtended
from xknx.knxip.srp import SRP


class TestKNXIPSearchRequestExtended:
    """Test class for KNX/IP SearchRequest Extended objects."""

    def test_search_request_extended(self) -> None:
        """Test parsing and streaming SearchRequest Extended KNX/IP packet."""
        raw = bytes.fromhex("06 10 02 0b 00 0e 08 01 e0 00 17 0C 0E 57")
        knxipframe, _ = KNXIPFrame.from_knx(raw)

        assert isinstance(knxipframe.body, SearchRequestExtended)
        assert knxipframe.body.discovery_endpoint == HPAI(
            ip_addr="224.0.23.12", port=3671
        )

        knxipframe2 = KNXIPFrame.init_from_body(
            SearchRequestExtended(
                discovery_endpoint=HPAI(ip_addr="224.0.23.12", port=3671)
            )
        )

        assert knxipframe2.to_knx() == raw

    def test_search_request_extended_srp(self) -> None:
        """Test parsing and streaming SearchRequest Extended with SRPs KNX/IP packet."""
        raw = bytes.fromhex("06 10 02 0b 00 10 08 01 e0 00 17 0c 0e 57 02 81")
        knxipframe, _ = KNXIPFrame.from_knx(raw)

        assert isinstance(knxipframe.body, SearchRequestExtended)
        assert knxipframe.body.discovery_endpoint == HPAI(
            ip_addr="224.0.23.12", port=3671
        )
        assert len(knxipframe.body.srps) == 1
        assert knxipframe.body.srps[0] == SRP.with_programming_mode()

        knxipframe2 = KNXIPFrame.init_from_body(
            SearchRequestExtended(
                discovery_endpoint=HPAI(ip_addr="224.0.23.12", port=3671),
                srps=[SRP.with_programming_mode()],
            )
        )

        assert knxipframe2.to_knx() == raw

    def test_search_request_extended_multiple_srp(self) -> None:
        """Test parsing and streaming SearchRequest Extended with SRPs KNX/IP packet."""
        raw = bytes.fromhex(
            "06 10 02 0b 00 18 08 01 e0 00 17 0c 0e 57 02 81 08 82 01 02 03 04 05 06"
        )
        knxipframe, _ = KNXIPFrame.from_knx(raw)

        assert isinstance(knxipframe.body, SearchRequestExtended)
        assert knxipframe.body.discovery_endpoint == HPAI(
            ip_addr="224.0.23.12", port=3671
        )
        assert len(knxipframe.body.srps) == 2
        assert knxipframe.body.srps[0] == SRP.with_programming_mode()
        assert knxipframe.body.srps[1] == SRP.with_mac_address(
            bytes([1, 2, 3, 4, 5, 6])
        )

        knxipframe2 = KNXIPFrame.init_from_body(
            SearchRequestExtended(
                discovery_endpoint=HPAI(ip_addr="224.0.23.12", port=3671),
                srps=[
                    SRP.with_programming_mode(),
                    SRP.with_mac_address(bytes([1, 2, 3, 4, 5, 6])),
                ],
            )
        )

        assert knxipframe2.to_knx() == raw

    @pytest.mark.parametrize(
        "raw_hex",
        [
            # Fall-through SRP (SELECT_BY_PROGRAMMING_MODE) with wire size 4 leaves
            # 2 trailing bytes that used to be re-parsed as a *phantom* SRP.
            "06 10 02 0b 00 12 08 01 e0 00 17 0c 0e 57 04 81 02 81",
            # Same shape but trailing bytes encode an unknown type (0x7f); used to
            # raise an uncaught ValueError instead of CouldNotParseKNXIP.
            "06 10 02 0b 00 12 08 01 e0 00 17 0c 0e 57 04 81 02 7f",
            # Crafted payload of a fall-through SRP that used to make the leftover
            # bytes parse as a fully-valid cross-type (MAC) phantom SRP.
            "06 10 02 0b 00 18 08 01 e0 00 17 0c 0e 57 0a 81 08 82 aa bb cc dd ee ff",
        ],
    )
    def test_malformed_srp_raises_could_not_parse(self, raw_hex: str) -> None:
        """Test malformed fall-through SRPs are rejected, not silently misparsed."""
        with pytest.raises(CouldNotParseKNXIP):
            KNXIPFrame.from_knx(bytes.fromhex(raw_hex))

    def test_udp_transport_handles_malformed_srp(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """
        Test the UDP transport logs and ignores a malformed SRP datagram.

        Before the fix a malformed fall-through SRP either silently misparsed
        (creating phantom SRPs) or raised an uncaught ``ValueError`` that escaped
        ``datagram_received`` to the asyncio default exception handler. The
        transport only catches ``CouldNotParseKNXIP``, so the malformed SRP
        must surface as that exception and be logged as an unsupported frame.
        """
        transport = UDPTransport(local_addr=("0.0.0.0", 0), remote_addr=("0.0.0.0", 0))
        source = ("224.0.23.12", 3671)
        malformed_datagrams = [
            # phantom misparse
            bytes.fromhex("06 10 02 0b 00 12 08 01 e0 00 17 0c 0e 57 04 81 02 81"),
            # uncaught ValueError path
            bytes.fromhex("06 10 02 0b 00 12 08 01 e0 00 17 0c 0e 57 04 81 02 7f"),
        ]
        with caplog.at_level(logging.DEBUG, logger="xknx.knx"):
            for raw in malformed_datagrams:
                transport.data_received_callback(raw, source)

        # No exception escaped data_received_callback (the call returned normally).
        unsupported = [
            r for r in caplog.records if r.message.startswith("Unsupported KNXIPFrame")
        ]
        assert len(unsupported) == len(malformed_datagrams)
        # No error-level record should be raised for these malformed frames.
        assert not [r for r in caplog.records if r.levelno >= logging.ERROR]
