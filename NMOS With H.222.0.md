# Matrox: NMOS With H.222.0
{:.no_toc}

{:toc}

## Introduction

H.222.0 is a transmission multiplexing and synchronization technology standardized in Rec. [ITU-T H.222.0][H.222.0] | ISO/IEC 13818-1.

The Rec. [ITU-T H.222.0][H.222.0] | ISO/IEC 13818-1 specification and associated amendments describe the embedding of various media streams in an MPEG2-TS transport stream. An RTP payload format specification for MPEG2-TS transport stream was developed through the IETF Payloads working group, IETF [RFC 2250][RFC-2250] for transport over RTP and [RFC 3551][RFC-3551] defines the payload format `video/MP2T`. Other normative documents describe the requirements for the streaming of an MPEG2-TS transport stream over other non-RTP transports.

The [Video Services Forum][VSF] developed Technical Recommendation [TR-07][TR-07] fro the transport of JPEG-XS video and AES3 audio in an MPEG2-TS stream over IP.

## Use of Normative Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY",
and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119][RFC-2119].

## Definitions

The NMOS terms 'Controller', 'Node', 'Source', 'Flow', 'Sender', 'Receiver' are used as defined in the [NMOS Glossary](https://specs.amwa.tv/nmos/main/docs/Glossary.html).

A 'sub-Flow' is defined as a Flow of format `urn:x-nmos:format:audio`, `urn:x-nmos:format:video` or `urn:x-nmos:format:data` part of a MPEG2-TS Stream produced by a Sender.

A 'sub-Stream' is defined as a Stream of format `urn:x-nmos:format:audio`, `urn:x-nmos:format:video` or `urn:x-nmos:format:data` part of a MPEG2-TS Stream consumed by a Receiver.

## H.222.0 IS-04 Sources, Flows and Senders

Nodes implementing IS-04 v1.3 or higher that are capable of transmitting H.222.0 mux streams MUST have Source, Flow and Sender resources in the IS-04 Node API.

### Sources

A mux Source resource MUST indicate `urn:x-nmos:format:mux` for the `format` attribute. A Source of format `urn:x-nmos:format:audio`, `urn:x-nmos:format:video` or `urn:x-nmos:format:data`, associated with a sub-Flow MUST be a member of the mux Source's `parents` attribute.

In addition to those attributes defined in IS-04 for all mux Sources, the following attributes defined in the [Flow Attributes](https://github.com/alabou/NMOS-MatroxOnly/blob/main/SourceAttributes.md) are used for H.222.0.

A Source of format `urn:x-nmos:format:audio`, `urn:x-nmos:format:video` or `urn:x-nmos:format:data` having a non-null `urn:x-matrox:receiver_id` attribute where the associated Receiver `format` attribute is `urn:x-nmos:format:mux` MUST have a `urn:x-matrox:layer` attribute indicading the Receiver's sub-Stream providing the media content to the Source.

Examples Source resources are provided in [Examples](../examples/).

### Flows

A mux Flow resource MUST indicate `video/MP2T` or `application/mp2t` in the `media_type` attribute, and `urn:x-nmos:format:mux` for the `format` attribute.  When the mux Flow is associated with a Sender using the `urn:x-nmos:transport:rtp` transport, the `media_type` MUST be `video/MP2T. Otherwise for other transports it the `media_type` MUST be `application/mp2t`. A sub-Flow MUST be a member of the mux Flow's `parents` attribute.

A mux Flow MUST have a `source_id` attribute referencing a Source of the same `format`.

In addition to those attributes defined in IS-04 for all mux Flows, the following attributes defined in the [Flow Attributes](https://github.com/alabou/NMOS-MatroxOnly/blob/main/FlowAttributes.md) are used for H.222.0.

A mux Flow MUST have `urn:x-matrox:audio_layers`, `urn:x-matrox:video_layers` and `urn:x-matrox:data_layers` attributes indicating the number of sub-Flows of each `format` making an MPEG2-TS stream. A non-mux Flow MUST not have such attributes. The MPEG2-TS Stream MUST not have more or less sub-Streams than indicated by those attributes.

A sub-Flow MUST have a `urn:x-matrox:layer` attribute identifying the sub-Flow within all the other sub-Flows of the same `format` making an MPEG2-TS stream. A mux Flow MUST not have such attribute.

A sub-Flow MUST have a `urn:x-matrox:layer_compatibility_groups` attribute identifying the sub-Flow compatibility with other sub-Flows making an MPEG2-TS stream. A mux Flow MUST not have such attribute.

Examples Flow resources are provided in [Examples](../examples/).

### Senders

A Sender associated with a mux Flow through the `flow_id` attribute MUST provide Sender's Capabilities for the mux Flow and each sub-Flow using Constraint Set `urn:x-matrox-format`, `urn:x-matrox-layer` and `urn:x-matrox-layer_compatibility_groups` meta attributes values matching the sub-Flows.

The following parameter constraints can be used to express limits or preferences on the mux stream:

- [audio_layers](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md#audio_layers)  
  Indicate the minimum and maximum audio layers supported in the MPEG2-TS stream. The Sender Capabilities MUST provide Constraint Sets for as many as the maximum layers.

- [video_layers](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md#video_layers)  
  Indicate the minimum and maximum video layers supported in the MPEG2-TS stream. The Sender Capabilities MUST provide Constraint Sets for as many as the maximum layers.

- [data_layers](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md#data_layers)  
  Indicate the minimum and maximum audio layers supported in the MPEG2-TS stream. The Sender Capabilities MUST provide Constraint Sets for as many as the maximum layers.

A coded format specification MAY define additional parameter constraints that can be used to express limits or preferences on the audio, video and data sub-streams.

#### RTP transport based on RFC 2250 and RFC 3551

For Nodes transmitting H.222.0 using the RTP payload mapping defined by RFC 2250 adn RFC 3551, the Sender resource MUST indicate `urn:x-nmos:transport:rtp` or one of its subclassifications for the `transport` attribute.

An example Sender resource is provided in the [Examples](../examples/).

##### SDP format-specific parameters

The SDP file at the `manifest_href` MUST comply with the requirements of RFC 2250 adn RFC 3551.

An example SDP file is provided in the [Examples](../examples/).

#### Other transports

For Nodes transmitting H.222.0 using other transports, the Sender resource MUST indicate the associated `urn:x-nmos:transport:` label of the transport or one of its subclassifications for the `transport` attribute.

The `manifest_href` attribute MAY be `null` if an SDP transport file is not supported by the transport. Otherwise the SDP transport file MUST comply with the transport specific requirements. There is no SDP format-specific parameters requirements for transports other than RTP.

## H.222.0 IS-04 Receivers

Nodes implementing IS-04 v1.3 or higher that are capable of receiving H.222.0 video streams MUST have Receiver resources in the IS-04 Node API.

A mux Receiver MUST indicate `urn:x-nmos:format:mux` for the `format` attribute and MUST provide Receiver's Capabilities for the mux Stream and each sub-Stream using Constraint Set `urn:x-matrox-format`, `urn:x-matrox-layer` and `urn:x-matrox-layer_compatibility_groups` meta attributes values defining the Receiver's sub-Streams.

If the Receiver has limitations on or preferences regarding the H.222.0 streams that it supports, the Receiver resource MUST indicate constraints in accordance with the [Receiver Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/ReceiverCapabilities.md) Receiver Capabilities specification. The Receiver SHOULD express its constraints as precisely as possible, to allow a Controller to determine with a high level of confidence the Receiver's compatibility with the available streams and sub-streams. It is not always practical for the constraints to indicate every type of stream or sub-stream that a Receiver can or cannot consume successfully; however, they SHOULD describe as many of its commonly used operating points as practical and any preferences among them.

The `constraint_sets` parameter within the `caps` object MUST be used to describe combinations of parameters which the receiver can support, using the parameter constraints defined in the [Capabilities register](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/) of the NMOS Parameter Registers and [Matrox Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md).

The following parameter constraints can be used to express limits or preferences on the mux stream. For a given format, a mux stream MUST provide at least the minimum and no more than the maximum number of layers supported by the Receiver. Layers in excess of the number of layers supported by the Receiver MUST be ignored. by the Receiver.

- [audio_layers](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md#audio_layers)  
  Indicate the minimum and maximum audio layers supported from the MPEG2-TS stream. The Receiver Capabilities MUST provide Constraint Sets for as many as the maximum layers.

- [video_layers](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md#video_layers)  
  Indicate the minimum and maximum video layers supported from the MPEG2-TS stream. The Receiver Capabilities MUST provide Constraint Sets for as many as the maximum layers.

- [data_layers](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md#data_layers)  
  Indicate the minimum and maximum audio layers supported from the MPEG2-TS stream. The Receiver Capabilities MUST provide Constraint Sets for as many as the maximum layers.

A coded format specification MAY define additional parameter constraints that can be used to express limits or preferences on the audio, video and data sub-streams.


An example Receiver resource is provided in the [Examples](../examples/).

### RTP transport based on RFC 2250 and RFC 3551

For Nodes consuming H.222.0 using the RTP payload mapping defined by RFC 2250 adn RFC 3551, the Receiver resource MUST indicate `urn:x-nmos:transport:rtp` or one of its subclassifications for the `transport` attribute.

### Other transports

For Nodes consuming H.222.0 using other transports, the Receiver resource MUST indicate the associated `urn:x-nmos:transport:` label of the transport or one of its subclassifications for the `transport` attribute.
  
## H.222.0 IS-05 Senders and Receivers

### RTP transport

Connection Management using IS-05 proceeds in exactly the same manner as for any other stream format carried within RTP.

If IS-04 Sender `manifest_href` is not `null`, the SDP transport file at the **/transportfile** endpoint on an IS-05 Sender MUST comply with the same requirements described for the SDP transport file at the IS-04 Sender `manifest_href`.

A `PATCH` request on the **/staged** endpoint of an IS-05 Receiver can contain an SDP transport file in the `transport_file` attribute. The SDP transport file for a H.222.0 stream is expected to comply with RFC 2250 adn RFC 3551. It need not comply with the additional requirements specified for SDP transport files at Senders.

If the Receiver is not capable of consuming the stream described by a `PATCH` on the **/staged** endpoint, it SHOULD reject the request. If it is unable to assess the stream compatibility because some parameters are not included `PATCH` request, it MAY accept the request and postpone stream compatibility assessment.
  
### Other transports

Connection Management using IS-05 proceeds in exactly the same manner as for any other stream format carried within other transports.

If IS-04 Sender `manifest_href` is not `null`, the SDP transport file at the **/transportfile** endpoint on an IS-05 Sender MUST comply with the same requirements described for the SDP transport file at the IS-04 Sender `manifest_href`.

If the Receiver is not capable of consuming the stream described by a `PATCH` on the **/staged** endpoint, it SHOULD reject the request. If it is unable to assess the stream compatibility because some parameters are not included `PATCH` request, it MAY accept the request and postpone stream compatibility assessment.

### Receivers

A Receiver MUST verify that the active parameter sets comply with the Receiver's Capabilities. If a Receiver support only out-of-band parameter sets it SHOULD perform the verification when a Controller PATCH the **/staged** endpoint for activation. In this situation, all the out-of-band parameter sets MUST be compliant with the Receiver Capabilities. Otherwise if a Receiver supports both out-of-band and in-band parameter sets it SHOULD perform the verification of the out-of-band parameter sets when a Controller PATCH the **/staged** endpoint for activation and it MUST perform the verification of the in-band parameter sets just-in-time as it decodes the stream. In this situation, all the out-of-band and in-band parameter sets MUST be compliant with the Receiver Capabilities.

### Senders

A Sender MAY, unless constrained by IS-11, produce any H.222.0 coded stream that is compliant with the associated Flow `urn:x-matrox:audio_layers`, `urn:x-matrox:video_layers` and `urn:x-matrox:data_layers`.

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