# Matrox: NMOS With Privacy Encryption
{:.no_toc}  
Copyright 2023, Matrox Graphics Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

{:toc}  

## Introduction

The Privacy Encryption Protocol (PEP) is defined by the [VSF][] technical recommendation [TR-10-13][]. It describes a method to generate keying material for the encryption, decryption and authentication of media content over multicast and unicast networks. It is designed to support multiple types of transport protocol adaptations. The default adaptation defined in [TR-10-13][] technical recommendation describes privacy encryption of media streams having an RTP payload format. The [VSF][] technical recommendation [TR-10-14][] provides the adaptation for the USB-IP protocol. This document provides additional adaptations for the SRT and UDP protocols.

This document briefly describes the PEP parameters. Detailed information is provided by the [TR-10-13][] technical recommendations.

Although the Privacy Encryption Protocol (PEP) is specified for an IPMX streaming environment, it may be used in non-IPMX streaming environments with devices supporting the PEP adaptation specific stream format and the configuration of PEP Pre-Shared Keys.

## Use of Normative Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119][RFC-2119].

## Definitions

PSK             A Pre-Shared Key used as the root secret in a privacy encryption key derivation process.
PEP             Privacy Encryption Protocol documented in IPMX [TR-10-13][] technical recommendation
ECDH            Elliptic Curve Diffie-Hellman
Administrator   An individual or entity with administrative authority and responsibility for managing devices deployed within a network, ensuring compliance with security policies, configuration requirements, and operational standards under a specified administrative domain.

## Compliance

An implementation MUST be compliant with the strict requirements of [TR-10-13][] that are introduced by a `shall` clause. Those requirements could be repeated in this specification to emphasis their importance without impacting their original normative scope. This specification MAY document additional `protocol`, `mode` and `ecdh_curve` in addition to those specified in [TR-10-13][], [TR-10-14] or other VSF/IPMX technical recommendations. Allowing additional values for those parameters MUST be interpreted as a violation of a `shall` clause of those technical recommendations.

An implementation MUST be compliant with the non-strict requirements of [TR-10-13][] that are introduced by `should` and `may` clauses and that are elevated to strict requirements in this specification by a `MUST` clause.

An implementation MUST be compliant with new requirements introduced by this specification that are not part of [TR-10-13][].

## Enabling/disabling privacy encryption

As indicated in [TR-10-13][], the enabling and disabling of privacy encryption in devices supporting the PEP technology is under the control of the device manufacturer. This process MUST be performed by an Administrator in a secure way through a proprietary device configuration interface using a secure communication method and secure storage of the information in the device. Secure communication and storage MUST follow industry-recognized best practices to ensure confidentiality, integrity, and protection against unauthorized access during configuration. An NMOS API MUST NOT allow changing the enabling or disabling of privacy encryption. Refer to "SDP transport file parameters / NMOS transport parameters" of [TR-10-13][] for more details about enabling/disabling privacy encryption.

The enabling and disabling of privacy encryption is intentionally kept under the control of the device manufacturer, allowing flexibility in implementation methods to accommodate diverse environments and security requirements. 

The enabling and disabling of privacy encryption MAY be performed by an Administrator on a device basis or on a per-Sender/Receiver basis. The default method MUST be on a device basis.

When privacy encryption is managed on a per-Sender basis the implementation MUST provide a warning to the Administrator if content, optionally composited, mixed, or multiplexed, that is transmitted by a Sender with privacy encryption is also transmitted in clear by another Sender of the same device.

When privacy encryption is managed on a per-Receiver basis the implementation MUST provide a warning to the Administrator if content consumed by a Receiver with privacy encryption is to be composited, mixed, or multiplexed with content in clear from another Receiver of the same device.

An implementation MUST provide a warning to an Administrator or to a log accessible to an Administrator if dynamic switching of the essences within the device violates the previous requirements.

> Note: The security postulate for a Sender is that privacy-encrypted content must always remain protected and must never be transmitted in clear by the same device. For a Receiver, the postulate is that content can be trusted only if received with privacy encryption, requiring that privacy-encrypted content is never composited, mixed, or multiplexed with content received in clear. 

> Note: Privacy encryption is not a content protection mechanism and providing access to a low quality stream violates the privacy objective.

## PSK provisioning

As indicated in [TR-10-13][], the provisioning of PSK(s) in devices supporting the PEP technology is under the control of the device manufacturer. This process MUST be performed by an Administrator in a secure way through a proprietary device configuration interface, using a secure communication method and secure storage for the information in the device. Secure communication and storage MUST follow industry-recognized best practices to ensure confidentiality, integrity, and protection against unauthorized access during provisioning and configuration. An NMOS API MUST NOT allow the provisioning of PSK in devices. Refer to the section "Key distribution" of [TR-10-13][] for more details about the keys distribution/provisioning process.

