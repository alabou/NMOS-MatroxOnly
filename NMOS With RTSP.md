# Matrox: NMOS With RTSP
{:.no_toc}  
Copyright 2024, Matrox Graphics Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
  
---
  
{:toc}

## Introduction

[RFC-2326][] defines the Real-Time Streaming Protocol (RTSP) version 1.0. RTSP is an application-layer protocol for the setup and control of the delivery of data with real-time properties. RTSP provides an extensible framework to enable controlled, on-demand delivery of real-time data, such as audio and video. Sources of data can include both live data feeds and stored clips. The RTSP protocol is implemented by many non-NMOS devices to transmit and receive multicast/unicast media streams.

This document presents how RTSP is used in an NMOS environment. One use-case is for NMOS RTSP Senders/Receivers to interoperate with non-NMOS RTSP clients/servers. Another user-case is to use RTSP to enhance the control of unicast streams in 1-to-N scenarios (1 Sender to N Receivers). A last use-case is to allow additional flexibility in the negotiation of various media transport schemes by a single Sender/Receiver (parallel streams over RTP/AVP/UDP, single multiplexed stream over RTP/AVP/UDP, single multiplexed stream over UDP).

RTSP is used as a specific NMOS transport protocol `urn:x-matrox:transport:rtsp` or `urn:x-matrox:transport:rtsp.tcp` for both RTSP Senders and Receivers. This transport is available for RTSP Receivers of format `urn:x-nmos:format:mux` and RTSP Senders attached to a Flow of format `urn:x-nmos:format:mux`. The RTSP transport can deliver a multiplexed stream that combines audio, video, and data sub-streams, which can be either transmitted independently in parallel or aggregated into a single, fully multiplexed stream.

The `urn:x-matrox:transport:rtsp` transport identifies the `non-interleaved` mode of operation and allows the transmission/reception of a) multiple independent RTP/AVP/UDP sub-streams, b) a single aggregated multiplexed RTP/AVP/UDP stream and c) a single aggregated multiplexed UDP stream. The `media_type` associated with the mux Flow/Stream determine the effective transport scheme.

`urn:x-matrox:transport:rtsp` => media type `application/rtsp` (over RTP/AVP/UDP) or `application/MP2T` (over RTP/AVP/UDP) or `application/mp2t` (over UDP)

The `urn:x-matrox:transport:rtsp.tcp` transport identifies the `interleaved` mode of operation and allows the transmission/reception of a single aggregated multiplexed RTP/RTSP/TCP stream.

`urn:x-matrox:transport:rtsp.tcp` => media type `application/rtsp` or `application/MP2T` (over RTP/RTSP/TCP) 

> Note: The RTSP interleaved mode is supported by an NMOS device as a specific transport to emphasis the TCP nature of this option. TCP-based interleaving is often necessary for firewall/NAT traversal.

The RTSP control endpoints of RTSP Senders/Receivers support the same security features (rtsp versus rtsps, OAuth2.0 authorizations or not) as the IS-05 control point of the associated Senders/Receivers.

The media sub-streams of an RTSP session support the same privacy encryption features that non-RTSP streams offer.

The `DESCRIBE` method of an RTSP Sender provides a mechanism for retrieving the SDP transport file that describe the sub-Flows/sub-Streams making the RTSP mux Flow/Stream. The SDP transport file media level attribute `a=control:` is used to name sub-Flows/sub-Streams according to the `<role-in-group> <role-index>` rules described in the [NMOS With Natural Groups](https://github.com/alabou/NMOS-MatroxOnly/blob/main/NMOS%20With%20Natural%20Groups.md). A session level attribute `a=control:` attribute is used for the aggregated control of the RTSP mux stream according tot he `<group-name><group-index>` rules described in [NMOS With Natural Groups](https://github.com/alabou/NMOS-MatroxOnly/blob/main/NMOS%20With%20Natural%20Groups.md)

For a non-NMOS RTSP Sender, the use of aggregate and/or individual controls and the URL path of such controls is out of the scope of this document. An RTSP Receiver adapts, as a best effort, to the non-NMOS RTSP Sender.

The SDP transport file of an RTSP Sender using the `urn:x-matrox:transport:rtsp` or `urn:x-matrox:transport:rtsp.tcp` transports is only about how to access, through TCP, the RTSP server of such Sender. The client uses the `DESCRIBE` method to obtain information about the media streams available and uses the `SETUP` method to select/configure sub-streams transport parameters.

## Use of Normative Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY",
and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119][RFC-2119].

