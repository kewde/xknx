"""
DM_Restart — KNX 03.05.02 §3.7 (PDF p. 76).

Spec text (verbatim from spec):

    3.7.1 Definition
    This Management Procedure can be used in a point-to-point connectionless communication mode
    (DM_Restart_RCl) or point-to-point connection-oriented communication mode (DM_Restart_RCo).

    DM_Restart (flags)
        flags  All bits are reserved. These shall be set to 0. This shall be tested
               by the Management Client.

    This Management Procedure shall be used to execute in the Management Server a Basic Restart or a
    Master Reset.

    3.7.1.1 Basic Restart

    3.7.1.1.1 Definition
    To perform a Basic Restart the Management Server shall
    - switch off Programming Mode
    - clear runtime errors
    - reset all access levels
      This is, the access levels possibly granted to the Management Client shall be set to the
      highest access level set with FFFFFFFFh.
    - switch off safe state
    - send an appropriate LM_Reset.ind message through the EMI interface
    - reset its KNX communication system
    - close all KNX Transport Layer connections
    - close all KNXnet/IP connections (Device Management, Tunnelling or other)
    - close all KNX Secure Sessions
    - close all KNX TCP connections
    - apply changed configuration Parameters at the latest 30 s after completing the restart
      (see [11] clause 2.5.1 - "Coming into effect of changed KNXnet/IP Parameters – general
      rule").
    Please refer to the respective protocol specifications for the requirements. The above list is mandatory
    but may not be complete.

    It is recommended to
    - break down any Transport Layer connection 8)
      The Management Server should send a T_Disconnect-PDU to the Management Client.

    3.7.1.1.2 Timing (Management Client and Management Server)

                    t0            t1                                           t2

                                       Figure 19 – Timing of the restart

    Time                        MaC                                                 MaS
    t0     =0s
           The MaC sends out the A_Restart-PDU       The MaS shall start the actions included
           (unconfirmed) or receives the             in the Basic Restart.
           A_Restart_Response-PDU.
    t1–t0  The MaC shall not make any assumptions   The MaS may react under the pre-reset
           on the MaS.                               conditions, may not react at all, or may
                                                     already react according the post-reset
                                                     conditions.

    8) Due to the required restart of the communication system, a possible Transport Layer connection will break. It
       is however recommended that a T_Disconnect-PDU is sent to any communication partner to whom a
       TL-connection may be established at that time.
       Devices have been reported that hold the Transport Layer connection throughout a restart and send a
       T_Disconnect-PDU when they experience the normal Transport Layer timeout after restart.

    Time                        MaC                                                  MaS
           NOTE 8 With "pre-reset conditions" are meant all access and Permissions, all Session keys,
           authorisations, access levels and parameter values as active before the reset.

    t1     = 1 s, unless specified differently for any service or Resource.
           This is the earliest point at which the MaC The MaS shall not react anymore
           may expect the MaS to successfully have     according the pre-reset conditions.
           executed a Basic Restart.
           The MaC may start connecting to the
           MaS again (TCP connections, KNX IP
           Sessions, KNXnet/IP connections, TL
           connections).
    t2–t1  The MaC may try to connect to the MaS      The MaS may be unresponsive or it
           again.                                      may already react with the post-reset
                                                       conditions.
           NOTE 9 With "post-reset" conditions are meant all access and Permissions, all Session keys,
           authorisations, access levels and parameter values as active after the reset. These are typically
           cleared or have default values; configuration Parameters shall assume the values as possibly set
           before the reset.
           EXAMPLE 5 If the MaC changes the IP multicast address then it shall at the latest become active
           after the reset.

    t2     = 5 s, unless specified differently for any service or Resource, or unless responded
           differently by the MaS in the A_Restart_Response-PDU if it is larger than 5 s:
           see 3.7.1.2.2
                                                       The MaS shall be responsive again with
                                                       the post restart conditions.
    > t2   If there is further communication between
           the MaC and the restarted MaS, the
           reaction failure of successive communi-
           cation due to longer MaS restart timing
           depends on the error handling of the
           Configuration Procedure in which this
           DM_Restart is used.

    3.7.1.1.3 Calling a Basic Restart through A_Restart (Management Client and Management Server)
    The Basic Restart shall be identified by an A_Restart-PDU
    - with the field Response cleared, and
    - with all bits 4 to 1 of the APCI/ASDU cleared, and
    - with the field restart_type cleared, and
    - without the field erase_code, and
    - without the field channel_number.

                                    Octet 6            Octet 7

                              7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0
                                                 APCI
                                                 APCI
                                                 APCI
                                                 APCI
                                               Response
                                               reserved
                                               reserved
                                               reserved
                                               reserved
                                              Restart Type
                              1 1 1 0 0 0 0 0 0 0

                     Figure 20 - A_Restart-PDU (example with restart_type = 0)

    The Application Layer of the Management Server shall not confirm the A_Restart-service if a Basic
    Restart is called; to obtain the same result with an AL-confirmation, the Management Client should
    instead call a Master Reset with Erase Code 00h.

    3.7.1.2 Master Reset

    3.7.1.2.1 Definition
    To perform a Master Reset, the Management Server shall reset its configuration data according the
    following, if supported and as requested by the Management Client.
    - In the Group Address Table and the Group Object Association Table the following link
      information shall be cleared.
      - If the field Channel Number equals 00h then all link information in these tables shall be
        cleared.
      - If the field Channel Number differs from 00h, then only the link information in these tables
        for the Group Objects of the indicated application Channel Number shall be cleared.
      For the error handling concerning invalid values of the field Channel Number, please refer to the
      specification of the A_Restart-service in [03].
    - The application parameters are set to their default value.
      - If the field Channel Number equals 00h then all parameters shall be reset.
      - If the field Channel Number differs from 00h, then only the parameters of the indicated
        application Channel Number shall be cleared.
      - In case of an E-Mode device with one or more Adjustable E-Mode Channels, this means that
        the Adjustable Parameter shall for each E-Mode Channel be set back to its default value,
        which shall be 0. Consequently, other E-Mode Channel configuration data (Channel Codes,
        Connection Codes and Connection Flags) shall be reset to their default value as well.
    - The application is reset to the default application.
    - The IA is reset to the devices' medium dependent default IA.
    - A Basic Restart is executed.

    3.7.1.2.2 Timing (Management Client and Management Server)
    To execute the requested Master Reset, the Management Server may need some time, during which it
    may not be accessible to the Management Client. Therefore, the Management Server shall use the
    Process Time to report on the time that it needs in worst case for the execution of the requested Master
    Reset.
    This field shall be encoded as a 2 octet unsigned integer value expressed in seconds. This shall comply
    with the encoding of DPT_TimePeriodSec (DPT_ID = 7.005).

    The Management Server user shall fill in the Process Time if this time exceeds 5 s. If not, this field
    may
    - either be left to its default value 0000h, or
    - be filled with the correct process time. The MaC is however not required to respect this
      received process time if this is shorter than the standard process time for the Management
      Procedure that it is executing. The process time is thus a minimal time for the MaC to wait,
      not a maximal time.
      EXAMPLE 6 If the MaS indicates it can be available after a Confirmed Restart already after 2 s and the MaS
      handles a default waiting time of 3 s, then the MaC may still wait for 3 s.

    If the Management Server confirms the Master Reset negatively (Error Code ≠ 00h), then it shall set
    the Process Time to 0000h in the A_Restart_Response-PDU.
    If this field is different from 0000h, then the Management Client shall consider it in the error handling
    (pauses, retries, attempts to reconnect) of its possible further Application Layer services. If the Process
    Time expires without reaction by the Management Server, then the Management Client shall try to
    call the failed next Application Layer service one last time before it may consider the related
    Configuration Procedure as failed.
    The Management Server shall execute the Master Reset only after the A_Restart_Response-PDU has
    been sent on the bus.
    NOTE 10 This shall guarantee that the Master Reset is in all cases a confirmed service: the A_Restart_Response-PDU shall
    in all cases by sent by the Management Server and received by the Management Client and not go lost due to the possible
    reset of the communication stack of the Management Server.
    NOTE 11 This shall also guarantee that in case the Master Reset changes the Indvidual Address of the Management Server,
    that the A_Restart_Response-PDU is transmitted on the bus with the current IA of the Management Server prior to calling this
    service.

    3.7.1.2.3 Calling a Master Reset through A_Restart (Management Client and Management Server)

    3.7.1.2.3.1 General requirements
    The Master Reset shall be identified by an A_Restart-PDU
    - with the field Response cleared, and
    - with all bits 4 to 1 of the APCI/ASDU cleared, and
    - with the field restart_type set to 1, and
    - with the field erase_code encoded, and
    - with the field Channel Number.

                    Octet 6               Octet 7                    Octet 8     Octet 9
              7 6 5 4 3 2 1 0  7 6 5 4 3 2 1 0  7 6 5 4 3 2 1 0  7 6 5 4 3 2 1 0
                              Response reserved reserved reserved reserved Restart Type
                        APCI APCI APCI APCI                                 Erase Code Channel Number
                         1    1    1    0    0    0    0    0    0    1

                               Figure 21 – A_Restart-PDU (example)

    The Erase Code shall indicate which Resource value shall be reset in the Management Server. The
    Channel Number shall indicate to which application channel the reset applies. These fields shall be
    encoded and used as specified in Table 4.

    Table 4 – Definition of Erase Code and Channel Number

    Erase Code   Description
    01h          Confirmed Restart
                 No Resource value shall be reset.
                 This encoding shall allow using the Master Reset as a confirmed alternative to the
                 unconfirmed Basic Restart.
                 Both Erase Code values shall have the same effect.
                 NOTE 12 This encoding uses the same values for the Erase Code as for the Reset Command in [09].
                 Channel Number: Fixed: 00h
    02h          Factory Reset
                 This shall reset the device to its ex-factory state.
                 Which Resources are reset and their value after reset are implementation dependent.
                 However, for "Factory Reset" and "Factory Reset without IA" there are requirements
                 concerning the effect on system network Resources. See 3.7.1.2.3.2.
                 Channel Number:
                    = 00h: The Resources of all Channels shall be reset.
                    ≠ 00h: Only the Resources of the Channel with this given Channel Number shall be reset.
    03h          ResetIA
                 The IA shall be reset to the medium specific default IA when this A_Restart is executed.
                 Channel Number: Fixed: 00h
    04h          ResetAP
                 Application Program Memory shall be reset to the default application when an
                 A_Restart-PDU is received.
                 Channel Number: Fixed: 00h
    05h          ResetParam
                 Application Parameter Memory shall be reset to its default value when an
                 A_Restart-PDU is received.
                 Channel Number:
                    = 00h: The application parameters of all Channels shall be reset.
                    ≠ 00h: The application parameters of only this given Channel shall be reset.
    06h          ResetLinks
                 Link information for Group Objects (Group Address Table, Group Object Association
                 Table) shall be reset to default state when an A_Restart-PDU is received.
                 Channel Number:
                    = 00h: The link information of all Channels shall be reset.
                    ≠ 00h: The link information of only this given Channel shall be reset.
    07h          Factory Reset without IA
                 This shall reset the device to its ex-factory state.
                 Which Resources are reset and their value after reset are implementation dependent.
                 Opposite to Erase Code 02h, the Individual Address shall not be reset. Further specific
                 requirements as specified in 3.7.1.2.3.2 shall apply.
                 Channel Number:
                    = 00h: The Resources of all Channels shall be reset.
                    ≠ 00h: Only the Resources of the Channel with this given Channel Number shall be reset.
    08h          Erase persistently stored application data
                 Persistently stored application data (definition in 3.7.1.2.3.2.4) shall become invalid when an
                 A_Restart-PDU is received.
                 Channel Number:
                    = 00h: The persistently stored application data of all channels shall be reset.
                    ≠ 00h: The persistently stored application data of only this given Channel shall be reset.
    00h          These values are reserved.
    09h to FFh   The Management Client shall not use these Erase Codes.
                 The Management Server shall on reception of an A_Restart-PDU with an Erase Code
                 value in this range
                 - neither execute a Basic Restart nor any Master Reset, and
                 - respond with an A_Restart.res with Error Code "Unsupported Erase Code".
                 Channel Number: not defined

    The Management Server shall handle the requested Master Reset as specified above and shall respond
    with an A_Restart_Response-PDU as follows:
    - with the field Response set to 1, and
    - with all bits 4 to 1 of the APCI/ASDU cleared, and
    - with the field restart_type set to 1, and
    - with the field Error Code, and
    - with the field Process Time.

              Octet 6     Octet 7     Octet 8     Octet 9     Octet 10
        7 6 5 4 3 2 1 0  ...
                         APCI
                         APCI
                         APCI
                         APCI
                       Response
                       reserved
                       reserved   Error Code   Process Time
                       reserved
                       reserved
                      Restart Type
        1 1 1 0 1 0 0 0 0 1

                         Figure 22 - A_Restart_Response-PDU (example)

    The Error Code shall indicate to the Management Client the result of the requested A_Restart from the
    Management Server. The field Error Code shall be encoded and sent as specified in Table 5.

    Table 5 – Error Code

    Error Code   Description
    00h          No Error
                 The Management Server has properly received the A_Restart-PDU and will execute it.
    01h          Access denied
                 The Management Server has properly received the A_Restart-PDU.
                 Master Reset functionality is in this Management Server protected by authorization and
                 the requesting Management Client is not properly authorized.
                 It is recommended that this Error Code be responded only if Resources are involved
                 that are protected by an access level of 2 and higher.
    02h          Unsupported Erase Code
                 The Management Server has properly received the A_Restart-PDU; the Management
                 Client may have the required authorization; the requested Erase Code is not supported.
    03h          Invalid Channel Number
                 This Erase Code value shall be responded in the following cases.
                 - The requested Erase Code requires the Channel Number to be 00h but it is not.
                 - A Channel Number different from 00h is requested but the Management Server
                   does not support application channels.
                 - The Channel Number is used for an application channel that is not supported.
    04h to 255h  These values are reserved. The Management Server shall not use any value in this range.

    3.7.1.2.3.2 Specific requirements

    3.7.1.2.3.2.1 Factory Reset and Factory Reset without IA
    Some system network Resources shall or shall not be reset, as specified in Table 6.

    Table 6 – Reset of network Resources in function of the Erase Code
                                                         Erase Code
                                                         Factory Reset  Factory Reset without IA
    Parameter                                            02h            07h
    - IA
    - Domain Address (RF and PL)
    - IP address
    - IP address mask
    - IP multicast address                               shall be reset shall NOT be reset
    - IP address assignment method
    - IP default gateway
    - KNXnet/IP Tunnelling PID_ADDITIONAL_-
      INDIVIDUAL_ADDRESSES

    After a Factory Reset the IP device obviously assumes an IP address that is implementation specific. It
    may be a default fixed IP address, or it may depend on the default assignment method.

    3.7.1.2.3.2.2 "Reset to default" and KNX Security
    In the below, for "Reset to default", this is, Master Reset with the Erase Codes 02h "Reset to default
    state", 07h "Reset to default without IA" and "Local Reset to default state" the requirements shall be
    interpreted as follows.

    Effect              Length shall be set   Still used memory        Unused memory
    cleared             to 0                  does not exist           shall be set to 00h
    reset to default    as appropriate        implementation           shall be set to 00h
    value                                     specific values

    So, not-only the length of the array Property Values may be set back to 0, but also that the unused
    memory shall be set to 00h.

    NOTE 13 Otherwise, if only the length would be set to 0, a malicious Client could after the "Reset to default"
    use the FDSK to set the length back and read any possible remaining data that was not wiped, like Group Keys,
    etc.

    3.7.1.2.3.2.3 "Reset to default" and Authorisation Keys
    NOTE 14 The below concerns the keys used in the services A_Key_Write and A_Authorise and should not
    be confused with the keys specified further in this paper related to KNX Secure.
    If the MaS performs a Master Reset, then the following shall apply.

    Erase Code   Effect on the Authorisation Keys
    01h          Confirmed Restart: not influenced: the Authorisation Keys shall not change.
    02h          Reset to default state: The MaS shall set the Authorisation Keys of the
                 access level to which the requesting MaC is authorised and higher level (higher numerical value)
                 to their default settings.
                 EXAMPLE 7 According [04] 9), the MaC will typically be authorised for the access level 2. If it requests a
                 "Reset to default" or a "Reset to default without IA", then the MaS shall sets all Authorisation Keys of
                 level 2 to level 16 (or maximum supported level) to default values.
                 NOTE 15 The ex-factory value for an Authorisation Key is typically FFFFFFFFh.
    03h          ResetIA: not influenced: the Authorisation Keys shall not change.
    04h          ResetAP: See Erase Code 03h "ResetIA".
    05h          ResetParam: See Erase Code 03h "ResetIA".
    06h          ResetLinks: See Erase Code 03h "ResetIA".
    07h          Reset to default without IA: See Erase Code 02h "Reset to default state".
    n.a.         Local Reset to default state: See Erase Code 02h "Reset to default state".
                 Additionally, the Authorisation Keys for the lower levels (lower numerical value) may either remain
                 unchanged or be reset to their default values; the behaviour is implementation specific.

    3.7.1.2.3.2.4 Persistently stored application data and Erase Code 08h

    9) See [03] Table 1 – "Use of access levels for different purposes and Profiles".

    Definition
    In the context of Erase Code 08h, additionally, the expression "Persistently stored application data" is
    used. Characteristics of these data are the following.
    - They are stored persistently in a device in such a way that they are not erased by interruption
      of mains or bus voltage, or a basic restart.
    - They are application specific; they are not KNX system data (like load states, run states,
      security settings…), they are not standardised.
    - They are no data of the download image from the MaC.
      They can be changed data from the download image of the MaC but after erasing the
      persistently stored data the originally downloaded data from the MaC must be valid again.
    - It is application specific which data will be erased on reception of a Master Reset with the
      Erase Code 08h.
      EXAMPLE 08 Temperature sensor calibration data that took effort to be measured and calculated
      most likely shall not be erased.
      EXAMPLE 09 an adapted set point temperature value
      EXAMPLE 10 a fan speed level of a room temperature controller device
      EXAMPLE 11 an adapted dimmer characteristic in a dimmer
    - Their handling via Master Reset and the Erase Code 08h are recommended to be subject to
      the device documentation. The documentation should list the data that are persistently stored
      and those that are erased on reception of Master Reset with the Erase Code 08h.

    Procedure
    To erase persistently stored application data with the help of the Master Reset the installer operates the
    MaC to issue a Master Reset with type "Erase persistently saved application data".
    The MaC shall issue an A_Restart with restart type = 1 (Master Reset) with Erase Code "Erase
    persistently saved application data". A channel number may be used to define a device channel for the
    erasing action.
    If the device receives the message, it shall execute a Basic Restart. After starting-up the memory
    content of the persistently stored application data is invalid. So, the device application starts working
    without use of the formerly persistently stored application data.
    If a channel number ≠ 00h is set in the A_Restart and the channel number is present in the device, then
    only the persistently stored application data of the referred channel are invalid at start-up.
    The device starts normal working.
    The affected data from this procedure are the persistently stored application data and runtime data that
    are changed by a basic restart.
    The target device shall support channel number 00h for all channels or for general erasing of persistent
    application data. It may support further channel numbers > 00h. If the requested channel number in the
    A_Restart is not supported by the target device, it shall respond with an A_Restart_Response-PDU
    with the Error Code "Invalid Channel Number".

    3.7.2 Procedure: DM_Restart_RCl
    Use
    This method shall use the point-to-point connectionless communication mode.
    The Management Client shall prior to calling this Management Procedure with a Master Reset verify
    that this feature is effectively supported by the Management Server. If not, the procedure shall only be
    called with a Basic Restart 10).

    10) Existing implementations may not check bit 0 of octet 7 and may not react as expected. They may ignore the
       service entirely, only perform a Basic Restart if a Master Reset is called or exhibit another behaviour.

    Used Application Layer services for Management
    - A_Restart

    Parameters of the Management Procedure
    DM_Restart_RCl (/* [in] */ mpp_RestartType, /* [in] */ mpp_EraseCode,
                   /* [in] */ mpp_ChannelNumber, /* [out] */ mpp_ErrorCode,
                   /* [out] */ mpp_ProcessTime)
        mpp_RestartType    This Management Procedure Parameter shall indicate whether a Basic
                           Restart or a Master Reset shall be executed.
        mpp_EraseCode      This Management Procedure Parameter shall indicate which
                           Resource(s) shall be reset to its (their) default value. This is void in case
                           only a Basic Restart is executed.
        mpp_ChannelNumber  The number of the application channel that shall be reset or 00h.
        mpp_ErrorCode      This Management Procedure Parameter shall contain the Error Code
                           returned by the Management Client.
        mpp_ProcessTime    This Management Procedure Parameter shall return to the Management
                           Client the Process Time needed by the Management Server. The
                           Management Client shall consider this mpp_ProcessTime as time-out
                           after which communication attempts following a Master Reset shall be
                           considered without success.

    Variables
    None.

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        Note over C: The Management Client shall send an A_Restart-PDU to the Management Server in point-to-point connectionless communication mode; the fields of the A_Restart-PDU shall be set according the values of the Parameters of this Management Procedure. Reserved and unused fields shall be set to 0.
        C->>S: A_Restart-PDU (restart_type = mpp_RestartType, erase_code = mpp_EraseCode, channel_number = mpp_ChannelNumber)
        Note over S: The Management Server shall confirm with an A_Restart_Response-PDU if a Master Reset is requested. It shall then execute a Basic Restart or Master Reset as requested.
        S->>C: A_Restart_Response-PDU (restart_type = mpp_RestartType, mpp_ErrorCode = error_code, mpp_ProcessTime = process_time)
        Note over S: The Management Server shall reset the Resource(s) as indicated in the A_Restart-PDU. The Management Server shall additionally restart.
        Note over C: The Management Client shall interpret any error. If further Management Procedures follow, the Management Client has to poll the Management Server for at least the period given by the mpp_ProcessTime. If mpp_ProcessTime expires without reaction from the Management Server, then the Management Client shall try the subsequent Management Procedure one last time, before it may conclude that the Management Server does no longer respond.
    ```

    Exception handling
    The general exception handling shall be applicable.
    The following errors and exceptions shall be checked in the below given priority.
    (1) If the Management Server receives an A_Restart-PDU with a reserved field with a value
        different from 0, then this service request shall be ignored.
    (2) If the Management Server receives an A_Restart-PDU but the Management Client does not
        have the required access rights (KNX Authorization) then it shall respond with an
        A_Restart_Response-PDU with Error Code = 01h "Access Denied".
    (3) If the Management Server receives an A_Restart-PDU with an Erase Code that it does not
        support or that is specified as "reserved" then it shall respond with an A_Restart_Response-
        PDU with Error Code = 02h "Unsupported Erase Code".
    (4) The Management Server shall respond with the Error Code 03h = "Invalid Channel Number"
        in any of the following cases.
        - It receives an A_Restart-PDU with a Channel Number that is not 00h with an Erase
          Code for which the Channel Number shall be 00h.
        - It receives an A_Restart-PDU with an Erase Code that allows the Channel Number to be
          different from 00h; the Channel Number is different from 00h but the Management
          Server does not support application channels.
        - It receives an A_Restart-PDU with an Erase Code that allows the Channel Number to be
          different from 00h; the Channel Number is different from 00h and the Management
          Server does support application channels but does not have a channel with the requested
          channel number.

    3.7.3 Procedure: DM_Restart_RCo
    Use
    This method shall use the point-to-point connection oriented remote communication.
    The Management Client shall prior to calling this Management Procedure with a Master Reset verify
    that this feature is effectively supported by the Management Server. If not, the procedure shall only be
    called with a Basic Restart 11).
    A DM_Connect shall be executed before executing this Management Procedure.
    After reception of the A_Restart-PDU this Transport Layer connection breaks down with the
    execution of the A_Restart service; nevertheless an explicit DM_Disconnect procedure shall follow.

    11) Existing implementations may not check bit 0 of octet 7 and may not react as expected. They may ignore the
       service entirely, only perform a Basic Restart if a Master Reset is called or exhibit another behaviour.

    Used Application Layer services for Management
    - A_Restart

    Parameters of the Management Procedure
    DM_Restart_RCo (/* [in] */ mpp_RestartType, /* [in] */ mpp_EraseCode,
                   /* [in] */ mpp_ChannelNumber, /* [out] *mpp_ErrorCode,
                   /* [out] */ mpp_ProcessTime)
        mpp_RestartType    This Management Procedure Parameter shall indicate whether a Basic
                           Restart or a Master Reset shall be executed.
        mpp_EraseCode      This Management Procedure Parameter shall indicate which
                           Resource(s) shall be reset to its (their) default value. This is void in
                           case only a Basic Restart is executed.
        mpp_ChannelNumber  The number of the application channel that shall be reset or 00h.
        mpp_ErrorCode      This Management Procedure Parameter shall contain the Error Code
                           returned by the Management Client.
        mpp_ProcessTime    This Management Procedure Parameter shall return to the Management
                           Client the Process Time needed by the Management Server. The
                           Management Client shall consider this mpp_ProcessTime as time-out
                           after which communication attempts following a Master Reset shall be
                           considered without success.

    Variables
    None.

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        Note over C: The Management Client shall send an A_Restart-PDU to the Management Server in point-to-point connection-oriented communication mode; the fields of the A_Restart-PDU shall be set according the values of the Parameters of this Management Procedure. Reserved and unused fields shall be set to 0.
        C->>S: A_Restart-PDU (restart_type = mpp_RestartType, erase_code = mpp_EraseCode, channel_number = mpp_ChannelNumber)
        Note over S: The Management Server shall confirm with an A_Restart_Response-PDU if a Master Reset is requested. It shall then execute a Basic Restart or Master Reset as requested.
        S->>C: A_Restart_Response-PDU (restart_type = mpp_RestartType, mpp_ErrorCode = error_code, mpp_ProcessTime = process_time)
        Note over S: The Management Server shall reset the related Resource as indicated in the A_Restart-PDU (1). The Management Server shall additionally restart.
        Note over C,S: It is recommended that the execution of the Basic Restart includes closing the Transport Layer connection. This is however not required.
        Note over S: Additionally, it may be that the reset of the Management Server's communication system leads to the effect that the handling of the T_Disconnect in the Management Server's communication stack "down" is not completed and that no T_Disconnect–frame is sent on the bus.
        S-->>C: T_Disconnect-PDU ()
        Note over C: abort the connection of the client side Transport Layer
        C->>S: T_Disconnect-PDU ()
    ```

    Exception handling
    The general exception handling shall be applicable.
    (1) If the Management Server receives an A_Restart-PDU with a reserved field with a value
        different from 0, then this service request shall be ignored.
    (2) If the Management Server receives an A_Restart-PDU but the Management Client does not
        have the required access rights (KNX Authorization) then it shall respond with an
        A_Restart_Response-PDU with Error Code = 01h "Access Denied".
    (3) If the Management Server receives an A_Restart-PDU with an Erase Code that it does not
        support then it shall respond with an A_Restart_Response-PDU with Error Code = 02h
        "Unsupported Erase Code".
    (4) The Management Server shall respond with the Error Code 03h = "Invalid Channel Number"
        in any of the following cases.
        - It receives an A_Restart-PDU with a Channel Number that is not 00h with an Erase
          Code for which the Channel Number.
        - It receives an A_Restart-PDU with an Erase Code that allows the Channel Number to be
          different from 00h; the Channel Number is different from 00h but the Management
          Server does not support application channels.
        - It receives an A_Restart-PDU with an Erase Code that allows the Channel Number to be
          different from 00h; the Channel Number is different from 00h and the Management
          Server does support application channels but does not have a channel with the requested
          channel number.
    (5) All telegrams sent out by the Management Server shall be ignored, except negative
        TL-confirmations.
        In particular, the recommended T_Disconnect-PDU from the Management Server may or may
        not be sent on the bus. The Management Client shall take that into account.
        1 Regardless of whether or not a T_Disconnect-PDU is received from the Management
          Server, the Management Client shall issue a T_Disconnect-PDU to the Management
          Server.
        2 The Management Client shall wait for a possible T_Disconnect-PDU for
          6 seconds.(See NOTE 16)
          - If after this time no T_Disconnect-PDU is received, then this shall not be regarded as
            a protocol error.
          - If the Management Client receives a T_Disconnect-PDU then it shall ignore this
            message. This T_Disconnect-PDU may be received before or after the "own"
            mandatory T_Disconnect-PDU from the Management Client specified under 1.
          In both cases, at first after this time-out has elapsed, the Management Client shall
          continue the possible further configuration of the Management Server: the configuration
          shall not be continued while this time-out has not elapsed.
          NOTE 16 This is because a possible subsequent T_Connect-PDU from the MaC and the awaited
          T_Disconnect-PDU from the MaS may miss each other on the network. Cause and consequence are then
          unclear to both MaS and MaC, which will leave the TL state machines in an unpredictable state.

    3.7.4 Procedure: DMP_Restart_LEmi1
    This Management Procedure shall use the local communication with EMI 1.

    Used EMI-services for Management
    - PC_Set_Value

    Parameters of the Management Procedure
    DMP_Restart_LEmi1(/* [out] */ DmpError)
        DmpError  Possible error indication.

    Sequence

    ```mermaid
    sequenceDiagram
        participant C as Management Client
        participant S as Management Server
        C->>S: PC_Set_Value.req message (Length = 1 octet, Address = 0060h, data = C0h)
        Note over C,S: wait until Management Server was restarted
    ```

    Exception handling
    The general exception handling shall apply.

Inputs (from spec):
    (see body)
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from xknx import XKNX


async def dm_restart(xknx: XKNX) -> None:
    """DM_Restart — see module docstring for the verbatim spec text."""
    raise NotImplementedError("DM_Restart (KNX 03.05.02 §3.7) — implementation pending")
