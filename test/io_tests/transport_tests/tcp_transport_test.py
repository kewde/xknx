"""Unit test for KNX/IP TCPTransport receive-path parsing."""

from unittest.mock import Mock

from xknx.io.transport import TCPTransport
from xknx.knxip import KNXIPServiceType


class TestTCPTransport:
    """Test class for xknx/io/TCPTransport receive-path parsing."""

    def test_data_received_malformed_complete_frame_does_not_raise(self) -> None:
        """
        A complete-but-malformed frame is dropped instead of crashing the transport.

        A TUNNELLING_REQUEST with ``total_length == 6`` carries an empty body, so
        the body parser raises ``CouldNotParseKNXIP``. The TCP receive callback
        must catch it and drop the frame gracefully rather than raising an
        ``UnboundLocalError`` (which asyncio treats as a fatal protocol error and
        uses to tear the transport down).
        """
        tcp_transport = TCPTransport(remote_addr=("192.168.1.2", 3671))
        malformed = bytes((0x06, 0x10, 0x04, 0x20, 0x00, 0x06))

        tcp_transport.data_received_callback(malformed)

        assert not tcp_transport._buffer

    def test_data_received_malformed_short_body_does_not_raise(self) -> None:
        """
        A too-short-but-present body (``total_length`` 7-9) is dropped without raising.

        Such a frame raises ``CouldNotParseKNXIP`` from the body parser; it must be
        handled by the same graceful drop path as the empty-body case.
        """
        tcp_transport = TCPTransport(remote_addr=("192.168.1.2", 3671))
        malformed = bytes((0x06, 0x10, 0x04, 0x20, 0x00, 0x07, 0x99))

        tcp_transport.data_received_callback(malformed)

        assert not tcp_transport._buffer

    def test_data_received_valid_frame_dispatches_and_continues(self) -> None:
        """
        A valid frame is dispatched and trailing data in the segment is parsed too.

        Two concatenated TUNNELLING_REQUEST frames received in a single TCP
        segment must each be dispatched (continuation parsing on the success path
        must keep working after the ``CouldNotParseKNXIP`` path was guarded).
        """
        tcp_transport = TCPTransport(remote_addr=("192.168.1.2", 3671))
        callback_mock = Mock()
        tcp_transport.register_callback(
            callback_mock, [KNXIPServiceType.TUNNELLING_REQUEST]
        )
        valid = bytes.fromhex("061004200015040117001100bce000004808010081")
        two_frames = valid + valid

        tcp_transport.data_received_callback(two_frames)

        assert callback_mock.call_count == 2

    def test_data_received_incomplete_frame_is_buffered(self) -> None:
        """
        An incomplete frame (declared length larger than available) is buffered.

        Declared ``total_length == 0x15`` (21) with only 7 bytes present must raise
        ``IncompleteKNXIPFrame`` and buffer the pending bytes rather than dispatch.
        """
        tcp_transport = TCPTransport(remote_addr=("192.168.1.2", 3671))
        callback_mock = Mock()
        tcp_transport.register_callback(
            callback_mock, [KNXIPServiceType.TUNNELLING_REQUEST]
        )
        incomplete = bytes((0x06, 0x10, 0x04, 0x20, 0x00, 0x15, 0x03))

        tcp_transport.data_received_callback(incomplete)

        callback_mock.assert_not_called()
        assert tcp_transport._buffer == incomplete
