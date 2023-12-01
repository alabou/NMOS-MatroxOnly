# Matrox: NMOS With Privacy Encryption
{:.no_toc}  
Copyright 2023, Matrox Graphics Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
  
---
  
{:toc}

## Introduction

The Privacy Encryption Protocol (PEP) is defined in the [VSF][] specification [TR-10-13][]. It provides encryption and authentication of media streams using various transport protocols.
The [VSF][] TR-10-13 specification provides the adaptation for the RTP transport protocol. Another [VSF][] document [TR-10-14] provides the adaptation for the IPMX USB protocol. 
This document will provide the adaptations for the SRT and UDP protocols.

The PEP parameters are provided by a Sender through IS-05 extended transport parameters and through an SDP transport file for the transport protocols supporting SDP. 
A Controller provides the PEP parameters to a Receiver through IS-05 extended transport parameters and through an SDP transport file for the transport protocols supporting SDP. This document will briefly describe the PEP parameters. Detailed information is provided by the [VSF][] specifications.

Although the Privacy Encryption Protocol (PEP) is specified for an IPMX streaming environment, it may be used in non-IPMX streaming environments that support the PEP adaptation specific stream format and the configuration of streaming devices with PEP Pre-Shared Keys.

## Use of Normative Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY",
and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119][RFC-2119].

## Definitions

## Parameters

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

### Protocol
The `protocol` parameter MUST be one of: "RTP", "RTP_KV", "UDP", "UDP_KV", "SRT", "USB", "USB_KV", "NULL"

### Mode
#### For protocol "RTP" and "RTP_KV"
The `mode` parameter MUST be one of: "AES-128-CTR", "AES-256-CTR", "AES-128-CTR_CMAC-64", "AES-256-CTR_CMAC-64", "AES-128-CTR_CMAC-64-AAD", "AES-256-CTR_CMAC-64-AAD", "ECDH_AES-128-CTR", "ECDH_AES-256-CTR", "ECDH_AES-128-CTR_CMAC-64", "ECDH_AES-256-CTR_CMAC-64", "ECDH_AES-128-CTR_CMAC-64-AAD", "ECDH_AES-256-CTR_CMAC-64-AAD".
#### For protocol "UDP" and "UDP_KV"
The `mode` parameter MUST be one of: "AES-128-CTR", "AES-256-CTR", "AES-128-CTR_CMAC-64", "AES-256-CTR_CMAC-64", "AES-128-CTR_CMAC-64-AAD", "AES-256-CTR_CMAC-64-AAD", "ECDH_AES-128-CTR", "ECDH_AES-256-CTR", "ECDH_AES-128-CTR_CMAC-64", "ECDH_AES-256-CTR_CMAC-64", "ECDH_AES-128-CTR_CMAC-64-AAD", "ECDH_AES-256-CTR_CMAC-64-AAD".
#### For protocol "USB" and "USB_KV"
The `mode` parameter MUST be one of: "AES-128-CTR_CMAC-64-AAD", "AES-256-CTR_CMAC-64-AAD", "ECDH_AES-128-CTR_CMAC-64-AAD", "ECDH_AES-256-CTR_CMAC-64-AAD".
#### For protocol "SRT"
The `mode` parameter MUST be one of: "AES-128-CTR", "AES-256-CTR", "ECDH_AES-128-CTR", "ECDH_AES-256-CTR"

## SRT transport

The `protocol` MUST be "SRT".

The `mode` parameter MUST be one of "AES-128-CTR", "AES-256-CTR", "ECDH_AES-128-CTR", "ECDH_AES-256-CTR".

The SRT `passphrase` MUST correspond to the `privacy_key` defined in the Privacy Key Derivation section. The SRT `passphrase` will be used by the SRT protocol to derive the encryption key. SRT encryption takes control of the `iv'_ctr` value and performs its own key management (renewal, derivation) and the `iv` parameter of PEP is unused.

## UDP transport with MPEG2-TS

The `protocol` MUST be "UDP" or "UDP_KV".

A Sender using the "UDP_KV" protocol MUST transmit the *key_version* along with the ciphered content in the `dynamic_key_version` field of the CTR Full Header. When using the "UDP" protocol, the `dynamic_key_version` field of the CTR Full Header MUST be set to 0. A Receiver using the "UDP" protocol MUST ignore the `dynamic_key_version` field of the CTR Full Header. When using the "UDP_KV" protocol the Receiver MUST monitor it.

The `mode` parameter MUST be one of "AES-128-CTR", "AES-256-CTR", "ECDH_AES-128-CTR", "ECDH_AES-256-CTR".

A Sender / Receiver MUST support the "AES-128-CTR" mode. Support for all other modes is optional.

The `key` MUST correspond to the `privacy_key` defined in the Privacy Key Derivation section.

