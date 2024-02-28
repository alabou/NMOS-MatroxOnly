# Matrox: NMOS With AES3
{:.no_toc}  
Copyright 2024, Matrox Graphics Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
  
---
  
{:toc}

## Introduction

AES3 is a technology for the transmission and multiplexing of digital audio signals, standardized in AES/EBU Tech. 3250-E Third edition [AES/EBU Tech 3250-E][AES3] | IEC 60958.

The Rec. [AES/EBU Tech 3250-E][AES3] | IEC 60958 specification and associated amendments describe the embedding of various media streams in an AES3 transport stream. An RTP payload format specification for AES3 transport stream was developed by SMPTE ST 2110-31 specification for transport over RTP using the payload format `audio/AM824`.

The [Video Services Forum][VSF] developed Technical Recommendation [VSF_TR-10-12][] for the transport of AES3 audio in an AES3 stream over IP.

This specification outlines AES3 streams that are opaque and fully described. An opaque AES3 Flow does not have `parents` Flows as opposed to a fully described Flow describing the `parents` Flows making the AES stream. The former case is useful when an AES3 stream is captured from a baseband signal and is transmitted "as is". The later case is useful when an a DEvice creates an AES3 stream from some sub-streams and that the Device which to expose through IS-04 the characteristics of such sub-streams and allow a user to configure them through IS-11.

## Use of Normative Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY",
and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119][RFC-2119].

## Definitions