## Definitions

The NMOS terms 'Controller', 'Node', 'Source', 'Flow', 'Sender', 'Receiver' are used as defined in the [NMOS Glossary](https://specs.amwa.tv/nmos/main/docs/Glossary.html).

A 'sub-Flow' is defined as a Flow of format `urn:x-nmos:format:audio`, `urn:x-nmos:format:video` or `urn:x-nmos:format:data` which is part of an RTSP stream produced by a Sender.

A 'sub-Stream' is defined as a Stream of format `urn:x-nmos:format:audio`, `urn:x-nmos:format:video` or `urn:x-nmos:format:data` which is part of an RTSP stream consumed by a Receiver.

A non-NMOS RTSP Sender is an RTSP sender device that is not an NMOS Node and as such not part of an NMOS system.

A non-NMOS RTSP Receiver is an RTSP receiver device that is not an NMOS Node and as such not part of an NMOS system.

## RTSP IS-04 Sources, Flows and Senders

Nodes implementing IS-04 v1.3 or higher, that are capable of transmitting RTSP mux streams, MUST have Source, Flow and Sender resources in the IS-04 Node API.

### Sources

A mux Source resource MUST indicate `urn:x-nmos:format:mux` for the `format` attribute and it MUST be associated with a mux Flow of the same `format` through the `source_id` attribute of the mux Flow. A Source of format `urn:x-nmos:format:audio`, `urn:x-nmos:format:video` or `urn:x-nmos:format:data`, associated with a sub-Flow of said Flow, through the `source_id` attribute of the the sub-Flow, MUST be a member of said mux Source's `parents` attribute.

In addition to those attributes defined in IS-04 for all mux Sources, the following attributes defined in the [Source Attributes](https://github.com/alabou/NMOS-MatroxOnly/blob/main/SourceAttributes.md) are used for RTSP.

A Source of format `urn:x-nmos:format:audio`, `urn:x-nmos:format:video` or `urn:x-nmos:format:data` having a non-null `urn:x-matrox:receiver_id` attribute where the associated Receiver `format` attribute is `urn:x-nmos:format:mux` MUST have a `urn:x-matrox:layer` attribute indicading the Receiver's sub-Stream providing the media content to the Source.

Examples Source resources are provided in [Examples](../examples/).

### Flows

A mux Flow resource MUST indicate one of `application/rtsp`, `application/MP2T`, `application/mp2t` in the `media_type` attribute and `urn:x-nmos:format:mux` for the `format` attribute. A mux Flow MUST have a `source_id` attribute referencing a Source of the same `format`. A sub-Flow of format `urn:x-nmos:format:audio`, `urn:x-nmos:format:video` or `urn:x-nmos:format:data`, MUST be a member of said mux Flow's `parents` attribute.

In addition to those attributes defined in IS-04 for all mux Flows, the following attributes defined in the [Flow Attributes](https://github.com/alabou/NMOS-MatroxOnly/blob/main/FlowAttributes.md) are used for RTSP.

A mux Flow MUST have `urn:x-matrox:audio_layers`, `urn:x-matrox:video_layers` and `urn:x-matrox:data_layers` attributes indicating the number of sub-Flows of each `format` making an RTSP stream. A non-mux Flow MUST NOT have such attributes. The RTSP Stream MUST NOT have more or less sub-Streams than indicated by those attributes.

A sub-Flow MUST have a `urn:x-matrox:layer` attribute identifying the sub-Flow within all the other sub-Flows of the same `format` making an RTSP stream. A Flow that is not a sub-Flow MUST NOT have such attribute.

A sub-Flow SHOULD have a `urn:x-matrox:layer_compatibility_groups` attribute identifying the sub-Flow compatibility with other sub-Flows making an RTSP stream. A sub-Flow without a `urn:x-matrox:layer_compatibility_groups` attribute MUST be assumed as being part of all groups. A Flow that is not a sub-Flow MUST NOT have such attribute.

Examples Flow resources are provided in [Examples](../examples/).

### Senders

An RTSP Sender resource MUST indicate `urn:x-matrox:transport:rtsp` or `urn:x-matrox:transport:rtsp.tcp` for the `transport` attribute.

A Sender associated with a mux Flow through the `flow_id` attribute MUST provide Sender's Capabilities for the mux Flow and each sub-Flow making an RTSP stream using the Constraint Set `urn:x-matrox:cap:meta:format`, `urn:x-matrox:cap:meta:layer` and `urn:x-matrox:cap:meta:layer_compatibility_groups` attributes values matching the Sender's sub-Flows.

A mux Sender not exposing the sub-Streams MAY omit the Sender's Capabilities for the sub-Streams, indicating that it is unconstrained with respect to the individual sub-Streams making the RTSP stream and that it cannot be constrained as no sub-Flows are exposed.

The mux Sender MUST express its limitations or preferences regarding the RTSP streams that it supports indicating constraints in accordance with the [Sender Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/SenderCapabilities.md) Sender Capabilities specification. The Sender SHOULD express its constraints as precisely as possible, to allow a Controller to determine with a high level of confidence the Sender's streams and sub-streams capabilities. It is not always practical for the constraints to indicate every type of stream or sub-stream that a Sender can or cannot produce; however, they SHOULD describe as many of its commonly used operating points as practical and any preferences among them.

The `constraint_sets` parameter within the `caps` object MUST be used to describe combinations of parameters which the sender can support, using the parameter constraints defined in the [Capabilities register](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/) of the NMOS Parameter Registers and [Matrox Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md).

The following parameter constraints can be used to express limits or preferences on the mux stream:

- [audio_layers](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md#audio_layers)  
  Indicate the minimum and maximum audio layers supported in the RTSP stream. The Sender Capabilities MUST provide Constraint Sets for as many as the maximum number of layers.

- [video_layers](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md#video_layers)  
  Indicate the minimum and maximum video layers supported in the RTSP stream. The Sender Capabilities MUST provide Constraint Sets for as many as the maximum number of layers.

- [data_layers](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md#data_layers)  
  Indicate the minimum and maximum data layers supported in the RTSP stream. The Sender Capabilities MUST provide Constraint Sets for as many as the maximum number of layers.

A coded format specification MAY define additional parameter constraints that can be used to express limits or preferences on the audio, video and data sub-streams.

A coded format specification MAY define Sender's attributes and associated transport capabilities that, for the corresponding audio, video or data sub-stream, MUST be assumed as having their default value.

Note: The Sender's attributes and associated transport capabilities of a coded format specification are assumed to exist for each sub-Stream, each having their default values. For example the `parameter_sets_flow_mode` and `parameter_sets_transport_mode` associated with some coded format specification are assumed as having their default value of `dynamic` and `in_band` respectively.

An example Sender resource is provided in the [Examples](../examples/).

#### SDP format-specific parameters

The SDP transport file at the `manifest_href` MUST comply with RFC 4145 and the following requirements. It MUST provides the information about the RTSP control endpoint. The SDP transport file describing the sub-Streams of an RTSP Sender MUST be provided as the response of a `DESCRIBE` request.

When Privacy Encryption Protocol is used, as described in [NMOS With Privacy Encryption](https://github.com/alabou/NMOS-MatroxOnly/blob/main/NMOS%20With%20Privacy%20Encryption.md), the SDP transport file MUST provides the `a=privacy:` attributeand the SDP transport files received from `DESCRIBE` MUST NOT contain any `a=privacy:` attribute. The privacy encryption `iv'` parameter of an independently encrypted sub-Streams is derived as described in the section "Privacy Encryption" of this document.

##### Sender's SDP transport file

The SDP transport file from the RTSP Sender MUST contain an `a=control:rtsp://<host [ ":" port ]>/x-nmos/<group-name><group-index>` session attribute that indicate to the RTSP Receiver and non-NMOS RTSP Receiver the URL to use for RTSP commands. The `/x-nmos/` path element indicates that the RTSP server is of an NMOS RTSP Sender, otherwise it must be assumed as being of non-NMOS RTSP Sender.

The media type MUST be “application/rtsp” for both `urn:x-matrox:transport:rtsp` transports.

`m=application <port> TCP rtsp`

`<port>`: TCP server port of the RTSP Sender

The `role` of the `a=setup` attribute MUST be “passive”.

`a=setup:passive`

An example SDP file is provided in the [Examples](../examples/).

##### DESCRIBE SDP transport file

The response by an RTSP Sender of a `DESCRIBE` for an aggregate control URL MUST be an `application/sdp` SDP transport file describing all the media streams of the associated group <group-name><group-index>. A `a=control:rtsp://<host [ ":" port ]>/x-nmos/<group-name><group-index>` session attribute MUST indicate the URL to use for aggregate control. A `a=control:rtsp://<host [ ":" port ]>/x-nmos/<group-name><group-index>/<role-in-group><role-index>` media attribute MUST indicate for each sub-Stream the URL to use for individual control.

The response by an RTSP Sender of a `DESCRIBE` for a sub-Stream individual control URL MUST be an `application/sdp` SDP transport file describing a specific media stream of the associated group hint `<group-name><group-index>:<role-in-group><role-index>`.

## RTSP IS-04 Receivers

An RTSP Receiver resource MUST indicate `urn:x-matrox:transport:rtsp` or `urn:x-matrox:transport:rtsp.tcp` for the `transport` attribute.

Nodes implementing IS-04 v1.3 or higher that are capable of receiving RTSP streams MUST have Receiver resources in the IS-04 Node API.

A mux Receiver MUST indicate `urn:x-nmos:format:mux` for the `format` attribute and MUST provide Receiver's Capabilities for the mux Stream and each sub-Stream using the Constraint Set `urn:x-matrox:cap:meta:format`, `urn:x-matrox:cap:meta:layer` and `urn:x-matrox:cap:meta:layer_compatibility_groups` attributes values matching the Receiver's sub-Streams.

A mux Receiver not exposing the sub-Streams MAY omit the Receiver's Capabilities for the sub-Streams, indicating that it is unconstrained with respect to the individual sub-Streams making the RTSP stream.

The mux Receiver MUST express its limitations or preferences regarding the RTSP streams that it supports indicating constraints in accordance with the [Receiver Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/ReceiverCapabilities.md) Receiver Capabilities specification. The Receiver SHOULD express its constraints as precisely as possible, to allow a Controller to determine with a high level of confidence the Receiver's compatibility with the available streams and sub-streams. It is not always practical for the constraints to indicate every type of stream or sub-stream that a Receiver can or cannot consume successfully; however, they SHOULD describe as many of its commonly used operating points as practical and any preferences among them.

The `constraint_sets` parameter within the `caps` object MUST be used to describe combinations of parameters which the receiver can support, using the parameter constraints defined in the [Capabilities register](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/) of the NMOS Parameter Registers and [Matrox Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md).

The following parameter constraints can be used to express limits or preferences on the mux stream. For a given format, a mux stream MUST provide at least the minimum number of layers supported by the Receiver. Sub-Streams that are not mapped to the Receiver's layers are ignored.

- [audio_layers](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md#audio_layers)  
  Indicate the minimum and maximum audio layers supported from the RTSP stream. The Receiver Capabilities MUST provide Constraint Sets for as many as the maximum layers.

- [video_layers](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md#video_layers)  
  Indicate the minimum and maximum video layers supported from the RTSP stream. The Receiver Capabilities MUST provide Constraint Sets for as many as the maximum layers.

- [data_layers](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md#data_layers)  
  Indicate the minimum and maximum data layers supported from the RTSP stream. The Receiver Capabilities MUST provide Constraint Sets for as many as the maximum layers.

A coded format specification MAY define additional parameter constraints that can be used to express limits or preferences on the audio, video and data sub-streams.

An example Receiver resource is provided in the [Examples](../examples/).

## RTSP IS-05 Senders and Receivers

Connection Management using IS-05 proceeds in exactly the same manner as for any other transports, using the RTSP specific transport parameters defined in [TCP Sender transport parameters](https://github.com/alabou/NMOS-MatroxOnly/blob/main/schemas/sender_transport_params_tcp.json) and [TCP Receiver transport parameters](https://github.com/alabou/NMOS-MatroxOnly/blob/main/schemas/receiver_transport_params_ndi.json). Because of the one Sender to N Receivers relationship of the RTSP transport the `receiver_id` attribute of the RTSP Sender's activation MUST be `null`. The `sender_id` attribute of the RTSP Receiver's activation MUST be set to the id of an RTSP Sender or `null` if connecting to a non-NMOS RTSP Sender.

RTSP Senders and Receivers MUST be controlled through IS-05 only. The activation of a Sender / Receiver and the associated transport parameters MUST be under the control of IS-05 only.

### Receivers

If the Receiver is not capable of consuming the stream described by a `PATCH` on the **/staged** endpoint, it SHOULD reject the request. If it is unable to assess the stream compatibility because some parameters are not included `PATCH` request, it MAY accept the request and postpone stream compatibility assessment. An RTSP Receiver MUST obtain the SDP transport files describing the sub-Streams using the `DESCRIBE` method and assess the stream compatibility.

An RTSP Receiver MAY connect to a non-NMOS RTSP Sender. IS-05 is then used only on the Receiver side and an unspecified mechanism MUST be used to activate such non-NMOS RTSP Sender. Such RTSP Receiver SHOULD as a best effort interoperate with the non-NMOS RTSP Sender.

An RTSP Receiver MUST use the `GET_PARAMETER` method with no entity body ping the RTSP server and keep the connection alive. The RTSP Receiver SHOULD NOT send a ping before half the session `timeout` period, from the last `SETUP` response, is reached.

### Senders

An RTSP Sender MAY, unless constrained by IS-11, produce any RTSP stream that is compliant with the associated Flow `urn:x-matrox:audio_layers`, `urn:x-matrox:video_layers` and `urn:x-matrox:data_layers`.

A non-NMOS RTSP Receiver MAY connect to an RTSP Sender. IS-05 is then used only on the Sender side and an unspecified mechanism MUST be used to activate such non-NMOS RTSP Receiver. Such RTSP Sender MUST behave as if an RTSP Receiver was connecting.

An RTSP Sender MUST support all the required method of [RFC-2326][] and additionally it MUST support the `DESCRIBE` and `GET_PARAMETER` methods. The `GET_PARAMETER` method with no entity body MUST be used by an RTSP Receiver or non-NMOS RTSP Receiver to ping the RTSP server and keep the connection alive.

## RTSP IS-11 Senders and Receivers

### RTP transport

### Other transports

## Controllers


## Privacy Encryption

When privacy encryption is used, the SDP transport file of the RTSP control endpoint MUST provide the `a=privacy:` attribute and parameters. The `iv` parameter as described in the [PEP](https://vsf.tv/download/technical_recommendations/VSF_TR-10-13_2024-01-19.pdf) correspond to a base value and a `sub-stream-id` MUST be added modulo 2^64 to obtain the effective sub-stream `iv'` of an independently encrypted sub-stream.

The `sub-stream-id` is defined as follow, using the definitions of [NMOS With Natural Groups](https://github.com/alabou/NMOS-MatroxOnly/blob/main/NMOS%20With%20Natural%20Groups.md):

if role-in-group == `VIDEO` role-major = 0
else if role-in-group == `AUDIO` role-major = 256
else if role-in-group == `DATA` role-major = 512

sub-stream-id = role-major + role-index

iv' = (iv + sub-stream-id) mod 2^64

> Note: An RTSP Receiver gets the role-in-group and role-index values from a `DESCRIBE` SDP transport file `a=control:` attribute from an RTSP Sender. This is no privacy encryption for non-NMOS RTSP Sender.

## TLS and OAuth2.0

The server endpoint of an RTSP Sender MUST follow the IS-05 Device's `urn:x-nmos:control:sr-ctrl` control scheme (`http` or `https`) and `authorization` mode. If the scheme is `http` then the RTSP scheme MUST be `rtsp` otherwise it MUST be `rtsps` (RTSP with TLS). When authorizations are required the client MUST provide an authorization token to access teh RTSP server.

## Redundancy

The sub-Streams MUST use the media interfaces that are specified for the RTSP IS-05 transport parameters.

The SDP transport file describing all the media of a group MUST include multiple `a=group:` session attributes to describe all the duplicate pairs of media streams that are described after the session section of the SDP transport file.

Example:

```
v=0
o=- 1122334455 1122334466 IN IP4 example.com
s=SDP transport file example
t=0 0
a=control:rtsp://matrox.com/x-nmos/RTSP0
a=group:DUP S1a S1b
a=group:DUP S2a S2b

m=video 5000 RTP/AVP 103
c=IN IP4 233.252.0.1/127
a=rtpmap:103 raw/90000
a=source-filter: incl IN IP4 233.252.0.1 198.51.100.1
a=mid:S1a
a=control:rtsp://matrox.com/x-nmos/RTSP0/VIDEO0/leg0`
m=video 5000 RTP/AVP 103
c=IN IP4 233.252.0.2/127
a=rtpmap:103 raw/90000
a=source-filter: incl IN IP4 233.252.0.2 198.51.100.1
a=mid:S1b
a=control:rtsp://matrox.com/x-nmos/RTSP0/VIDEO0/leg1`

m=audio 5004 RTP/AVP 96
c=IN IP4 233.252.0.1/127
a=rtpmap:96 L24/48000/2
a=source-filter: incl IN IP4 233.252.0.1 198.51.100.1
a=mid:S2a
a=control:rtsp://matrox.com/x-nmos/RTSP0/AUDIO0/leg0`
m=audio 5004 RTP/AVP 96
c=IN IP4 233.252.0.2/127
a=rtpmap:96 L24/48000/2
a=source-filter: incl IN IP4 233.252.0.2 198.51.100.1
a=mid:S2b
a=control:rtsp://matrox.com/x-nmos/RTSP0/AUDIO0/leg1`
```

> Note: This is an incomplete example without the format specific parameters

[RFC-2326]: https://datatracker.ietf.org/doc/html/rfc2326 "Real Time Streaming Protocol (RTSP)"
[RFC-2119]: https://tools.ietf.org/html/rfc2119 "Key words for use in RFCs"
[IS-04]: https://specs.amwa.tv/is-04/ "AMWA IS-04 NMOS Discovery and Registration Specification"
[IS-05]: https://specs.amwa.tv/is-05/ "AMWA IS-05 NMOS Device Connection Management Specification"
[NMOS Parameter Registers]: https://specs.amwa.tv/nmos-parameter-registers/ "Common parameter values for AMWA NMOS Specifications"
[SMPTE]: https://www.smpte.org/ "Society of Media Professionals, Technologists and Engineers"
[BCP-004-01]: https://specs.amwa.tv/bcp-004-01/ "AMWA BCP-004-01 NMOS Receiver Capabilities"


