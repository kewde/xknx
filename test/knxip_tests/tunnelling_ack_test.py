"""Unit test for KNX/IP TunnellingAck objects."""

import pytest

from xknx.exceptions import CouldNotParseKNXIP
from xknx.knxip import ErrorCode, KNXIPFrame, TunnellingAck


class TestKNXIPTunnellingAck:
    """Test class for KNX/IP TunnellingAck objects."""

    def test_tunnelling_ack(self) -> None:
        """Test parsing and streaming tunneling ACK KNX/IP packet."""
        raw = bytes((0x06, 0x10, 0x04, 0x21, 0x00, 0x0A, 0x04, 0x2A, 0x17, 0x00))
        knxipframe, _ = KNXIPFrame.from_knx(raw)

        assert isinstance(knxipframe.body, TunnellingAck)
        assert knxipframe.body.communication_channel_id == 42
        assert knxipframe.body.sequence_counter == 23
        assert knxipframe.body.status_code == ErrorCode.E_NO_ERROR

        tunnelling_ack = TunnellingAck(
            communication_channel_id=42,
            sequence_counter=23,
        )
        knxipframe2 = KNXIPFrame.init_from_body(tunnelling_ack)

        assert knxipframe2.to_knx() == raw

    def test_from_knx_wrong_ack_information(self) -> None:
        """Test parsing and streaming wrong TunnellingAck (wrong length byte)."""
        raw = bytes((0x06, 0x10, 0x04, 0x21, 0x00, 0x0A, 0x03, 0x2A, 0x17, 0x00))
        with pytest.raises(CouldNotParseKNXIP):
            KNXIPFrame.from_knx(raw)

    def test_from_knx_wrong_ack_information2(self) -> None:
        """Test parsing and streaming wrong TunnellingAck (wrong length)."""
        raw = bytes((0x06, 0x10, 0x04, 0x21, 0x00, 0x0A, 0x04, 0x2A, 0x17))
        with pytest.raises(CouldNotParseKNXIP):
            KNXIPFrame.from_knx(raw)

    def test_from_knx_empty_body_raises_could_not_parse(self) -> None:
        """Test header-only frame (total_length == 6) raises CouldNotParseKNXIP."""
        # 06 10 04 21 00 06: valid 6-byte header, total_length=6, empty body
        raw = bytes.fromhex("061004210006")
        with pytest.raises(CouldNotParseKNXIP):
            KNXIPFrame.from_knx(raw)
