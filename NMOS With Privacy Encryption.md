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