The PSK provisioning is intentionally kept under the control of the device manufacturer, allowing flexibility in implementation methods to accommodate diverse environments and security requirements. While PSK provisioning mechanisms are not defined at the PEP level, they MUST ensure confidentiality of PSKs during provisioning and storage and unambiguous identification of each PSK.

### Identification

A PSK has a value and a size (128, 256, or 512 bits). Each PSK is identified by a `key_id`, which MUST be unique among all devices within a network under a given administrative authority. This ensures that each PSK is uniquely identifiable across devices in the network and prevents ambiguity or potential security risks arising from duplicate key associations. Only one `key_id` SHOULD be associated with a given PSK value. For high-security deployments, only one `key_id` MUST be associated with a given PSK value. If a device spawn multiple administrative authorities, the various authorities MUST use an identical definition (value, size, `key_id`) of the shared PSK(s). The key provisioning process MUST ensure that, for a given `key_id`, all devices within the network under a given administrative authority receive the same PSK value and size.

> Note: The [TR-10-13][] technical recommendation imposes precise requirements about the identification of the PSK size to the vendor specific PSK provisioning API.

To simplify the management PSK Administrators SHOULD use either a) only PSK of 128 bit or b) only PSK of 256 adn 512 bit.

### Association

A device MAY be provisioned with multiple PSK. For a Sender device each Sender using privacy encryption MUST be associated with a provisioned PSK through its `key_id`. For a Receiver device each Receiver using privacy encryption MUST be associated with a set of allowed provisioned PSK through their `key_id`. A Receiver MUST populate the constraints associated with the IS-05 extended `ext_privacy_key_id` transport parameter with all the `key_id` values allowed by the Receiver. A Receiver using privacy encryption becomes associated with one such provisioned PSK through its `key_id` at activation time. A Receiver MUST fail the activation if the provided `key_id` is not provisioned in the Receiver device or not present in the Receiver `ext_privacy_key_id` transport parameter constraints.

## Parameters

The [TR-10-13][] technical recommendation defines the following parameters that are accessible as IS-05 extended transport parameters and constraints, and also as a `privacy` attribute parameters in an SDP transport file.

Transport Parameter Name | Type | SDP Name | Sender | Receiver
 --- | --- | --- | --- | --- 
ext_privacy_protocol | string | protocol | r/w | r/w
ext_privacy_mode | string | mode | r/w | r/w
ext_privacy_iv | string | iv | read-only | r/w
ext_privacy_key_generator | string | key_generator | read-only | r/w
ext_privacy_key_version | string | key_version | read-only | r/w
ext_privacy_key_id | string | key_id | read-only | r/w
ext_privacy_ecdh_sender_public_key | string | - | read-only | r/w
ext_privacy_ecdh_receiver_public_key | string | - | r/w | read-only
ext_privacy_ecdh_curve | string | - | r/w | r/w

### IS-05 Transport Parameters

A Sender/Receiver implementing [TR-10-13][] MUST provide the following IS-05 extended transport parameters in the active, staged and constraints endpoints: `ext_privacy_protocol`, `ext_privacy_mode`, `ext_privacy_iv`, `ext_privacy_key_generator`, `ext_privacy_key_version` and `ext_privacy_key_id`.

A Sender/Receiver implementing [TR-10-13][] and supporting the ECDH mode MUST also provide the following IS-05 extended transport parameters in the active, staged and constraints endpoints: `ext_privacy_ecdh_sender_public_key`, `ext_privacy_ecdh_receiver_public_key` and `ext_privacy_ecdh_curve`.

The `ext_privacy` transport parameters MAY be used with any transport supporting privacy encryption and having a protocol adaptation specified in either one of [TR-10-13], [TR-10-14], other VSF/IPMX technical recommendations or this specification.

### IS-05 Transport Parameters Constraints

Each `ext_privacy` transport parameter MUST have an associated constraint that indicates either that the parameter is unconstrained, allowing any valid value, or that it is constrained to a specific set of allowable values. A parameter identified as `read-only` in the parameter definitions table MUST always be constrained to a single value. A Sender/Receiver MUST fail an activation if any IS-05 `ext_privacy` transport parameter violates its defined constraints.

The constraints endpoint of parameters `ext_privacy_protocol`, `ext_privacy_mode` of Senders and Receivers MUST list all the supported protocols and modes.

Sender/Receiver constraints associated with parameters `ext_privacy_protocol` and `ext_privacy_mode` MUST declare all the supported protocols and modes. These parameters MUST NOT be unconstrained.

### Protocol
The `protocol` parameter MUST be one of: "RTP", "RTP_KV", "UDP", "UDP_KV", "USB", "USB_KV", "SRT", "RTSP", "RTSP_KV", "NULL"

If privacy encryption is disabled or not supported by a Sender/Receiver and the `ext_privacy` transport parameters are present, the "NULL" protocol MUST be used for the active and staged `ext_privacy_protocol` extended transport parameters to indicate that privacy encryption is not available / disabled. The associated constraints MUST allow only the "NULL" protocol when an active or staged `ext_privacy_protocol` value is "NULL".

