# Matrox: NMOS With IPMX
{:.no_toc}  
Copyright 2024, Matrox Graphics Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
  
---
  
{:toc}

## Introduction

This document presents the various aspects of using IPMX compliant Senders and Receivers in an NMOS environment. It complements the IPMX specifications, most specifically the TR-10-8 (NMOS Requirements) specification.

## Use of Normative Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY",
and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119][RFC-2119].

## Definitions

The NMOS terms 'Controller', 'Node', 'Source', 'Flow', 'Sender', 'Receiver' are used as defined in the [NMOS Glossary](https://specs.amwa.tv/nmos/main/docs/Glossary.html).

## Common Reference Clock

A Receiver SHOULD provide a `urn:x-matrox:cap:transport:clock_ref_type` capability to indicate its support for IPMX Senders not using a common reference clock (PTP). The capability value `ptp` indicates the support of a common reference clock (PTP) while the value `internal` indicates the support of an internal clock (not PTP).

A Receiver MAY support either or both clock reference types.

A Controller MAY verify the compliance of the Receiver with a Sender using the Sender's SDP transport file and check for the a=ts-refclk attribute. It MAY also verify the compliance using the Sender's associated Source `clock_name` attribute and checking the clock's `ref_type` atribute.

A Sender MAY provide a `urn:x-matrox:cap:transport:clock_ref_type` capability to indicate the reference clocks that it supports. A controller MAY use Sender capabilities, if supported, to verify the compliance of a Receiver with a Sender and if necessary constrain the Sender to make it compliant with the Receivers.

## Asynchronous/Synchronous Media

A Receiver SHOULD provide a `urn:x-matrox:cap:transport:synchronous_media` capability to indicate its support for IPMX Senders media that is synchronous to the Sender's reference clock. The capability value `true` indicates the support of synchronous media while the value `false` indicates the support of asynchronous media.

A Receiver MAY support either or both clock reference types.

A Controller MAY verify the compliance of the Receiver with a Sender using the Sender's SDP transport file and check for the a=mediaclk attribute. It MAY also verify the compliance using the Sender's associated Source `urn:x-matrox:synchronous_media` attribute.

A Sender MAY provide a `urn:x-matrox:cap:transport:synchronous_media` capability to indicate the media synchronisation that it supports. A controller MAY use Sender capabilities, if supported, to verify the compliance of a Receiver with a Sender and if necessary constrain the Sender to make it compliant with the Receivers.

## Info Block

A Receiver SHOULD provide a `urn:x-matrox:cap:transport:info_block` capability to indicate its support for IPMX Senders media info blocks (in RTCP Sender Report). The capability SHOULD enumerate the media info block types (integer) supported by the Receiver. An empty enumeration indicate that the Receiver does not support IPMX in-band media info block. Enumerating the value 0 which is an invalid media info block type identifier serves the same purpose.

A Receiver MAY support none, some or all the IPMX media info block types.

When media stream attributes associated with a Sender change, a Controller MAY let the Receiver handle the media stream attributes changes from the media info blocks produced by the Sender, if all of media info block types produced by a Sender are supported by the Receiver.

A Sender SHOULD provide a `urn:x-matrox:cap:transport:info_block` capability to indicate the media info block types that it generates. A controller MAY use Sender capabilities, if supported, to verify the compliance of a Receiver with a Sender. It is not allowed to constrain a Sender for such capability as info block are a required feature of IPMX.

## HKEP

A Receiver SHOULD provide a `urn:x-matrox:cap:transport:hkep` capability to indicate its support for IPMX Senders HDCP encryption and the HKEP protocol. The capability value `true` indicates the support of HDCP encryption and the HKEP protocol. The capability value `false` indicates that HDCP encryption and the HKEP protocol are not supported.

A Receiver MAY support either or both true and false values.

A Controller MUST verify the compliance of the Receiver with a Sender using HDCP encryption from the SDP transport file `hkep` attribute. The presence of such attribute in an SDP transport file indicate that the stream is HDCP protected. Only Receivers supporting HDCP encryption and the HKEP protocol can consume such streams.

A Sender MAY provide a `urn:x-matrox:cap:transport:hkep` capability to indicate that HDCP encryption and the HKEP protocol are supported. A Sender MAY support either or both true and false values. A controller MAY use Sender capabilities, if supported, to verify the compliance of a Receiver with a Sender and if necessary constrain the Sender to make it compliant with the Receivers. A Sender constrained to `false` for such capability MUST NOT be part of an HDCP topology and MUST NOT access/produce/stream HDCP protected content.

Informative Note: A Sender indicating both `true` and `false` values in its capabilities describes that it may produce both HDCP and non-HDCP streams according to some internal criteria at activation time. 

### RTP Payload Header

Refer to the Privacy section "RTP Payload Header" for the detailed definition of an RTP Payload Header for various audio and video media types. Those definitions MUST be used to determine the part of the RTP Payload that is HDCP encrypted.

## Privacy

A Receiver SHOULD provide a `urn:x-matrox:cap:transport:privacy` capability to indicate its support for IPMX Senders privacy encryption and the PEP protocol. The capability value `true` indicates the support of privacy encryption and the PEP protocol. The capability value `false` indicates that privacy encryption and the PEP protocol are not supported.

A Receiver MAY support either or both true and false values.

A Controller MUST verify the compliance of the Receiver with a Sender using privacy encryption from the SDP transport file `privacy` attribute. The presence of such attribute in an SDP transport file indicate that the stream is privacy protected. Only Receivers supporting privacy encryption and the PEP protocol can consume such streams. The fine grained Receiver privacy capabilities are provided as part of the associated Receiver's transport parameters constraints.

A Sender MAY provide a `urn:x-matrox:cap:transport:privacy` capability to indicate that privacy encryption and the PEP protocol are supported. A Sender MAY support either true or false values. A controller MAY use Sender capabilities, if supported, to verify the compliance of a Receiver with a Sender. It is not allowed to constrain a Sender for such capability as PEP is a protection mechanism under the control of the Sender.

Informative Note: A Sender is configured by an administrator to produce either privacy encrypted streams or non-encrypted streams. The Sender capability indicates the current configuration.

### RTP Payload Header

The concept of RTP Payload Header as defined by RFC 8088 (How to Write an RTP Payload Format) "RTP payload formats often need to include metadata relating to the payload data being transported. Such metadata is sent as a payload header, at the start of the payload section of the RTP packet." is important to encryption as such RTP Payload Headers are not encrypted. We define here the propoer interpretation of the various RTP paylado specifications.

#### RFC 4175 (video/raw)
As per [section 4](https://datatracker.ietf.org/doc/html/rfc4175#section-4) the RTP Payload Header is defined as the first 2 + (6 * lines) byte of the RTP Payload. The size of the RTP Payload Header depends on the number of lines or partial lines that are part of the RTP Payload. Those byte MUST NOT be encrypted.

#### RFC 9134 (video/jxsv)
As per [section 4.3](https://datatracker.ietf.org/doc/html/rfc9134#section-4.3) the RTP Payload Header is defined as the first 4 byte of the RTP Payload. Those byte MUST NOT be encrypted.

#### RFC 3640 (audio/mpeg4-generic)
As per [section 3.3.6](https://www.rfc-editor.org/rfc/rfc3640.html#section-3.3.6) and by the requirements of [NMOS With AAC](https://github.com/alabou/NMOS-MatroxOnly/blob/main/NMOS%20With%20AAC.md) that supports only the `hbr` mode, the first bytes of the RTP Payload defined as the AU Header section correspond to the RFC 8088 definition of RTP Paylaod Header and MUST NOT be encrypted. The RTP Payload Header is then defined as the first 2 + (2 * frames) byte of the RTP Payload. The size of the RTP Payload Header depends on the number of access units (AAC frames) that are part of the RTP Payload.

#### RFC 6416 (audio/MP4A-LATM)
As per [section 6.1](https://datatracker.ietf.org/doc/html/rfc6416#section-6.1) there is no RTP Payload Header defined. The complete RTP Payload MUST be encrypted.

#### RFC 2250 (video/MP2T)
As per [section 2](https://datatracker.ietf.org/doc/html/rfc2250#section-2) there is no RTP Payload Header defined. The complete RTP Payload MUST be encrypted.

#### RFC 6184 (video/H264)
As per [section 5.2](https://datatracker.ietf.org/doc/html/rfc6184#section-5.2) the RTP Payload Header is defined as the first byte of the RTP Payload. This byte MUST NOT be encrypted.

#### RFC 7798 (video/H265)
As per [section 54.2](https://datatracker.ietf.org/doc/html/rfc7798#section-4.2) the RTP Payload Header is defined as the first 2 byte of the RTP Payload. Those byte MUST NOT be encrypted. As PACI carrying RTP packet are not supported as per [NMOS With H.265](https://github.com/alabou/NMOS-MatroxOnly/blob/main/NMOS%20With%20H.265.md) this 2 byte definition applies in all scenarios.

#### RFC 8331 (video/smpte291)
As per [section 2.1](https://datatracker.ietf.org/doc/html/rfc8331#section-2.1)The RTP Payload Header is defined as the first 8 byte of the RTP Payload. Those byte MUST NOT be encrypted.

#### ST 2110-31 (audio/AM824)
As per ST 2110-31 there is no RTP Payload Header defined. The complete RTP Payload MUST be encrypted.

## Channel Order

A Receiver SHOULD provide a `urn:x-matrox:cap:transport:channel_order` capability for opaque AM824 multiplexed audio streams to indicate its support for IPMX Senders transparent transport of AES3 streams. The channel_order MUST follow the SMPTE2110 `channel-order` convention. The `channel_order` capability allows a Receiver to describe the number of audio sub-streams that it supports and for each the channels configuration and wether it is linear PCM or non-PCM data.

A Controller MAY verify the compliance of the Receiver with a Sender using the Sender's SDP transport file and check for the format specific `channel-order` parameter.

A Sender MAY provide a `urn:x-matrox:cap:transport:channel_order` capability to indicate the channels ordering that are supported. A controller MAY use Sender capabilities, if supported, to verify the compliance of a Receiver with a Sender. It is not allowed to constrain a Sender for such capability as it is not allowed to change the layering of audio, video and data sub-Flows.

## Audio layers

A Receiver SHOULD provide a `urn:x-matrox:cap:transport:audio_layers` capability for fully described AM824 multiplexed audio streams to indicate its support for IPMX Senders transparent transport of AES3 streams. The `audio_layers` capability allows a Receiver to describe the number of audio sub-streams that it supports. A Receiver SHOULD also provide sub-streams capabilities for each audio layer to indicate what audio sub-streams it supports.

A Controller MAY verify the compliance of the Receiver with a Sender using the Sender's SDP transport file format specific `channel-order` parameter and the Sender's mux Flow atributes and parent sub-Flows attributes.

A Sender MAY provide a `urn:x-matrox:cap:transport:audio_layers` capability to indicate the number of audio layers that are supported. A controller MAY use Sender capabilities, if supported, to verify the compliance of a Receiver with a Sender and if necessary constrain the Sender to make it compliant with the Receivers. Only the number of audio layers MAY be constrained.

A Controller MAY use IS-11 to constrain the Sender's sub-Flows to make them compliant with the Receiver.

[RFC-2119]: https://tools.ietf.org/html/rfc2119 "Key words for use in RFCs"
[IS-04]: https://specs.amwa.tv/is-04/ "AMWA IS-04 NMOS Discovery and Registration Specification"
[IS-05]: https://specs.amwa.tv/is-05/ "AMWA IS-05 NMOS Device Connection Management Specification"
[NMOS Parameter Registers]: https://specs.amwa.tv/nmos-parameter-registers/ "Common parameter values for AMWA NMOS Specifications"
