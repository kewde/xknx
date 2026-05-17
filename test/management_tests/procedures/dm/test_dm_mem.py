"""Tests for dmp_mem_read_r_co and dmp_mem_write_r_co - KNX 03.05.02 sections 3.16/3.18."""

import asyncio
from unittest.mock import AsyncMock

import pytest

from xknx import XKNX
from xknx.exceptions import ManagementConnectionError
from xknx.management.procedures.dm.dm_mem_read import dmp_mem_read_r_co
from xknx.management.procedures.dm.dm_mem_write import dmp_mem_write_r_co
from xknx.telegram import IndividualAddress, Telegram, TelegramDirection, apci, tpci


@pytest.fixture
def xknx_setup() -> XKNX:
    """Set up XKNX with mocked cemi_handler."""
    xknx = XKNX()
    xknx.cemi_handler = AsyncMock()
    return xknx


async def test_dmp_mem_read_r_co_single_chunk(xknx_setup: XKNX) -> None:
    """Test dmp_mem_read_r_co with data fitting in single chunk."""
    xknx = xknx_setup
    ia = IndividualAddress("4.0.10")

    conn = await xknx.management.connect(ia)
    xknx.cemi_handler.send_telegram.reset_mock()

    async def respond() -> None:
        while xknx.cemi_handler.send_telegram.call_count < 1:  # noqa: ASYNC110
            await asyncio.sleep(0)
        ack = Telegram(
            source_address=ia,
            destination_address=xknx.current_address,
            direction=TelegramDirection.INCOMING,
            tpci=tpci.TAck(0),
        )
        response = Telegram(
            source_address=ia,
            destination_address=xknx.current_address,
            direction=TelegramDirection.INCOMING,
            tpci=tpci.TDataConnected(0),
            payload=apci.MemoryResponse(address=0x1000, data=b"\x01\x02\x03\x04"),
        )
        xknx.management.process(ack)
        xknx.management.process(response)

    responder = asyncio.create_task(respond())
    data = await dmp_mem_read_r_co(conn, address=0x1000, count=4)
    await responder

    assert data == b"\x01\x02\x03\x04"
    await conn.disconnect()


async def test_dmp_mem_read_r_co_multiple_chunks(xknx_setup: XKNX) -> None:
    """Test dmp_mem_read_r_co with data requiring multiple chunks."""
    xknx = xknx_setup
    ia = IndividualAddress("4.0.10")

    conn = await xknx.management.connect(ia)
    xknx.cemi_handler.send_telegram.reset_mock()

    async def respond() -> None:
        while xknx.cemi_handler.send_telegram.call_count < 1:  # noqa: ASYNC110
            await asyncio.sleep(0)
        ack0 = Telegram(
            source_address=ia,
            destination_address=xknx.current_address,
            direction=TelegramDirection.INCOMING,
            tpci=tpci.TAck(0),
        )
        response0 = Telegram(
            source_address=ia,
            destination_address=xknx.current_address,
            direction=TelegramDirection.INCOMING,
            tpci=tpci.TDataConnected(0),
            payload=apci.MemoryResponse(address=0x1000, data=b"\x01\x02\x03\x04"),
        )
        xknx.management.process(ack0)
        xknx.management.process(response0)

        while xknx.cemi_handler.send_telegram.call_count < 3:  # noqa: ASYNC110
            await asyncio.sleep(0)
        ack1 = Telegram(
            source_address=ia,
            destination_address=xknx.current_address,
            direction=TelegramDirection.INCOMING,
            tpci=tpci.TAck(1),
        )
        response1 = Telegram(
            source_address=ia,
            destination_address=xknx.current_address,
            direction=TelegramDirection.INCOMING,
            tpci=tpci.TDataConnected(1),
            payload=apci.MemoryResponse(address=0x1004, data=b"\x05\x06"),
        )
        xknx.management.process(ack1)
        xknx.management.process(response1)

    responder = asyncio.create_task(respond())
    data = await dmp_mem_read_r_co(conn, address=0x1000, count=6, max_chunk_size=4)
    await responder

    assert data == b"\x01\x02\x03\x04\x05\x06"
    await conn.disconnect()


async def test_dmp_mem_read_r_co_empty(xknx_setup: XKNX) -> None:
    """Test dmp_mem_read_r_co with zero count returns empty bytes."""
    xknx = xknx_setup
    ia = IndividualAddress("4.0.10")

    conn = await xknx.management.connect(ia)
    data = await dmp_mem_read_r_co(conn, address=0x1000, count=0)

    assert data == b""
    await conn.disconnect()


