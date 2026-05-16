"""
NM_IndividualAddress_Check — KNX 03.05.02 §2.19 (PDF p. 33).

Spec text (verbatim from spec):

    NOTE         This procedure has also been named NM_IndividualAddress_Scan.

    Use
    This Network Management Procedure shall be used by a network Management Client to check
    whether a given Individual Address is occupied on the network or not.
    Used Application Layer Services for Management
          • A_Connect
          • A_DeviceDescriptor_Read
          • A_Disconnect

    Parameters of the Management Procedure
    NM_IndividualAddress_Check(/* [in] */ IA_test, /* [out] */ result, /* [out] */ DDType,
    /* [out] */ DDx)
         IA_test:      Individual Address of which the occupation on the network has to be tested.
         result:       Result back to the user of the Management Procedure to indicate whether the IA_test is
                       occupied on the network or not.
         DDType: The Device Descriptor Type as reported by the device
         DDx:          The Device Descriptor value according the format DDType as reported by the device.

    Sequence
    Management                                                                     Network /                   remark
    Client                                                                         Management
                                                                                   Server
                                      A_Connect-PDU
                               (destination_address = IA_test)

    if negative A_Connect.Lcon ⇒ IA_test occupied; end procedure.
    else (this is, a positive A_Connect.Lcon is received)
                                                                                          If the device that occupies the IA_test
                                                                                  does not support Transport Layer connections,
                                                                                              it shall send a T_Disconnect-PDU.
                                      A_Disconnect-PDU
                                             ()

    if A_Disconnect-PDU is received then IA_test shall be regarded as occupied; end procedure.
    else (no A_Disconnect-PDU is received)
                                                                If a device that occupies IA_test is present on the network,
                                                                             and does support Transport Layer connections,
                                                                                   it shall have no other reaction on the bus
                                                   than the Layer-2 acknowledge that initiates the above A_Connect.Lcon
        The A_DeviceDescriptor_Read-PDU shall use DD0.
                              A_DeviceDescriptor_Read-PDU
                              (destination_address = IA_test,
                                 descriptor_type = 0000h)

                            A_DeviceDescriptor_Response-PDU
                            (descriptor_type, device_descriptor)
    1), 2)
    If the Management Client receives an A_DeviceDescriptor_Response-PDU it shall conclude that the Individual Address IA_test is
    occupied.
    if no A_DeviceDescriptor_Response-PDU is received after time-out ⇒ IA_test is not occupied
    endif
    3)                          A_Disconnect-PDU
                          (destination_address = IA_test)

    Possible reactions
    1)   If the Network Management Server reacts on the connection oriented
         A_DeviceDescriptor_Read-PDU then the Management Client shall assume that the IA IA_test is
         occupied on the network and that the device that occupies this IA_test supports the
         connection-oriented Transport Layer.

    2)     The descriptor_type and the device_descriptor in the response by the device shall be reported
           back via DDType respectively DDx. The Device Descriptor Type may differ from 0 and the
           format of the Device Descriptor may be encoded accordingly as well.
    3)     If the Network Management Client receives an A_Disconnect-PDU and no A_Device-
           Descriptor_Response-PDU, then the Management Client shall assume that the IA_test is occupied
           on the network and that the device that occupies this IA_test does not support the
           connection-oriented Transport Layer.

    2.20 Procedures with A_SystemNetworkParameter_Read
    2.20.1.1 Introduction (informative)
    This procedure shall be the alternative to the procedure NM_NetworkParameter_Read_R on system
    broadcast communication mode.

    2.20.1.2 General Procedure
    Precondition
    This procedure shall be executed on system broadcast communication mode. This service is designed
    for the management (discovery, setting and diagnostics) of KNX open medium specific parameters.
    This is typically done at the beginning of the Configuration, when the Individual Addresses of the
    devices in the communication path between MaC and MaS have not yet been established. It is thus not
    possible to execute the procedure “Discovery of maximal Frame length” as specified in [06]. If using
    this procedure, the MaC shall thus make sure that the size request – and response-PDUs remains
    limited to an APDU of 14 octets at maximum.
    Use
    The MaC shall use this Management Procedure to find if a system- or device parameter of a given type
    and value is used in the network or not, using system broadcast communication mode on KNX open
    media.
    Used Application Layer Services for Management
          •      A_SystemNetworkParameter_Read

    The ASDU of the A_SystemNetworkParameter_Read-PDU shall contain the following fields.
    -     object_type:                  Value that shall be used by the MaC for the subfield object_type of the
                                        field parameter_type of the A_SystemNetworkParameter_Read-PDU.
    -     PID:                          Value that shall be used by the MaC for the subfield PID of the field
                                        parameter_type of the A_SystemNetworkParameter_Read-PDU.
    -     test_info:                    Value that shall be used by the MaC for the field test_info of the
                                        A_SystemNetworkParameter_Read-PDU.

           octet 6            octet 7           octet 8             octet 9           octet 10  octet 11 ... n
                            APCI                                     parameter_type                     test_info
                                                object_type                   PID           reserved           operand
    7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0
                     APCI
                     APCI
                     APCI
                     APCI
                     APCI
                     APCI
                     APCI
                     APCI
                     APCI
                     APCI

                     0 1 1 1 0 0 1 0 0 0                                                              0 0 0 0

                           Figure 5 - A_SystemNetworkParameter_Read-PDU (example)

    The conditions for the MaS to respond to this service depend on the specific use and are given in the
    detailed procedures below.

    •       If the MaS receives an A_SystemNetworkParameter_Read PDU of which it does not support any
            of the service parameters (object_type, PID or further) or the reaction for these service parameters
            is not specified, then it shall not react.
    •       If the MaS finds the conditions for replying are not fulfilled, this is if the check of its investigated
            parameters against the test information is negative, then it shall ignore the service.
    •       If the MaS does accept the service, it shall respond with an A_SystemNetworkParameter_Read.res
            primitive after a random wait time. This random wait time is specified either per parameter_type
            in the detailed procedures below; additionally or alternatively, it is possible that the random wait
            time is communication by the MaC as part of the test_info. The data in the response shall depend
            on the network parameter type being read. The TSDU shall be an
            A_SystemNetworkParameter_Response-PDU as shown in Figure 6.
    •       The MaC shall not call this service with any service parameters (parameter_type, test_info) that
            are not specified in this paper.
                  octet 6            octet 7           octet 8           octet 9           octet 10
                                                                                                  octet 11
                                   APCI                                   parameter_type                test_info
                                                         object_type                   PID              reserved
             7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0
                            APCI
                            APCI
                            APCI
                            APCI
                            APCI
                            APCI
                            APCI
                            APCI
                            APCI
                            APCI

                            0 1 1 1 0 0 1 0 0 1

                                                     octet 12 ... n octet n + 1 ... m
                                                       test_info
                                                                      test_result
                                                       operand
                                                  7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0

                            Figure 6 - A_SystemNetworkParameter_Response-PDU (example)

    2.20.1.3 Overview of the accepted usage (informative)
    All values are decimal, unless indicated otherwise. Indexes denote the bit length.
        •    NM_Read_SerialNumber_By_ProgrammingMode
             To read the KNX Serial Numbers of all devices in which Programming Mode is active.
             object_type:       Device Object
             PID:               11 (PID_SERIAL_NUMBER)
             test_info:         operand:             01h
                                                     The MaS shall respond only if its Programming Mode
                                                     is active.
             test_result:       KNX Serial Number of responder
             random wait time: constant: 0 s to 1 s

      •     NM_Read_SerialNumber_By_ExFactoryState
          To discover the devices in the network that have the factory default Domain Address and the
          factory default Individual Address.
          object_type:           Device Object
          PID:                   11 (PID_SERIAL_NUMBER)
          test_info:             operand:          02h
                                                   The MaS shall respond only if its Domain Address and
                                                   its Individual address both have their factory default
                                                   value.
                                 wait_time:        1 octet: random wait time expressed in seconds (0 s
                                                   to 255 s).
                                                   Pending responses can be cancelled. Please check
                                                   the specification of NM_Read_SerialNumber_By_-
                                                   ExFactoryState.
          test_result:           KNX Serial Number of responder
          random wait time: variable: contained in test_info
      •   NM_Read_SerialNumber_By_PowerReset
          To discover the devices in the network of that have just been powered off and on again.
          object_type:         Device Object
          PID:                 11 (PID_SERIAL_NUMBER)
          test_info:           operand:             03h
                                                    The MaS shall respond only if it has just been
                                                    powered on.
                               wait_time:           1 octet: random wait time expressed in seconds (0 s
                                                    to 255 s).
                                                    Pending responses can be cancelled. Please check
                                                    the specification of NM_Read_SerialNumber_By_-
                                                    PowerReset.
          test_result:         KNX Serial Number of responder
          random wait time: variable: contained in test_info
      •   Manufacturer specific use of A_SystemNetworkParameter_Read
          To perform manufacturer specific operations on system broadcast communication mode.
          object_type:       any Interface Object Type: manufacturer and use specific
          PID:               any Property Identifier: manufacturer and use specific
          test_info:         operand:              FEh
                                                   The use and response conditions are implementation
                                                   specific.
                             manufacturer_id: Manufacturer Code of the MaS that may react to the
                                                   service.
                             The test_info may contain additional implementation specific fields.
          test_result:       manufacturer and use specific
          random wait time: manufacturer and use specific
                             The cancellation of pending responses is optionally possible; the methods
                             are implementation specific without further requirements.
    Other tests will be added in the future when needed.

    2.20.1.4 Detailed procedure 1 – NM_Read_SerialNumber_By_ProgrammingMode
    Use
    This Network Management Procedure shall be used to read the KNX Serial Number of devices in
    which Programming Mode is active.
    This procedure shall use system broadcast communication mode and is by that independent of the
    configuration of the Domain Addresses and the Individual Addresses of the devices and the (Media)
    Couplers.

    If the expected device is an IP device supporting IP System Broadcast, then, if there is a KNXnet/IP
    Router between the MaC and the MaS, the MaC sets the IP System Broadcast Routing Mode of the
    router to “Enable” by sending an A_FunctionPropertyCommand(…) or
    A_FunctionPropertyExtCommand(…). The Management Procedure shall then continue as below. In
    situations where it is not known beforehand if the device(s) in which Programming Mode is “enabled”
    support IP system broadcasts, or if also non-IP devices need to be found, the procedure shall be
    executed once with - and once without step 1.
    The test_info shall consist of a single octet operand 01h.
          octet 6                octet 7            octet 8                   octet 9    octet 11    octet 10
                                APCI                                           parameter_type  test_info
                                                object_type                   PID              reserved
    7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0
                     APCI
                     APCI
                                                              Device Object                        PID_SERIAL_NUMBER
                     APCI
                     APCI
                     APCI
                     APCI
                     APCI
                     APCI
                     APCI
                     APCI

                      0 1 1 1 0 0 1 0 0 0                                                                                   0 0 0 0

                                                                       octet 12
                                                                       test_info
                                                                       operand
                                                                  7 6 5 4 3 2 1 0

                                                                            01h

                                    Figure 7 - A_SystemNetworkParameter_Read-PDU
                                   with NM_Read_SerialNumber_By_ProgrammingMode

                    octet 6            octet 7                octet 8                   octet 9  octet 11   octet 10
                                      APCI                                               parameter_typetest_info
                                                        object_type                   PID              reserved
            7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0
                              APCI
                              APCI
                                                                        Device Object                     PID_SERIAL_NUMBER
                              APCI
                              APCI
                              APCI
                              APCI
                              APCI
                              APCI
                              APCI
                              APCI

                              0 1 1 1 0 0 1 0 0 1                                                                                 0 0 0 0

                                       octet 12        octet 13                            octet 18
                                       test_info                      test_result
                                       operand
                                  7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6             1 0 7 6 5 4 3 2 1 0

                                           01h                                  KNX Serial Number

                                   Figure 8 - A_SystemNetworkParameter_Response-PDU
                                   with NM_Read_SerialNumber_By_ProgrammingMode

    Used Application Layer Services for Management
        •      A_SystemNetworkParameter_Read

    Requirements to the MaS (device)
    The MaS shall only reply to the A_SystemNetworkParameter_Read in this service, if its Programming
    Mode is active.
    The random wait time for responding in this procedure shall be between 0 s and 1 s.

    Parameters of the Management Procedure
    NM_Read_SerialNumber_By_ProgrammingMode(/* [out] */ mpp_KNX_Serial_Number[])
        mpp_KNX_Serial_Number[]      This shall be the list of KNX Serial Numbers of devices that respond
                                     to this procedure, that is, in which Programming Mode is active.
    This Management Procedure does not have input parameters.
    The A_SystemNetworkParameter_Read-PDU shall be transmitted with priority System.

    Management                                                                    Management
    Client                                                                        Server (device)

                         A_SystemNetworkParameter_Read-PDU
                             (object_type = Device Object,
                            PID = PID_SERIAL_NUMBER,
                                test_info = operand 01h)

                 If Programming Mode is active in the MaS, then the MaS shall respond with the KNX Serial Number of the MaS
                                                                         in the response, else, the MaS shall ignore the service.
                      A_SystemNetworkParameter_Response-PDU
                            (object_type = Device Object,
                           PID = PID_SERIAL_NUMBER,
                               test_info = operand 01h,
                          test_result = KNX Serial Number)

    NOTE 3    The value 01h of test_info identifies this specific use of A_SystemNetworkParameter_Read with the PID_SERIAL_-
    NUMBER. It shall not be mistaken for a comparison between the state of the Programming Mode (‘1’ = ‘active’) and the value
    01h.

    2.20.1.5 Detailed procedure 2 – NM_Read_SerialNumber_By_ExFactoryState
    Use
    This Network Management Procedure shall be used to scan for devices in the network of which both
    the Domain Address (if available) and the Individual Address have their factory default value.
          The factory default values are specified here:
                • for the DoA Realisation Type 1 (2 octets):                    in [18] clause 2.4.4.3.2.1.4 “Default
                                                                                value and Master Reset” in the
                                                                                specification of PID_PL110_DOA
                 •   for the DoA Realisation Type 2 (6 octets):                 in [05] clause 3.2.4
                 •   for the Individual Address:                                in [05] clause 3.3
    This procedure shall use system broadcast communication        mode and is by that independent of
    the configuration of the Domain Addresses and the Individual Addresses of the devices and the
    (Media) Couplers.
    Used Application Layer Services for Management
          •   A_SystemNetworkParameter_Read

    Requirements to the MaS (device)
    The MaS shall only reply to the A_SystemNetworkParameter_Read-PDU in this service, if both its
    Domain Address (if available) and its Individual Address have the factory default value.

    The random wait time for responding in this procedure shall be variable and shall be contained in the
    field wait_time in the A_SystemNetworkParameter_Read-PDU as specified in Figure 9.
    If the MaS concludes on responding to this service request, then it shall delay its response until a
    random time in the period from 0 s to the number of seconds as indicated in the wait_time in the
    request.
    •   If during this delay the MaS receives a next A_SystemNetworkParameter_Read-PDU with the
        same parameters (object_type, PID and operand), but with the random wait time equal to 255
        (FFh), then it shall cancel its response and not send an A_SystemNetworkParameter_Response
        PDU.
    •   If however the delay has already elapsed and the MaS has already requested the transmission of its
        request, then there are no further requirements.
          octet 6                octet 7            octet 8                    octet 9   octet 11     octet 10
                                APCI                                            parameter_type test_info
                                                object_type                   PID              reserved
    7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0
                     APCI
                     APCI
                                                              Device Object                         PID_SERIAL_NUMBER
                     APCI
                     APCI
                     APCI
                     APCI
                     APCI
                     APCI
                     APCI
                     APCI

                      0 1 1 1 0 0 1 0 0 0                                                                                    0 0 0 0

                                                              octet 12       octet 13
                                                                 test_info
                                                         operand         random wait time
                                                    7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0

                                                                02h

                                         Figure 9 - A_SystemNetworkParameter_Read-PDU
                                         with NM_Read_SerialNumber_By_ExFactoryState

                    octet 6               octet 7             octet 8                    octet 9
                                                                                               octet 11      octet 10
                                         APCI                                             parameter_type
                                                                                                     test_info
                                                      object_type                   PID              reserved
          7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0
                              APCI
                              APCI
                                                                         Device Object                     PID_SERIAL_NUMBER
                              APCI
                              APCI
                              APCI
                              APCI
                              APCI
                              APCI
                              APCI
                              APCI

                              0 1 1 1 0 0 1 0 0 1                                                                                  0 0 0 0

                              octet 12           octet 13     octet 14                           octet 19
                                     test_info                              test_result
                             operand         random wait time
                        7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6             1 0 7 6 5 4 3 2 1 0

                                02h                                                          KNX Serial Number

                                  Figure 10 - A_SystemNetworkParameter_Response-PDU
                                     with NM_Read_SerialNumber_By_ExFactoryState

    NM_Read_SerialNumber_By_ExFactoryState(/* [out] */ mpp_KNX_Serial_Number[])
        mpp_KNX_Serial_Number[]      This shall be the list of KNX Serial Numbers of devices that
                                     respond to this procedure, that is, which have the factory default
                                     DoA and IA.
    This Management Procedure does not have input parameters.

    The A_SystemNetworkParameter_Read-PDU shall be transmitted with priority System.
    Management                                                                  Management
    Client                                                                      Server (device)
                      A_SystemNetworkParameter_Read-PDU
                           (object_type = Device Object,
                 PID = PID_SERIAL_NUMBER, test_info = operand
                             02h + random_wait_time)

                                                 If MaS has the factory default DoA (if available) and the factory default IA,
                                                  then the MaS shall respond with the KNX Serial Number of the MaS in the
                                               response, else the MaS shall ignore the service. The response shall be sent at a
                                                                                  random time in between 0 s and wait_time.
                                                                                                 start random wait
                      A_SystemNetworkParameter_Read-PDU
                           (object_type = Device Object,
                 PID = PID_SERIAL_NUMBER, test_info = operand
                          02h + random_wait_time = 255)

                                               If during the random wait period an identical request is received with the field
                                                                   random_wait_time = 255, then the MaS shall not respond.

                                                                                               end random wait
                                                             If the random wait time elapses with a 2nd identical request with
                                                         random_wait_time = 255 is received, then the MaS shall request the
                                                                                                transmission of its response.
                       A_SystemNetworkParameter_Read-PDU
                     (operand = 02h, object_type = Device Object,
                            PID = PID_SERIAL_NUMBER,
                     test_info =operand 02h + random_wait_time,
                           test_result = KNX Serial Number)

    Risks
    •     As this procedure uses system broadcast communication mode, if there are devices in ex-factory
          state outside the managed network, in neighbouring networks, these will respond as well.

    2.20.1.6 Detailed procedure 3 – NM_Read_SerialNumber_By_PowerReset
    Use
    This Network Management Procedure shall be used to scan for devices in the network of which have
    just been powered on.
    This procedure shall help identifying and addressing “inaccessible devices”.
    Opposite to the procedure NM_Read_SerialNumber_By_ExFactoryState, this procedure requires a
    human activity on the device and therefore has a better probability of excluding devices in neighbour-
    ing installations.
    This procedure shall use system broadcast communication mode and is by that independent of the
    configuration of the Domain Addresses and the Individual Addresses of the devices and the (Media)
    Couplers.
    Used Application Layer Services for Management
          •   A_DomainAddressSelective_Read

    Requirements to the MaS (device)
    The MaS shall only reply to the A_SystemNetworkParameter_Read-PDU in this service, if it has been
    powered on since less than 4 minutes. After 4 minutes, the device shall no longer react to this service
    with this operand. To these 4 minutes, there may be a tolerance of 30 seconds.
    Additionally, the MaS shall not react if it has already replied to a preceding request since it has last
    powered on. This requires that the MaS keeps track of this.
    If the MaS concludes on responding to this service request, then it shall delay its response until a
    random time in the period from 0 s to the number of seconds as indicated in the wait_time in the
    request.
    •   If during this delay the MaS receives a next A_SystemNetworkParameter_Read-PDU with the
        same parameters (object_type, PID and operand), but with the random wait time equal to 255
        (FFh), then it shall cancel its response and not send an A_SystemNetworkParameter_Response
        PDU.
    •   If however the delay has already elapsed and the MaS has already requested the transmission of its
        request, then there are no further requirements.
          octet 6                octet 7            octet 8                    octet 9   octet 11     octet 10
                                APCI                                            parameter_type test_info
                                                object_type                   PID              reserved
    7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0
                     APCI
                     APCI
                                                              Device Object                         PID_SERIAL_NUMBER
                     APCI
                     APCI
                     APCI
                     APCI
                     APCI
                     APCI
                     APCI
                     APCI

                      0 1 1 1 0 0 1 0 0 0                                                                                    0 0 0 0

                                                              octet 12       octet 13
                                                                 test_info
                                                         operand         random wait time
                                                    7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0

                                                                03h

                              Figure 11 - A_SystemNetworkParameter_Read-PDU
                     (Domain Parameter Read) with NM_Read_SerialNumber_By_PowerReset

                    octet 6               octet 7             octet 8                    octet 9
                                                                                               octet 11      octet 10
                                         APCI                                             parameter_type
                                                                                                     test_info
                                                      object_type                   PID              reserved
          7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0
                              APCI
                              APCI
                                                                         Device Object                     PID_SERIAL_NUMBER
                              APCI
                              APCI
                              APCI
                              APCI
                              APCI
                              APCI
                              APCI
                              APCI

                              0 1 1 1 0 0 1 0 0 1                                                                                  0 0 0 0

                              octet 12           octet 13     octet 14                           octet 19
                                     test_info                              test_result
                             operand         random wait time
                        7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6             1 0 7 6 5 4 3 2 1 0

                                03h                                                          KNX Serial Number

                                  Figure 12 - A_SystemNetworkParameter_Response-PDU
                                      with NM_Read_SerialNumber_By_PowerReset

    Requirements to the MaC
    The MaC shall send the A_SystemNetworkParameter_Read-PDU in this procedure
    NM_Read_SerialNumber_By_PowerReset and repeat every 30 s during 4 minutes. It shall collect all
    the answers that arrive.
              EXAMPLE 3       It is possible that the installer resets the MaS firstly and that the MaS completes its power up
                              procedure before the installer triggers the procedure on the MaC (ETS). In this case, the MaS
                              (device) will react immediately.

                                           A_SystemNetworkParameter_Read-PDU

                              MaC
                                                                                                   t
                                            A_SystemNetworkParameter_Response-PDU

                              MaS
                                                                                                   t

                                                  Figure 13 – The MaC triggers the procedure
                                                   well after the MaS completes its power up
              EXAMPLE 4       If the installer firstly triggers the procedure on the MaC (ETS) and then only resets the power of
                              the MaS, then the MaS will not react.

                                           A_SystemNetworkParameter_Read-PDU

                                           MaC
                                                                                                                 t
                                           The MaS has not       The MaS is restar-
                                           just powered and      ting and does not
                                           does not respond.     receive the request.
                                           MaS
                                                                                                                 t

                                                  Figure 14 – The MaC triggers the procedure
                                                     before the MaS completes its power up
                              Therefore, the MaC shall repeat the A_ SystemNetworkParameter_Read-PDU with a period of
                              30 s.

                                                 A_SystemNetworkParameter_Read-PDU

                                     MaC
                                                                                                           t
                                                                          A_SystemNetworkParameter_Response-PDU

                                     MaS
                                                                                                           t

                              Figure 15 – The MaC repeats the request periodically. The MaS responds
                                          on the first request that it receives after power up.

    To make sure that the MaS reacts, the MaC repetition period shall be sufficiently smaller (30 s) than
    the after powering up during which the MaS reacts to the request.

    NM_Read_SerialNumber_By_PowerReset(/* [out] */ mpp_KNX_Serial_Number[])
        mpp_KNX_Serial_Number[]      This shall be the list of KNX Serial Numbers of devices that
                                     respond to this procedure, that is, which are powered up in the
                                     preceding 4 minutes.
    This Management Procedure does not have input parameters.
    The A_SystemNetworkParameter_Read-PDU shall be transmitted with priority System.

    Management                                                                  Management
    Client                                                                      Server (device)

                        A_SystemNetworkParameter_Read-PDU
                             (object_type = Device Object,
                            PID = PID_SERIAL_NUMBER,
                     test_info = operand 03h + random_wait_time)

                                                  If MaS is powered up in the last 4 minutes, then the MaS shall respond with
                                                      the KNX Serial Number of the MaS in the response, else, the MaS shall
                                                ignore the service. The response shall be sent at a random time in between 0 s
                                                                                                                and wait_time.
                                                                                                  start random wait
                       A_SystemNetworkParameter_Read-PDU
                             (object_type = Device Object,
                           PID = PID_SERIAL_NUMBER,
                 test_info = operand 03h + random_wait_time = FFh)

                                               If during the random wait period an identical request is received with the field
                                                                   random_wait_time = 255, then the MaS shall not respond.

                                                                                               end random wait
                                                             If the random wait time elapses with a 2nd identical request with
                                                         random_wait_time = 255 is received, then the MaS shall request the
                                                                                                transmission of its response.
                       A_SystemNetworkParameter_Read-PDU
                               (test_info = operand = 02h,
                              object_type = Device Object,
                            PID = PID_SERIAL_NUMBER,
                     test_info = operand 03h + random_wait_time,
                           test_result = KNX Serial Number)

    Risks
    •   As this procedure uses system broadcast communication mode, in the unlikely case that also
        devices outside the managed network, in neighbouring networks have just been powered on, these
        will respond as well.

    2.20.1.7 Operand FEh – Manufacturer specific use of
             A_SystemNetworkParameter_Read
    This procedure shall be used for manufacturer specific Network Configuration Procedures.
    This allows for the manufacturer specific support of A_SystemNetworkParameter_Read
         -   for standard Properties for which no standard use of A_SystemNetworkParameter_Read is
             specified, and
         -   for non-standard Interface Objects and - Properties.
    In the A_SystemNetworkParameter_Read-PDU, the ASDU shall be composed of the Interface Object
    Type, the PID, the operand FEh and the 2 octet manufacturer code; further manufacturer specific
    service parameters may follow.
    The A_SystemNetworkParameter_Read-PDU for manufacturer specific use shall thus be formatted as
    specified in Figure 16.
          octet 6           octet 7              octet 8                   octet 9           octet 10
                                                                                         octet 11
                           APCI                                             parameter_type     test_info
                                                object_type                   PID              reserved
    7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0
                    APCI
                    APCI
                                                           Device Object
                    APCI
                    APCI
                    APCI
                    APCI
                    APCI
                    APCI
                    APCI
                    APCI

                    0 1 1 1 0 0 1 0 0 0                                                                      0 0 0 0

                                      octet 12             octet 13   octet 14  (octet 15 to n)
                                                          test_info
                                  operand             manufacturer code               …
                             7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0

                                       FEh

                    Figure 16 - A_SystemNetworkParameter_Read-PDU – Type FEh (example)

    The A_SystemNetworkParameter_Response-PDU for this operand FEh shall repeat all the fields of
    the A_SystemNetworkParameter_Read-PDU which may be followed by further manufacturer specific
    response fields.
    There are no further requirements concerning fields, use or timing for this manufacturer specific use. It
    is allowed to foresee the cancellation of pending responses by implementation specific means.

    2.21 Procedures with A_SystemNetworkParameter_Write
    2.21.1.1 General Procedure
    Precondition
    This procedure shall be executed on system broadcast communication mode. This service is mainly
    designed for the management (discovery, setting and diagnostics) of KNX open medium specific
    parameters. This is typically done at the beginning of the Configuration, when the Individual
    Addresses of the devices in the communication path between MaC and MaS have not yet been
    established. It is thus not possible to execute the procedure “Discovery of maximal Frame length” as
    specified in [06]. If using this procedure, the MaC shall thus make sure that the size request – and
    response-PDUs remains limited to an APDU of 14 octets at maximum.
    Use
    The MaC shall use this Management Procedure to set a system – or device parameter of a given type
    to a given value, using system broadcast communication model on KNX open media.

    Used Application Layer Services for Management
            •      A_SystemNetworkParameter_Write

    The ASDU of the A_SystemNetworkParameter_Write-PDU shall contain the following fields.
    -       object_type:             Value that shall be used by the MaC for the subfield object_type of the
                                     field parameter_type of the A_SystemNetworkParameter_Write-PDU.
    -       PID:                     Value that shall be used by the MaC for the subfield PID of the field
                                     parameter_type of the A_SystemNetworkParameter_Write-PDU.
    -       value:                   Value that shall be used by the MaC and that shall be interpreted by the
                                     MaS when accessing the Property indicated in the object_type and PID.

    2.21.1.2 Overview of the accepted usage (informative)
    All values are decimal, unless indicated otherwise. Indexes denote the bit length.
        •       Keep the bidrectional mode actwive in more than one KNX RF S-Mode device
                To keep the bidirectional model enabled in KNX RF S-Mode semi-directional devices
                object_type:         RF Medium Object
                PID:                 60 (PID_RF_BIDIR_TIMEOUT)
                value:               New value for the bidirectional mode time-out timer.

    Please refer to the specification of PID_RF_BIDIR_TIMEOUT in [17]In case the MaC is requested to
    perform the Network – and Device Configuration Procedures of multiple KNX RF S-Mode devices
    together, then it may happen that, while the MaC is handling one device, the bidirectional mode time
    out in one or more other devices. To prevent from this, the MaC may keep the bidirectional mode
    enabled by accessing PID_RF_BIDIR_TIMEOUT over system broadcast communication.

          /* Set the Bidirectional Mode Time-out in all semi-directional devices */
          /* in which bidirectional mode is currently enabled. */
    A_SystemNetworkParameter_Write(object_type = “RF Medium Object”, PID = PID_RF_BIDIR_TIMEOUT,
          value = “new bidirectional mode time-out”)

    The MaC shall set the value of the new bidirectional mode time-out to a value that it estimates to need
    before it can handle the first next device (in point-to-point communication). This action may be
    repeated as long as necessary to keep the bidirectional mode enabled in further devices.

    2.22 Procedures with A_NetworkParameter_Write

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from xknx.exceptions import ManagementConnectionRefused, ManagementConnectionTimeout
from xknx.telegram import apci
from xknx.telegram.address import IndividualAddress, IndividualAddressableType

if TYPE_CHECKING:
    from xknx import XKNX

logger = logging.getLogger("xknx.management.procedures")


async def nm_individual_address_check(
    xknx: XKNX, individual_address: IndividualAddressableType
) -> bool:
    """
    Check if the individual address is occupied on the network.

    :param xknx: XKNX object
    :param individual_address: address to check
    """
    try:
        async with xknx.management.connection(
            address=IndividualAddress(individual_address)
        ) as connection:
            try:
                response = await connection.request(
                    payload=apci.DeviceDescriptorRead(descriptor=0),
                    expected=apci.DeviceDescriptorResponse,
                )

            except ManagementConnectionTimeout as ex:
                # if nothing is received (-> timeout) IA is free
                logger.debug("No device answered to connection attempt. %s", ex)
                return False
            if isinstance(response.payload, apci.DeviceDescriptorResponse):
                # if response is received IA is occupied
                logger.debug("Device found at %s", individual_address)
                return True
            return False
    except ManagementConnectionRefused as ex:
        # if Disconnect is received immediately, IA is occupied
        logger.debug("Device does not support transport layer connections. %s", ex)
        return True
