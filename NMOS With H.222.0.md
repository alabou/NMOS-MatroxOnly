# Matrox: NMOS With H.222.0
{:.no_toc}  
Copyright 2023, Matrox Graphics Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
  
---
  
{:toc}

## Introduction

H.222.0 is a transmission multiplexing and synchronization technology standardized in Rec. [ITU-T H.222.0][H.222.0] | ISO/IEC 13818-1.

The Rec. [ITU-T H.222.0][H.222.0] | ISO/IEC 13818-1 specification and associated amendments describe the embedding of various media streams in an MPEG2-TS transport stream. An RTP payload format specification for MPEG2-TS transport stream was developed through the IETF Payloads working group, IETF [RFC 2250][RFC-2250] for transport over RTP and [RFC 3551][RFC-3551] defines the payload format `video/MP2T`. Other normative documents describe the requirements for the streaming of an MPEG2-TS transport stream over other non-RTP transports.

The [Video Services Forum][VSF] developed Technical Recommendation [VSF_TR-07][] for the transport of JPEG-XS video and AES3 audio in an MPEG2-TS stream over IP.

This specification outlines MPEG2-TS transport streams that are either opaque or fully described. An opaque `video/MP2T` Flow does not have parents Flows as opposed to a fully described `application/MP2T` or `application/mp2t` Flow that describe the parents Flows making the `application/MP2T` or `application/mp2t` Flow. For the fully described case the media type uses the type `application` instead of `video` to differentiate it from the opaque case.

Note: In the SDP transport file the media type will always be `video/MP2T` irrespective of the opaque or fully described definition of the Senders/Receivers when using the RTP transport. It will always be `application/mp2t` for other transports using an SDP transport file.

This document presents the fully-described `application/MP2T` or `application/mp2t` cases and allows for the opaque case to use the `video/MP2T` media type. The complete specification of the opaque case is to be defined in another document.

## Use of Normative Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY",
and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119][RFC-2119].

## Definitions

