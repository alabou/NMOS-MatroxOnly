# Matrox: NMOS With SRT
{:.no_toc}  
Copyright 2023, Matrox Graphics Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
  
---
  
{:toc}

## Introduction

SRT (Secure Reliable Transport) is an open source media transport protocol that utilises the UDP protocol and supports packet recovery. The open source project is available at [SRT](https://github.com/Haivision/srt).

The SRT protocol provides a reliable transport of anything using the UDP protocol. As such it can be used to transport an MPEG2-TS stream over SRT or an RTP stream over SRT. This specification supports both uses. The former MPEG2-TS mode is the default when using the `urn:x-matrox:transport:srt` transport, more specificatlly identified as `urn:x-matrox:transport:srt.mp2t`. The later RTP mode is identified as `urn:x-matrox:transport:srt.rtp`. Although SRT is well known for the reliable transport of an MPEG2-TS stream, it can also be used for the reliable transport of an RTP stream.

The SRT protocol provides 3 approaches for connecting SRT Senders and Receivers: Listener, Caller and RendezVous. Although various combinations are supported by this specification, the default configuration is to have an SRT Sender be a Listerer while an SRT Receiver is a Caller. It is this configuration that is most compatible with NMOS Controller model and the only one that will be presented in details.

The multi-paths redundancy (bonding) and the Stream ID features of SRT are supported by this specification as optional features.

## Use of Normative Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY",
and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119][RFC-2119].

## Definitions

