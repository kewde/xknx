"""Unit test for KNX/IP TCP transport stream parsing."""

from unittest.mock import Mock

from xknx.io.transport import TCPTransport
from xknx.knxip import HPAI, HostProtocol, KNXIPFrame

VALID_FRAME = bytes.fromhex(
    "06 10 04 20 00 15 04 02 51 00 29 00 bc e0 10 fa 09 2d 01 00 80"
)
TWO_VALID_FRAMES = bytes.fromhex(
    "06 10 04 20 00 15 04 02 51 00 29 00 bc e0 10 fa 09 2d 01 00 80"
    "06 10 04 20 00 15 04 02 52 00 29 00 bc e0 10 1f 08 2d 01 00 80"
)


def _remote_hpai() -> HPAI:
    return HPAI("127.0.0.1", 3671, protocol=HostProtocol.IPV4_TCP)


class TestTCPTransport:
    """Test class for TCPTransport.data_received_callback."""

    def test_supported_frame_invokes_callback(self) -> None:
        """A single valid KNX/IP frame is parsed and dispatched to callbacks."""
        transport = TCPTransport(remote_addr=("127.0.0.1", 3671))
        callback = Mock()
        transport.register_callback(callback, None)

        transport.data_received_callback(VALID_FRAME)

        callback.assert_called_once_with(
            KNXIPFrame.from_knx(VALID_FRAME)[0], _remote_hpai(), transport
        )
        assert transport._buffer == b""

    def test_pipelined_frames_each_invoke_callback(self) -> None:
        """Concatenated frames delivered in one chunk are all parsed and dispatched."""
        transport = TCPTransport(remote_addr=("127.0.0.1", 3671))
        callback = Mock()
        transport.register_callback(callback, None)

        transport.data_received_callback(TWO_VALID_FRAMES)

        assert callback.call_count == 2
        frame_1, rest_1 = KNXIPFrame.from_knx(TWO_VALID_FRAMES)
        frame_2, _rest_2 = KNXIPFrame.from_knx(rest_1)
        callback.assert_any_call(frame_1, _remote_hpai(), transport)
        callback.assert_any_call(frame_2, _remote_hpai(), transport)
        assert transport._buffer == b""

    def test_unsupported_service_type_does_not_raise(self) -> None:
        """An unimplemented KNX/IP service type (0xffff) is logged and skipped, not crashing."""
        transport = TCPTransport(remote_addr=("127.0.0.1", 3671))
        callback = Mock()
        transport.register_callback(callback, None)
        unparsable = bytes([0x06, 0x10, 0xFF, 0xFF, 0x00, 0x10]) + b"\x00" * 10

        transport.data_received_callback(unparsable)

        callback.assert_not_called()
        assert transport._buffer == b""

    def test_unsupported_service_type_followed_by_valid_frame_resumes(self) -> None:
        """A valid frame pipelined right after an unparsable frame is still processed."""
        transport = TCPTransport(remote_addr=("127.0.0.1", 3671))
        callback = Mock()
        transport.register_callback(callback, None)
        unparsable = bytes((0x06, 0x10, 0x00, 0x00, 0x00, 0x0A)) + b"\x00" * 4

        transport.data_received_callback(unparsable + VALID_FRAME)

        callback.assert_called_once_with(
            KNXIPFrame.from_knx(VALID_FRAME)[0], _remote_hpai(), transport
        )
        assert transport._buffer == b""

    def test_malformed_body_of_known_service_type_does_not_raise(self) -> None:
        """A malformed TunnellingAck body (invalid structure_length) is dropped without raising."""
        transport = TCPTransport(remote_addr=("127.0.0.1", 3671))
        callback = Mock()
        transport.register_callback(callback, None)
        malformed = bytes((0x06, 0x10, 0x04, 0x21, 0x00, 0x0A, 0x05, 0x00, 0x00, 0x00))

        transport.data_received_callback(malformed)

        callback.assert_not_called()
        assert transport._buffer == b""

    def test_wrong_header_length_does_not_raise_nor_resume(self) -> None:
        """A wrong header-length byte leaves no recoverable frame boundary; the chunk is dropped."""
        transport = TCPTransport(remote_addr=("127.0.0.1", 3671))
        callback = Mock()
        transport.register_callback(callback, None)
        bad = bytes((0x05, 0x10, 0x04, 0x21, 0x00, 0x0A)) + b"\x00" * 4 + VALID_FRAME

        transport.data_received_callback(bad)

        callback.assert_not_called()
        assert transport._buffer == b""

    def test_incomplete_frame_is_buffered_then_completed(self) -> None:
        """A truncated frame is buffered until its remainder arrives and is then parsed."""
        transport = TCPTransport(remote_addr=("127.0.0.1", 3671))
        callback = Mock()
        transport.register_callback(callback, None)
        partial = VALID_FRAME[:15]

        transport.data_received_callback(partial)

        callback.assert_not_called()
        assert transport._buffer == partial

        transport.data_received_callback(VALID_FRAME[15:])

        callback.assert_called_once_with(
            KNXIPFrame.from_knx(VALID_FRAME)[0], _remote_hpai(), transport
        )
        assert transport._buffer == b""