The NMOS terms 'Controller', 'Node', 'Source', 'Flow', 'Sender', 'Receiver' are used as defined in the [NMOS Glossary](https://specs.amwa.tv/nmos/main/docs/Glossary.html).

A 'sub-Flow' is defined as a Flow of format `urn:x-nmos:format:audio`, `urn:x-nmos:format:video` or `urn:x-nmos:format:data` which is part of a MPEG2-TS Stream produced by a Sender.

A 'sub-Stream' is defined as a Stream of format `urn:x-nmos:format:audio`, `urn:x-nmos:format:video` or `urn:x-nmos:format:data` which is part of a MPEG2-TS Stream consumed by a Receiver.

## AES3 IS-04 Sources, Flows and Senders

Nodes implementing IS-04 v1.3 or higher, that are capable of transmitting AES3 mux streams and opaque AES3 audio streams, MUST have Source, Flow and Sender resources in the IS-04 Node API.

### Sources

An audio Source resource MUST indicate `urn:x-nmos:format:audio` for the `format` attribute and it MUST be associated with a Flow of the same format through the `source_id` attribute of the audio Flow. A Source of format `urn:x-nmos:format:audio` or `urn:x-nmos:format:data`, associated with a sub-Flow of said Flow, through the `source_id` attribute of the the sub-Flow, MUST be a member of said mux Source's `parents` attribute. The existence of sub-Flows for a AES3 Flow indicate that the AES3 stream is fully described.

In addition to those attributes defined in IS-04 for audio and data Sources, the following attributes defined in the [Source Attributes](https://github.com/alabou/NMOS-MatroxOnly/blob/main/SourceAttributes.md) are used for AES3.

A Source of format `urn:x-nmos:format:audio` or `urn:x-nmos:format:data` having a non-null `urn:x-matrox:receiver_id` attribute where the associated Receiver `format` attribute is `urn:x-nmos:format:mux` MUST have a `urn:x-matrox:layer` attribute indicading the Receiver's sub-Stream providing the media content to the Source.

Examples Source resources are provided in [Examples](../examples/).

### Flows

An AES3 audio Flow resource MUST indicate `audio/AM824` in the `media_type` attribute and `urn:x-nmos:format:audio` for the `format` attribute. An AES3 audio Flow MUST have a `source_id` attribute referencing a Source of the same `format`. A sub-Flow of format `urn:x-nmos:format:audio` or `urn:x-nmos:format:data`, MAY be a member of said audio Flow's `parents` attribute if the AES stream is meant to be fully described. Such audio sub-flows MUST NOT use the `audio/AM824` `media_type`.

In addition to those attributes defined in IS-04 for a coded audio Flow, the following attributes defined in the [Flow Attributes](https://github.com/alabou/NMOS-MatroxOnly/blob/main/FlowAttributes.md) are used for AES3.

A fully described AES3 audio Flow MUST have `urn:x-matrox:audio_layers` and `urn:x-matrox:data_layers` attributes indicating the number of sub-Flows of each `format` making an AES3 stream. An opaque AES3 audio Flow MUST NOT have such attributes. The fully described AES3 Stream MUST NOT have more or less sub-Streams than indicated by those attributes.

A sub-Flow MUST have a `urn:x-matrox:layer` attribute identifying the sub-Flow within all the other sub-Flows of the same `format` making an AES3 stream. An `audio/AM824` Flow MUST NOT have such attribute.

A sub-Flow MUST have a `urn:x-matrox:layer_compatibility_groups` attribute identifying the sub-Flow compatibility with other sub-Flows making an AES3 stream. An `audio/AM824` Flow MUST NOT have such attribute.

Examples Flow resources are provided in [Examples](../examples/).

### Senders

A Sender associated with an `audio/AM824` Flow through the `flow_id` attribute MUST provide Sender's Capabilities for the `audio/AM824` Flow and if fully described for each sub-Flow making an AES3 stream using the Constraint Set `urn:x-matrox-format`, `urn:x-matrox-layer` and `urn:x-matrox-layer_compatibility_groups` attributes values matching the Sender's sub-Flows.

An opaque AES3 Sender MUST omit the Sender's Capabilities for the sub-Streams, indicating that it is unconstrained with respect to the individual sub-Streams making the AES3 stream and that it cannot be constrained as no sub-Flows are exposed.

The Sender MUST express its limitations or preferences regarding the AES3 streams that it supports indicating constraints in accordance with the [Sender Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/SenderCapabilities.md) Sender Capabilities specification. The Sender SHOULD express its constraints as precisely as possible, to allow a Controller to determine with a high level of confidence the Sender's streams and sub-streams capabilities. It is not always practical for the constraints to indicate every type of stream or sub-stream that a Sender can or cannot produce; however, they SHOULD describe as many of its commonly used operating points as practical and any preferences among them.

The `constraint_sets` parameter within the `caps` object MUST be used to describe combinations of parameters which the sender can support, using the parameter constraints defined in the [Capabilities register](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/) of the NMOS Parameter Registers and [Matrox Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md).

The following parameter constraints can be used to express limits or preferences on a fully described AES3 stream:

- [audio_layers](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md#audio_layers)  
  Indicate the minimum and maximum audio layers supported in the AES3 stream. The Sender Capabilities MUST provide Constraint Sets for as many as the maximum number of layers.

- [data_layers](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md#data_layers)  
  Indicate the minimum and maximum data layers supported in the AES3 stream. The Sender Capabilities MUST provide Constraint Sets for as many as the maximum number of layers.

A format specification MAY define additional parameter constraints that can be used to express limits or preferences on the audio and data sub-streams.

A coded format specification MAY define Sender's attributes and associated transport capabilities that, for the corresponding audio or data sub-stream, MUST be assumed as having their default value.

Note: The Sender's attributes and associated transport capabilities of a coded format specification are assumed to exist for each sub-Stream, each having their default values. For example the `parameter_sets_flow_mode` and `parameter_sets_transport_mode` associated with some coded format specification are assumed as having their default value of `dynamic` and `in_band` respectively.

Other existing parameter constraints, such as the following, are also appropriate to express limitations on supported AES3 streams:

- [Media Type](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#media-type)
- [Channel Count](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#channel-count)
- [Sample Rate](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#sample-rate)
- [Packet Time](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#packet-time)
- [Max Packet Time](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#max-packet-time)
- [ST 2110-21 Sender Type](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#st-2110-21-sender-type)

#### RTP transport based on ST 2110-31

For Nodes transmitting AES3 using the RTP payload mapping defined by ST 2110-31, the Sender resource MUST indicate `urn:x-nmos:transport:rtp` or one of its subclassifications for the `transport` attribute.

An example Sender resource is provided in the [Examples](../examples/).

##### SDP format-specific parameters

The SDP file at the `manifest_href` MUST comply with the requirements of ST 2110-31 for the `audio/AM824` stream.

An example SDP file is provided in the [Examples](../examples/).

#### Other transports

For Nodes transmitting AES3 using other transports, the Sender resource MUST indicate the associated `urn:x-nmos:transport:` or `urn:x-matrox:transport:` label of the transport or one of its subclassifications for the `transport` attribute.

The `manifest_href` attribute MAY be `null` if an SDP transport file is not supported by the transport. Otherwise the SDP transport file MUST comply with the transport specific requirements. There is no SDP format-specific parameters requirements for transports other than RTP.

## AES3 IS-04 Receivers

Nodes implementing IS-04 v1.3 or higher that are capable of receiving AES3 streams MUST have Receiver resources in the IS-04 Node API.

A Receiver MUST indicate `urn:x-nmos:format:audio` for the `format` attribute and MUST provide Receiver's Capabilities for the `audio/AM824` Stream and if fully described for each sub-Stream using the Constraint Set `urn:x-matrox-format`, `urn:x-matrox-layer` and `urn:x-matrox-layer_compatibility_groups` attributes values matching the Receiver's sub-Streams.

An opaque AES3 Receiver MUST omit the Receiver's Capabilities for the sub-Streams, indicating that it is unconstrained with respect to the individual sub-Streams making the AES3 stream.

The Receiver MUST express its limitations or preferences regarding the AES3 streams that it supports indicating constraints in accordance with the [Receiver Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/ReceiverCapabilities.md) Receiver Capabilities specification. The Receiver SHOULD express its constraints as precisely as possible, to allow a Controller to determine with a high level of confidence the Receiver's compatibility with the available streams and sub-streams. It is not always practical for the constraints to indicate every type of stream or sub-stream that a Receiver can or cannot consume successfully; however, they SHOULD describe as many of its commonly used operating points as practical and any preferences among them.

The `constraint_sets` parameter within the `caps` object MUST be used to describe combinations of parameters which the receiver can support, using the parameter constraints defined in the [Capabilities register](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/) of the NMOS Parameter Registers and [Matrox Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md).

The following parameter constraints can be used to express limits or preferences on a fully described stream. For a given format, a fully described AES3 stream MUST provide at least the minimum number of layers supported by the Receiver. Sub-Streams that are not mapped to the Receiver's layers are ignored.

- [audio_layers](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md#audio_layers)  
  Indicate the minimum and maximum audio layers supported from the AES3 stream. The Receiver Capabilities MUST provide Constraint Sets for as many as the maximum layers.

- [data_layers](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md#data_layers)  
  Indicate the minimum and maximum data layers supported from the AES3 stream. The Receiver Capabilities MUST provide Constraint Sets for as many as the maximum layers.

A format specification MAY define additional parameter constraints that can be used to express limits or preferences on the audio and data sub-streams.

Other existing parameter constraints, such as the following, are also appropriate to express limitations on supported AES3 streams:

- [Media Type](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#media-type)
- [Channel Count](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#channel-count)
- [Sample Rate](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#sample-rate)
- [Packet Time](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#packet-time)
- [Max Packet Time](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#max-packet-time)
- [ST 2110-21 Sender Type](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#st-2110-21-sender-type)

An example Receiver resource is provided in the [Examples](../examples/).

### RTP transport based on ST 2110-31

For Nodes consuming AES3 using the RTP payload mapping defined by ST 2110-31, the Receiver resource MUST indicate `urn:x-nmos:transport:rtp` or one of its subclassifications for the `transport` attribute and MUST indicate `audio.AM824` as the `media_type`.

### Other transports

For Nodes consuming AES3 using other transports, the Receiver resource MUST indicate the associated `urn:x-nmos:transport:` or or `urn:x-matrox:transport:` label of the transport or one of its subclassifications for the `transport` attribute and MUST indicate `audio.AM824` as the `media_type`.
  
## AES3 IS-05 Senders and Receivers

### RTP transport

Connection Management using IS-05 proceeds in exactly the same manner as for any other stream format carried within RTP.

If IS-04 Sender `manifest_href` is not `null`, the SDP transport file at the **/transportfile** endpoint on an IS-05 Sender MUST comply with the same requirements described for the SDP transport file at the IS-04 Sender `manifest_href`.

A `PATCH` request on the **/staged** endpoint of an IS-05 Receiver can contain an SDP transport file in the `transport_file` attribute. The SDP transport file for a AES3 stream is expected to comply with ST 2110-31. It need not comply with the additional requirements specified for SDP transport files at Senders.

If the Receiver is not capable of consuming the stream described by a `PATCH` on the **/staged** endpoint, it SHOULD reject the request. If it is unable to assess the stream compatibility because some parameters are not included `PATCH` request, it MAY accept the request and postpone stream compatibility assessment.
  
### Other transports

Connection Management using IS-05 proceeds in exactly the same manner as for any other stream format carried within other transports.

If IS-04 Sender `manifest_href` is not `null`, the SDP transport file at the **/transportfile** endpoint on an IS-05 Sender MUST comply with the same requirements described for the SDP transport file at the IS-04 Sender `manifest_href`.

If the Receiver is not capable of consuming the stream described by a `PATCH` on the **/staged** endpoint, it SHOULD reject the request. If it is unable to assess the stream compatibility because some parameters are not included `PATCH` request, it MAY accept the request and postpone stream compatibility assessment.

### Receivers

### Senders

A Sender MAY, unless constrained by IS-11, produce any AES3 coded stream that is compliant with the associated Flow `urn:x-matrox:audio_layers` and `urn:x-matrox:data_layers`.

## AES3 IS-11 Senders and Receivers

### RTP transport

### Other transports

## Controllers

[AES3]: http://tech.ebu.ch/docs/tech/tech3250.pdf "SPECIFICATION OF THE DIGITAL AUDIO INTERFACE (The AES/EBU interface)"
[RFC-2119]: https://tools.ietf.org/html/rfc2119 "Key words for use in RFCs"
[IS-04]: https://specs.amwa.tv/is-04/ "AMWA IS-04 NMOS Discovery and Registration Specification"
[IS-05]: https://specs.amwa.tv/is-05/ "AMWA IS-05 NMOS Device Connection Management Specification"
[NMOS Parameter Registers]: https://specs.amwa.tv/nmos-parameter-registers/ "Common parameter values for AMWA NMOS Specifications"
[VSF]: https://vsf.tv/ "Video Services Forum"
[SMPTE]: https://www.smpte.org/ "Society of Media Professionals, Technologists and Engineers"
[BCP-004-01]: https://specs.amwa.tv/bcp-004-01/ "AMWA BCP-004-01 NMOS Receiver Capabilities"
[VSF_TR-10-12]: https://vsf.tv/download/technical_recommendations/VSF_TR-10-12_2023-08-30.pdf "Internet Protocol Media Experience (IPMX): AES3 Transparent Transport"
