"""
DM_Connect — KNX 03.05.02 §3.2 (PDF p. 67).

Spec text (verbatim from spec):

    Use
    This device Management Procedure shall be used to establish a connection to a Management Server
    with a specific Individual Address and to check the existence by reading the mask version.
    The connection is closed with a DM_Disconnect.
    Parameters of the Management Procedure
    DM_Connect (flags)
        flags    bit 0    use connection oriented / connectionless communication
                            0: connection oriented communication
                            1: connectionless communication
                 All other bits are reserved. These shall be set to 0. This shall be
                 tested by the Management Client.

    3.2.1 DMP_Connect_RCo
    This Management Procedure shall use the connection oriented communication mode.
    Used Application Layer Services for Management
    - A_Connect
    - A_DeviceDescriptor_Read

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Network / Management Server
        C->>S: A_Connect-PDU (destination_address = IA_target)
        alt negative A_Connect.Lcon => error: no connection established
        else this is, a positive A_Connect.Lcon is received
            Note right of S: If the device that occupies the IA_target does not support Transport Layer connections, it shall send a T_Disconnect-PDU.
            S->>C: A_Disconnect-PDU ()
            alt A_Disconnect-PDU is received => error: the device refuses the connection-oriented connection
            else no A_Disconnect-PDU is received
                Note right of S: If a device that occupies IA_target is present on the network, and does support Transport Layer connections, it shall have no other reaction on the bus than the Layer-2 acknowledge that initiates the above A_Connect.Lcon
                Note over C,S: The A_DeviceDescriptor_Read-PDU shall use DD0.
                C->>S: A_DeviceDescriptor_Read-PDU (destination_address = IA_test, descriptor_type = 0000h)
                S->>C: A_DeviceDescriptor_Response-PDU (descriptor_type, device_descriptor)
                Note over C,S: If the Management Client receives an A_DeviceDescriptor_Response-PDU it shall conclude that the Transport Layer connection has been established successfully.
                Note over C,S: If no A_DeviceDescriptor_Response-PDU is received after time-out => error: no connection established
            end
        end
    ```

    Exception handling
    There are several error situations when building up a connection oriented communication.
    - If the T_Connect.req telegram is not acknowledged by a Link Layer acknowledge (negative
        A_Connect.Lcon) then the Management Server with the Individual Address does not exist or the
        system is not configured correctly. (e.g. coupler, Domain Address ...)
    - If a T_Disconnect-telegram is sent out by the Management Server but no
        A_DeviceDescriptor_Response, the device with the Individual Address exists. The reason for this
        may either be that the Management Server is already using another connection, doesn't support
        connection oriented mode, or the time-out has elapsed.
    - If a T_Disconnect-telegram is sent out by the transport layer of the Management Client, then the
        system may not be configured correctly, or the Management Server doesn't exist.
    - If more than one A_DeviceDescriptor_Response-PDU is received, there is more than one device
        with the target address.
    If the above indicates the network may be configured incorrectly, than the network topology shall be
    checked. In all other cases, the DM_Connect may be repeated several times. If this procedure is not
    successful, the depending procedures shall be aborted.

    3.2.2 Procedure: DMP_Connect_RCl
    This Management Procedure shall be used to read the Device Descriptor of one Management Server
    (device). It shall allow differentiating between requesting DD0 and DD2 and is capable of handling
    both DD-types expected and unexpected.
    This Management Procedure shall use the point-to-point connectionless communication mode.
    DMP_Connect_RCl (/* [in] */ nm_ASAP, /* [in] */ nm_desc_type_req,
                    /* [out] */ nm_desc_type_res, /* [out] */ nm_desc_value_res)
        nm_ASAP:              The parameter shall contain the IA of the communication partner of
                              which the Device Descriptor is to be read.
        nm_desc_type_req:     This parameter shall contain the requested Device Descriptor Type; it
                              can be DD0 or DD2.
        nm_desc_type_res:     This result shall contain the DD-type with which the Management
                              Server has responded. This may be different from nm_desc_type_req.
                              Please refer to the exception handling.
        nm_desc_value_res:    This result shall contain the Device Descriptor value responded by the
                              Management Server.

    Used Application Layer services for Management
    - A_DeviceDescriptor_Read

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        Note over C,S: The Management Client shall send the A_DeviceDescriptor_Read-PDU to the Management Server. The ASAP shall equal nm_ASAP.
        C->>S: A_DeviceDescriptor_Read-PDU (descriptor_type = nm_desc_type_req)
        S->>C: A_DeviceDescriptor_Response-PDU (descriptor_type = nm_desc_type_res, device_descriptor = nm_desc_value_res)
    ```

    Exception handling
    There are several error situations when building up a connectionless communication.
    - If no A_DeviceDescriptor_Response-PDU is received, the Management Server with the Individual
        Address does not exist or the network is not configured correctly.
    - If more than one A_DeviceDescriptor_Response-PDU is received, there is more than one device
        with the target address.
    If the above indicates the network may be configured incorrectly, than the network topology shall be
    checked. In all other cases, the DM_Connect_RCl may be repeated several times. If this procedure is
    not successful, the depending procedures shall be aborted.

    3.2.3 Procedure: DMP_Connect_LEmi1
    Use
    This Management Procedure shall use the local communication with EMI 1. The Device Descriptor
    Type 0 shall be read from the memory location 4Eh – 4Fh.
    Used EMI-services for Management
    - PC_Get_Value

    Parameters of the Management Procedure
    DMP_Restart_LEmi1(/* [out] */ DD0, /* [out] */ DmpError)
        DD0:         Value of the Device Descriptor 0 as returned by the device.
        DmpError:    Possible error indication.

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        C->>S: PC_Get_Value.req message (Length = 2 octet, Address = 004Eh)
        S->>C: PC_Get_Value.con message (Length = 2 octet, Address = 004Eh, Data = DD0)
    ```

    Exception handling
    The general exception handling is applicable

    3.2.5 DMP_Connect_LcEMI
    If local management via the cEMI interface is required, the Management Client shall connect to the
    local device via cEMI and switch the communication mode to cEMI Transport Layer by setting
    PID_COMM_MODE to "cEMI Transport Layer". Further discovery (Device Descriptor,
    manufacturer…) is then done by the classic Application Layer services transferred via cEMI
    T_Data_Connected and T_Data_Individual.

    3.2.6 DMP_Connect_R_KNXnetIPDeviceManagement
    The Management Client establishes a KNXnet/IP Device Management connection to the KNX IP - or
    KNXnet/IP device. The device shall by this autonomously switch its cEMI communication mode to
    cEMI Transport Layer mode. Further discovery (Device Descriptor, manufacturer…) is then done by
    the classic Application Layer services transferred via cEMI T_Data_Connected and
    T_Data_Individual via KNXnet/IP DEVICE_CONFIGURATION_REQUEST frames.

    3.2.7 Procedure: DM_DeviceDescriptor_InfoReport
    Use
    This Management Procedure shall be used to spontaneously send a Device Descriptor value. This
    procedure is typically spontaneously executed by the Manegement Server (device) and not by the
    Management Client!
    On KNX RF, the A_DeviceDescriptor_InfoReport-PDU shall betransmitted in a RF
    AddrExtensionType = 0; the frame shall then contain the KNX Serial Number of the sender.
    Used Application Layer Services for Management
    - A_DeviceDescriptor_InfoReport

    Parameters of the Management Procedure
    DM_DeviceDescriptor_InfoReport (/* [in] */ DM_DDType, /* [in] */ DM_DD)
        DM_DDType    type of the Device Descriptor
        DM_DD        the Device Descriptor of the device
    This Management Procedure shall use the system broadcast communication mode.

    Sequence

    ```mermaid
    sequenceDiagram
        participant S as Management Server
        participant C as Management Client
        Note right of C: Set client in teaching mode.
        S->>C: A_DeviceDescriptor_InfoReport-PDU (descriptor_type = DM_DDType, device_descriptor = DM_DD)
    ```

    Error and exception handling
    Not applicable.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dm_connect(xknx: XKNX) -> None:
    """DM_Connect — see module docstring for the verbatim spec text."""
    raise NotImplementedError("DM_Connect (KNX 03.05.02 §3.2) — implementation pending")
