"""Package for management procedures as described in KNX-Standard 3.5.2."""

# ruff: noqa: F401
from .interface_object import nm_interface_object_scan
from .management import Management, P2PConnection
from .max_apdu import (
    MaxApduResult,
    nm_discover_max_apdu_length,
    nm_read_max_apdu_length,
)
