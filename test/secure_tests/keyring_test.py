"""Unit test for keyring reader."""

from pathlib import Path

import pytest

from xknx.exceptions.exception import InvalidSecureConfiguration
from xknx.secure.keyring import (
    InterfaceType,
    Keyring,
    KeyringSAXContentHandler,
    XMLDevice,
    XMLInterface,
    sync_load_keyring,
    verify_keyring_signature,
)
from xknx.telegram import GroupAddress, IndividualAddress


class TestKeyRing:
    """Test class for keyring."""

    keyring_test_file = Path(__file__).parent / "resources/keyring.knxkeys"
    testcase_file: str = Path(__file__).parent / "resources/testcase.knxkeys"
    special_chars_file = (
        Path(__file__).parent / "resources/special_chars_secure_tunnel.knxkeys"
    )
    data_secure_ip = (
        Path(__file__).parent / "resources/DataSecure_only_one_interface.knxkeys"
    )
    data_secure_usb = Path(__file__).parent / "resources/DataSecure_usb.knxkeys"

    @staticmethod
    def assert_interface(
        keyring: Keyring, password: str, ia: IndividualAddress
    ) -> None:
        """Verify password for given user."""
        matched = False
        if interface := keyring.get_tunnel_interface_by_individual_address(ia):
            matched = True
            assert interface.decrypted_password == password

        assert matched

    def test_load_keyring_test(self) -> None:
        """Test load keyring from knxkeys file."""
        keyring = sync_load_keyring(self.keyring_test_file, "pwd")
        TestKeyRing.assert_interface(keyring, "user4", IndividualAddress("1.1.4"))
        TestKeyRing.assert_interface(keyring, "@zvI1G&_", IndividualAddress("1.1.6"))
        TestKeyRing.assert_interface(keyring, "ZvDY-:g#", IndividualAddress("1.1.7"))
        TestKeyRing.assert_interface(keyring, "user2", IndividualAddress("1.1.2"))
        assert keyring.backbone.multicast_address == "224.0.23.12"
        assert keyring.backbone.latency == 1000
        assert keyring.backbone.decrypted_key == bytes.fromhex(
            "96f034fccf510760cbd63da0f70d4a9d"
        )

    def test_load_testcase_file(self) -> None:
        """Test load keyring from knxkeys file."""
        keyring = sync_load_keyring(self.testcase_file, "password")
        TestKeyRing.assert_interface(keyring, "user1", IndividualAddress("1.0.1"))
        TestKeyRing.assert_interface(keyring, "user2", IndividualAddress("1.0.11"))
        TestKeyRing.assert_interface(keyring, "user3", IndividualAddress("1.0.12"))
        TestKeyRing.assert_interface(keyring, "user4", IndividualAddress("1.0.13"))
        assert keyring.devices[0].decrypted_management_password == "commissioning"
        assert keyring.backbone.multicast_address == "224.0.23.12"
        assert keyring.backbone.latency == 1000
        assert keyring.backbone.decrypted_key == bytes.fromhex(
            "cf89fd0f18f4889783c7ef44ee1f5e14"
        )

        interface: XMLInterface = keyring.interfaces[0]
        device: XMLDevice = keyring.get_device_by_interface(interface)
        assert device is not None
        assert device.decrypted_authentication == "authenticationcode"

    def test_load_special_chars_file(self) -> None:
        """Test load keyring from knxkeys file."""
        keyring = sync_load_keyring(self.special_chars_file, "test")
        TestKeyRing.assert_interface(keyring, "tunnel_2", IndividualAddress("1.0.2"))
        TestKeyRing.assert_interface(keyring, "tunnel_3", IndividualAddress("1.0.3"))
        TestKeyRing.assert_interface(keyring, "tunnel_4", IndividualAddress("1.0.4"))
        TestKeyRing.assert_interface(keyring, "tunnel_5", IndividualAddress("1.0.5"))
        TestKeyRing.assert_interface(keyring, "tunnel_6", IndividualAddress("1.0.6"))
        assert keyring.backbone is None

    def test_load_data_secure_ip(self) -> None:
        """Test load keyring from knxkeys file."""
        keyring = sync_load_keyring(self.data_secure_ip, "test")
        assert len(keyring.interfaces) == 1
        tunnel = keyring.interfaces[0]
        assert tunnel is not None
        assert tunnel.password is None
        assert tunnel.decrypted_password is None
        assert tunnel.user_id is None
        assert tunnel.type is InterfaceType.TUNNELING
        assert len(tunnel.group_addresses) == 3
        assert tunnel.group_addresses[GroupAddress("0/0/1")] == [
            IndividualAddress("1.0.1"),
            IndividualAddress("1.0.2"),
        ]
        assert tunnel.group_addresses[GroupAddress("0/0/3")] == [
            IndividualAddress("1.0.1"),
            IndividualAddress("1.0.2"),
        ]
        assert tunnel.group_addresses[GroupAddress("31/7/255")] == []
        assert keyring.backbone is None

    def test_load_data_secure_usb(self) -> None:
        """Test load keyring from knxkeys file."""
        keyring = sync_load_keyring(self.data_secure_usb, "test")
        assert len(keyring.interfaces) == 1
        interface = keyring.interfaces[0]
        assert interface is not None
        assert interface.password is None
        assert interface.decrypted_password is None
        assert interface.user_id is None
        assert interface.host is None
        assert interface.type is InterfaceType.USB
        assert len(interface.group_addresses) == 1
        assert interface.group_addresses[GroupAddress("31/7/255")] == [
            IndividualAddress("1.0.4")
        ]
        assert keyring.backbone is None

    def test_verify_signature(self) -> None:
        """Test signature verification."""
        assert verify_keyring_signature(self.keyring_test_file, "pwd")
        assert verify_keyring_signature(self.testcase_file, "password")
        assert verify_keyring_signature(self.special_chars_file, "test")

    def test_invalid_signature(self) -> None:
        """Test invalid signature throws error."""
        with pytest.raises(InvalidSecureConfiguration):
            sync_load_keyring(self.testcase_file, "wrong_password")

    def test_raises_error(self) -> None:
        """Test raises error if password is wrong."""
        with pytest.raises(InvalidSecureConfiguration):
            sync_load_keyring(
                self.testcase_file, "wrong_password", validate_signature=False
            )

    def test_append_string_accepts_values_up_to_255_bytes(self) -> None:
        """append_string accepts values whose UTF-8 byte length is <= 255."""
        handler = KeyringSAXContentHandler("pwd")

        # exactly 255 single-byte characters (boundary) is accepted
        handler.append_string("a" * 255)
        assert handler.output[-256] == 255

        # multi-byte UTF-8: 254 bytes (127 x ö) + 1 single byte = 255 bytes
        handler.output.clear()
        handler.append_string("ö" * 127 + "a")
        assert handler.output[0] == 255
        assert len(handler.output) == 256

        # bytes input at exactly the boundary is also accepted
        handler.output.clear()
        handler.append_string(b"\x00" * 255)
        assert handler.output[0] == 255

    def test_append_string_rejects_values_exceeding_255_bytes(self) -> None:
        """append_string raises InvalidSecureConfiguration (not ValueError) for >255 bytes."""
        # single-byte characters exceeding the boundary
        handler = KeyringSAXContentHandler("pwd")
        with pytest.raises(InvalidSecureConfiguration):
            handler.append_string("a" * 256)

        # multi-byte UTF-8: char count below 256 but byte count above the boundary
        handler = KeyringSAXContentHandler("pwd")
        with pytest.raises(InvalidSecureConfiguration):
            handler.append_string("ö" * 128)  # 256 UTF-8 bytes

        # bytes input exceeding the boundary
        handler = KeyringSAXContentHandler("pwd")
        with pytest.raises(InvalidSecureConfiguration):
            handler.append_string(b"\x00" * 256)

    def _write_long_attribute_keyring(self, tmp_path: Path) -> Path:
        """Write a keyring file whose Senders attribute exceeds 255 UTF-8 bytes."""
        long_senders = " ".join(f"1.0.{i}" for i in range(40))
        assert len(long_senders.encode("utf-8")) > 255
        keyring_file = tmp_path / "long_senders.knxkeys"
        keyring_file.write_text(
            '<?xml version="1.0" encoding="utf-8"?>\n'
            '<Keyring Project="Test" CreatedBy="ETS" '
            'Created="2023-01-01T00:00:00" '
            'Signature="AAAAAAAAAAAAAAAAAAAAAA==" '
            'xmlns="http://knx.org/xml/keyring/1">\n'
            '  <Interface Type="Tunneling" Host="1.0.0" '
            'IndividualAddress="1.0.1">\n'
            f'    <Group Address="1" Senders="{long_senders}" />\n'
            "  </Interface>\n"
            "</Keyring>\n",
            encoding="utf-8",
        )
        return keyring_file

    def test_verify_keyring_signature_long_attribute_raises_invalid(
        self, tmp_path: Path
    ) -> None:
        """verify_keyring_signature raises InvalidSecureConfiguration, not ValueError."""
        keyring_file = self._write_long_attribute_keyring(tmp_path)
        with pytest.raises(InvalidSecureConfiguration):
            verify_keyring_signature(keyring_file, "pwd")

    def test_sync_load_keyring_long_attribute_raises_invalid(
        self, tmp_path: Path
    ) -> None:
        """
        sync_load_keyring raises InvalidSecureConfiguration for >255 byte attrs.

        Consistent with the established failure-path pattern
        (test_invalid_signature / test_raises_error), not a raw ValueError.
        """
        keyring_file = self._write_long_attribute_keyring(tmp_path)
        with pytest.raises(InvalidSecureConfiguration):
            sync_load_keyring(keyring_file, "pwd")

    def test_sync_load_keyring_long_attribute_without_signature_validation(
        self, tmp_path: Path
    ) -> None:
        """
        The long-attribute bug is isolated to the SAX signature handler.

        The DOM parser path (used when validate_signature=False) handles long
        string attributes fine: the Senders list is parsed into individual
        addresses without any 255-byte limit, and there is no encrypted payload
        to fail. The loader therefore succeeds rather than crashing.
        """
        keyring_file = self._write_long_attribute_keyring(tmp_path)
        keyring = sync_load_keyring(keyring_file, "pwd", validate_signature=False)
        assert len(keyring.interfaces) == 1
        group_addresses = keyring.interfaces[0].group_addresses
        assert len(group_addresses) == 1
        senders = next(iter(group_addresses.values()))
        assert len(senders) == 40
        assert senders[0] == IndividualAddress("1.0.0")
        assert senders[-1] == IndividualAddress("1.0.39")

    def test_keyring_get_methods_full(self) -> None:
        """Test keyring get_* methods for full project export."""
        keyring = sync_load_keyring(self.keyring_test_file, "pwd")
        test_interfaces = keyring.get_tunnel_interfaces_by_host(
            host=IndividualAddress("1.1.10")
        )
        assert len(test_interfaces) == 1
        test_interface = test_interfaces[0]

        test_device = keyring.get_device_by_interface(interface=test_interface)
        assert test_device.individual_address == IndividualAddress("1.1.10")

        test_host = keyring.get_tunnel_host_by_interface(
            tunnelling_slot=IndividualAddress("1.1.8")
        )
        assert test_host == IndividualAddress("1.1.0")

        test_host = keyring.get_tunnel_host_by_interface(
            tunnelling_slot=IndividualAddress("1.1.10")
        )
        assert test_host is None

        test_interface = keyring.get_tunnel_interface_by_host_and_user_id(
            host=IndividualAddress("1.1.0"), user_id=4
        )
        assert test_interface.individual_address == IndividualAddress("1.1.7")

        test_interface = keyring.get_tunnel_interface_by_individual_address(
            tunnelling_slot=IndividualAddress("1.1.8")
        )
        assert test_interface.user_id == 8

        test_interface = keyring.get_tunnel_interface_by_individual_address(
            tunnelling_slot=IndividualAddress("1.1.20")
        )
        assert test_interface.user_id is None
        assert test_interface.host == IndividualAddress("1.1.10")
        # this doesn't check for `type`, but there are no other than TUNNELLING interfaces in this keyring
        test_interface = keyring.get_interface_by_individual_address(
            individual_address=IndividualAddress("1.1.20")
        )
        assert test_interface.host == IndividualAddress("1.1.10")

        full_ga_key_table = keyring.get_data_secure_group_keys()
        assert len(full_ga_key_table) == 1

        individual_ga_key_table = keyring.get_data_secure_group_keys(
            receiver=IndividualAddress("1.1.7")
        )
        assert len(individual_ga_key_table) == 0

        ia_seq_nums = keyring.get_data_secure_senders()
        assert len(ia_seq_nums) == 5

    def test_keyring_get_methods_one_interface(self) -> None:
        """Test keyring get_* methods for partial export."""
        keyring = sync_load_keyring(self.data_secure_ip, "test")

        full_ga_key_table = keyring.get_data_secure_group_keys()
        assert len(full_ga_key_table) == 3

        individual_ga_key_table = keyring.get_data_secure_group_keys(
            receiver=IndividualAddress("1.0.4")
        )
        assert len(individual_ga_key_table) == 3

        ia_seq_nums = keyring.get_data_secure_senders()
        assert ia_seq_nums == {
            IndividualAddress("1.0.1"): 0,
            IndividualAddress("1.0.2"): 0,
        }

    def test_keyring_metadata(self) -> None:
        """Test keyring metadata parsing."""
        keyring = sync_load_keyring(self.data_secure_ip, "test")
        assert keyring.project_name == "DataSecure_only"
        assert keyring.created_by == "ETS 5.7.7 (Build 1428)"
        assert keyring.created == "2023-02-06T21:17:09"
        assert keyring.xmlns == "http://knx.org/xml/keyring/1"
