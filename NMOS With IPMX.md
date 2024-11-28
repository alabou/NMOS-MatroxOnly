# BCP-???-??: NMOS With IPMX
 
{:toc}

## Introduction

This document presents the various aspects of using IPMX compliant Senders and Receivers in an NMOS environment and complements the IPMX technical recommendations, most specifically the [TR-10-8][] (NMOS Requirements), [TR-10-5][] (HDCP Key Exchange Protocol - HKEP), [TR-10-13][] (Privacy Encryption Protocol - PEP), [TR-10-1][] (System Timing and Definitions) technical recommendations. Some of the aspects presented in this document are not specific to IPMX compliant devices and apply to the larger family of ST 2110 compliant devices.

## Use of Normative Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY",
and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119][RFC-2119].

## Definitions

The NMOS terms 'Controller', 'Node', 'Source', 'Flow', 'Sender', 'Receiver' are used as defined in the [NMOS Glossary](https://specs.amwa.tv/nmos/main/docs/Glossary.html).

## Common Reference Clock

A Receiver SHOULD provide a `urn:x-nmos:cap:transport:clock_ref_type` capability to indicate its support for IPMX Senders not using a common reference clock (PTP). The capability value `ptp` indicates the support of a common reference clock (PTP) while the value `internal` indicates the support of an internal clock (not PTP).

A Receiver MAY support either or both clock reference types.

A Controller MAY verify the compliance of the Receiver with a Sender using the Sender's SDP transport file and check for the a=ts-refclk attribute. It MAY also verify the compliance using the Sender's associated Source `clock_name` attribute and checking the clock's `ref_type` atribute.

A Sender MAY provide a `urn:x-nmos:cap:transport:clock_ref_type` capability to indicate the reference clocks that it supports. A controller MAY use Sender capabilities, if supported, to verify the compliance of a Receiver with a Sender and if necessary constrain the Sender to make it compliant with the Receivers. A Sender indicates that it supports being constrained for such capability by enumerating the `urn:x-nmos:cap:transport:clock_ref_type` capability in its [IS-11][] `constraints/supported` endpoint.

## Asynchronous/Synchronous Media

A Receiver SHOULD provide a `urn:x-nmos:cap:transport:synchronous_media` capability to indicate its support for IPMX Senders media that is synchronous to the Sender's reference clock. The capability value `true` indicates the support of synchronous media while the value `false` indicates the support of asynchronous media.

A Receiver MAY support either or both clock reference types.

A Controller MAY verify the compliance of the Receiver with a Sender using the Sender's SDP transport file and check for the a=mediaclk attribute. It MAY also verify the compliance using the Sender's associated Source `urn:x-nmos:synchronous_media` attribute.

A Sender MAY provide a `urn:x-nmos:cap:transport:synchronous_media` capability to indicate the media synchronisation that it supports. A controller MAY use Sender capabilities, if supported, to verify the compliance of a Receiver with a Sender and if necessary constrain the Sender to make it compliant with the Receivers. A Sender indicates that it supports being constrained for such capability by enumerating the `urn:x-nmos:cap:transport:synchronous_media` capability in its [IS-11][] `constraints/supported` endpoint.

## Info Block

A Receiver SHOULD provide a `urn:x-nmos:cap:transport:info_block` capability to indicate its support for IPMX Senders media info blocks (in RTCP Sender Report). The capability SHOULD enumerate the media info block types (integer) supported by the Receiver. An empty enumeration indicate that the Receiver does not support IPMX in-band media info block. Enumerating the value 0 which is an invalid media info block type identifier serves the same purpose.

A Receiver MAY support none, some or all the IPMX media info block types.

When media stream attributes associated with a Sender change, a Controller MAY let the Receiver handle the media stream attributes changes from the media info blocks produced by the Sender, if all the media info block types produced by a Sender are supported by the Receiver.

A Sender SHOULD provide a `urn:x-nmos:cap:transport:info_block` capability to indicate the media info block types that it generates. A controller MAY use Sender capabilities, if supported, to verify the compliance of a Receiver with a Sender. It is not allowed to constrain a Sender for such capability as info blocks are a required feature of IPMX.

> Note: VSF_TR-10-0 "Media Info block Type" section presents the various IPMX info block types.

## HKEP

A Receiver SHOULD provide a `urn:x-nmos:cap:transport:hkep` capability to indicate its support for IPMX Senders HDCP encryption and the HKEP protocol. The capability value `true` indicates the support of HDCP encryption and the HKEP protocol. The capability value `false` indicates that HDCP encryption and the HKEP protocol are not supported.

A Receiver MAY support either or both true and false values.

A Controller MUST verify the compliance of the Receiver with a Sender using HDCP encryption and the HKEP protocol from the SDP transport file `hkep` attribute. The presence of such attribute in an SDP transport file indicate that the stream is HDCP protected. Only Receivers supporting HDCP encryption and the HKEP protocol can consume such streams.

A Sender MAY provide a `urn:x-nmos:cap:transport:hkep` capability to indicate that HDCP encryption and the HKEP protocol are supported. A Sender MAY support either or both true and false values. A controller MAY use Sender capabilities, if supported, to verify the compliance of a Receiver with a Sender and if necessary constrain the Sender to make it compliant with the Receivers. A Sender constrained to `false` for such capability MUST NOT be part of an HDCP topology and MUST NOT access/produce/stream HDCP protected content. A Sender indicates that it supports being constrained for such capability by enumerating the `urn:x-nmos:cap:transport:hkep` capability in its [IS-11][] `constraints/supported` endpoint.

Informative Note: A Sender indicating both `true` and `false` values in its capabilities describes that it may produce both HDCP and non-HDCP streams according to some internal criteria evaluated at activation time. 

### HDCP Content Protection

A Receiver implementing [BCP-008-01][] supporting HDCP encryption and the HKEP protocol MAY notify that the HDCP content protection system prevents the Receiver from accessing or re-transmitting HDCP content using the `streamStatus` and `streamStatusMessage` properties of the Receiver's associated `NcReceiverMonitor`.

A Sender implementing [BCP-008-02][] supporting HDCP encryption and the HKEP protocol MAY notify that the HDCP content protection system prevents the Sender from accessing or re-transmitting HDCP content using the `essenceStatus` and `essenceStatusMessage` properties of the Sender's associated `NcSenderMonitor`.

### RTP Payload Header

Refer to the "Privacy" section "RTP Payload Header" sub-section for the detailed definition of an RTP Payload Header for various audio and video media types. Those definitions MUST be used to determine the part of the RTP Payload that is HDCP encrypted.

## Privacy

A Receiver SHOULD provide a `urn:x-nmos:cap:transport:privacy` capability to indicate its support for IPMX Senders privacy encryption and the PEP protocol. The capability value `true` indicates the support of privacy encryption and the PEP protocol. The capability value `false` indicates that privacy encryption and the PEP protocol are not supported.

A Receiver MAY support either or both true and false values.

A Controller MUST verify the compliance of the Receiver with a Sender using privacy encryption and the PEP protocol from the SDP transport file `privacy` attribute. The presence of such attribute in an SDP transport file indicate that the stream is privacy protected. Only Receivers supporting privacy encryption and the PEP protocol can consume such streams. The fine grained Receiver privacy capabilities are provided as part of the associated Receiver's IS-05 transport parameters constraints.

A Sender MAY provide a `urn:x-nmos:cap:transport:privacy` capability to indicate that privacy encryption and the PEP protocol are supported. A Sender MAY support either true or false values. A controller MAY use Sender capabilities, if supported, to verify the compliance of a Receiver with a Sender. It is not allowed to constrain a Sender for such capability as PEP is a protection mechanism under the control of the Sender. The fine grained Sender privacy capabilities are provided as part of the associated Sender's IS-05 transport parameters constraints.

A Controller MAY configure Senders and Receivers privacy encryption parameters through their assocaited IS-05 transport parameters on activation. See the "NMOS With Privacy Encryption" document for more details.

Informative Note: A Sender is configured by an administrator to produce either privacy encrypted streams or non-encrypted streams. The Sender  `urn:x-nmos:cap:transport:privacy` capability indicates the current configuration.

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

A Receiver SHOULD provide a `urn:x-nmos:cap:transport:channel_order` capability for opaque AM824 multiplexed audio streams to indicate its support for IPMX Senders transparent transport of AES3 streams. The capability MUST follow the ST 2110 `channel-order` convention. The `channel_order` capability allows a Receiver to describe the number of audio sub-streams that it supports and for each one, the channels configuration and wether it is linear PCM or non-PCM data.

A Controller MAY verify the compliance of the Receiver with a Sender using the Sender's SDP transport file and check for the format specific `channel-order` parameter.

A Sender MAY provide a `urn:x-nmos:cap:transport:channel_order` capability to indicate the channels ordering that are supported. A controller MAY use Sender capabilities, if supported, to verify the compliance of a Receiver with a Sender and if necessary constrain the Sender to make it compliant with the Receivers. A Sender indicates that it supports being constrained for such capability by enumerating the `urn:x-nmos:cap:transport:channel_order` capability in its [IS-11][] `constraints/supported` endpoint.

## Group Hint

Senders and Receivers MUST declare a "urn:x-nmos:tag:grouphint/v1.0" tag in their `tags` attribute.

The "urn:x-nmos:tag:grouphint/v1.0" tag array MUST comprise a single string formatted as follow:

`"<group-descriptor>:<role-in-group> <role-index>"`

The `<group-descriptor>`, `<role-in-group>`, `<role-index>` sequences MUST be replaced with the proper value as defined in the following sections. The `<group-descriptor>` MUST be a sequence of printable characters excluding `:` as `[a-zA-Z0-9!"#$%&'()*+,-./;<=>?@[\\\]^_{|}~ ]`. The `<role-in-group>` MUST be a sequence of the letters [a-zA-Z]. The `<role-index>` MUST be a decimal number where the leftmost digit MUST not be '0' unless the value is zero. The `<role-in-group>` and `<role-index>` sequences MUST be separated by a single space. The `<group-descriptor>` and `<role-in-group>` MUST be separated by a colon ':'.

The scope is always `device` which is the default value as per [Group Hint](https://specs.amwa.tv/nmos-parameter-registers/branches/main/tags/grouphint.html#group-hint-urn).

### Format

A `<role-in-group>` is associated with the format of a Sender or Receiver. For the formats `urn:x-nmos:format:video`, `urn:x-nmos:format:audio`, `urn:x-nmos:format:data` and `urn:x-nmos:format:mux` the `<role-in-group>` MUST be "VIDEO", "AUDIO", "DATA" and "MUX" respectively.

### Layer

The `<role-index>` is associated with the concept of "layer" of sub-Flows/sub-Streams and independent streams. For independent Senders/Receivers it describes an ordering of the independent Senders/Receivers for a given role/format. The `<role-index>` MUST start at 0 and increment for each succesive layer of the same format. The `<role-index>` values MUST be consecutive integer values starting at 0.

### Senders

The `<group-descriptor>` value for a Sender "urn:x-nmos:tag:grouphint/v1.0" tag MUST be unique among the various groups of Senders within a Device. The groups of Senders SHOULD be considered independent of the groups of Receivers within a Device. Identical `<group-descriptor>` groups for Senders and Receivers have no special meaning and are allowed.

### Receivers

The `<group-descriptor>` value for a Receiver "urn:x-nmos:tag:grouphint/v1.0" tag MUST be unique among the various groups of Receivers within a Device. The groups of Receivers SHOULD be considered independent of the groups of Senders within a Device. Identical `<group-descriptor>` groups for Senders and Receivers have no special meaning and are allowed.

[RFC-2119]: https://tools.ietf.org/html/rfc2119 "Key words for use in RFCs"
[IS-04]: https://specs.amwa.tv/is-04/ "AMWA IS-04 NMOS Discovery and Registration Specification"
[IS-05]: https://specs.amwa.tv/is-05/ "AMWA IS-05 NMOS Device Connection Management Specification"
[IS-11]: https://specs.amwa.tv/is-11/ "AMWA IS-11 NMOS Stream Compatibility Management Specification"
[NMOS Parameter Registers]: https://specs.amwa.tv/nmos-parameter-registers/ "Common parameter values for AMWA NMOS Specifications"
[TR-10-1]: https://vsf.tv/download/technical_recommendations/VSF_TR-10-1_2024-02-23.pdf "System Timing and Definitions"
[TR-10-5]: https://vsf.tv/download/technical_recommendations/VSF_TR-10-5_2024-02-23.pdf "HDCP Key Exchange Protocol - HKEP"
[TR-10-8]: https://vsf.tv/download/technical_recommendations/VSF_TR-10-8_2024-02-23.pdf "NMOS Requirements"
[TR-10-13]: https://vsf.tv/download/technical_recommendations/VSF_TR-10-13_2024-01-19.pdf "Privacy Encryption Protocol - PEP"
[BCP-008-01]: https://specs.amwa.tv/bcp-008-01/ "NMOS Receiver Status"
[BCP-008-02]: https://specs.amwa.tv/bcp-008-02/ "NMOS Sender Status"