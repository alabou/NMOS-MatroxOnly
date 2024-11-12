# Matrox: NMOS With NDI
{:.no_toc}  
Copyright 2024, Matrox Graphics Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
  
---
  
{:toc}

## Introduction

NDI (Network Display Interface) is an IP transport and control technology created by Newtek, a division of Vizrt Group. It allows the transport of multiplexed audio, video and data sub-streams over IP. Senders and Receivers using the NDI transport have their `format` attribute set to `urn:x-nmos:format:mux` and their `transport` attribute set to  `urn:x-matrox:transport:ndi`. The `media_type` attribute of an NDI Receiver is `application/ndi`. The `media_type` of a multiplexed Flow connected with an NDI Sender is `application/ndi`.

NDI can be used to transport uncompress raw video and PCM audio sub-streams or H.254/H.265 compressed video and AAC compressed audio sub-streams. It currently transports one  sub-stream of each format but this specification allows for future enhancement with multiple sub-streams of each format.

This specification allows for NDI Receivers to connect to non-NMOS aware active NDI producers and for non-NMOS NDI consumers to connect to active NDI Senders.

## Use of Normative Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY",
and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119][RFC-2119].

## Definitions

The NMOS terms 'Controller', 'Node', 'Source', 'Flow', 'Sender', 'Receiver' are used as defined in the [NMOS Glossary](https://specs.amwa.tv/nmos/main/docs/Glossary.html).

A 'sub-Flow' is defined as a Flow of format `urn:x-nmos:format:audio`, `urn:x-nmos:format:video` or `urn:x-nmos:format:data` which is part of an NDI stream produced by a Sender.

A 'sub-Stream' is defined as a Stream of format `urn:x-nmos:format:audio`, `urn:x-nmos:format:video` or `urn:x-nmos:format:data` which is part of an NDI stream consumed by a Receiver.

A non-NMOS NDI Sender is an NDI sender device that is not an NMOS Node and as such not part of an NMOS system.

A non-NMOS NDI Receiver is an NDI receiver device that is not an NMOS Node and as such not part of an NMOS system.

## NDI IS-04 Sources, Flows and Senders

Nodes implementing IS-04 v1.3 or higher, that are capable of transmitting NDI mux streams, MUST have Source, Flow and Sender resources in the IS-04 Node API.

### Sources

A mux Source resource MUST indicate `urn:x-nmos:format:mux` for the `format` attribute and it MUST be associated with a mux Flow of the same `format` through the `source_id` attribute of the mux Flow. A Source of format `urn:x-nmos:format:audio`, `urn:x-nmos:format:video` or `urn:x-nmos:format:data`, associated with a sub-Flow of said Flow, through the `source_id` attribute of the the sub-Flow, MUST be a member of said mux Source's `parents` attribute.

In addition to those attributes defined in IS-04 for all mux Sources, the following attributes defined in the [Source Attributes](https://github.com/alabou/NMOS-MatroxOnly/blob/main/SourceAttributes.md) are used for NDI.

A Source of format `urn:x-nmos:format:audio`, `urn:x-nmos:format:video` or `urn:x-nmos:format:data` having a non-null `urn:x-matrox:receiver_id` attribute where the associated Receiver `format` attribute is `urn:x-nmos:format:mux` MUST have a `urn:x-matrox:layer` attribute indicading the Receiver's sub-Stream providing the media content to the Source.

Examples Source resources are provided in [Examples](https://github.com/alabou/NMOS-MatroxOnly/tree/main/examples).

### Flows

A mux Flow resource MUST indicate `application/ndi` in the `media_type` attribute and `urn:x-nmos:format:mux` for the `format` attribute. A mux Flow MUST have a `source_id` attribute referencing a Source of the same `format`. A sub-Flow of format `urn:x-nmos:format:audio`, `urn:x-nmos:format:video` or `urn:x-nmos:format:data`, MUST be a member of said mux Flow's `parents` attribute.

In addition to those attributes defined in IS-04 for all mux Flows, the following attributes defined in the [Flow Attributes](https://github.com/alabou/NMOS-MatroxOnly/blob/main/FlowAttributes.md) are used for NDI.

A mux Flow MUST have `urn:x-matrox:audio_layers`, `urn:x-matrox:video_layers` and `urn:x-matrox:data_layers` attributes indicating the number of sub-Flows of each `format` making an NDI stream. A non-mux Flow MUST NOT have such attributes. The NDI Stream MUST NOT have more or less sub-Streams than indicated by those attributes.

A mux Flow SHOULD have a `urn:x-matrox:layer_compatibility_groups` attribute identifying the mux Flow compatibility with the sub-Flows making an NDI stream. A mux Flow without a `urn:x-matrox:layer_compatibility_groups` attribute MUST be assumed as being part of all groups. A Flow that is not a sub-Flow or a mux Flow MUST NOT have such attribute.

A sub-Flow MUST have a `urn:x-matrox:layer` attribute identifying the sub-Flow within all the other sub-Flows of the same `format` making an NDI stream. A Flow that is not a sub-Flow MUST NOT have such attribute.

A sub-Flow SHOULD have a `urn:x-matrox:layer_compatibility_groups` attribute identifying the sub-Flow compatibility with other sub-Flows making an NDI stream. A sub-Flow without a `urn:x-matrox:layer_compatibility_groups` attribute MUST be assumed as being part of all groups. A Flow that is not a sub-Flow or a mux Flow MUST NOT have such attribute.

The sub-Flows of an NDI multiplexed stream SHOULD either all be uncompressed or all be compressed. However, a Sender MAY provide additional flexibility by combining compressed and uncompressed sub-Flows of different media types (e.g., compressed video with uncompressed audio).

#### Uncompressed video and audio

The transport of uncompressed video and audio is referred to as the NDI "native" transport.

A sub-Flow having the `media_type` atribute set to `video/raw` enters and emerges from the NDI transport as `video/raw`, possibly transformed during the transport by an NDI native codec.

A sub-Flow having the `media_type` atribute set to `audio/L16`, `audio/L20` or `audio/L24` enters and emerges from the NDI transport as `audio/L16`, `audio/L20` or `audio/L24`, possibly transformed during the transport by an NDI native codec.

#### Compressed video and audio

The transport of compressed video and audio is referred to as the NDI "advanced" transport.

A sub-Flow having the `media_type` atribute set to `video/H264` or `video/H265` enters and emerges from the NDI transport as `video/H264` or `video/H265` respectively. It is transported as-is by NDI.

A sub-Flow having the `media_type` atribute set to `audio/mpeg4-generic` enters and emerges from the NDI transport as `audio/mpeg4-generic`. It is transported as-is by NDI.

Examples Flow resources are provided in [Examples](https://github.com/alabou/NMOS-MatroxOnly/tree/main/examples).

### Senders

An NDI Sender resource MUST indicate `urn:x-nmos:transport:ndi` or `urn:x-matrox:transport:ndi `for the `transport` attribute.

A Sender associated with a mux Flow through the `flow_id` attribute MUST provide Sender's Capabilities for the mux Flow and each sub-Flow making an NDI stream using the Constraint Set `urn:x-matrox:cap:meta:format`, `urn:x-matrox:cap:meta:layer` and `urn:x-matrox:cap:meta:layer_compatibility_groups` attributes values matching the Sender's sub-Flows.

A mux Sender not exposing the sub-Streams MAY omit the Sender's Capabilities for the sub-Streams, indicating that it is unconstrained with respect to the individual sub-Streams making the NDI stream and that it cannot be constrained as no sub-Flows are exposed.

The mux Sender MUST express its limitations or preferences regarding the NDI streams that it supports indicating constraints in accordance with the [Sender Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/SenderCapabilities.md) Sender Capabilities specification. The Sender SHOULD express its constraints as precisely as possible, to allow a Controller to determine with a high level of confidence the Sender's streams and sub-streams capabilities. It is not always practical for the constraints to indicate every type of stream or sub-stream that a Sender can or cannot produce; however, they SHOULD describe as many of its commonly used operating points as practical and any preferences among them.

The `constraint_sets` parameter within the `caps` object MUST be used to describe combinations of parameters which the sender can support, using the parameter constraints defined in the [Capabilities register](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/) of the NMOS Parameter Registers and [Matrox Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md).

The following parameter constraints can be used to express limits or preferences on the mux stream:

- [audio_layers](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md#audio_layers)  
  Indicate the minimum and maximum audio layers supported in the NDI stream. The Sender Capabilities MUST provide Constraint Sets for as many as the maximum number of layers.

- [video_layers](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md#video_layers)  
  Indicate the minimum and maximum video layers supported in the NDI stream. The Sender Capabilities MUST provide Constraint Sets for as many as the maximum number of layers.

- [data_layers](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md#data_layers)  
  Indicate the minimum and maximum data layers supported in the NDI stream. The Sender Capabilities MUST provide Constraint Sets for as many as the maximum number of layers.

A coded format specification MAY define additional parameter constraints that can be used to express limits or preferences on the audio, video and data sub-streams.

A coded format specification MAY define Sender's attributes and associated transport capabilities that, for the corresponding audio, video or data sub-stream, MUST be assumed as having their default value.

Note: The Sender's attributes and associated transport capabilities of a coded format specification are assumed to exist for each sub-Stream, each having their default values. For example the `parameter_sets_flow_mode` and `parameter_sets_transport_mode` associated with some coded format specification are assumed as having their default value of `dynamic` and `in_band` respectively.

An example Sender resource is provided in the [Examples](https://github.com/alabou/NMOS-MatroxOnly/tree/main/examples).

##### SDP format-specific parameters

The `manifest_href` MUST be null as there is no SDP transport file with NDI.

## NDI IS-04 Receivers

An NDI Receiver resource MUST indicate `urn:x-nmos:transport:ndi` or `urn:x-matrox:transport:ndi` for the `transport` attribute.

Nodes implementing IS-04 v1.3 or higher that are capable of receiving NDI multiplexed streams MUST have Receiver resources in the IS-04 Node API.

A mux Receiver MUST indicate `urn:x-nmos:format:mux` for the `format` attribute and MUST provide Receiver's Capabilities for the mux Stream and each sub-Stream using the Constraint Set `urn:x-matrox:cap:meta:format`, `urn:x-matrox:cap:meta:layer` and `urn:x-matrox:cap:meta:layer_compatibility_groups` attributes values matching the Receiver's sub-Streams.

A mux Receiver not exposing the sub-Streams MAY omit the Receiver's Capabilities for the sub-Streams, indicating that it is unconstrained with respect to the individual sub-Streams making the NDI stream.

The mux Receiver MUST express its limitations or preferences regarding the NDI streams that it supports indicating constraints in accordance with the [Receiver Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/ReceiverCapabilities.md) Receiver Capabilities specification. The Receiver SHOULD express its constraints as precisely as possible, to allow a Controller to determine with a high level of confidence the Receiver's compatibility with the available streams and sub-streams. It is not always practical for the constraints to indicate every type of stream or sub-stream that a Receiver can or cannot consume successfully; however, they SHOULD describe as many of its commonly used operating points as practical and any preferences among them.

The `constraint_sets` parameter within the `caps` object MUST be used to describe combinations of parameters which the receiver can support, using the parameter constraints defined in the [Capabilities register](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/) of the NMOS Parameter Registers and [Matrox Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md).

The following parameter constraints can be used to express limits or preferences on the mux stream. For a given format, a mux stream MUST provide at least the minimum number of layers supported by the Receiver. Sub-Streams that are not mapped to the Receiver's layers are ignored.

- [audio_layers](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md#audio_layers)  
  Indicate the minimum and maximum audio layers supported from the NDI stream. The Receiver Capabilities MUST provide Constraint Sets for as many as the maximum layers.

- [video_layers](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md#video_layers)  
  Indicate the minimum and maximum video layers supported from the NDI stream. The Receiver Capabilities MUST provide Constraint Sets for as many as the maximum layers.

- [data_layers](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md#data_layers)  
  Indicate the minimum and maximum data layers supported from the NDI stream. The Receiver Capabilities MUST provide Constraint Sets for as many as the maximum layers.

A coded format specification MAY define additional parameter constraints that can be used to express limits or preferences on the audio, video and data sub-streams.

An example Receiver resource is provided in the [Examples](https://github.com/alabou/NMOS-MatroxOnly/tree/main/examples).

## NDI IS-05 Senders and Receivers

Connection Management using IS-05 proceeds in exactly the same manner as for any other transports, using the NDI specific transport parameters defined in [NDI Sender transport parameters](https://github.com/alabou/NMOS-MatroxOnly/blob/main/schemas/sender_transport_params_ndi.json) and [NDI Receiver transport parameters](https://github.com/alabou/NMOS-MatroxOnly/blob/main/schemas/receiver_transport_params_ndi.json). Because of the one Sender to N Receivers relationship of the NDI transport the `receiver_id` attribute of the NDI Sender's activation MUST be `null`. The `sender_id` attribute of the NDI Receiver's activation MUST be set to the id of an NDI Sender or `null` if connecting to a non-NMOS NDI Sender.

NDI Senders and Receivers MUST be controlled through IS-05 only. The activation of a Sender / Receiver and the associated transport parameters MUST be under the control of IS-05 only.

The `source_name` associated with a Sender MUST be made of the following characters: lower case characters from 'a' to 'z', upper case characters from 'A' to 'Z', numeric characters from '0' to '9', underscore character '_'. If the `source_name` transport parameter is a Receiver is not null, it follows the same rule.

### Receivers

An NDI Receiver MUST search for NDI Senders first in the `Public` group and then in other groups, unless configured differently through a vendor-specific mechanism.

> Note: The NDI transport parameters of a Receiver do not include information about the Sender's group membership. A vendor-specific mechanism could be employed to configure NDI Senders and Receivers to utilize groups other than the default NDI `Public` group.

If the Receiver is not capable of consuming the stream described by a `PATCH` on the **/staged** endpoint, it SHOULD reject the request. If it is unable to assess the stream compatibility because some parameters are not included `PATCH` request, it MAY accept the request and postpone stream compatibility assessment.

An NDI Receiver MAY connect to a non-NMOS NDI Sender. IS-05 is then used only on the Receiver side and an unspecified mechanism MUST be used to activate such non-NMOS NDI Sender.

### Senders

An NDI Sender MUST be a member of the default `Public` NDI group unless configured otherwise through a vendor-specific mechanism.

An NDI Sender MAY, unless constrained by IS-11, produce any NDI stream that is compliant with the associated Flow `urn:x-matrox:audio_layers`, `urn:x-matrox:video_layers` and `urn:x-matrox:data_layers`.

A non-NMOS NDI Receiver MAY connect to an NDI Sender. IS-05 is then used only on the Sender side and an unspecified mechanism MUST be used to activate such non-NMOS NDI Receiver.

## NDI IS-11 Senders and Receivers

### RTP transport

### Other transports

## Controllers

[RFC-2119]: https://tools.ietf.org/html/rfc2119 "Key words for use in RFCs"
[IS-04]: https://specs.amwa.tv/is-04/ "AMWA IS-04 NMOS Discovery and Registration Specification"
[IS-05]: https://specs.amwa.tv/is-05/ "AMWA IS-05 NMOS Device Connection Management Specification"
[NMOS Parameter Registers]: https://specs.amwa.tv/nmos-parameter-registers/ "Common parameter values for AMWA NMOS Specifications"
[VSF]: https://vsf.tv/ "Video Services Forum"
[SMPTE]: https://www.smpte.org/ "Society of Media Professionals, Technologists and Engineers"
[BCP-004-01]: https://specs.amwa.tv/bcp-004-01/ "AMWA BCP-004-01 NMOS Receiver Capabilities"