The `protocol` "RTP" MUST be supported by all devices implementing [TR-10-13][] for the `urn:x-nmos:transport:rtp`, `urn:x-nmos:transport:rtp.mcast` and `urn:x-nmos:transport:rtp.ucast` transports.

The `protocol` "RTP" MAY be supported by devices implementing [TR-10-13][] for the `urn:x-matrox:transport:srt.rtp` transports.

The `protocol` "RTP_KV" MAY be supported by devices supporting the "RTP" `protocol`.

The `protocol` "UDP" MUST be supported by all devices implementing [TR-10-13][] for the `urn:x-matrox:transport:udp`, `urn:x-matrox:transport:udp.mcast` and `urn:x-matrox:transport:udp.ucast` transports.

The `protocol` "UDP" MAY be supported by devices implementing [TR-10-13][] for the `urn:x-matrox:transport:srt` and `urn:x-matrox:transport:mp2t` transports.

The `protocol` "UDP_KV" MAY be supported by devices supporting the "UDP" `protocol`.

The `protocol` "USB_KV" MUST be supported by all devices implementing [TR-10-13][] and [TR-10-14][] for the `urn:x-matrox:transport:usb` transport.

The `protocol` "USB" MAY be supported by devices supporting the "USB_KV" `protocol`.

The `protocol` "SRT" MUST be supported by all devices implementing [TR-10-13][] for the `urn:x-matrox:transport:srt`, `urn:x-matrox:transport:srt.rtp` and `urn:x-matrox:transport:srt.mp2t` transports.

### Mode

If privacy encryption is disabled or not supported by a Sender/Receiver and the `ext_privacy` transport parameters are present, the "NULL" mode MUST be used for the active and staged `ext_privacy_mode` extended transport parameters to indicate that privacy encryption is not available / disabled. The associated constraints MUST allow only the "NULL" mode when an active or staged `ext_privacy_mode` parameter is "NULL".

#### For protocols "RTP" and "RTP_KV"
The `mode` parameter MUST be one of: "AES-128-CTR", "AES-256-CTR", "AES-128-CTR_CMAC-64", "AES-256-CTR_CMAC-64", "AES-128-CTR_CMAC-64-AAD", "AES-256-CTR_CMAC-64-AAD", "ECDH_AES-128-CTR", "ECDH_AES-256-CTR", "ECDH_AES-128-CTR_CMAC-64", "ECDH_AES-256-CTR_CMAC-64", "ECDH_AES-128-CTR_CMAC-64-AAD", "ECDH_AES-256-CTR_CMAC-64-AAD".

The `mode` "AES-128-CTR" MUST be supported by all devices implementing the "RTP" or "RTP_KV" protocols.

A Sender configured by an Administrator to use a 256 or 512 bit PSK MUST support only modes based on AES-256. A Sender configured to use a 128 but PSK MAY support either or both AES-128 and AES-256 based modes.

> Note: if the IS-05 `ext_privacy_mode` transport parameter constraints of a Sender only allow modes based on AES-128, it indicates that only PSK of 128 bit are used.

A Receiver configured by an Administrator to allow the use a 256 or 512 bit PSK MUST support modes based on AES-256. A Receiver configured to allow the  use of a 128 bit PSK MUST support modes based on AES-128. A Receiver MAY simultaneously support modes based on AES-128 and AES-256. A Receiver MUST fail activation if a `key_id` associated with a 256 or 512 bit PSK is used along with a `mode` that is not based on AES-256.

> Note: if the IS-05 `ext_privacy_mode` transport parameter constraints of a Receiver only allow modes based on AES-128, it indicates that only PSK of 128 bit are allowed.

The PEP "urn:ietf:params:rtp-hdrext:PEP-Full-IV-Counter" and "urn:ietf:params:rtphdrext:PEP-Short-IV-Counter" RTP Extension Headers MUST be declared in the SDP transport file. The declaration MUST be performed as per RFC8285 using the "sendonly" direction.

#### For protocol "UDP" and "UDP_KV"
The `mode` parameter MUST be one of: "AES-128-CTR", "AES-256-CTR", "ECDH_AES-128-CTR", "ECDH_AES-256-CTR".

The `mode` "AES-128-CTR" MUST be supported by all devices implementing the "UDP" or "UDP_KV" protocols.

#### For protocol "USB" and "USB_KV"
The `mode` parameter MUST be one of: "AES-128-CTR_CMAC-64-AAD", "AES-256-CTR_CMAC-64-AAD", "ECDH_AES-128-CTR_CMAC-64-AAD", "ECDH_AES-256-CTR_CMAC-64-AAD".

The `mode` "AES-128-CTR_CMAC-64-AAD" MUST be supported by all devices implementing the "USB" or "USB_KV" protocols.

