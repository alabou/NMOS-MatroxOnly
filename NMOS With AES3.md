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

The Rec. [AES/EBU Tech 3250-E][AES3] | IEC 60958 specification and associated amendments describe the embedding of various media streams in an AES3 transport stream. The SMPTE ST 2110-31 specification describes the `audio/AM824` RTP payload format for the transport over RTP of AES3 transport streams. The SMPTE specification [ST 302M][] describes the embedding of AES3 transport streams into an MPEG2-TS stream. The SMPTE specification [ST 337][] describes the embedding of compressed digital audio in an AES3 transport stream.

The [Video Services Forum][VSF] developed Technical Recommendation [VSF_TR-10-12][] for the transport of AES3 audio in an AES3 stream over IP.

This specification outlines AES3 transport streams that are either opaque or fully described. An opaque `audio/AM824` Flow does not have `parents` Flows as opposed to a fully described one that describe the `parents` Flows making the `audio/AM824` Flow. For the opaque case, the Flow's `format` is `urn:x-nmos:format:audio` and for the fully descvribed case the Flow's `format` is `urn:x-nmos:format:mux`.

## Use of Normative Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY",
and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119][RFC-2119].

## Definitions

The NMOS terms 'Controller', 'Node', 'Source', 'Flow', 'Sender', 'Receiver' are used as defined in the [NMOS Glossary](https://specs.amwa.tv/nmos/main/docs/Glossary.html).

A 'sub-Flow' is defined as a Flow of format `urn:x-nmos:format:audio` or `urn:x-nmos:format:data` which is part of a AM824 Stream produced by a Sender.

A 'sub-Stream' is defined as a Stream of format `urn:x-nmos:format:audio` or `urn:x-nmos:format:data` which is part of a AM824 Stream consumed by a Receiver.

## AES3 Stream / AM824 Stream

An AES3 Stream MUST be compliant with the standard implementation of the channel status as per section 7.2.2 of [AES3][] and only byte 0, 1, 2 and 23 MAY have a non-zero value. The AES3 Stream MUST be compliant with [AES/EBU Tech 3250-E][AES3] for the base functionality and PCM audio. Additionally it MUST be compliant with [ST 337] for non-PCM coded audio and data. As per ST 2110-31 or [ST 302M][] many such AES3 Streams can be multiplexed together into an RTP or MPEG2-TS stream. The `channel mode` field of byte 1 of the the channel status SHOULD be one of `mode not indicated`, `two-channel mode` or `stereophonic mode`.

An AM824 Flow/Stream MUST have an associated `audio/AM824` media type and MAY comprise of a number of AES3 Streams. An opaque AM824 Flow/Stream does not provide information about the embedded AES3 Streams other than their count and common sample rate. A fully described AM824 Flow/Stream provides information about each embedded AES3 Stream in addition to their count and common sample rate.

Note: This definition of an an AES Stream applies in the context of ST 2110-31 or [ST 302M][]. An AES/EBU digital audio interface MAY support enhanced functionality. It is expected that a conversion from/to the AES/EBU digital audio interface to/from an AM824 Flow/Stream will be performed when enhanced functionality is used/required on the AES/EBU digital audio interface.

## AES3 IS-04 Sources, Flows and Senders

Nodes implementing IS-04 v1.3 or higher, that are capable of transmitting opaque and fully described AM824 Flows, MUST have Source, Flow and Sender resources in the IS-04 Node API.

### Sources

A Source resource associated with an opaque AM824 Flow MUST indicate `urn:x-nmos:format:audio` for the `format` attribute and it MUST be associated with a Flow of the same format through the `source_id` attribute of the Flow. 

A Source resource associated with a fully described AM824 Flow MUST indicate `urn:x-nmos:format:mux` for the `format` attribute and it MUST be associated with a Flow of the same format through the `source_id` attribute of the Flow. 

A Source of format `urn:x-nmos:format:audio` or `urn:x-nmos:format:data`, associated with a sub-Flow of said fully described AM824 Flow, through the `source_id` attribute of the  sub-Flow, MUST be a member of said fully described AM824 Flow associated Source `parents` attribute. The existence of sub-Flows for an AM824 Flow indicate that the it is fully described.

In addition to those attributes defined in IS-04 for audio and data Sources, the following attributes defined in the [Source Attributes](https://github.com/alabou/NMOS-MatroxOnly/blob/main/SourceAttributes.md) are used for AM824 Flows.

A Source of format `urn:x-nmos:format:audio` or `urn:x-nmos:format:data` having a non-null `urn:x-matrox:receiver_id` attribute where the associated Receiver `format` attribute is `urn:x-nmos:format:mux` MUST have a `urn:x-matrox:layer` attribute indicading the Receiver's sub-Stream providing the media content to the Source.

Examples Source resources are provided in [Examples](../examples/).

### Flows

An opaque AM824 Flow resource MUST indicate `audio/AM824` in the `media_type` attribute and `urn:x-nmos:format:audio` for the `format` attribute. An AM824 Flow MUST have a `source_id` attribute referencing a Source of the same `format`.

A fully described AM824 Flow resource MUST indicate `audio/AM824` in the `media_type` attribute and `urn:x-nmos:format:mux` for the `format` attribute. An AM824 Flow MUST have a `source_id` attribute referencing a Source of the same `format`. A sub-Flow of format `urn:x-nmos:format:audio` or `urn:x-nmos:format:data` MUST be a member of said fully described AM824 Flow's `parents` attribute. Such audio sub-flows MUST NOT use the `audio/AM824` media type.

In addition to those attributes defined in IS-04 for a coded audio Flow, the following attributes defined in the [Flow Attributes](https://github.com/alabou/NMOS-MatroxOnly/blob/main/FlowAttributes.md) are used for AM824 Flows.

A fully described AM824 Flow MUST have `urn:x-matrox:audio_layers` and `urn:x-matrox:data_layers` attributes indicating the number of sub-Flows of each `format` making an AM824 Stream. An opaque AM824 Flow MUST NOT have such attributes. The fully described AM824 Stream MUST NOT have more or less sub-Streams than indicated by those attributes.

A sub-Flow MUST have a `urn:x-matrox:layer` attribute identifying the sub-Flow within all the other sub-Flows of the same `format` making an AM824 Stream. An AM824 Flow MUST NOT have such attribute.

A sub-Flow MUST have a `urn:x-matrox:layer_compatibility_groups` attribute identifying the sub-Flow compatibility with other sub-Flows making an AM824 Stream. An AM824 Flow MUST NOT have such attribute.

Examples Flow resources are provided in [Examples](../examples/).

### Senders

A Sender associated with an AM824 Flow through the `flow_id` attribute MUST provide Sender's Capabilities for the AM824 Stream and if fully described for each sub-Flow making an AM824 Stream using the Constraint Set `urn:x-matrox-format`, `urn:x-matrox-layer` and `urn:x-matrox-layer_compatibility_groups` attributes values matching the Sender's sub-Flows.

An opaque AM824 Sender MUST omit the Sender's Capabilities for the sub-Streams, indicating that it is unconstrained with respect to the individual sub-Streams making the AM824 Stream and that sub-Flows cannot be constrained as they are not exposed.

The Sender MUST express its limitations or preferences regarding the AM824 Streams that it supports indicating constraints in accordance with the [Sender Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/SenderCapabilities.md) Sender Capabilities specification. The Sender SHOULD express its constraints as precisely as possible, to allow a Controller to determine with a high level of confidence the Sender's streams and sub-streams capabilities. It is not always practical for the constraints to indicate every type of stream or sub-stream that a Sender can or cannot produce; however, they SHOULD describe as many of its commonly used operating points as practical and any preferences among them.

The `constraint_sets` parameter within the `caps` object MUST be used to describe combinations of parameters which the sender can support, using the parameter constraints defined in the [Capabilities register](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/) of the NMOS Parameter Registers and [Matrox Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md).

The following parameter constraints can be used to express limits or preferences for a fully described AM824 Stream:

- [audio_layers](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md#audio_layers)  
  Indicate the minimum and maximum audio layers supported in the AM824 Stream. The Sender Capabilities MUST provide Constraint Sets for as many as the maximum number of layers.

- [data_layers](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md#data_layers)  
  Indicate the minimum and maximum data layers supported in the AM834 Stream. The Sender Capabilities MUST provide Constraint Sets for as many as the maximum number of layers.

- [Sample Rate](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#sample-rate)

- [Media Type](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#media-type)

A format specification MAY define additional parameter constraints that can be used to express limits or preferences on the audio and data sub-streams.

A coded format specification MAY define Sender's attributes and associated transport capabilities that, for the corresponding audio or data sub-stream, MUST be assumed as having their default value.

Note: The Sender's attributes and associated transport capabilities of a coded format specification are assumed to exist for each sub-Stream, each having their default values. For example the `parameter_sets_flow_mode` and `parameter_sets_transport_mode` associated with some coded format specification are assumed as having their default value of `dynamic` and `in_band` respectively.

Other existing parameter constraints, such as the following, are also appropriate to express limitations for supported opaque AM824 Streams:

- [Media Type](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#media-type)
- [Channel Count](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#channel-count)
- [Channel Order](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md#channel_order)  
    When both `channel_order` and `channel_count` capabilities are declared, they MUST enumerate the same number of elements where element i of the `channel_count` array indicates the number of channels for all the groups of the `channel_order` element i.
- [Sample Rate](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#sample-rate)
- [Packet Time](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#packet-time)
- [Max Packet Time](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#max-packet-time)
- [ST 2110-21 Sender Type](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#st-2110-21-sender-type)

#### RTP transport based on ST 2110-31

For Nodes transmitting AM824 Streams using the RTP payload mapping defined by ST 2110-31, the Sender resource MUST indicate `urn:x-nmos:transport:rtp` or one of its subclassifications for the `transport` attribute.

An example Sender resource is provided in the [Examples](../examples/).

##### SDP format-specific parameters

The SDP file at the `manifest_href` MUST comply with the requirements of ST 2110-31 for the AM824 Stream.

###### channel-order

The SDP transport file associated with an AM824 Stream MUST have `channel-order` parameter to indicate the grouping of channels in AM824 Stream. The `channel-order` parameter MUST use the ST 2110-30 channel grouping symbols for linear PCM AES3 Streamsand the ST 2110-31 channel grouping symbol `AES3` for non-linear AES Streams. Such layout MUST indicate the number of audio layers multiplexed in the AM824 Stream. This requirement applies to both opaque and fully described AM824 Streams.

An example SDP file is provided in the [Examples](../examples/).

#### Other transports

For Nodes transmitting AM824 Streams using other transports, the Sender resource MUST indicate the associated `urn:x-nmos:transport:` or `urn:x-matrox:transport:` label of the transport or one of its subclassifications for the `transport` attribute.

The `manifest_href` attribute MAY be `null` if an SDP transport file is not supported by the transport. Otherwise the SDP transport file MUST comply with the transport specific requirements. There is no SDP format-specific parameters requirements for transports other than RTP.

## AES3 IS-04 Receivers

Nodes implementing IS-04 v1.3 or higher that are capable of receiving AM824 Streams MUST have Receiver resources in the IS-04 Node API.

An opaque AM824 Receiver MUST indicate `urn:x-nmos:format:audio` for the `format` attribute and MUST provide Receiver's Capabilities for the `audio/AM824` Stream. An opaque AM824 Receiver MUST omit the Receiver's Capabilities for the sub-Streams, indicating that it is unconstrained with respect to the individual sub-Streams making the AM824 Stream.

A fully described AM824 Receiver MUST indicate `urn:x-nmos:format:mux` for the `format` attribute and MUST provide Receiver's Capabilities for the `audio/AM824` Stream and for each sub-Stream using the Constraint Set `urn:x-matrox-format`, `urn:x-matrox-layer` and `urn:x-matrox-layer_compatibility_groups` attributes values matching the Receiver's sub-Streams.

The Receiver MUST express its limitations or preferences regarding the AM824 Streams that it supports indicating constraints in accordance with the [Receiver Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/ReceiverCapabilities.md) Receiver Capabilities specification. The Receiver SHOULD express its constraints as precisely as possible, to allow a Controller to determine with a high level of confidence the Receiver's compatibility with the available streams and sub-streams. It is not always practical for the constraints to indicate every type of stream or sub-stream that a Receiver can or cannot consume successfully; however, they SHOULD describe as many of its commonly used operating points as practical and any preferences among them.

The `constraint_sets` parameter within the `caps` object MUST be used to describe combinations of parameters which the receiver can support, using the parameter constraints defined in the [Capabilities register](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/) of the NMOS Parameter Registers and [Matrox Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md).

The following parameter constraints can be used to express limits or preferences on a fully described stream. For a given format, a fully described AM824 Stream MUST provide at least the minimum number of layers supported by the Receiver. Sub-Streams that are not mapped to the Receiver's layers are ignored.

- [audio_layers](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md#audio_layers)  
  Indicate the minimum and maximum audio layers supported from the AM824 Stream. The Receiver Capabilities MUST provide Constraint Sets for as many as the maximum layers.

- [data_layers](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md#data_layers)  
  Indicate the minimum and maximum data layers supported from the AM824 Stream. The Receiver Capabilities MUST provide Constraint Sets for as many as the maximum layers.

- [Sample Rate](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#sample-rate)

- [Media Type](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#media-type)

A format specification MAY define additional parameter constraints that can be used to express limits or preferences on the audio and data sub-streams.

Other existing parameter constraints, such as the following, are also appropriate to express limitations on supported opaque AM824 Streams:

- [Media Type](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#media-type)
- [Channel Count](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#channel-count)
- [Channel Order](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md#channel_order)  
    When both `channel_order` and `channel_count` capabilities are declared, they MUST enumerate the same number of elements where element i of the `channel_count` array indicates the number of channels for all the groups of the `channel_order` element i.
- [Sample Rate](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#sample-rate)
- [Packet Time](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#packet-time)
- [Max Packet Time](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#max-packet-time)
- [ST 2110-21 Sender Type](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#st-2110-21-sender-type)

A Receiver MUST be able to consume compliant AES3 Streams.

An example Receiver resource is provided in the [Examples](../examples/).

### RTP transport based on ST 2110-31

For Nodes consuming AM824 Streams using the RTP payload mapping defined by ST 2110-31, the Receiver resource MUST indicate `urn:x-nmos:transport:rtp` or one of its subclassifications for the `transport` attribute and MUST indicate `audio/AM824` as the `media_type`.

### Other transports

For Nodes consuming AM824 Streams using other transports, the Receiver resource MUST indicate the associated `urn:x-nmos:transport:` or or `urn:x-matrox:transport:` label of the transport or one of its subclassifications for the `transport` attribute and MUST indicate `audio/AM824` as the `media_type`.
  
## AES3 IS-05 Senders and Receivers

### RTP transport

Connection Management using IS-05 proceeds in exactly the same manner as for any other stream format carried within RTP.

If IS-04 Sender `manifest_href` is not `null`, the SDP transport file at the **/transportfile** endpoint on an IS-05 Sender MUST comply with the same requirements described for the SDP transport file at the IS-04 Sender `manifest_href`.

A `PATCH` request on the **/staged** endpoint of an IS-05 Receiver can contain an SDP transport file in the `transport_file` attribute. The SDP transport file for a AM824 Stream is expected to comply with ST 2110-31. It need not comply with the additional requirements specified for SDP transport files at Senders.

If the Receiver is not capable of consuming the stream described by a `PATCH` on the **/staged** endpoint, it SHOULD reject the request. If it is unable to assess the stream compatibility because some parameters are not included `PATCH` request, it MAY accept the request and postpone stream compatibility assessment.
  
### Other transports

Connection Management using IS-05 proceeds in exactly the same manner as for any other stream format carried within other transports.

If IS-04 Sender `manifest_href` is not `null`, the SDP transport file at the **/transportfile** endpoint on an IS-05 Sender MUST comply with the same requirements described for the SDP transport file at the IS-04 Sender `manifest_href`.

If the Receiver is not capable of consuming the stream described by a `PATCH` on the **/staged** endpoint, it SHOULD reject the request. If it is unable to assess the stream compatibility because some parameters are not included `PATCH` request, it MAY accept the request and postpone stream compatibility assessment.

### Receivers

### Senders

A Sender MAY, unless constrained by IS-11, produce any AM824 Stream that is compliant with the associated Flow `urn:x-matrox:audio_layers` and `urn:x-matrox:data_layers`.

## AES3 IS-11 Senders and Receivers

### RTP transport

### Other transports

## Controllers
A Sender exposes either an opaque AM824 Stream (audio format) or an fully described one (mux format). Similarly a Receiver exposes either an opaque AM824 Stream (audio format) or an fully described one (mux format). 

A Controller SHOULD allow opaque and fully described AM824 Streams to interoperate, converting Receiver capabilities to ones corresponding to the `format` of the Sender before verifying compatibility.

### AM824 fully described Receiver with an opaque Sender
A Controller attempting to connect a fully described AM824 Receiver to an opaque AM824 Sender MUST consider the Receiver as being of `format` `urn:x-nmos:format:audio` and construct new capabilities for such Receiver with a `media_types` attribute having `audio/AM824` as the only member and the following capabilities if they exist for the actual mux Receiver capabilities:

  - NewAudioConstraintSet."urn:x-nmos:cap:meta:enabled" = CurrentMuxConstraintSet."urn:x-nmos:cap:meta:enabled"  
  - NewAudioConstraintSet."urn:x-nmos:cap:meta:preference" = CurrentMuxConstraintSet."urn:x-nmos:cap:meta:preference"  
  - NewAudioConstraintSet."urn:x-nmos:cap:meta:label" = CurrentMuxConstraintSet."urn:x-nmos:cap:meta:label"  
  - NewAudioConstraintSet."urn:x-nmos:cap:format:media_type" = `audio/AM824`  
  - NewAudioConstraintSet."urn:x-nmos:cap:format:sample_rate" = 48 KHz  
  - NewAudioConstraintSet."urn:x-matrox:cap:transport:hkep" = CurrentMuxConstraintSet."urn:x-matrox:cap:transport:hkep" *if defined*  
  - NewAudioConstraintSet."urn:x-matrox:cap:transport:privacy" = CurrentMuxConstraintSet."urn:x-matrox:cap:transport:privacy" *if defined*  
    
The mux capabilities (constraint sets) of the fully described AM824 audio Receiver are retrieved and converted to audio capabilities of an opaque AM824 Receiver before checking compliance with the opaque Sender. The Controller SHOULD use the `channel-order` parameter of the SDP transport file to verify the compliance of the Sender with the Receiver `audio_layers` capability. A Receiver MUST verify that the `channel-order` parameter of the SDP transport file complies with its `audio_layers` capability.

### AM824 opaque Receiver with a fully described Sender
A Controller attempting to connect an opaque AM824 Receiver to a fully described AM824 Sender MUST consider the Receiver as being of `format` `urn:x-nmos:format:mux` and construct new capabilities for such Receiver with a `media_types` attribute having `audio/AM824` as the only member and the following capabilities if they exist for the actual audio Receiver capabilities:

  - NewMuxConstraintSet."urn:x-nmos:cap:meta:enabled" = CurrentAudioConstraintSet."urn:x-nmos:cap:meta:enabled"  
  - NewMuxConstraintSet."urn:x-nmos:cap:meta:preference" = CurrentAudioConstraintSet."urn:x-nmos:cap:meta:preference"  
  - NewMuxConstraintSet."urn:x-nmos:cap:meta:label" = CurrentAudioConstraintSet."urn:x-nmos:cap:meta:label"  
  - NewMuxConstraintSet."urn:x-nmos:cap:format:media_type" = `audio/AM824`  
  - NewMuxConstraintSet."urn:x-matrox:cap:format:audio_layers" = 1 to MAX groups in CurrentAudioConstraintSet."urn:x-matrox:cap:transport:channel_order" elements  
  - NewMuxConstraintSet."urn:x-matrox:cap:transport:hkep" = CurrentAudioConstraintSet."urn:x-matrox:cap:transport:hkep" *if defined*  
  - NewMuxConstraintSet."urn:x-matrox:cap:transport:privacy" = CurrentAudioConstraintSet."urn:x-matrox:cap:transport:privacy" *if defined*  

  For layer = 0 to layer smaller than MAX groups of CurrentAudioConstraintSet."urn:x-nmos:cap:format:channel_order" elements:  
    - SubStreamConstraintSet."urn:x-nmos:cap:meta:enabled" = true  
    - SubStreamConstraintSet."urn:x-nmos:cap:meta:preference" = CurrentAudioConstraintSet."urn:x-nmos:cap:meta:preference"  
    - SubStreamConstraintSet."urn:x-nmos:cap:meta:format" = "urn:x-nmos:format:audio"  
    - SubStreamConstraintSet."urn:x-nmos:cap:meta:layer" = layer  
    - SubStreamConstraintSet."urn:x-nmos:cap:format:sample_rate" = 48 KHz  

The audio capabilities (constraint sets) of the opaque AM824 audio Receiver are retrieved and converted to mux capabilities of a fully described AM824 Receiver being unconstrained at the sub-streams level except for the `sample_rate`, before checking compliance with the fully described Sender. The Controller SHOULD use the `channel-order` parameter of the SDP transport file to verify the compliance of the Sender with the Receiver `channel_order` capability. A Receiver MUST verify that the `channel-order` parameter of the SDP transport file complies its `channel_order` capability.

[AES3]: http://tech.ebu.ch/docs/tech/tech3250.pdf "SPECIFICATION OF THE DIGITAL AUDIO INTERFACE (The AES/EBU interface)"
[RFC-2119]: https://tools.ietf.org/html/rfc2119 "Key words for use in RFCs"
[IS-04]: https://specs.amwa.tv/is-04/ "AMWA IS-04 NMOS Discovery and Registration Specification"
[IS-05]: https://specs.amwa.tv/is-05/ "AMWA IS-05 NMOS Device Connection Management Specification"
[NMOS Parameter Registers]: https://specs.amwa.tv/nmos-parameter-registers/ "Common parameter values for AMWA NMOS Specifications"
[VSF]: https://vsf.tv/ "Video Services Forum"
[SMPTE]: https://www.smpte.org/ "Society of Media Professionals, Technologists and Engineers"
[BCP-004-01]: https://specs.amwa.tv/bcp-004-01/ "AMWA BCP-004-01 NMOS Receiver Capabilities"
[VSF_TR-10-12]: https://vsf.tv/download/technical_recommendations/VSF_TR-10-12_2023-08-30.pdf "Internet Protocol Media Experience (IPMX): AES3 Transparent Transport"
[ST 337]: https://ieeexplore.ieee.org/document/7291671 "ST 337:2015: Format for Non-PCM Audio and Data in an AES3 Serial Digital Audio Interface"
[ST 302M]: https://ieeexplore.ieee.org/document/7291632 "SMPTE 302M: Mapping of AES3 Data into MPEG-2 Transport Stream"
