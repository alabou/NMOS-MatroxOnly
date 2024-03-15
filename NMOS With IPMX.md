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

## Asynchronous/Synchronous Media

A Receiver SHOULD provide a `urn:x-matrox:cap:transport:synchronous_media` capability to indicate its support for IPMX Senders media that is synchronous or not to the Sender's reference clock. The capability value `true` indicates the support of synchronous media while the value `false` indicates the support of asynchronous media.

A Receiver MAY support either or both clock reference types.

A Controller MAY verify the compliance of the Receiver with a Sender using the Sender's SDP transport file and check for the a=mediaclk attribute. It MAY also verify the compliance using the Sender's associated Source `synchronous_media` attribute.

## Info Block

A Receiver SHOULD provide a `urn:x-matrox:cap:transport:info_block` capability to indicate its support for IPMX Senders info blocks (in RTCP Sender Report). The capability SHOULD enumerate the media info block types (integer) supported by the Receiver. An empty enumeration indicate that the Receiver does not support IPMX in-band info block. Enumerating the value 0 which is an invalid media info block type identifier serves the same purpose.

A Receiver MAY support none, some or all the IPMX media info block types.

A Controller MUST either a) assume that the Receiver is not processing the info blocks and always PATCH the latest SDP transport file from a Sender to the Receiver, or b) verify which content of an SDP transport file has changed and if not provided as part of an IPMX info block supported by the Receiver, PATCH the latest SDP transport file from a Sender to the Receiver, otherwise let the Receiver handle the SDP transport file changes from the info block.

## HKEP

A Receiver SHOULD provide a `urn:x-matrox:cap:transport:hkep` capability to indicate its support for IPMX Senders HDCP encryption and the HKEP protocol. The capability value `true` indicates the support of HDCP encryption and the HKEP protocol. The capability value `false` indicates that HDCP encryption and the HKEP protocol are not supported.

A Receiver MAY support either or both true and false values.

A Controller MUST verify the compliance of the Receiver with a Sender using HDCP encryption from the SDP transport file `hkep` attribute. The presence of such attribute in an SDP transport file indicate that the stream is HDCP protected. Only Receivers supporting HDCP encryption and the HKEP protocol can consume such streams.

## Privacy

A Receiver SHOULD provide a `urn:x-matrox:cap:transport:privacy` capability to indicate its support for IPMX Senders privacy encryption and the PEP protocol. The capability value `true` indicates the support of privacy encryption and the PEP protocol. The capability value `false` indicates that privacy encryption and the PEP protocol are not supported.

A Receiver MAY support either or both true and false values.

A Controller MUST verify the compliance of the Receiver with a Sender using privacy encryption from the SDP transport file `privacy` attribute. The presence of such attribute in an SDP transport file indicate that the stream is privacy protected. Only Receivers supporting privacy encryption and the PEP protocol can consume such streams. The fine grained Receiver privacy capabilities are provided as part of the associated Receiver's transport parameters constraints.

## Channel Order

A Receiver SHOULD provide a `urn:x-matrox:cap:transport:channel_order` capability for opaque AM824 multiplexed audio streams to indicate its support for IPMX Senders transparent transport of AES3 streams. The channel_order MUST follow the SMPTE2110 `channel-order` convention. The `channel_order` capability allows a Receiver to describe the number of audio sub-streams that it supports and for each the channels configuration and wether it is linear PCM or non-PCM data.

A Controller MAY verify the compliance of the Receiver with a Sender using the Sender's SDP transport file and check for the format specific `channel-order` parameter.

## Audio layers

A Receiver SHOULD provide a `urn:x-matrox:cap:transport:audio_layers` capability for fully described AM824 multiplexed audio streams to indicate its support for IPMX Senders transparent transport of AES3 streams. The `audio_layers` capability allows a Receiver to describe the number of audio sub-streams that it supports. A Receiver SHOULD also provide sub-streams capabilities for each audio layer to indicate what audio sub-streams it supports.

A Controller MAY verify the compliance of the Receiver with a Sender using the Sender's SDP transport file format specific `channel-order` parameter and the Sender's mux Flow atributes and parent sub-Flows attributes.

A Controller MAY use IS-11 to constrain the Sender's sub-Flows to make them compliant with the Receiver.

[RFC-2119]: https://tools.ietf.org/html/rfc2119 "Key words for use in RFCs"
[IS-04]: https://specs.amwa.tv/is-04/ "AMWA IS-04 NMOS Discovery and Registration Specification"
[IS-05]: https://specs.amwa.tv/is-05/ "AMWA IS-05 NMOS Device Connection Management Specification"
[NMOS Parameter Registers]: https://specs.amwa.tv/nmos-parameter-registers/ "Common parameter values for AMWA NMOS Specifications"