#### For protocol "SRT"
The `mode` parameter MUST be one of: "AES-128-CTR", "AES-256-CTR", "ECDH_AES-128-CTR", "ECDH_AES-256-CTR", "AES-128-GMAC-128", "AES-256-GMAC-128", "ECDH_AES-128-GMAC-128", "ECDH_AES-256-GMAC-128"

The `mode` "AES-128-CTR" MUST be supported by all devices implementing the "SRT" protocol.

### Elliptic Curve Diffie-Hellman (ECDH)

The ECDH mode allows Perfect Forward Secrecy.

The `ecdh_curve` parameter MUST be one of: "secp256r1", "secp521r1", "25519", "448" or "NULL".

If the ECDH mode is not supported by a Sender/Receiver and the `ext_privacy_ecdh` transport parameters are present, the "NULL" curve MUST be used for the active and staged `ext_privacy_ecdh_curve` extended transport parameters to indicate that the ECDH mode is not available. The associated constraints MUST allow only the "NULL" protocol when an active or staged `ext_privacy_ecdh_curve` parameter is "NULL".

The `ecdh_curve` “secp256r1" MUST be supported by all devices implementing the ECDH mode.

Sender/Receiver constraints associated with parameter `ext_privacy_ecdh_curve`  MUST declare all the supported curves. This parameter MUST NOT be unconstrained.

The ECDH functionality is available through the IS-05 extended transport parameters only. There are no ECDH parameters in the `privacy` attribute of an SDP transport file. The ECDH modes of operation are optional and none of those modes are required to be supported by an implementation conforming with [TR-10-13], [TR-10-14][] or other VSF/IPMX technical recommendations.

> Note: A Sender/Receiver generates a new public key whenever it explicitly or implicitly becomes inactive.

## IS-04, IS-05, IS-11 Senders

A Sender supporting privacy encryption MUST follow the requirements of the "Privacy" section of the "NMOS With IPMX" specification regarding IS-04 Sender Capabilities, IS-05 transport parameter constraints and IS-11 supported constraints.


## IS-04, IS-05 Receivers

A Receiver supporting privacy encryption MUST follow the requirements of the "Privacy" section of the "NMOS With IPMX" specification regarding IS-04 Receiver Capabilities and IS-05 transport parameter constraints.

## Controller

A Receiver supporting privacy encryption MUST follow the requirements of the "Privacy" section of the "NMOS With IPMX" specification regarding IS-04 Sender/Receiver Capabilities, IS-05 transport parameter constraints and IS-11 supported constraints.

A Controller has the responsibility of assessing the privacy encryption compatibility of Receivers with a Sender. This process is performed both at the IS-04 and IS-05 levels. If the Sender and the Receivers implement the `urn:x-matrox:cap:transport:privacy` capability, a Controller MAY perform quick compatibility verification using this capability. Then, if the Sender and Receivers are compatible at the IS-04 level or if the `urn:x-matrox:cap:transport:privacy` capability is not implemented by all the parties, a Controller MUST perform a final compatibility verification using the IS-05 `ext_privacy` transport parameters and associated constraints. A Controller MAY constrain the Sender with privacy encryption parameters compatible with the Receivers.

A Controller MUST ensure that the `protocol` and `mode` parameters are identical among the subscribing/connecting Receivers and the Sender. When an ECDH `mode` is used the Controller MUST also ensure that the `ecdh_curve` parameter is identical between the subscribing/connecting Receiver and the peer Sender and exchange the ECDH `public_key` parameters between the peers.

A Controller MUST forward the `key_generator`, `key_version` and `key_id` of a Sender to the subscribing/connecting Receivers.

If a mismatch is detected in `protocol`, `mode`, or `ecdh_curve` parameters, or if the ECDH `public_key` parameters cannot be exchanged, the Controller MUST prevent activation and SHOULD notify the User or an Administrator.

> Note: IS-11 operates at the IS-04 capabilities/constraints level and cannot be used to constrain privacy encryption, which must be managed using IS-05.

### IS-05 Sender Activation

The effective values of the IS-05 `ext_privacy` transport parameters and the `privacy` attribute parameters of the SDP transport file of a Sender are not fixed until the activation of the Sender and `master_enable` becomes `true` at the active endpoint. A Controller MUST NOT assume final values for the IS-05 `ext_privacy` transport parameters of a Sender prior to activation. A Controller MUST NOT assume final values for the SDP transport file `privacy` attribute parameters of a Sender prior to activation.

The values of the parameters of the `privacy` attribute of the SDP transport file of an active Sender MUST match the values of the active `ext_privacy` transport parameters of such an active Sender.