The NMOS terms 'Controller', 'Node', 'Source', 'Flow', 'Sender', 'Receiver' are used as defined in the [NMOS Glossary](https://specs.amwa.tv/nmos/main/docs/Glossary.html).

A 'sub-Flow' is defined as a Flow of format `urn:x-nmos:format:audio`, `urn:x-nmos:format:video` or `urn:x-nmos:format:data` which is part of a MPEG2-TS Stream produced by a Sender.

A 'sub-Stream' is defined as a Stream of format `urn:x-nmos:format:audio`, `urn:x-nmos:format:video` or `urn:x-nmos:format:data` which is part of a MPEG2-TS Stream consumed by a Receiver.

## H.222.0 IS-04 Sources, Flows and Senders

Nodes implementing IS-04 v1.3 or higher, that are capable of transmitting H.222.0 mux streams, MUST have Source, Flow and Sender resources in the IS-04 Node API.

### Sources

A mux Source resource MUST indicate `urn:x-nmos:format:mux` for the `format` attribute and it MUST be associated with a mux Flow of the same `format` through the `source_id` attribute of the mux Flow. A Source of format `urn:x-nmos:format:audio`, `urn:x-nmos:format:video` or `urn:x-nmos:format:data`, associated with a sub-Flow of said Flow, through the `source_id` attribute of the the sub-Flow, MUST be a member of said mux Source's `parents` attribute.

In addition to those attributes defined in IS-04 for audio, video and data Sources, the following attributes defined in the [Source Attributes](https://github.com/alabou/NMOS-MatroxOnly/blob/main/SourceAttributes.md) are used for H.222.0.

A Source of format `urn:x-nmos:format:audio`, `urn:x-nmos:format:video` or `urn:x-nmos:format:data` having a non-null `urn:x-matrox:receiver_id` attribute where the associated Receiver `format` attribute is `urn:x-nmos:format:mux` MUST have a `urn:x-matrox:layer` attribute indicading the Receiver's sub-Stream providing the media content to the Source.

Examples Source resources are provided in [Examples](https://github.com/alabou/NMOS-MatroxOnly/tree/main/examples).

### Flows

A mux Flow resource MUST indicate `application/MP2T` or `application/mp2t` in the `media_type` attribute and `urn:x-nmos:format:mux` for the `format` attribute. A mux Flow MUST have a `source_id` attribute referencing a Source of the same `format`. A sub-Flow of format `urn:x-nmos:format:audio`, `urn:x-nmos:format:video` or `urn:x-nmos:format:data`, MUST be a member of said mux Flow's `parents` attribute.

When a mux Flow is associated with a Sender using the `urn:x-nmos:transport:rtp` transport or one of its subclassifications, the `media_type` MUST be `application/MP2T`. Otherwise for other transports the `media_type` MUST be `application/mp2t`.

In addition to those attributes defined in IS-04 for all mux Flows, the following attributes defined in the [Flow Attributes](https://github.com/alabou/NMOS-MatroxOnly/blob/main/FlowAttributes.md) are used for H.222.0.

A mux Flow MUST have `urn:x-matrox:audio_layers`, `urn:x-matrox:video_layers` and `urn:x-matrox:data_layers` attributes indicating the number of sub-Flows of each `format` making an MPEG2-TS stream. A non-mux Flow MUST NOT have such attributes. The MPEG2-TS Stream MUST NOT have more or less sub-Streams than indicated by those attributes.

A mux Flow SHOULD have a `urn:x-matrox:layer_compatibility_groups` attribute identifying the mux Flow compatibility with the sub-Flows making an MPEG2-TS stream. A mux Flow without a `urn:x-matrox:layer_compatibility_groups` attribute MUST be assumed as being part of all groups. A Flow that is not a sub-Flow or a mux Flow MUST NOT have such attribute.

A sub-Flow MUST have a `urn:x-matrox:layer` attribute identifying the sub-Flow within all the other sub-Flows of the same `format` making an MPEG2-TS stream. A Flow that is not a sub-Flow MUST NOT have such attribute.

A sub-Flow SHOULD have a `urn:x-matrox:layer_compatibility_groups` attribute identifying the sub-Flow compatibility with other sub-Flows making an MPEG2-TS stream. A sub-Flow without a `urn:x-matrox:layer_compatibility_groups` attribute MUST be assumed as being part of all groups. A Flow that is not a sub-Flow or a mux Flow MUST NOT have such attribute.

A sub-Flow of format `urn:x-nmos:format:audio` and of media type `audio/L16`, `audio/L20` or `audio/L24` MUST be embedded in the MPEG2-TS stream as per [ST 302M][]. The sub-Flow MUST have an odd number of channels that will produce (channels/2) linear PCM AES3 streams.

A sub-Flow of format `urn:x-nmos:format:audio` and of media type `audio/AM824` MUST be embedded in the MPEG2-TS stream as per [ST 302M][]. Such sub-Flow MUST be an opaque AM824 Flow as per [NMOS with AES3](https://github.com/alabou/NMOS-MatroxOnly/blob/main/NMOS%20With%20AES3.md). Such sub-Flow MAY contain linear PCM and non-linear data. The sub-Flow MUST have an odd number of channels that will produce (channels/2) AES3 streams.

Note: Linear PCM Flows and opaque AM824 Flows are implicitely embedded in the MPEG2-TS stream as per [ST 302M][]. Coded audio Flows are embedded according to their format as per [H.222.0][]. A fully described AM824 Flow cannot be a sub-Flow of an H.222.0 mux Flow.

Examples Flow resources are provided in [Examples](https://github.com/alabou/NMOS-MatroxOnly/tree/main/examples).

### Senders

A Sender associated with a mux Flow through the `flow_id` attribute MUST provide Sender's Capabilities for the mux Flow and each sub-Flow making an MPEG2-TS stream using the Constraint Set `urn:x-matrox:cap:meta:format`, `urn:x-matrox:cap:meta:layer` and `urn:x-matrox:cap:meta:layer_compatibility_groups` attributes values matching the Sender's sub-Flows.

A mux Sender not exposing the sub-Streams MAY omit the Sender's Capabilities for the sub-Streams, indicating that it is unconstrained with respect to the individual sub-Streams making the MPEG2-TS stream and that it cannot be constrained as no sub-Flows are exposed.

The mux Sender MUST express its limitations or preferences regarding the H.222.0 streams that it supports indicating constraints in accordance with the [Sender Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/SenderCapabilities.md) Sender Capabilities specification. The Sender SHOULD express its constraints as precisely as possible, to allow a Controller to determine with a high level of confidence the Sender's streams and sub-streams capabilities. It is not always practical for the constraints to indicate every type of stream or sub-stream that a Sender can or cannot produce; however, they SHOULD describe as many of its commonly used operating points as practical and any preferences among them.

The `constraint_sets` parameter within the `caps` object MUST be used to describe combinations of parameters which the sender can support, using the parameter constraints defined in the [Capabilities register](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/) of the NMOS Parameter Registers and [Matrox Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md).

The following parameter constraints can be used to express limits or preferences on the mux stream:

- [audio_layers](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md#audio_layers)  
  Indicate the minimum and maximum audio layers supported in the MPEG2-TS stream. The Sender Capabilities MUST provide Constraint Sets for as many as the maximum number of layers.

- [video_layers](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md#video_layers)  
  Indicate the minimum and maximum video layers supported in the MPEG2-TS stream. The Sender Capabilities MUST provide Constraint Sets for as many as the maximum number of layers.

- [data_layers](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md#data_layers)  
  Indicate the minimum and maximum data layers supported in the MPEG2-TS stream. The Sender Capabilities MUST provide Constraint Sets for as many as the maximum number of layers.

A coded format specification MAY define additional parameter constraints that can be used to express limits or preferences on the audio, video and data sub-streams.

A coded format specification MAY define Sender's attributes and associated transport capabilities that, for the corresponding audio, video or data sub-stream, MUST be assumed as having their default value.

Note: The Sender's attributes and associated transport capabilities of a coded format specification are assumed to exist for each sub-Stream, each having their default values. For example the `parameter_sets_flow_mode` and `parameter_sets_transport_mode` associated with some coded format specification are assumed as having their default value of `dynamic` and `in_band` respectively.

#### RTP transport based on RFC 2250 and RFC 3551

For Nodes transmitting H.222.0 using the RTP payload mapping defined by RFC 2250 and RFC 3551, the Sender resource MUST indicate `urn:x-nmos:transport:rtp` or one of its subclassifications for the `transport` attribute.

An example Sender resource is provided in the [Examples](https://github.com/alabou/NMOS-MatroxOnly/tree/main/examples).

##### SDP format-specific parameters

The SDP file at the `manifest_href` MUST comply with the requirements of RFC 2250 and RFC 3551.

An example SDP file is provided in the [Examples](https://github.com/alabou/NMOS-MatroxOnly/tree/main/examples).

#### Other transports

For Nodes transmitting H.222.0 using other transports, the Sender resource MUST indicate the associated `urn:x-nmos:transport:` or `urn:x-matrox:transport:` label of the transport or one of its subclassifications for the `transport` attribute.

The `manifest_href` attribute MAY be `null` if an SDP transport file is not supported by the transport. Otherwise the SDP transport file MUST comply with the transport specific requirements. There is no SDP format-specific parameters requirements for transports other than RTP.

If the [Privacy Encryption Protocol](https://github.com/alabou/NMOS-MatroxOnly/blob/main/NMOS%20With%20Privacy%20Encryption.md) is used to encrypt the MPEG2-TS stream and the transport is UDP, a Sender MUST NOT use the `private_data_byte` bytes of the MPEG2-TS `adaptation_field()` structure, as signaled by `transport_private_data_flag` and `transport_private_data_length`, for other purpose than sending the CTR Full Header and CTR Short Header.

## H.222.0 IS-04 Receivers

Nodes implementing IS-04 v1.3 or higher that are capable of receiving H.222.0 multiplexed streams MUST have Receiver resources in the IS-04 Node API.

A mux Receiver MUST indicate `urn:x-nmos:format:mux` for the `format` attribute and MUST provide Receiver's Capabilities for the mux Stream and each sub-Stream using the Constraint Set `urn:x-matrox:cap:meta:format`, `urn:x-matrox:cap:meta:layer` and `urn:urn:x-matrox:cap:meta:layer_compatibility_groups` attributes values matching the Receiver's sub-Streams.

A mux Receiver not exposing the sub-Streams MAY omit the Receiver's Capabilities for the sub-Streams, indicating that it is unconstrained with respect to the individual sub-Streams making the MPEG2-TS stream.

The mux Receiver MUST express its limitations or preferences regarding the H.222.0 streams that it supports indicating constraints in accordance with the [Receiver Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/ReceiverCapabilities.md) Receiver Capabilities specification. The Receiver SHOULD express its constraints as precisely as possible, to allow a Controller to determine with a high level of confidence the Receiver's compatibility with the available streams and sub-streams. It is not always practical for the constraints to indicate every type of stream or sub-stream that a Receiver can or cannot consume successfully; however, they SHOULD describe as many of its commonly used operating points as practical and any preferences among them.

The `constraint_sets` parameter within the `caps` object MUST be used to describe combinations of parameters which the receiver can support, using the parameter constraints defined in the [Capabilities register](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/) of the NMOS Parameter Registers and [Matrox Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md).

The following parameter constraints can be used to express limits or preferences on the mux stream. For a given format, a mux stream MUST provide at least the minimum number of layers supported by the Receiver. Sub-Streams that are not mapped to the Receiver's layers are ignored.

- [audio_layers](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md#audio_layers)  
  Indicate the minimum and maximum audio layers supported from the MPEG2-TS stream. The Receiver Capabilities MUST provide Constraint Sets for as many as the maximum layers.

- [video_layers](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md#video_layers)  
  Indicate the minimum and maximum video layers supported from the MPEG2-TS stream. The Receiver Capabilities MUST provide Constraint Sets for as many as the maximum layers.

- [data_layers](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md#data_layers)  
  Indicate the minimum and maximum data layers supported from the MPEG2-TS stream. The Receiver Capabilities MUST provide Constraint Sets for as many as the maximum layers.

A coded format specification MAY define additional parameter constraints that can be used to express limits or preferences on the audio, video and data sub-streams.

An example Receiver resource is provided in the [Examples](https://github.com/alabou/NMOS-MatroxOnly/tree/main/examples).

### RTP transport based on RFC 2250 and RFC 3551

For Nodes consuming H.222.0 using the RTP payload mapping defined by RFC 2250 and RFC 3551, the Receiver resource MUST indicate `urn:x-nmos:transport:rtp` or one of its subclassifications for the `transport` attribute and MUST indicate `application/MP2T` as the `media_type`.

Note: A Controller can connect a fully-described MPEG2-TS Receiver to an opaque Sender, matching the Receiver `application/MP2T` media type with the Sender `video/MP2T` media type.

### Other transports

For Nodes consuming H.222.0 using other transports, the Receiver resource MUST indicate the associated `urn:x-nmos:transport:` or or `urn:x-matrox:transport:` label of the transport or one of its subclassifications for the `transport` attribute and MUST indicate `application/mp2t` in the `media_type`.
  
Note: In the SDP transport file the media type will always be `video/MP2T` irrespective of the opaque or fully described definition of the Senders/Receivers when using the RTP transport. It will always be `application/mp2t` for other transports using an SDP transport file. For an RTP based Receiver, the `application/MP2T` media type of the `media_types` and `constraint_sets` capabilities always matches the SDP transport file `video/MP2T` media type. For Receivers using other transports the `application/mp2t` is used in the SDP transport file and the Receiver's capabilities.

## H.222.0 IS-05 Senders and Receivers

### RTP transport

Connection Management using IS-05 proceeds in exactly the same manner as for any other stream format carried within RTP.

If IS-04 Sender `manifest_href` is not `null`, the SDP transport file at the **/transportfile** endpoint on an IS-05 Sender MUST comply with the same requirements described for the SDP transport file at the IS-04 Sender `manifest_href`.

A `PATCH` request on the **/staged** endpoint of an IS-05 Receiver can contain an SDP transport file in the `transport_file` attribute. The SDP transport file for a H.222.0 stream is expected to comply with RFC 2250 and RFC 3551. It need not comply with the additional requirements specified for SDP transport files at Senders.

If the Receiver is not capable of consuming the stream described by a `PATCH` on the **/staged** endpoint, it SHOULD reject the request. If it is unable to assess the stream compatibility because some parameters are not included `PATCH` request, it MAY accept the request and postpone stream compatibility assessment.
  
### Other transports

Connection Management using IS-05 proceeds in exactly the same manner as for any other stream format carried within other transports.

If IS-04 Sender `manifest_href` is not `null`, the SDP transport file at the **/transportfile** endpoint on an IS-05 Sender MUST comply with the same requirements described for the SDP transport file at the IS-04 Sender `manifest_href`.

If the Receiver is not capable of consuming the stream described by a `PATCH` on the **/staged** endpoint, it SHOULD reject the request. If it is unable to assess the stream compatibility because some parameters are not included `PATCH` request, it MAY accept the request and postpone stream compatibility assessment.

### Receivers

### Senders

A Sender MAY, unless constrained by IS-11, produce any H.222.0 coded stream that is compliant with the associated Flow `urn:x-matrox:audio_layers`, `urn:x-matrox:video_layers` and `urn:x-matrox:data_layers`.

### [VSF_TR-07][] compatibility

An MPEG2-TS stream compatible with [VSF_TR-07][] is achieved by multiplexing a JPEG-XS video stream (video/JXSV, VIDEO 0) along with up to 4 audio streams (SMPTE ST 302M embedding, audio/AM824, AUDIO 0-3) and one ancillary data stream (SMPTE ST 2038 embedding, video/smpte291, DATA 0).

## H.222.0 IS-11 Senders and Receivers

### RTP transport

### Other transports

## Controllers

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
[VSF_TR-07]: https://vsf.tv/download/technical_recommendations/VSF_TR-07_2022-04-20.pdf "Transport of JPEG XS Video in MPEG-2 Transport Stream over IP"
[ST 337]: https://ieeexplore.ieee.org/document/7291671 "ST 337:2015: Format for Non-PCM Audio and Data in an AES3 Serial Digital Audio Interface"
[ST 302M]: https://ieeexplore.ieee.org/document/7291632 "SMPTE 302M: Mapping of AES3 Data into MPEG-2 Transport Stream"
[AES3]: http://tech.ebu.ch/docs/tech/tech3250.pdf "SPECIFICATION OF THE DIGITAL AUDIO INTERFACE (The AES/EBU interface)"
