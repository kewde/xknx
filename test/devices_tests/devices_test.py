"""Unit test for devices container within XKNX."""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from xknx import XKNX
from xknx.devices import BinarySensor, Device, Light, Switch
from xknx.dpt import DPTBinary
from xknx.telegram import GroupAddress, Telegram
from xknx.telegram.apci import GroupValueWrite


class TestDevices:
    """Test class for devices container within XKNX."""

    #
    # XKNX Config
    #
    def test_get_item(self) -> None:
        """Test get item by name or by index."""
        xknx = XKNX()
        light1 = Light(xknx, "Living-Room.Light_1", group_address_switch="1/6/7")
        xknx.devices.async_add(light1)
        switch1 = Switch(xknx, "TestOutlet_1", group_address="1/2/3")
        xknx.devices.async_add(switch1)
        light2 = Light(xknx, "Living-Room.Light_2", group_address_switch="1/6/8")
        xknx.devices.async_add(light2)
        switch2 = Switch(xknx, "TestOutlet_2", group_address="1/2/4")
        xknx.devices.async_add(switch2)

        assert xknx.devices["Living-Room.Light_1"] == light1
        assert xknx.devices["TestOutlet_1"] == switch1
        assert xknx.devices["Living-Room.Light_2"] == light2
        assert xknx.devices["TestOutlet_2"] == switch2
        with pytest.raises(KeyError):
            # pylint: disable=pointless-statement
            xknx.devices["TestOutlet_2sdds"]

        assert xknx.devices[0] == light1
        assert xknx.devices[1] == switch1
        assert xknx.devices[2] == light2
        assert xknx.devices[3] == switch2
        with pytest.raises(IndexError):
            # pylint: disable=pointless-statement
            xknx.devices[4]

    def test_device_by_group_address(self) -> None:
        """Test get devices by group address."""
        xknx = XKNX()

        light1 = Light(xknx, "Livingroom", group_address_switch="1/6/7")
        sensor1 = BinarySensor(xknx, "Diningroom", group_address_state="3/0/1")
        sensor2 = BinarySensor(xknx, "Diningroom", group_address_state="3/0/1")
        light2 = Light(xknx, "Livingroom", group_address_switch="1/6/8")
        xknx.devices.async_add(light1)
        xknx.devices.async_add(sensor1)
        xknx.devices.async_add(sensor2)
        xknx.devices.async_add(light2)

        assert tuple(xknx.devices.devices_by_group_address(GroupAddress("1/6/7"))) == (
            light1,
        )
        assert tuple(xknx.devices.devices_by_group_address(GroupAddress("1/6/8"))) == (
            light2,
        )
        assert tuple(xknx.devices.devices_by_group_address(GroupAddress("3/0/1"))) == (
            sensor1,
            sensor2,
        )

    def test_iter(self) -> None:
        """Test __iter__() function."""
        xknx = XKNX()

        light1 = Light(xknx, "Livingroom", group_address_switch="1/6/7")
        sensor1 = BinarySensor(xknx, "Diningroom", group_address_state="3/0/1")
        sensor2 = BinarySensor(xknx, "Diningroom", group_address_state="3/0/1")
        light2 = Light(xknx, "Livingroom", group_address_switch="1/6/8")
        xknx.devices.async_add(light1)
        xknx.devices.async_add(sensor1)
        xknx.devices.async_add(sensor2)
        xknx.devices.async_add(light2)

        assert tuple(iter(xknx.devices)) == (light1, sensor1, sensor2, light2)

    def test_len(self) -> None:
        """Test len() function."""
        xknx = XKNX()
        assert len(xknx.devices) == 0

        light = Light(xknx, "Living-Room.Light_1", group_address_switch="1/6/7")
        xknx.devices.async_add(light)
        assert len(xknx.devices) == 1

        binary_sensor = BinarySensor(
            xknx, "DiningRoom.Motion.Sensor", group_address_state="3/0/1"
        )
        xknx.devices.async_add(binary_sensor)
        assert len(xknx.devices) == 2

        xknx.devices.async_remove(light)
        assert len(xknx.devices) == 1

        xknx.devices.async_add(light)
        assert len(xknx.devices) == 2

    def test_contains(self) -> None:
        """Test __contains__() function."""
        xknx = XKNX()
        xknx.devices.async_add(
            Light(xknx, "Living-Room.Light_1", group_address_switch="1/6/7")
        )
        xknx.devices.async_add(
            Light(xknx, "Living-Room.Light_2", group_address_switch="1/6/8")
        )

        assert "Living-Room.Light_1" in xknx.devices
        assert "Living-Room.Light_2" in xknx.devices
        assert "Living-Room.Light_3" not in xknx.devices

    @patch.multiple(Device, __abstractmethods__=set())
    def test_add_remove(self) -> None:
        """Tesst add and remove functions."""
        xknx = XKNX()
        device1 = Device(xknx, "TestDevice1")
        device2 = Device(xknx, "TestDevice2")
        xknx.devices.async_add(device1)
        xknx.devices.async_add(device2)
        assert len(xknx.devices) == 2
        xknx.devices.async_remove(device1)
        assert len(xknx.devices) == 1
        assert "TestDevice1" not in xknx.devices
        xknx.devices.async_remove(device2)
        assert len(xknx.devices) == 0

    async def test_modification_of_device(self) -> None:
        """Test if devices object does store references and not copies of objects."""
        xknx = XKNX()
        light1 = Light(xknx, "Living-Room.Light_1", group_address_switch="1/6/7")
        xknx.devices.async_add(light1)
        for device in xknx.devices:
            await device.set_on()
            xknx.devices.process(xknx.telegrams.get_nowait())
        assert light1.state

        device2 = xknx.devices["Living-Room.Light_1"]
        await device2.set_off()
        xknx.devices.process(xknx.telegrams.get_nowait())
        assert not light1.state

        for device in xknx.devices.devices_by_group_address(GroupAddress("1/6/7")):
            await device.set_on()
            xknx.devices.process(xknx.telegrams.get_nowait())
        assert light1.state

    #
    # TEST SYNC
    #
    @patch.multiple(Device, __abstractmethods__=set())
    async def test_sync(self) -> None:
        """Test sync function."""
        xknx = XKNX()
        xknx.devices.async_add(Device(xknx, "TestDevice1"))
        xknx.devices.async_add(Device(xknx, "TestDevice2"))
        with patch("xknx.devices.Device.sync", new_callable=AsyncMock) as mock_sync:
            await xknx.devices.sync()
            assert mock_sync.call_count == 2

    #
    # TEST CALLBACK
    #
    @patch.multiple(Device, __abstractmethods__=set())
    def test_device_updated_callback(self) -> None:
        """Test if device updated callback is called correctly if device was updated."""
        xknx = XKNX()
        device1 = Device(xknx, "TestDevice1")
        device2 = Device(xknx, "TestDevice2")
        xknx.devices.async_add(device1)
        xknx.devices.async_add(device2)

        after_update_callback1 = Mock()
        after_update_callback2 = Mock()

        # Registering both callbacks
        xknx.devices.register_device_updated_cb(after_update_callback1)
        xknx.devices.register_device_updated_cb(after_update_callback2)

        # Triggering first device. Both callbacks to be called
        device1.after_update()
        after_update_callback1.assert_called_with(device1)
        after_update_callback2.assert_called_with(device1)
        after_update_callback1.reset_mock()
        after_update_callback2.reset_mock()

        # Triggering 2nd device. Both callbacks have to be called
        device2.after_update()
        after_update_callback1.assert_called_with(device2)
        after_update_callback2.assert_called_with(device2)
        after_update_callback1.reset_mock()
        after_update_callback2.reset_mock()

        # Unregistering first callback
        xknx.devices.unregister_device_updated_cb(after_update_callback1)

        # Triggering first device. Only second callback has to be called
        device1.after_update()
        after_update_callback1.assert_not_called()
        after_update_callback2.assert_called_with(device1)
        after_update_callback1.reset_mock()
        after_update_callback2.reset_mock()

        # Unregistering second callback
        xknx.devices.unregister_device_updated_cb(after_update_callback2)

        # Triggering second device. No callback should be called
        device2.after_update()
        after_update_callback1.assert_not_called()
        after_update_callback2.assert_not_called()
        after_update_callback1.reset_mock()
        after_update_callback2.reset_mock()

    #
    # TEST RE-ENTRANT MUTATION DURING DISPATCH
    #
    async def test_process_self_removing_device_does_not_skip_siblings(self) -> None:
        """
        Test that a device removing itself mid-dispatch doesn't skip siblings.

        A device_updated_cb that synchronously calls async_remove() from within a
        device's own process() frame must not cause still-registered siblings
        sharing the group address to be silently skipped.
        """
        xknx = XKNX()
        a = BinarySensor(xknx, "A", group_address_state="1/2/3", always_callback=True)
        b = BinarySensor(xknx, "B", group_address_state="1/2/3", always_callback=True)
        c = BinarySensor(xknx, "C", group_address_state="1/2/3", always_callback=True)
        xknx.devices.async_add(a)
        xknx.devices.async_add(b)
        xknx.devices.async_add(c)

        def cb(dev: Device) -> None:
            if dev is a:
                xknx.devices.async_remove(a)  # a removes ITSELF mid-process

        xknx.devices.register_device_updated_cb(cb)
        xknx.devices.process(
            Telegram(
                destination_address=GroupAddress("1/2/3"),
                payload=GroupValueWrite(DPTBinary(1)),
            )
        )

        assert a.state is True
        assert b.state is True
        assert c.state is True

    async def test_after_update_unregister_cb_does_not_skip_later_cb(self) -> None:
        """Test Device.after_update doesn't skip later callbacks on re-entrant unregister."""
        xknx = XKNX()
        device = BinarySensor(
            xknx, "D", group_address_state="1/2/3", always_callback=True
        )
        xknx.devices.async_add(device)
        calls: list[str] = []

        def cb_b(dev: Device) -> None:
            calls.append("cb_b")

        def cb_a(dev: Device) -> None:
            calls.append("cb_a")
            device.unregister_device_updated_cb(cb_b)

        device.register_device_updated_cb(cb_a)
        device.register_device_updated_cb(cb_b)
        device.after_update()
        assert calls == ["cb_a", "cb_b"]

    async def test_device_updated_unregister_cb_does_not_skip_later_cb(self) -> None:
        """Test Devices.device_updated doesn't skip later callbacks on re-entrant unregister."""
        xknx = XKNX()
        device = BinarySensor(
            xknx, "D", group_address_state="1/2/3", always_callback=True
        )
        xknx.devices.async_add(device)
        calls: list[str] = []

        def cb_b(dev: Device) -> None:
            calls.append("cb_b")

        def cb_a(dev: Device) -> None:
            calls.append("cb_a")
            xknx.devices.unregister_device_updated_cb(cb_b)

        xknx.devices.register_device_updated_cb(cb_a)
        xknx.devices.register_device_updated_cb(cb_b)
        device.after_update()
        assert calls == ["cb_a", "cb_b"]