The NMOS terms 'Controller', 'Node', 'Source', 'Flow', 'Sender', 'Receiver' are used as defined in the [NMOS Glossary](https://specs.amwa.tv/nmos/main/docs/Glossary.html).

A 'sub-Flow' is defined as a Flow of format `urn:x-nmos:format:audio`, `urn:x-nmos:format:video` or `urn:x-nmos:format:data` which is part of a MPEG2-TS Stream produced by a Sender.

A 'sub-Stream' is defined as a Stream of format `urn:x-nmos:format:audio`, `urn:x-nmos:format:video` or `urn:x-nmos:format:data` which is part of a MPEG2-TS Stream consumed by a Receiver.

A non-NMOS SRT Sender is an SRT sender device that is not an NMOS Node and as such not part of an NMOS system.

A non-NMOS SRT Receiver is an SRT receiver device that is not an NMOS Node and as such not part of an NMOS system.

## SRT IS-04 Senders

Nodes implementing IS-04 v1.3 or higher, that are capable of transmitting SRT streams, MUST have Source, Flow and Sender resources in the IS-04 Node API.

### MPGE2-TS

Senders having the `transport` attribute set to `urn:x-matrox:transport:srt` or `urn:x-matrox:transport:srt.mp2t` MUST be associated with a Flow through the `flow_id` attribute having  a `format` attribute set to `urn:x-nmos:format:mux` and a `media_type` attribute set to `application/mp2t`.

The [NMOS with H.222.0](https://github.com/alabou/NMOS-MatroxOnly/blob/other-transports/NMOS%20With%20H.222.0.md) specification provides the detailed requirements for the Source, Flow and Senders of such multiplexed stream for non-RTP transports.

#### SDP format-specific parameters

The `manifest_href` attribute of the Sender MUST provide the URL to an SDP transport file compliant with the following requirements:

- The media description line `m=<media> <port> <proto> <fmt> ...` MUST have `<media>` set to `application`, `<proto>` set to `UDP` and `<fmt>` set to `mp2t` to express that the `media_type` is `application/mp2t` and the UDP protocol is used by the `urn:x-nmos:transport:srt` and `urn:x-nmos:transport:srt.mp2t` transports. The `<port>` MUST be set to the UDP port of the SRT Sender listener.

- The connection information lines `c=<nettype> <addrtype> <connection-address>` MUST have `<connection-address>` set to the IP address of the SRT Sender listener.

- When multi-paths redundancy is used there MUST be one media descriptor per path. There SHOULD be two paths.

### RTP

Senders having the `transport` attribute set to `urn:x-matrox:transport:srt.rtp` MAY be associated with a Flow through the `flow_id` attribute having  a `format` attribute set to any of `urn:x-nmos:format:mux`, `urn:x-nmos:format:audio`, `urn:x-nmos:format:video` and `urn:x-nmos:format:data` and MUST implement the requirements of the `urn:x-nmos:transport:rtp` transport and related subclassifications.

#### SDP format-specific parameters

The `manifest_href` attribute of the Sender MUST provide the URL to an SDP transport file compliant with the requirements of transport `urn:x-nmos:transport:rtp` or one of its subclassifications and the following:

- The media description line `m=<media> <port> <proto> <fmt> ...` MUST have `<port>` MUST be set to the UDP port of the SRT Sender listener.

- The connection information lines `c=<nettype> <addrtype> <connection-address>` MUST have `<connection-address>` set to the IP address of the SRT Sender listener.

- When multi-paths redundancy is used there MUST be one media descriptor per path. There SHOULD be two paths.

- When using RTP over SRT only the media channel is transmitted using SRT, the RTCP channel is routed according to the `a=rtcp` attribute, destination address and port as per [RFC-3605][]. The RTCP destination address corresponds to the Sender's `destination_ip` transport parameter or is established by the Sender if `auto`.

## SRT IS-04 Receivers

Nodes implementing IS-04 v1.3 or higher that are capable of receiving SRT streams MUST have Receiver resources in the IS-04 Node API.

### MPGE2-TS

Receivers having the `transport` attribute set to `urn:x-matrox:transport:srt` or `urn:x-matrox:transport:srt.mp2t` MUST have  a `format` attribute set to `urn:x-nmos:format:mux` and a support streams of `media_type` `application/mp2t`.

The [NMOS with H.222.0](https://github.com/alabou/NMOS-MatroxOnly/blob/other-transports/NMOS%20With%20H.222.0.md) specification provides the detailed requirements for Receivers of such multiplexed stream.

### RTP

Receivers having the `transport` attribute set to `urn:x-matrox:transport:srt.rtp` MAY have a `format` attribute set to any of `urn:x-nmos:format:mux`, `urn:x-nmos:format:audio`, `urn:x-nmos:format:video` and `urn:x-nmos:format:data` and MUST implement the requirements of the `urn:x-nmos:transport:rtp` transport and related subclassifications.
  
## SRT IS-05 Senders and Receivers

Connection Management using IS-05 proceeds in exactly the same manner as for any other transports, using the SRT specific transport parameters defined in [SRT Sender transport parameters](https://github.com/alabou/NMOS-MatroxOnly/blob/main/schemas/sender_transport_params_srt.json) and [SRT Receiver transport parameters](https://github.com/alabou/NMOS-MatroxOnly/blob/main/schemas/receiver_transport_params_srt.json).

All the Sender's  `source_ip`, `source_port`, `destination_ip`, `destination_port`, `protocol` and `latency` transport parameters MUST be part of the Sender's `active`, `staged` and `constraints` endpoints. For Senders supporting the Stream ID feature, the `stream_id` MUST also be part of the Sender's `active`, `staged` and `constraints` endpoints. When the `stream_id` transport parameters is not present, is MUST default to `null`.

The Sender's `stream_id` transport parameters MUST be `null` if the SRT Sender is using the `rendezvous` protocol, or if it is a `listener` and not using the Stream ID feature, or if it a `caller` and the `listener` is not using the Stream ID feature. For an SRT Sender that is a `listener` using the Stream ID feature the `stream_id` MUST be of the form: `#!::r=<grouphint>` where `<grouphint>` corresponds to the "urn:x-nmos:tag:grouphint/v1.0" tag of the associated Sender that MUST be unique among all the streams served by the SRT server at address `source_ip` and port `source_port`. For an SRT Sender that is a `caller` to an SRT Receiver using the Stream ID feature, the `stream_id` MUST be of the form: `#!::r=<grouphint>` where `<grouphint>`  corresponds to the "urn:x-nmos:tag:grouphint/v1.0" tag of the target Receiver that MUST be unique among all the streams served by the SRT server at address `destination_ip` and port `destination_port`. For an SRT Sender that is a `caller` to a non-NMOS SRT Receiver using the Stream ID feature, the `stream_id` MUST be a string compliant with the non-NMOS SRT Receiver.

An SRT Sender MAY indicate that it does not support the Stream ID feature by using a constraint on `stream_id` that only allow the `null` value.

All the Receivers's `destination_ip`, `destination_port`, `source_ip`, `source_port`, `protocol` and `latency` transport parameters MUST be part of the Receiver's `active`, `staged` and `constraints` endpoints. For Receivers supporting the Stream ID feature, the `stream_id` MUST also be part of the Receiver's `active`, `staged` and `constraints` endpoints. When the `stream_id` transport parameters is not present, is MUST default to `null`.

The Receiver's `stream_id` transport parameters MUST be `null` if the SRT Receiver is using the `rendezvous` protocol, or if it is a `listener` and not using the Stream ID feature, or if it a `caller` and the `listener` is not using the Stream ID feature. For an SRT Receiver that is a `listener` using the Stream ID feature the `stream_id` MUST be of the form: `#!::r=<grouphint>` where `<grouphint>` corresponds to the "urn:x-nmos:tag:grouphint/v1.0" tag of the associated Receiver that MUST be unique among all the streams served by the SRT server at address `destination_ip` and port `destination_port`. For an SRT Receiver that is a `caller` to an SRT Sender using the Stream ID feature, the `stream_id` MUST be of the form: `#!::r=<grouphint>` where `<grouphint>` corresponds to the "urn:x-nmos:tag:grouphint/v1.0" tag of the target Sender that MUST be unique among all the streams served by the SRT server at address `source_ip` and port `source_port`. For an SRT Receiver that is a `caller` to a non-NMOS SRT Sender using the Stream ID feature, the `stream_id` MUST be a string compliant with the non-NMOS SRT Sender.

An SRT Receiver MAY indicate that it does not support the Stream ID feature by using a constraint on `stream_id` that only allow the `null` value.

> Note: In an NMOS system the Stream ID feature is used for resource identification by SRT Senders and SRT Receivers. It is the SRT `listener` that define the stream_id value independently of being the source or destination. SRT Sender and Receiver in a `caller` role with non-NMOS devices could have additional uses of the Stream ID feature.

An SRT Sender/Receiver acting as a `listener` and supporting the Stream ID feature MUST ignore the `staged` value of the `stream_id` transport parameter and MUST set the `active` value to its "urn:x-nmos:tag:grouphint/v1.0" tag on activation.

The `protocol` transport parameter MUST default to `listener` on an SRT Sender and to `caller` on an SRT Receiver. A Controller MAY use other combinations in specific connection scenarios. Those are a) both Sender and Receiver using the `rendezvous` protocol or b) the Sender is the `caller` while the Receiver is the `listener`. The default `protocol` values provide an NMOS compatible configuration where a Receiver connects to a Sender based on information optionally received from an SDP transport file. Other configurations require that the Controller uses the transport parameters of both the Sender and Receiver to make a connection.

In `rendezvous` mode for both the Sender and Receiver the `source_port` and `destination_port` MUST be equal.

> The SDP transport file information is invariant to the value of the `protocol` transport parameter of the Sender. It always indicate the Sender's `source_ip` and `source_port` transport parameters.

When multi-paths redundancy is used the `stream_id`, `protocol` and `latency` transport parameters of each leg of a Sender/Receiver MUST be identical.

### Encryption

The SRT native stream encryption MAY be controlled using the [Privacy Encrption Protocol (PEP)](https://github.com/alabou/NMOS-MatroxOnly/blob/other-transports/NMOS%20With%20Privacy%20Encryption.md) using the SRT transport adaptation. When using this protocol adaptation the SRT passphrase is derived from the PEP key derivation function.

The SRT stream MAY further be encrypted using the [Privacy Encrption Protocol (PEP)](https://github.com/alabou/NMOS-MatroxOnly/blob/other-transports/NMOS%20With%20Privacy%20Encryption.md) using the UDP transport adaptation when the transport is `urn:x-matrox:transport:srt` or `urn:x-matrox:transport:srt.mp2t` or using the RTP transport adaptation when the transport is `urn:x-matrox:transport:srt.rtp`.

## SRT IS-11 Senders and Receivers

### MPEG2-TS

### RTP

## Controllers

[RFC-2119]: https://tools.ietf.org/html/rfc2119 "Key words for use in RFCs"
[IS-04]: https://specs.amwa.tv/is-04/ "AMWA IS-04 NMOS Discovery and Registration Specification"
[IS-05]: https://specs.amwa.tv/is-05/ "AMWA IS-05 NMOS Device Connection Management Specification"
[NMOS Parameter Registers]: https://specs.amwa.tv/nmos-parameter-registers/ "Common parameter values for AMWA NMOS Specifications"
[VSF]: https://vsf.tv/ "Video Services Forum"
[SMPTE]: https://www.smpte.org/ "Society of Media Professionals, Technologists and Engineers"
[BCP-004-01]: https://specs.amwa.tv/bcp-004-01/ "AMWA BCP-004-01 NMOS Receiver Capabilities"
[RFC-3605]: https://datatracker.ietf.org/doc/html/rfc3605 "Real Time Control Protocol (RTCP) attribute in Session Description Protocol (SDP)"
