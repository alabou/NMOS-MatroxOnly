# Matrox: NMOS With IPMX
{:.no_toc}  
Copyright 2024, Matrox Graphics Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
  
---
  
{:toc}

## Introduction

This document presents the various aspects of using IPMX compliant Senders and Receivers in an NMOS environment and complements the IPMX technical recommendations, most specifically the [TR-10-8][] (NMOS Requirements), [TR-10-5][] (HDCP Key Exchange Protocol - HKEP), [TR-10-13][] (Privacy Encryption Protocol - PEP), [TR-10-1][] (System Timing and Definitions) technical recommendations. Some of the aspects presented in this document are not specific to IPMX compliant devices and apply to the larger family of SMPTE ST 2110 compliant devices.

## Use of Normative Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119][RFC-2119].

## Definitions

The NMOS terms 'Controller', 'Node', 'Source', 'Flow', 'Sender', 'Receiver' are used as defined in the [NMOS Glossary](https://specs.amwa.tv/nmos/main/docs/Glossary.html).

## IS-11 Active Constraints

The application of active constraints to `urn:x-nmos:cap:transport:` and  `urn:x-matrox:cap:transport:` capabilities MUST NOT be allowed when the IS-05 `master_enable` active attribute of a Sender is `true`. An IS-11 `PUT` request to the `constraints/active` endpoint MUST return the `Locked` status (423) in that case.

A Sender MAY ignore `urn:x-nmos:cap:transport:` and `urn:x-matrox:cap:transport:` constraints that are not listed as supported in the IS-11 `constraints/supported` endpoint.

## Transport Capabilities

The `urn:x-nmos:cap:transport:` and  `urn:x-matrox:cap:transport:` capabilities MUST NOT be associated with sub-Flows/sub-Streams. For a multiplexed Flow/Stream, the scope of `transport` capabilities is the `mux` Sender/Receiver. For a non-multiplexed Flow/Stream, the scope of `transport` capabilities is the `audio` or `video` or `data` Sender/Receiver.

## Unsupported / Unconstrained Capabilities and Attributes

Receivers and Senders MAY choose not to support certain capabilities and attributes described in this document. Similarly, they MAY indicate that they are unconstrained for specific capabilities outlined herein.

## Common Reference Clock

A Receiver SHOULD provide a `urn:x-matrox:cap:transport:clock_ref_type` capability to indicate its support for Senders that do not use a common reference clock (PTP). The capability value `ptp` indicates support for a common reference clock (PTP), while the value `internal` indicates support for an internal clock (not PTP).

A Receiver MAY support either or both clock reference types.

A Controller MUST verify the compliance of Receivers with an active Sender using the Sender's SDP transport file to check for the `a=ts-refclk` attribute or using the Sender's associated Source's `clock_name` attribute and checking the `ref_type` attribute of the clock. For a `mux` Source, the parents Sources `clock_name` attribute MUST match with the `mux` Source's `clock_name` attribute.

A Sender MAY provide a `urn:x-matrox:cap:transport:clock_ref_type` capability to indicate the reference clocks that it supports. A Controller MAY use Sender capabilities, if supported, to verify the compliance of Receivers with a Sender and, if necessary, constrain the Sender to ensure compliance with the Receivers. A Sender indicates that it supports being constrained for this capability by enumerating the `urn:x-matrox:cap:transport:clock_ref_type` capability in its [IS-11][] `constraints/supported` endpoint.

The application of a constraint using IS-11 on a Sender's `urn:x-matrox:cap:transport:clock_ref_type` capability, if allowed, MUST NOT change the value of the `clocks` attribute of the associated Node.

A Sender constrained through IS-11 to `ptp` MUST NOT fallback to `internal` if there is not PTP clock available on the network and MUST consider this state as a constraint violation.

> Note: An IPMX unconstrained Sender follows the [TR-10-1][] technical recommendation and uses a `ptp` common reference clock if one is available, otherwise it falls back to using an `internal` reference clock. A non-IPMX unconstrained Sender in a ST 2110 environment follows the SMPTE ST 2110-10 specification and usually uses a `ptp` common reference clock.

## Asynchronous/Synchronous Media

A Receiver SHOULD provide a `urn:x-matrox:cap:transport:synchronous_media` capability to indicate its support for Senders that produce media that is not synchronous with the Sender's reference clock. The capability value `true` indicates support for synchronous media, while the value `false` indicates support for asynchronous media.

A Receiver MAY support either or both media types.

A Controller MUST verify the compliance of Receivers with an active Sender using the Sender's SDP transport file to check for the `a=mediaclk` attribute or by checking the Sender's associated Source's `urn:x-matrox:synchronous_media` attribute, if any. For a `mux` Source, the parents Sources `urn:x-matrox:synchronous_media` attribute MUST match with the `mux` Source's `urn:x-matrox:synchronous_media` attribute.

> Note: The SDP transport file attribute `a=mediaclk:sender` indicates an asynchronous media while `a=mediaclk:direct` indicates a synchronous one.

A Sender MAY provide a `urn:x-matrox:cap:transport:synchronous_media` capability to indicate the media synchronization that it supports. A Controller MAY use a Sender's `urn:x-matrox:cap:transport:synchronous_media` capability to verify the compliance of Receivers with a Sender and, if necessary, constrain the Sender to ensure compliance with the Receivers. A Sender indicates that it supports being constrained for this capability by enumerating the `urn:x-matrox:cap:transport:synchronous_media` capability in its [IS-11][] `constraints/supported` endpoint.

A Sender producing media that is synchronous with the Sender's reference clock MUST include an `urn:x-matrox:synchronous_media` attribute in its associated Source. A Sender producing media that is not synchronous with the Sender's reference clock MAY omit this attribute, which defaults to false.

## Info Block

A Receiver SHOULD provide a `urn:x-matrox:cap:transport:info_block` capability to indicate its support for IPMX Senders transmitting media info blocks (in RTCP Sender Report). The capability SHOULD enumerate the media info block types (integers) supported by the Receiver. An empty enumeration indicates that the Receiver does not support IPMX in-band media info blocks. Enumerating the value `0`, which is an invalid media info block type identifier, serves the same purpose.

A Receiver MAY support none, some, or all IPMX media info block types.

When media stream attributes associated with a Sender change, a Controller MAY allow the Receiver to handle these media stream attribute changes using the media info blocks produced by the Sender, provided that all the media info block types generated by the Sender are supported by the Receiver.

A Sender compliant with the "Info Block" section of this document MUST provide a `urn:x-matrox:info_block` Sender attribute to indicate the media info block types that it produces. This attribute MUST be a subset of the Sender's `urn:x-matrox:cap:transport:info_block` capability.

> Note: A Sender not providing the `urn:x-matrox:info_block` attribute is either not supporting IPMX media info blocks or declare itself as not being compatible with the "Info Block" section of this document.

A Sender SHOULD provide a `urn:x-matrox:cap:transport:info_block` capability to indicate the media info block types that it generates. A Controller MAY use a Sender's `urn:x-matrox:cap:transport:info_block` capability or the Sender's associated `urn:x-matrox:info_block` attribute to verify the compliance of Receivers with a Sender. It is not allowed to constrain a Sender for this capability, as media info blocks are a required feature of IPMX.

> Note: The "Media Info Block Type" section in [TR-10-0][] presents the various IPMX media info block types.

> Note: The info block types produced by a Sender and consumed by Receivers indicate the IPMX technical recommendations that establish the compliance of the associated stream.

The `info_block` attribute and capability describe the RTCP stream produced by an IPMX Sender. A Sender that either does not produce media info blocks (non-IPMX) or produces media info blocks (IPMX) that are not supported by a Receiver MUST NOT prevent a Controller from connecting such a Receiver to the Sender. Such non-compliance only affects the Receiver's ability to adapt autonomously to dynamic changes in stream parameters, requiring intervention by the Controller instead.

## HKEP

A Receiver SHOULD provide a `urn:x-matrox:cap:transport:hkep` capability to indicate its support for Senders that use HDCP encryption and the HKEP protocol. A capability value of `true` indicates support for HDCP encryption and the HKEP protocol, while a value of `false` indicates that they are not supported.

A Receiver MAY support either or both `true` and `false` values.

A Controller MUST verify the compliance of Receivers with an active Sender using HDCP encryption and the HKEP protocol by referring to the Sender's SDP transport file `hkep` attribute or by checking the Sender's associated `urn:x-matrox:hkep` attribute. The presence of the `hkep` attribute in an SDP transport file or a value of `true` for the associated `urn:x-matrox:hkep` Sender attribute indicates that the stream is HDCP-protected. Only Receivers supporting HDCP encryption and the HKEP protocol MAY consume such streams.

A Sender compliant with the [HKEP](#hkep) section of this document MUST provide a `urn:x-matrox:hkep` Sender attribute to indicate that HDCP encryption and the HKEP protocol are used by the Sender. This attribute MUST be `true` if an `hkep` attribute is present in the Sender's SDP transport file, and MUST be `false` if no `hkep` attributes are present. If an SDP transport file is not currently available because the Sender is inactive, this attribute indicates whether or not such an SDP transport file would contain an `hkep` attribute if the Sender were active at that time.

> Note: A Sender not providing the `urn:x-matrox:hkep` attribute is either not supporting HDCP encryption and the HKEP protocol or declares itself as not being compatible with the [HKEP](#hkep) section of this document.

A Sender MAY provide a `urn:x-matrox:cap:transport:hkep` capability to indicate that HDCP encryption and the HKEP protocol are supported. A Sender MAY support either or both `true` and `false` values. A Controller MAY use a Sender's `urn:x-matrox:cap:transport:hkep` capability to verify Receiver compliance with the Sender and, if necessary, constrain the Sender to ensure compliance with the Receivers. A Sender constrained to `false` for this capability MUST NOT be part of an HDCP topology and MUST NOT access, produce, or stream HDCP-protected content. A Sender indicates its support for being constrained for this capability by enumerating the `urn:x-matrox:cap:transport:hkep` capability in its [IS-11][] `constraints/supported` endpoint (Matrox products usually do not support being constrained).

> Note: A Sender indicating both `true` and `false` values in its capabilities describes that it may produce both HDCP and non-HDCP streams according to some internal criteria evaluated at activation time.

> Note: HKEP is only available for RTP based transport protocols, all of which use an SDP transport file.

### SDP Transport File

The `hkep` attribute defined in [TR-10-5][] is not yet registered with IANA. If it were, the definition would indicate "Usage Level: session, media" meaning that a session-level `hkep` attribute represents the default value for a media-level `hkep` attribute if the latter is not specified. The SDP transport file may therefore provide `hkep` information either at the session level and/or the media level.

In the HKEP specification, the use of the expression "hkep session attribute" does not define the usage level of the `hkep` attribute but simply refers to it at its most generic level, which is the session level.

### Activation

A Controller MAY activate a Receiver and configure HDCP encryption and the HKEP protocol using the SDP transport file from a Sender that includes `hkep` attributes. A Controller MUST use an SDP transport file to provide the `hkep` parameters of a stream to the Receiver.
> Note: The `hkep` parameters are only available in an SDP transport file. There is not equivalent transport parameters.

### Consistency

If the `urn:x-matrox:cap:transport:hkep` capability only allows the value `true`, then the Sender's associated SDP transport file MUST have an `hkep` attribute.

If the `urn:x-matrox:cap:transport:hkep` capability only allows the value `false`, then the Sender's associated SDP transport file MUST NOT have an `hkep` attribute.

If the `urn:x-matrox:cap:transport:hkep` capability allows both `true` and `false` values, then the Sender's associated SDP transport file MUST have an `hkep` attribute when the stream is HDCP-protected and MUST NOT have an `hkep` attribute when the stream is not HDCP-protected.

### HDCP Content Protection Notifications
The base notification method is not strictly required but is highly recommended. However, if a device implements notifications through BCP-008-01 or BCP-008-02, it MUST also implement the base notification method.

#### Base notification method
A Sender implementing [IS-11][] and supporting HDCP encryption and the HKEP protocol SHOULD notify that HDCP content protection system prevents the Sender from accessing or re-transmitting HDCP content using the IS-11 status objects. A message SHOULD be registered in the `debug` attribute of the IS-11 Sender's `status` object when the `state` of the Sender becomes `no_essence` or in the `debug` attribute of the IS-11 Input's `status` object when the `state` of the Input becomes `no_signal`.

A Receiver implementing [IS-11][] and supporting HDCP encryption and the HKEP protocol SHOULD notify that HDCP content protection system prevents the Receiver from accessing or re-transmitting HDCP content using the IS-11 status objects. A message SHOULD be registered in the `debug` attribute of the IS-11 Receiver's `status` object when the `state` of the Receiver becomes `unknown` or in the `debug` attribute of the IS-11 Output's `status` object when the `state` of the Output becomes `no_signal` or `default_signal`.

#### Additional notification method
A Sender implementing [BCP-008-02][] and supporting HDCP encryption and the HKEP protocol MAY notify that HDCP content protection system prevents the Sender from accessing or re-transmitting HDCP content using the essenceStatus and essenceStatusMessage properties of the Sender's associated NcSenderMonitor. Senders implementing [IS-11][] providing notifications through [BCP-008-02][] MUST also implement the [base notification method](#base-notification-method).

A Receiver implementing [BCP-008-01][] and supporting HDCP encryption and the HKEP protocol MAY notify that HDCP content protection system prevents the Receiver from accessing or re-transmitting HDCP content using the streamStatus and streamStatusMessage properties of the Receiver's associated NcReceiverMonitor. Receivers implementing [IS-11][] providing notifications through [BCP-008-01][] MUST also implement the [base notification method](#base-notification-method).

### RTP Payload Header

Refer to the "Privacy" section "RTP Payload Header" sub-section for the detailed definition of an RTP Payload Header for various audio and video media types. Those definitions MUST be used to determine the parts of the RTP Payload that is HDCP encrypted.

### IS-11

For an Input shared by multiple [IS-11][] Senders that support being constrained for the `urn:x-matrox:cap:transport:hkep` capability to either `true` or `false`, any Senders constrained to `false` MUST cause that Input to become non-HDCP protected. Consequently, any of these Senders  constrained to `true` MUST enter the IS-11 `active_constraints_violation` state, because the essence is no longer HDCP-protected until the `urn:x-matrox:cap:transport:hkep` capability of all relevant Senders is set to `true`.


## Privacy

A Receiver SHOULD provide a `urn:x-matrox:cap:transport:privacy` capability to indicate its support for Senders that use privacy encryption and the PEP protocol. A capability value of `true` indicates support for privacy encryption and the PEP protocol, while a value of `false` indicates that they are not supported. A Receiver implementing privacy encryption and the PEP protocol MUST provide IS-05 `ext_privacy` extended transport parameters and constraints that specify the extent of support for the features defined in [TR-10-13][].

A Receiver MAY support either `true` or `false` values.

> Note: A Sender/Receiver is not allowed by [TR-10-13][] to support both values. The NMOS API is not allowed to change the enabling/disable of privacy encryption.

A Controller MUST verify the compliance of Receivers with an active Sender using privacy encryption and the PEP protocol by referring to the Sender's SDP transport file `privacy` attribute or checking the Sender's associated `urn:x-matrox:privacy` attribute, and verifying the IS-05 active `ext_privacy` extended transport parameters. The presence of a `privacy` attribute in an SDP transport file or the value `true` for the associated `urn:x-matrox:privacy` Sender attribute indicates that the stream is privacy-protected. The presence of the IS-05 active `ext_privacy_protocol` and `ext_privacy_mode` transport parameters with a value that is not `NULL` indicates that the stream is privacy-protected. Only Receivers supporting privacy encryption and the PEP protocol MAY consume such streams.

A Sender compliant with the "Privacy" section of this document MUST provide a `urn:x-matrox:privacy` Sender attribute to indicate that privacy encryption and the PEP protocol are used by the Sender. This attribute MUST be `true` if a `privacy` attribute is present in the Sender's SDP transport file and MUST be `false` if no `privacy` attributes are present. If an SDP transport file is not currently available, because the Sender is inactive, this attribute indicate wether or not such SDP transport file would contain a `privacy` attribute if the Sender was active at this time. If the Sender's transport protocol does not use an SDP transport file, this attribute indicate wether or not privacy encryption and the PEP protocol are used by the Sender.

> Note: A Sender not providing the `urn:x-matrox:privacy` attribute is either not supporting privacy encryption and the PEP protocol or declare itself as not being compatible with the "Privacy" section of this document.

A Sender MAY provide a `urn:x-matrox:cap:transport:privacy` capability to indicate that privacy encryption and the PEP protocol are supported. A Sender MAY support either `true` or `false` values. A Sender implementing privacy encryption and the PEP protocol MUST provide IS-05 `ext_privacy` extended transport parameters and constraints that specify the extent of support for the features defined in [TR-10-13][]. A Controller MAY use a Sender's `urn:x-matrox:cap:transport:privacy` capability and the IS-05 `ext_privacy` transport parameters constraints to verify Receivers compliance with a Sender and if necessary constrain the Sender to make it compliant with the Receivers. It is not allowed to constrain a Sender for the `urn:x-matrox:cap:transport:privacy` capability as privacy encryption is a protection mechanism under the control of the Sender only. However, a Controller MAY select the value of IS-05 `ext_privacy` parameters within the limits of the associated constraints.

> Note: A Sender is configured by an administrator to produce either privacy encrypted streams or non-encrypted streams. The Sender  `urn:x-matrox:cap:transport:privacy` capability indicates the current configuration.

### SDP Transport File

The `privacy` attribute of [TR-10-13][] is not yet registered with IANA. If it would, the definition would indicate "Usage Level: session, media" indicating that a session-level `privacy` attribute represents the default value for a media-level `privacy` attribute that is not specified. The SDP transport file may provide the `privacy` information either at the session-level and media-level.

The PEP specification uses the expression "a privacy session attribute or a number of privacy media attributes" to clearly indicate the "Usage Level: session, media" usage.

### Activation

A Controller MAY activate and configure Senders' and Receivers' privacy encryption parameters through their associated IS-05 transport parameters during activation. A Controller MAY also activate and configure Receivers' privacy encryption parameters using the SDP transport file from a Sender, including the `privacy` attribute. See the "NMOS With Privacy Encryption" document for more details.

### Consistency

If the `urn:x-matrox:cap:transport:privacy` capability only allows the value `true` then the Sender's associated SDP transport file, if any, MUST have a `privacy` attribute and the IS-05 `ext_privacy_protocol` and `ext_privacy_mode` transport parameters MUST have a value that is not `NULL`.

If the `urn:x-matrox:cap:transport:privacy` capability only allows the value `false` then the Sender's associated SDP transport file, if any, MUST NOT have a `privacy` attribute and the IS-05 `ext_privacy_protocol` and `ext_privacy_mode` transport parameters, if present, MUST have a `NULL` value.

The `urn:x-matrox:cap:transport:privacy` capability MUST NOT allow both `true` and `false` values.

### RTP Payload Header

The concept of the RTP Payload Header, as defined in RFC 8088 ("How to Write an RTP Payload Format"), states: "RTP payload formats often need to include metadata relating to the payload data being transported. Such metadata is sent as a payload header, at the start of the payload section of the RTP packet." This concept is important for encryption, as RTP Payload Headers are not encrypted. Here, we define the proper interpretation of the various RTP payload specifications.

#### RFC 4175 (video/raw)
As per [section 4](https://datatracker.ietf.org/doc/html/rfc4175#section-4) the RTP Payload Header is defined as the first 2 + (6 * lines) byte of the RTP Payload. The size of the RTP Payload Header depends on the number of lines or partial lines that are part of the RTP Payload. Those byte MUST NOT be encrypted.

#### RFC 9134 (video/jxsv)
As per [section 4.3](https://datatracker.ietf.org/doc/html/rfc9134#section-4.3) the RTP Payload Header is defined as the first 4 byte of the RTP Payload. Those byte MUST NOT be encrypted.

#### RFC 3640 (audio/mpeg4-generic)
As per [section 3.3.6](https://www.rfc-editor.org/rfc/rfc3640.html#section-3.3.6) and by the requirements of [NMOS With AAC](https://github.com/alabou/NMOS-MatroxOnly/blob/main/NMOS%20With%20AAC.md) that supports only the `hbr` mode, the first bytes of the RTP Payload defined as the AU Header section correspond to the RFC 8088 definition of RTP Payload Header and MUST NOT be encrypted. The RTP Payload Header is then defined as the first 2 + (2 * frames) byte of the RTP Payload. The size of the RTP Payload Header depends on the number of access units (AAC frames) that are part of the RTP Payload.

#### RFC 6416 (audio/MP4A-LATM)
As per [section 6.1](https://datatracker.ietf.org/doc/html/rfc6416#section-6.1) there is no RTP Payload Header defined. The complete RTP Payload MUST be encrypted.

#### RFC 2250 (video/MP2T)
As per [section 2](https://datatracker.ietf.org/doc/html/rfc2250#section-2) there is no RTP Payload Header defined. The complete RTP Payload MUST be encrypted.

#### RFC 6184 (video/H264)
As per [section 5.2](https://datatracker.ietf.org/doc/html/rfc6184#section-5.2) the RTP Payload Header is defined as the first byte of the RTP Payload. This byte MUST NOT be encrypted.

#### RFC 7798 (video/H265)
As per [section 4.2](https://datatracker.ietf.org/doc/html/rfc7798#section-4.2) the RTP Payload Header is defined as the first 2 byte of the RTP Payload. Those byte MUST NOT be encrypted. As PACI carrying RTP packet are not supported as per [NMOS With H.265](https://github.com/alabou/NMOS-MatroxOnly/blob/main/NMOS%20With%20H.265.md) this 2 byte definition applies in all scenarios.

#### RFC 8331 (video/smpte291)
As per [section 2.1](https://datatracker.ietf.org/doc/html/rfc8331#section-2.1) the RTP Payload Header is defined as the first 8 byte of the RTP Payload. Those byte MUST NOT be encrypted.

#### ST 2110-31 (audio/AM824)
As per ST 2110-31 there is no RTP Payload Header defined. The complete RTP Payload MUST be encrypted.

## Channel Order

Receiver SHOULD provide a `urn:x-matrox:cap:transport:channel_order` capability for opaque AM824 multiplexed audio streams and PCM audio streams to indicate its support for the channels characteristics within an ST 2110-30 or ST 2110-31 stream produced by a Sender. The capability MUST follow the ST 2110 `channel-order` convention. The `channel_order` capability allows a Receiver to describe the number of audio sub-streams that it supports and, for each one, the channel configuration and whether it is linear PCM or non-PCM data.

A Controller MAY verify the compliance of Receivers with an active Sender, for opaque AM824 multiplexed audio streams and PCM audio streams, using the Sender's SDP transport file to check for the format-specific `channel-order` parameter.

A Sender MAY provide a `urn:x-matrox:cap:transport:channel_order` capability to indicate the channel ordering that it supports. A Controller MAY use a Sender's `urn:x-matrox:cap:transport:channel_order` capability to verify the compliance of Receivers with a Sender and, if necessary, constrain the Sender to ensure compliance with the Receivers. A Sender indicates that it supports being constrained for this capability by enumerating the `urn:x-matrox:cap:transport:channel_order` capability in its [IS-11][] `constraints/supported` endpoint (Matrox products usually do not support being constrained). A Controller MAY constrain a Sender's `urn:x-nmos:cap:format:channel_count` capability instead of `urn:x-matrox:cap:transport:channel_order`, selecting the required number of channel corresponding to the `channel_order`. A Sender is required as per IS-11 to support being constrained by the `urn:x-nmos:cap:channel_count` capability. If multiple `channel_order` have the same number of channels the Sender MAY select anyone matching the number of channels. A Sender MUST NOT support being constrained on the `urn:x-matrox:cap:transport:channel_order` capability for fully described AM824 multiplexed audio streams. 

> Note: The `urn:x-matrox:cap:transport:channel_order` and `urn:x-nmos:cap:format:channel_count` are competing capabilities expressing/constraining the same entity. It is advised to constrain only one of them and let the other unconstrained.

## Audio layers

A Receiver SHOULD provide a `urn:x-matrox:cap:format:audio_layers` capability for fully described AM824 multiplexed audio streams to indicate its support for the channels characteristics within an ST 2110-31 stream produced by a Sender. The `urn:x-matrox:cap:format:audio_layers` capability allows a Receiver to describe the number of audio sub-streams that it supports. A Receiver SHOULD also provide sub-streams capabilities for each audio layer to indicate what audio sub-streams it supports.

A Controller MUST verify the compliance of Receivers with an active Sender using the Sender's SDP transport file by checking for the format-specific `channel-order` parameter or by checking the Sender's mux Flow `urn:x-matrox:cap:format:audio_layers` attribute and parent sub-Flows attributes.

A Sender MAY provide a `urn:x-matrox:cap:format:audio_layers` capability to indicate the number of audio layers that are supported. A Controller MAY use the Sender's capabilities to verify the compliance of Receivers with a Sender and, if necessary, constrain the Sender to ensure compliance with the Receivers. Only the number of audio layers MAY be constrained. A Sender indicates that it supports being constrained for this capability by enumerating the `urn:x-matrox:cap:format:audio_layers` capability in its [IS-11][] `constraints/supported` endpoint.

A Controller MAY use IS-11 to constrain the Sender's sub-Flows to make them compliant with the Receiver.

[RFC-2119]: https://tools.ietf.org/html/rfc2119 "Key words for use in RFCs"
[IS-04]: https://specs.amwa.tv/is-04/ "AMWA IS-04 NMOS Discovery and Registration Specification"
[IS-05]: https://specs.amwa.tv/is-05/ "AMWA IS-05 NMOS Device Connection Management Specification"
[IS-11]: https://specs.amwa.tv/is-11/ "AMWA IS-11 NMOS Stream Compatibility Management Specification"
[NMOS Parameter Registers]: https://specs.amwa.tv/nmos-parameter-registers/ "Common parameter values for AMWA NMOS Specifications"
[TR-10-0]: https://vsf.tv/download/technical_recommendations/VSF_TR-10-0_2024-02-23.pdf "Document	Organization"
[TR-10-1]: https://vsf.tv/download/technical_recommendations/VSF_TR-10-1_2024-02-23.pdf "System Timing and Definitions"
[TR-10-5]: https://vsf.tv/download/technical_recommendations/VSF_TR-10-5_2024-02-23.pdf "HDCP Key Exchange Protocol - HKEP"
[TR-10-8]: https://vsf.tv/download/technical_recommendations/VSF_TR-10-8_2024-02-23.pdf "NMOS Requirements"
[TR-10-13]: https://vsf.tv/download/technical_recommendations/VSF_TR-10-13_2024-01-19.pdf "Privacy Encryption Protocol - PEP"
[BCP-008-01]: https://specs.amwa.tv/bcp-008-01/ "NMOS Receiver Status"
[BCP-008-02]: https://specs.amwa.tv/bcp-008-02/ "NMOS Sender Status"