It is important to consider this requirement of [IS-05][] [Re-Activating Senders & Receivers](https://specs.amwa.tv/is-05/releases/v1.1.2/docs/Behaviour.html#re-activating-senders--receivers) that states:

> "If an explicit activation is performed against a Sender or Receiver, the API MUST request a re-application of settings to the underlying Sender or Receiver implementation whether the settings have changed or not. For example, in the case of multicast Receivers, it is suggested that this involves an explicit IGMP leave and join. For a Sender, this might involve stopping and re-starting the stream."

The [TR-10-13][] expression "become inactive" MUST be interpreted as `master_enable` becomes `false` at the active endpoint of a Sender and as such the Sender MUST NOT change the IS-05 `ext_privacy` transport parameters and the `privacy` attribute parameters of the SDP transport file during "re-activation" because `master_enable` remains `true` at the active endpoint of the Sender. The privacy encryption parameters of a Sender MUST remain unchanged during "re-activation".

#### With ECDH

The ECDH mode is possible only in peer-to-peer mode where one Receiver connect/subscribe to one Sender.

The activation of a Sender with `master_enable` set to `false` MUST regenerate the value of the active and staged `ext_privacy_ecdh_sender_public_key` transport parameter if the ECDH mode is supported.

A Controller MUST read the value of the `ext_privacy_ecdh_sender_public_key` transport parameter after the activation of the Sender with `master_enable` set to `true`.

A Controller MUST provide the value of the peer Receiver's `ext_privacy_ecdh_receiver_public_key` transport parameter to the Sender at activation with `master_enable` set to `true`.

With ECDH a Controller MUST exchange the Sender and Receiver public keys to activate an ECDH session. The ECDH functionality is available for peer-to-peer connections only. A Sender becomes associated with a peer Receiver at activation when `master_enable` becomes true.

### IS-05 Receiver activation

For transports supporting an SDP transport file, if the ECDH mode is not used, the process of activating a Receiver is the same with and without privacy encryption. A Controller SHOULD get the SDP transport file of a Sender and provide it to the Receivers at activation. The privacy encryption parameters of the Sender are automatically taken from the SDP transport file.

It is important to consider this requirement of [IS-05][] [Re-Activating Senders & Receivers](https://specs.amwa.tv/is-05/releases/v1.1.2/docs/Behaviour.html#re-activating-senders--receivers) that states:

> "If an explicit activation is performed against a Sender or Receiver, the API MUST request a re-application of settings to the underlying Sender or Receiver implementation whether the settings have changed or not. For example, in the case of multicast Receivers, it is suggested that this involves an explicit IGMP leave and join. For a Sender, this might involve stopping and re-starting the stream."

The [TR-10-13][] expression "become inactive" MUST be interpreted as `master_enable` becomes `false` at the active endpoint of a Receiver and as such the Receiver MUST NOT change the IS-05 `ext_privacy` transport parameters during "re-activation" because `master_enable` remains `true` at the active endpoint of the Receiver. The privacy encryption parameters of a Receiver MUST remain unchanged during "re-activation".

#### With ECDH

The ECDH mode is possible only in peer-to-peer mode where one Receiver connect/subscribe to one Sender.

The activation of a Receiver with `master_enable` set to `false` MUST regenerate the value of the active and staged `ext_privacy_ecdh_receiver_public_key` transport parameter if the ECDH mode is supported. To change the value of the `ext_privacy_ecdh_curve` transport parameter of a Receiver, a Controller MUST set `master_enable` to false during an activation in order to regenerate a new value for the `ext_privacy_ecdh_receiver_public_key` transport parameter.

Once a Controller reads the `ext_privacy_ecdh_receiver_public_key` transport parameters of a Receiver to provide its value to a Sender it MUST NOT perform any other activation of the Receiver with `master_enable` set to `false` as otherwise the value of `ext_privacy_ecdh_receiver_public_key` would change.

A Controller MUST provide the value of the peer Sender's `ext_privacy_ecdh_sender_public_key` transport parameter to the Receiver at activation with `master_enable` set to `true`.

With ECDH a Controller MUST exchange the Sender and Receiver public keys to activate an ECDH session. The ECDH functionality is available for peer-to-peer connections only. A Sender becomes associated with a peer Receiver at activation when `master_enable` becomes true.

## RTP transport adaptation

This `protocol` is used for `urn:x-nmos:transport:rtp`, `urn:x-nmos:transport:rtp.mcast`, `urn:x-nmos:transport:rtp.ucast` and `urn:x-matrox:transport:rtp.tcp`.

This `protocol` MAY also be used for `urn:x-matrox:transport:srt.rtp`. In this scenario the privacy encryption is performed on the RTP stream prior to transmission with the SRT protocol. The SRT encryption is not used or enabled. This scenario allows to use this `protocol` adaptation with the reliable UDP transport protocol SRT.

See the [TR-10-13][] technical recommendation for the details.

See the [NMOS With IPMX](https://github.com/alabou/NMOS-MatroxOnly/blob/main/NMOS%20With%20IPMX.md) document for a detailed definition of the RTP Payload Header of various media types.

> Note: When the `urn:x-matrox:transport:rtp.tcp` transport is used the packets are transmitted as `RTP/AVP` and hence the protocol is either "RTP" or "RTP_KV".

## USB-IP transport adaptation

This `protocol` is used for `urn:x-matrox:transport:usb`.

See the [TR-10-14][] technical recommendation for the details.

## SRT transport adaptation

This `protocol` is used for `urn:x-matrox:transport:srt`, `urn:x-matrox:transport:srt.mp2t` and `urn:x-matrox:transport:srt.rtp`.

The `protocol` MUST be "SRT".

The `mode` parameter MUST be one of "AES-128-CTR", "AES-256-CTR", "ECDH_AES-128-CTR", "ECDH_AES-256-CTR".

The SRT `passphrase` MUST correspond to the `privacy_key` defined in the Privacy Key Derivation section of [TR-10-13][]. The SRT `passphrase` will be used by the SRT protocol to derive the encryption key. The SRT encryption takes control of the `iv'_ctr` value of the cipher and performs its own key management (renewal, derivation). The `iv` PEP parameter is not used with SRT.

## UDP transport adaptation

This `protocol` is used for `urn:x-matrox:transport:udp`, `urn:x-matrox:transport:udp.mcast`, `urn:x-matrox:transport:udp.ucast`, `urn:x-matrox:transport:udp.mp2t`, `urn:x-matrox:transport:udp.mp2t.mcast` and `urn:x-matrox:transport:udp.mp2t.ucast`.

This `protocol` MAY also be used for `urn:x-matrox:transport:srt` and `urn:x-matrox:transport:srt.mp2t`. In this scenario the privacy encryption is performed on the MPEG2-TS stream prior to transmission with the SRT protocol. The SRT encryption is not used or enabled. This scenario allows to use this `protocol` adaptation with the reliable UDP transport protocol SRT.

The `protocol` MUST be "UDP" or "UDP_KV".

A Sender using the "UDP_KV" protocol MUST transmit the `key_version` along with the ciphered content in the `dynamic_key_version` field of the CTR Full Header. When using the "UDP" protocol, the `dynamic_key_version` field of the CTR Full Header MUST be set to 0 unless the CTR Full Header field is being used for other purposes outside the scope of this specification. A Receiver using the "UDP" protocol MUST ignore the `dynamic_key_version` field of the CTR Full Header. When using the "UDP_KV" protocol the Receiver MUST monitor it.

The `mode` parameter MUST be one of "AES-128-CTR", "AES-256-CTR", "ECDH_AES-128-CTR", "ECDH_AES-256-CTR".

A Sender / Receiver MUST support the "AES-128-CTR" mode. Support for all other modes is optional.

The `key` MUST correspond to the `privacy_key` defined in the Privacy Key Derivation section.

The `iv'_ctr` value MUST correspond to `iv'` || `ctr`. The `iv'` value MUST be a 64-bit Octet String in binary form. It MUST derive from the `iv` parameter of the stream associated SDP transport file and/or NMOS transport parameters. The `iv'` value MUST correspond to the base `iv` value for a stand-alone unidirectional stream or the sum of the base `iv` and a sub-stream index in the range [0, 1023] for a multiplexed stream.

The `ctr` value MUST be a 64-bit Octet String in binary form. It MUST be transmitted by the Sender along with the ciphered content. This 64-bit value MUST be transmitted in the `ctr_high` and `ctr_low` fields of the CTR Full Header. The least significant 24 bits MUST be transmitted in the `ctr_short` field of the CTR Short Header. The `ctr` value MUST start at 0 and increment by 1 modulo 2^64 at every slice being encrypted. The ctr MUST start at 0 for a new key and may continue counting for a given key if it is known that the `ctr` value cannot wrap-around during the active time of the Sender/ Receiver.

A Receiver MUST recover the full `ctr` value from the `ctr_low` and `ctr_high` fields of the CTR Full Header as follow:

> ctr = ctr_high0 || ctr_high1 || ctr_high2 || ctr_high3 || ctr_low0 || ctr_low1 || ctr_low2 || ctr_low3

A Receiver MUST recover the full `ctr` value from the `ctr_short` field of the CTR Short Header as follow:

> prev24 = ctr5 || ctr6 || ctr7  
> new24 = ctr_short0 || ctr_short1 || ctr_short2

If the value corresponding to prev24 is smaller than the value corresponding to new24; then the recovered `ctr` is ctr0 || ctr1 || ctr2 || ctr3 || ctr4 || ctr_short0 || ctr_short1 || ctr_short2; else the recovered `ctr` is ctr0 || ctr1 || ctr2 || ctr3 || ctr4 || ctr_short0 || ctr_short1 || ctr_short2 + 00 || 00 || 00 || 00 || 01 || 00 || 00 || 00.

Privacy encryption MUST be applied to the `PES_packet_data_byte` bytes of a `PES_Packet` as defined by [H.222.0][] for streams having a `stream_id` other than `program_stream_map`, `padding_stream`, `private_stream_2`, `ECM`, `EMM`, `program_stream_directory`, `DSMCC_stream`, `ITU-T Rec. H.222.1 type E stream`. Multiple MPEG2-TS packets MAY be required to transport a single `PES_Packet`. MPEG2-TS packets of PID outside the range from 0x0010 to 0x1FFE MUST not be encrypted.

The `PES_packet_data_byte` bytes section of a `PES_Packet` MUST be encrypted. Other sections of a `PES_Packet` and MPEG2-TS packet MUST NOT be encrypted. The `PES_packet_data_byte` bytes MUST be processed as a big-endian sequence of bytes subdivided into zero or more complete data slices of 16 bytes, that MAY be terminated by a partial data slice of less than 16 bytes. Partial data slices MUST be assumed to be zero-filled to complete a big-endian data slice of 16 bytes by the AES encryption/decryption internal process. The provided bytes of the partial data slice correspond to the most significant bytes of the big-endian data slice. The zero filled bytes MUST be ignored/discarded and not be considered as being part of the PES packet data bytes.

Note: A `PES_packet_data_byte` bytes sequence is allowed to terminate with a partial data slice of less than 16 bytes.

The `private_data_byte` bytes of the MPEG2-TS `adaptation_field` structure, as signaled by `transport_private_data_flag` and `transport_private_data_length`, MUST be used to transport the required `dynamic_key_version`, `ctr_low`, `ctr_high` and `ctr_short` parameters of CTR Full Header and CTR Short Header. The CTR Full Header is signaled by the presence of 12 `private_data_byte` bytes while the CTR Short Header is signaled by the presence of 3 `private_data_byte` bytes. An MPEG2-TS packet with encrypted `PES_packet_data_byte` bytes in its payload MUST have a CTR Full Header or CTR Short Header in its `adaptation_field`.

Note: The use of `private_data_byte` bytes in encrypted MPEG2-TS packets is reserved for the PEP protocol implementation. such usage is signaled by the stream associated `privacy` SDP transport file attribute and/or NMOS transport parameters. A compliant MPEG2-TS stream is not allowed to use private data for other purposes.

An MPEG2-TS packet `adaptation_field` MAY be padded with `stuffing_byte` bytes to ensure that an integral multiple of 16 `PES_packet_data_byte` bytes are present in the MPEG2-TS packet payload for all but the last MPEG2-TS packets transporting the `PES_packet_data_byte` bytes of a `PES_Packet`.

Note: This approach makes privacy encryption compatible with the PES packet slicing of HDCP over MPEG-TS when the `adaptation_field` has space reserved for the `private_data_byte` bytes of the CTR Full/Short Header when `payload_unit_start_indicator` of an MPEG2-TS packet is 1 and that only CTR Full Header are used.

A CTR Full Header MUST be present in the `adaptation_field` of an encrypted MPEG2-TS packet having in its payload the first byte (`payload_unit_start_indicator` = 1) of the first `PES_Packet` of a video frame/field, a video frame/field slice, and an audio frame/packet. 

A CTR Short Header or a CTR Full Header MUST be present in the `adaptation_field` of an encrypted MPEG2-TS packet having in its payload the first byte (`payload_unit_start_indicator` = 1) of a subsequent `PES_packet`, if any, completing a video frame/field, a video frame/field slice or an audio frame/packet. A CTR Short Header SHOULD be used unless the distance between the associated `ctr` values of two consecutive CTR Full Headers is larger or equal than 2^24 units. The concept of “frame” is used for uncompressed and compressed audio and video. The concept of “field” is used for uncompressed and compressed video. The concept of “packet” is used for uncompressed and compressed audio.

A CTR Full Header MUST also be be present in the `adaptation_field` of an encrypted MPEG2-TS packet having in its payload the first byte (`payload_unit_start_indicator` = 1) of a `PES_Packet` that is not categorized as video or audio. 

A CTR Full Header MUST NOT be present in the `adaptation_field` of an encrypted MPEG2-TS packet unless the first byte (`payload_unit_start_indicator` = 1) of a `PES_Packet` is present in the MPEG2-TS payload. 

A CTR Short Header MUST be present in the `adaptation_field` of an encrypted MPEG2-TS packet unless a CTR Full Header is present.

### Headers

CTR Full Header|
--- |
 `0                   1                   2                   3   `|
 `0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 `|
 dynamic_key_version |
 ctr_high |
 ctr_low |

- All the field are in big-endian unless otherwise specified
-	ctr_high corresponds to the most significant bits of ctr (first 4 Octet of ctr Octet String)
    -	ctr0 || ctr1 || ctr2 || ctr3
-	ctr_low corresponds to the least significant bits of ctr (last 4 Octet of ctr Octet String)
    - ctr4 || ctr5 || ctr6 || ctr7

CTR Short Header|
--- |
 `0                   1                   2      `|
 `0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3`|
ctr_short |

-	All the field are in big-endian unless otherwise specified
-	ctr_short corresponds to the least significant bits of ctr (last 3 Octet of ctr Octet String)
    - ctr5 || ctr6 || ctr7

### Dynamic key_version

A Sender configured for in-band dynamic changes of the `key_version` MAY change the `key_version` value dynamically at natural boundaries of the media content (frame, field or GOP boundary for video and ancillary data, packet boundary for audio and generic data) to change the Privacy Cipher encryption key. The current value of the `key_version` MUST be transmitted in clear to the peer Receiver through the `dynamic_key_version` field of the CTR Full Header. The `dynamic_key_version` value MUST correspond to the `key_version` value used for deriving the encryption key of the associated PES packet data bytes.

A Receiver configured for in-band dynamic changes of the `key_version` MUST use the `key_version` received in clear from the peer through the `dynamic_key_version` field of the CTR Full Header to derive the Privacy Cipher decryption key of the associated PES packet data bytes.

Note: Bidirectional streams are not supported by the "UDP" and "UDP_KV" protocols.

## RTSP transport adaptation

This `protocol` is used for `urn:x-matrox:transport:rtsp`, `urn:x-matrox:transport:rtsp.tcp`.

This protocol indicates that the effective transport adaptation of the media streams is based upon the negotiation between the client and server for the transmission protocol. For "RTSP" the possibilities are "RTP" or "UDP" while for "RTSP_KV" the possibilities are "RTP_KV" or "UDP_KV". 

The constraints on the `ext_privacy_mode` parameter MAY describe a combination of modes supported for RTP base adaptations and UDP based adaptations. A Sender/Receiver MUST fail activation if the selected `mode` is not compliant with the transmission protocol negotiated between the RTSP client and server.

> Note: When the `urn:x-matrox:transport:rtsp.tcp` transport is used the packets are transmitted as `RTP/AVP` and hence the protocol is either "RTP" or "RTP_KV".

## Node Reservation

When [Node Reservation](https://github.com/alabou/NMOS-MatroxOnly/blob/main/NMOS%20With%20Node%20Reservation.md) is used along with the Privacy Encryption Protocol (PEP) an additional `key_xcl` parameter is used in the key derivation process.

The privacy_key MUST be derived from a Pre-Shared Key (PSK), a key generator (key_generator), a key version (key_version), a Perfect Forward Secrecy shared secret (key_pfs) and a Node Reservation shared exclusive key using a KDF in counter mode as per NIST.SP.800-108Rev1 section 4.1. 

### 128-bit key derivation (PSK is 128 bits):
```privacy_key = CMAC(PSK, AB || key_generator || key_version || key_pfs || key_xcl)```
### 256-bit key derivation (PSK is 128 or 256 bits):
```privacy_key = CMAC(PSK, AB || key_generator || key_version || HIGH(key_pfs) || key_xcl) ||```  
```              CMAC(PSK, CD || key_generator || key_version || LOW(key_pfs)  || key_xcl)```
### 256-bit key derivation (PSK is 512 bits):
```privacy_key = HMAC-SHA-512/256(PSK, AB || key_generator || key_version|| key_pfs || key_xcl)``` 

The `key_xcl` MUST be the 128 bit `exclusive_key` of the exclusive session, acquired through the `acquire` endpoint of the Node Reservation RestAPI, that activated an associated Senders / Receivers. When  Node Reservation is not used, the key_xcl value MUST be an empty Octet String and it is not used by the key derivation process. Otherwise it MUST be a 16 byte Octet String. It is an Octet String in binary form. 

[H.222.0]: https://www.itu.int/rec/T-REC-H.222.0 "Generic coding of moving pictures and associated audio information: Systems"
[RFC-2119]: https://tools.ietf.org/html/rfc2119 "Key words for use in RFCs"
[RFC-2250]: https://tools.ietf.org/html/rfc2250 "RTP Payload Format for MPEG1/MPEG2 Video"
[RFC-3551]: https://tools.ietf.org/html/rfc3551 "RTP Profile for Audio and Video Conferences with Minimal Control"
[IS-04]: https://specs.amwa.tv/is-04/ "AMWA IS-04 NMOS Discovery and Registration Specification"
[IS-05]: https://specs.amwa.tv/is-05/ "AMWA IS-05 NMOS Device Connection Management Specification"
[NMOS Parameter Registers]: https://specs.amwa.tv/nmos-parameter-registers/ "Common parameter values for AMWA NMOS Specifications"
[VSF]: https://vsf.tv/ "Video Services Forum"
[SMPTE]: https://www.smpte.org/ "Society of Media Professionals, Technologists and Engineers"
[BCP-004-01]: https://specs.amwa.tv/bcp-004-01/ "AMWA BCP-004-01 NMOS Receiver Capabilities"
[TR-10-13]: https://vsf.tv/download/technical_recommendations/VSF_TR-10-13_2024-01-19.pdf "Internet Protocol Media Experience (IPMX): Privacy Encryption Protocol (PEP)"
[TR-10-14]: https://vsf.tv/download/technical_recommendations/VSF_TR-10-14_2024-09-24.pdf "Internet	Protocol Media Experience (IPMX): IPMX USB"