async def test_dmp_mem_write_r_co_single_chunk(xknx_setup: XKNX) -> None:
    """Test dmp_mem_write_r_co with data fitting in single chunk (no response expected)."""
    xknx = xknx_setup
    ia = IndividualAddress("4.0.10")

    conn = await xknx.management.connect(ia)
    xknx.cemi_handler.send_telegram.reset_mock()

    async def respond() -> None:
        while xknx.cemi_handler.send_telegram.call_count < 1:  # noqa: ASYNC110
            await asyncio.sleep(0)
        ack = Telegram(
            source_address=ia,
            destination_address=xknx.current_address,
            direction=TelegramDirection.INCOMING,
            tpci=tpci.TAck(0),
        )
        xknx.management.process(ack)

    responder = asyncio.create_task(respond())
    await dmp_mem_write_r_co(conn, address=0x2000, data=b"\xAA\xBB\xCC")
    await responder

    await conn.disconnect()


async def test_dmp_mem_write_r_co_with_verify(xknx_setup: XKNX) -> None:
    """Test dmp_mem_write_r_co with verify enabled (write + read-back)."""
    xknx = xknx_setup
    ia = IndividualAddress("4.0.10")

    conn = await xknx.management.connect(ia)
    xknx.cemi_handler.send_telegram.reset_mock()

    async def respond() -> None:
        while xknx.cemi_handler.send_telegram.call_count < 1:  # noqa: ASYNC110
            await asyncio.sleep(0)
        ack0 = Telegram(
            source_address=ia,
            destination_address=xknx.current_address,
            direction=TelegramDirection.INCOMING,
            tpci=tpci.TAck(0),
        )
        xknx.management.process(ack0)

        while xknx.cemi_handler.send_telegram.call_count < 2:  # noqa: ASYNC110
            await asyncio.sleep(0)
        ack1 = Telegram(
            source_address=ia,
            destination_address=xknx.current_address,
            direction=TelegramDirection.INCOMING,
            tpci=tpci.TAck(1),
        )
        read_response = Telegram(
            source_address=ia,
            destination_address=xknx.current_address,
            direction=TelegramDirection.INCOMING,
            tpci=tpci.TDataConnected(0),
            payload=apci.MemoryResponse(address=0x2000, data=b"\xAA\xBB"),
        )
        xknx.management.process(ack1)
        xknx.management.process(read_response)

    responder = asyncio.create_task(respond())
    await dmp_mem_write_r_co(conn, address=0x2000, data=b"\xAA\xBB", verify=True)
    await responder

    await conn.disconnect()


async def test_dmp_mem_write_r_co_verify_failure(xknx_setup: XKNX) -> None:
    """Test dmp_mem_write_r_co raises error when verify fails."""
    xknx = xknx_setup
    ia = IndividualAddress("4.0.10")

    conn = await xknx.management.connect(ia)
    xknx.cemi_handler.send_telegram.reset_mock()

    async def respond() -> None:
        while xknx.cemi_handler.send_telegram.call_count < 1:  # noqa: ASYNC110
            await asyncio.sleep(0)
        ack0 = Telegram(
            source_address=ia,
            destination_address=xknx.current_address,
            direction=TelegramDirection.INCOMING,
            tpci=tpci.TAck(0),
        )
        xknx.management.process(ack0)

        while xknx.cemi_handler.send_telegram.call_count < 2:  # noqa: ASYNC110
            await asyncio.sleep(0)
        ack1 = Telegram(
            source_address=ia,
            destination_address=xknx.current_address,
            direction=TelegramDirection.INCOMING,
            tpci=tpci.TAck(1),
        )
        read_response = Telegram(
            source_address=ia,
            destination_address=xknx.current_address,
            direction=TelegramDirection.INCOMING,
            tpci=tpci.TDataConnected(0),
            payload=apci.MemoryResponse(address=0x2000, data=b"\xFF\xFF"),
        )
        xknx.management.process(ack1)
        xknx.management.process(read_response)

    responder = asyncio.create_task(respond())
    with pytest.raises(ManagementConnectionError, match="Memory verify failed"):
        await dmp_mem_write_r_co(conn, address=0x2000, data=b"\xAA\xBB", verify=True)
    await responder

    await conn.disconnect()


async def test_dmp_mem_write_r_co_empty(xknx_setup: XKNX) -> None:
    """Test dmp_mem_write_r_co with empty data does nothing."""
    xknx = xknx_setup
    ia = IndividualAddress("4.0.10")

    conn = await xknx.management.connect(ia)
    xknx.cemi_handler.send_telegram.reset_mock()

    await dmp_mem_write_r_co(conn, address=0x2000, data=b"")

    assert xknx.cemi_handler.send_telegram.call_count == 0
    await conn.disconnect()