The `iv'_ctr` value MUST correspond to `iv'` || `ctr`. The `iv'` value MUST be a 64-bit Octet String in binary form. It MUST derive from the `iv` parameter of the stream associated SDP transport file and/or NMOS transport parameters. The `iv'` value MUST correspond to the base `iv` value for a stand-alone unidirectional stream or the sum of the base `iv` and a sub-stream index in the range [0, 1023] for a multiplexed stream.

The `ctr` value MUST be a 64-bit Octet String in binary form. It MUST be transmitted by the Sender along with the ciphered content. This 64-bit value MUST be transmitted in the `ctr_high` and `ctr_low` fields of the CTR Full Header. The least significant 24 bits MUST be transmitted in the `ctr_short` field of the CTR Short Header. The `ctr` value MUST start at 0 and increment by 1 modulo 264 at every slice being encrypted
The ctr shall start at 0 for a new key and may continue counting for a given key if it is known that the ctr value cannot wrap-around during the active time of the Sender/ Receiver.

A Receiver MUST recover the full `ctr` value from the `ctr_low` and `ctr_high` fields of the CTR Full Header as follow:

ctr = ctr_high0|| ctr_high1 || ctr_high2 || ctr_high3 || ctr_low0 || ctr_low1 || ctr_low2 || ctr_low3

A Receiver MUST recover the full `ctr` value from the `ctr_short` field of the CTR Short Header as follow:

prev24 = ctr5|| ctr6 || ctr7

new24 = ctr_short0 || ctr_short1 || ctr_short2

If the value corresponding to prev24 is smaller than the value corresponding to new24; then the recovered ctr is ctr0 || ctr1 || ctr2 || ctr3 || ctr4 || ctr_short0 || ctr_short1 || ctr_short2; else the recovered ctr is ctr0 || ctr1 || ctr2 || ctr3 || ctr4 || ctr_short0 || ctr_short1 || ctr_short2 + 00 || 00 || 00 || 00 || 01 || 00 || 00 || 00.

For the UDP adaptation, private_data_byte in the MPEG2-TS adaptation_field() structure as signaled by transport_private_data_flag and transport_private_data_length MUST be used to transport the required `dynamic_key_version`, `ctr_low`, ctr_high` and `ctr_short` parameters described in the RTP adaptation.
The CTR Full HEader will be signaled by the presence of 12 private_data_byte bytes while the CTR Short Header will be signaled by the presence of 3 private_data_byte bytes.

A CTR Full Header MUST be used in the first MPEG2-TS packet of a video frame/field, a video frame/field slice, and an audio frame/packet. A CTR Full Header MUST also be used in every MPEG2-TS packet that is not categorized as video or audio. The usage of CTR Full Headers MUST ensure that the distance between the associated `ctr` values of two consecutive CTR Full Headers is less than 224 units. A CTR Short Header MUST be used when a CTR Full Header is not used.

The MPEG2-TS packets after the first one, if any, completing a video frame/field, a video frame/field slice or an audio frame/packet SHOULD use a CTR Short Header. The concept of “frame” is used for uncompressed and compressed audio and video. The concept of “field” is used for uncompressed and compressed video. The concept of “packet” is used for uncompressed and compressed audio.

Only the PES_packet_data_bytes section of a PES packet MUST be encrypted. The PES packet dta bytes MUST be encoded as a big-endian sequence of bytes subdivided into zero or more complete data slices of 16 bytes, that MAY be terminated by a partial data slice of less than 16 bytes. Partial data slices MUST be assumed to be zero-filled to complete a big-endian data slice of 16 bytes by the AES encryption/decryption internal process. The provided bytes of the partial data slice correspond to the most significant bytes of the big-endian data slice. The zero filled bytes MUST be ignored/discarded and not be considered as being part of the PES packet data bytes.

Note: Any PES packet data bytes sequence is allowed to terminate with a partial data slice of less than 16 bytes.

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

A Sender/Receiver configured for in-band dynamic changes of the `key_version` MAY change the `key_version` value dynamically at natural boundaries of the media content (frame, field or GOP boundary for video and ancillary data, packet boundary for audio and generic data) to change the Privacy Cipher encryption key. The current value of the `key_version` shall be transmitted in clear to the peer through the `dynamic_key_version` field of the CTR Full Header. The `dynamic_key_version` value shall correspond to the `key_version` value used for deriving the encryption key of the associated PES packet data bytes.

When a Receiver configured for in-band dynamic changes of the `key_version` becomes active it MUST select an initial `key_version` value. Subsequently it MAY increment the selected `key_version` value by 1 modulo 2^32 to change the associated `privacy_key` during the activation. The `key_version` MAY be shared by a number of streams / sub-streams encrypted by a Receiver Device. A Sender/Receiver configured for in-band dynamic changes of the `key_version` MUST use the `key_version` received in clear from the peer through the `dynamic_key_version` field of the CTR Full Header to derive the Privacy Cipher decryption key of the associated PES packet data bytes.


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
[TR-10-13]: https://vsf.tv/download/technical_recommendations/VSF_TR-10-13.pdf "Internet Protocol Media Experience (IPMX): Privacy Encryption Protocol (PEP)"
