# Matrox: NMOS With H.265
{:.no_toc}  
Copyright 2023, Matrox Graphics Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
  
---
  
{:toc}

---
## Introduction

H.265 is a video compression technology standardized in Rec. [ITU-T H.265][H.265] | ISO/IEC 23008-2.
A companion RTP payload format specification was developed through the IETF Payloads working group, IETF [RFC 7798][RFC-7798] for the transport of an H.265 bitstream over RTP.

The BCP-006-03 specification includes support for bitstreams that are compliant with the clauses of the main document and annexes A, B, C, D and E of the Rec. [ITU-T H.265][H.265] specification. It excludes support for bitstreams that are compliant with other annexes of the specification.
> Annex F (multi-layers extensions), Annex G (multiview high efficiency video coding), Annex H (scalable high efficiency video coding) and Annex I (3D high efficiency video coding) are not supported.

The Rec. [ITU-T H.222.0][H.222.0] | ISO/IEC 13818-1 specification and associated amendments describe the embedding of an H.265 stream in an MPEG2-TS transport stream. An RTP payload format specification for MPEG2-TS transport stream was developed through the IETF Payloads working group, IETF [RFC 2250][RFC-2250] for transport over RTP. Other normative documents describe the requirements for the streaming of an MPEG2-TS transport stream over other non-RTP transports.

The [Society of Media Professionals, Technologists and Engineers][SMPTE] developed Standard [ST 2110-22][ST-2110-22] of the ST 2110 suite of protocols, which cover the end-to-end application use of constant bit rate compression for video over managed IP networks.

> Note that the definition of constant bit rate of ST 2110-22 is very strict. "The video compression or the packetization of the video compression shall produce a constant number of bytes per frame. The packetization shall produce a constant number of RTP packets per frame." This definition of constant bit rate is hereafter described as strict-CBR, using the H.265 definition of constant bit rate for CBR.

The [Video Services Forum][VSF] developed Technical Recommendation [TR-10-11][TR-10-11] and [TR-10-7][TR-10-7] of the IPMX suite of protocols, which cover the end-to-end application use of constant and variable bit rate compression for video, using the SMPTE ST 2110 and IPMX suite of protocols.

TR-10-11 and TR-10-7 mandate the use of the AMWA [IS-04][IS-04] and [IS-05][IS-05] NMOS Specifications in IPMX compliant systems.

AMWA IS-04 and IS-05 have support for various transport protocols and can signal the media type `video/H265` as defined in RFC 7798.

## Use of Normative Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY",
and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119][RFC-2119].

## Definitions

The NMOS terms 'Controller', 'Node', 'Source', 'Flow', 'Sender', 'Receiver' are used as defined in the [NMOS Glossary](https://specs.amwa.tv/nmos/main/docs/Glossary.html).

The term 'strict-CBR' corresponds to the definition of constant bit-rate at section 4 "Video Compression and Packetization" of the ST 2110-22 standard.

The terms CBR and VBR are defined in the Rec. [ITU-T H.265][H.265] standard.

## H.265 IS-04 Sources, Flows and Senders

Nodes capable of transmitting H.265 video streams MUST have Source, Flow and Sender resources in the IS-04 Node API.

### Sources

The Source resource MUST indicate `urn:x-nmos:format:video` for the `format` attribute. 
- Source resources MAY be associated with many Flows at the same time. The Source is therefore unaffected by the use of H.265 compression.

### Flows

The Flow resource MUST indicate `video/H265` in the `media_type` attribute, and `urn:x-nmos:format:video` for the `format` attribute. This has been permitted since IS-04 v1.1. 
- H.265 Flow resources MAY be associated with many Senders at the same time through the Senders' `flow_id` attributes. The H.265 Flow is therefore unaffected by the use of a specific transport. 
- H.265 Flow resources MAY be associated with many Flows at the same time through the Flows' `parents` attributes. The H.265 Flow is therefore unaffected by being the parent of some other Flows.

For Nodes implementing IS-04 v1.3 or higher, the following additional requirements on the Flow resource apply.

In addition to those attributes defined in IS-04 for all coded video Flows, the following attributes defined in the [Flow Attributes Register](https://specs.amwa.tv/nmos-parameter-registers/branches/main/flow-attributes/) of the [NMOS Parameter Registers][] are used for H.265.

These attributes provide information for Controllers and Users to evaluate stream compatibility between Senders and Receivers.

- [Components](https://specs.amwa.tv/nmos-parameter-registers/branches/main/flow-attributes/#components)  
  The Flow resource MUST indicate the color (sub-)sampling, width, height and depth of the associated uncompressed picture using the `components` attribute. The `components` array values MUST correspond to the stream's active parameter sets. A Flow MUST track the stream's current active parameter sets.

- [Profile](https://specs.amwa.tv/nmos-parameter-registers/branches/main/flow-attributes/#profile)  
  The Flow resource MUST indicate the H.265 profile, which defines algorithmic features and limits that MUST be supported by all decoders conforming to that profile. The stream's active parameter sets MUST be compliant with the `profile` attribute of the Flow. The permitted `profile` values are strings, defined as per Rec. ITU-T H.265 Annex A

  - "Main", "Main-444"
  - "MainStillPicture", "MainStillPicture-444"
  - "Main10StillPicture"
  - "Main16StillPicture-444"
  - "Main10", "Main10-422", "Main10-444"
  - "Main12", "Main12-422", "Main12-444"
  - "MainIntra", "MainIntra-444"
  - "Main10Intra", "Main10Intra-422", "Main10Intra-444"
  - "Main12Intra", "Main12Intra-422", "Main12Intra-444"
  - "Main16Intra-444"
  - "Monochrome"
  - "Monochrome10"
  - "Monochrome12"
  - "Monochrome16"
  - "HighThroughput-444"
  - "HighThroughput10-444"
  - "HighThroughput14-444"
  - "HighThroughput16Intra-444"
  - "ScreenExtendedMain","ScreenExtendedMain-444"
  - "ScreenExtendedMain10", "ScreenExtendedMain10-444"
  - "ScreenExtendedHighThroughput-444"
  - "ScreenExtendedHighThroughput10-444"
  - "ScreenExtendedHighThroughput14-444"

  Informative note: The names of the profiles in string form have been derived from the names used at Annex A of the H.265 standard with whitespace omitted and the sampling mode always positioned at the end of the string, preceded by a '-'.

  The profile strings in this specification are included in the [NMOS Parameter Registers][]. Additional strings may be added there in the future.

  The Flow's `profile` attribute maps to the `profile-space`, `profile-id`, `profile-compatibility-indicator`, `interop-constraints` parameters of the SDP transport file. See the [SDP format-specific parameters](#sdp-format-specific-parameters) section.

  The Flow's `profile` attribute maps to the members profile_space, profile_idc, profile_compatibility_indication, progressive_source_flag, interlaced_source_flag, non_packed_constraint_flag, frame_only_constraint_flag and copied_44bits and  of the HEVC_video_descriptor of an MPEG2-TS transport stream. See the [RTP transport based on RFC 2250](#rtp-transport-based-on-rfc-2250) section.

- [Level](https://specs.amwa.tv/nmos-parameter-registers/branches/main/flow-attributes/#level)  
  The Flow resource MUST indicate the H.265 level, which defines a set of limits on the values that may be taken by the syntax elements of an H.265 bitstream. The stream's active parameter sets MUST be compliant with the `level` attribute of the Flow. The permitted `level` values are strings, defined as per Rec. ITU-T H.265 Annex A

  - "Main-1"
  - "Main-2", "Main-2.1"
  - "Main-3"
  - "Main-3.1"
  - "Main-4", "Main-4.1"
  - "Main-5", "Main-5.1", "Main-5.2"
  - "Main-6", "Main-6.1", "Main-6.2"
  - "High-4", "High-4.1"
  - "High-5", "High-5.1", "High-5.2"
  - "High-6", "High-6.1", "High-6.2"
  - "High-8.5"

  Informative note: The names of the levels in string form have been derived from the names used at Annex A of the H.265 standard where the tier name prefixes the level number.

  The level strings in this specification are included in the [NMOS Parameter Registers][]. Additional strings may be added there in the future.

  The Flow's `level` attribute map to the `level-id` and `tier-flag` parameters of the SDP transport file. See the [SDP format-specific parameters](#sdp-format-specific-parameters) section.

  The Flow's `level` attribute map to the members level_idc and tier_flag of the HEVC_video_descriptor of an MPEG2-TS transport stream. See the [RTP transport based on RFC 2250](#rtp-transport-based-on-rfc-2250) section.

Informative note: The Flow's `profile` and `level` attributes are always required. The SDP transport file `profile-space`, `profile-id`, `profile-compatibility-indicator`, `interop-constraints`, `level-id` and `tier-flag` parameters may be omitted when matching the default value.

- [Bit Rate](https://specs.amwa.tv/nmos-parameter-registers/branches/main/flow-attributes/#bit-rate)  
  The Flow resource MUST indicate the target encoding bit rate (kilobits/second) of the H.265 bitstream. The stream's active parameter sets MUST be compliant with the `bit_rate` attribute of the Flow. The `bit_rate` integer value is expressed in units of 1000 bits per second, rounding up.

  Informative note: The H.265 bitstream is not required to transport hypothetical reference decoder (HRD) parameters such that an H.265 decoder may not know the actual target bit rate of a stream. There are bit rate limits imposed by the level of the coded bitstream. IS-11 may be used to constrain the Sender to a target bit rate compatible with the Receiver Capabilities.

- [Constant Bit Rate](https://specs.amwa.tv/nmos-parameter-registers/branches/main/flow-attributes/#constant-bit-rate)  
  The Flow resource MUST indicate if it operates in constant bit rate (CBR) mode or variable bit rate mode (VBR or other). When operating in constant bit rate mode the `bit_rate` corresponds to the constant encoding bit rate. Otherwise it corresponds to the maximum encoding bit rate. Since the default value of this attribute is `false`, a Flow MAY omit this attribute when using a variable bit rate mode.

Informative note: The maximum bit rate information relates to the codec profile / level limits and the HRD buffering model. The CBR versus VBR mode of operation of the encoder provide essential clues about the coded bitstream produced.

Informative note: For streams compliant with ST 2110-22, the constant bit rate mode is more appropriately described as a strict-CBR mode where "the video compression or the packetization of the video compression shall produce a constant number of bytes per frame. The packetization shall produce a constant number of RTP packets per frame." For other streams, not compliant with ST 2110-22, it is the constant bit rate definition of the H.265 specification that prevails.

A Sender MUST declare its compliance to ST 2110-22 with the SSN parameter of the fmtp attribute of the SDP transport file set to one of "ST2110-22:2019" or "ST2110-22:2022". A Sender not declaring an SSN parameter or declaring one that does not start with "ST2110-22" SHOULD be assumed as not being compliant to ST 2110-22.

The H.265 encoder associated with the Flow MUST produce an H.265 bitstream that is compliant with the `profile` and `level` attributes. The bitstream NAL units MUST have nuh_layer_id set to zero.

Examples Flow resources are provided in [Examples](../examples/).

### Senders

This section applies to a Sender directly associated with an H.265 Flow through the Sender's `flow_id` attribute.

Informative note: When an H.265 Flow is not directly associated with a Sender but with a multiplexed Flow through the Flow's parents attribute, the Sender does not provide H.265 format-specific attributes. A Sender provides such attributes only when the H.265 Flow is directly associated with it. The attributes `parameter_sets_flow_mode` and `parameter_sets_transport_mode` associated with an H.265 Flow that are described in this section get their respective default value of `dynamic` and `in_band`. 

For multiplexed H.265 Flows, the Sender MUST conform to the behaviour dictated by the `dynamic` and `in_band` modes described in this specification.

Sender resources provide no indication of media type or format, since this is described by the associated Flow resource.

#### RTP transport based on RFC 7798

For Nodes transmitting H.265 using the RTP payload mapping defined by RFC 7798, the Sender resource MUST indicate `urn:x-nmos:transport:rtp` or one of its subclassifications for the `transport` attribute.

For Nodes implementing IS-04 v1.3 or higher, the following additional requirements on the Sender resource apply.

In addition to those attributes defined in IS-04 for Senders, the following attributes defined in the [Sender Attributes Register](https://specs.amwa.tv/nmos-parameter-registers/branches/main/sender-attributes/) of the NMOS Parameter Registers are used for H.265.

- [Bit Rate](https://specs.amwa.tv/nmos-parameter-registers/branches/main/sender-attributes/#bit-rate)  
  The Sender resource SHOULD indicate the target bit rate (kilobits/second) including the transport overhead of the H.265 stream. The value is for the IP packets, so for the RTP payload format per RFC 7798, that includes the RTP, UDP and IP packet headers and the payload. The `bit_rate` integer value is expressed in units of 1000 bits per second, rounding up. The Sender's transport `bit_rate` indicates a constant bit rate or a maximum bit rate depending on the `constant_bit_rate` attribute of the associated Flow. 

  If the Sender meets the traffic shaping and delivery timing requirements specified for ST 2110-22 it MUST indicate the transport `bit_rate`.

  Informative note: This definition is consistent with the definition of the bit rate attribute (`b=` line) required by ST 2110-22 in the SDP media description. This SDP attribute is not specified in RFC 7798.

- [Packet Transmission Mode](https://specs.amwa.tv/nmos-parameter-registers/branches/main/sender-attributes/#packet-transmission-mode)  
  A Sender using the interleaved mode MUST include the `packet_transmission_mode` attribute and set it to `interleaved_nal_units`. The `packet_transmission_mode` attribute maps the the RFC 7798 `sprop-max-don-diff` parameter with `non_interleaved_nal_units` corresponding to value 0, `interleaved_nal_units` to value greater than 0. Since the default value of this attribute is `non_interleaved_nal_units`, the Sender MAY omit this attribute when using that mode.

  PAyload Content Information (PACI) packets MUST not be produced by a Sender conforming to this specification.

- [ST 2110-21 Sender Type](https://specs.amwa.tv/nmos-parameter-registers/branches/main/sender-attributes/#st-2110-21-sender-type)  
  If the Sender complies with the traffic shaping and delivery timing requirements for ST 2110-22, it MUST include the `st2110_21_sender_type` attribute.

- [Parameter Sets Flow Mode](https://specs.amwa.tv/nmos-parameter-registers/branches/main/sender-attributes/#parameter-sets-flow-mode)  
  A Sender MUST set the `parameter_sets_flow_mode` attribute to `strict` if operating within the necessary restrictions for this mode, or `static` if operating within the necessary restrictions for that mode. Otherwise it MAY omit or set the `parameter_sets_flow_mode` attribute to `dynamic`. If unspecified the default value is `dynamic`. See the [Parameter Sets](#parameter-sets) section for more details.

- [Parameter Sets Transport Mode](https://specs.amwa.tv/nmos-parameter-registers/branches/main/sender-attributes/#parameter-sets-transport-mode)  
  A Sender operating with out-of-band parameter sets MUST set the `parameter_sets_transport_mode` attribute to either `out_of_band` or `in_and_out_of_band`. Otherwise it MAY omit or set the `parameter_sets_transport_mode` attribute to `in_band`. If unspecified the default value is `in_band`. See the [Parameter Sets](#parameter-sets) section for more details.

An example Sender resource is provided in the [Examples](../examples/).

##### SDP format-specific parameters

The SDP file at the `manifest_href` MUST comply with the requirements of RFC 7798 in the [Usage in Declarative Session Descriptions](https://www.rfc-editor.org/rfc/rfc7798.html#section-7.2.3) mode of operation. The SDP Offer/Answer Model described in Section 7.2.2 of RFC 7798 is not supported. The `fmtp` source attribute as specified in Section 6.3 of [RFC 5576][RFC-5576] is not supported, i.e. use-level-src-parameter-sets parameter is not present or equal 0. The `tx-mode` parameter of the SDP transport file MUST always be set to SRST (Single RTP Stream Transport).

Additionally, the SDP transport file needs to convey, so far as the defined format-specific parameters allow, the same information about the stream as conveyed by the Source, Flow and Sender attributes defined by this specification and IS-04, unless such information is conveyed through in-band parameter sets.

Therefore:

- The `profile-space`, `profile-id`, `profile-compatibility-indicator`, `interop-constraints`, `level-id` and `tier-flag` format-specific parameters MUST be included with the correct value unless it corresponds to the default value. "Main" is the default profile value and "Main-3.1" is the default level value (tier-flag 0, level-id 3.1).

- The `sprop-max-don-diff` format-specific parameters MUST be included with the correct value unless it corresponds to the default value.

- The `sprop-depack-buf-nalus`, `sprop-depack-buf-bytes` format-specific parameters SHOULD be included with the correct value if `sprop-max-don-diff` is not 0 unless it corresponds to the default value.

- The `sprop-vps`, `sprop-sps` and `sprop-pps` MUST always be included if the Sender `parameter_sets_transport_mode` attribute is `out_of_band`.

The stream's active parameter sets MUST be compliant with the format-specific parameters, except `sprop-vps`, `sprop-sps` and `sprop-pps`, declared in the "fmtp=" attribute of an SDP transport file.

If the Sender meets the traffic shaping and delivery timing requirements specified for ST 2110-22, the SDP transport file MUST also comply with the provisions of ST 2110-22.

Informative note: ST 2110-22 does not require the `sampling` or `depth` SDP parameters. RFC 7798 does not define any such SDP parameters. The `sampling` and `depth` of the associated uncompressed picture could be derived from the H.265 active parameter sets by a Receiver.

If the Sender meets the traffic shaping and delivery timing requirements specified for IPMX, the SDP transport file MUST also comply with the provisions of IPMX.

An example SDP file is provided in the [Examples](../examples/).

#### Other transports

For Nodes transmitting H.265 using other transports, the Sender resource MUST indicate the associated `urn:x-nmos:transport:` or `urn:x-matrox:transport:` label of the transport or one of its subclassifications for the `transport` attribute.

Sender resources provide no indication of media type or format, since this is described by the associated Flow resource.

The `manifest_href` attribute MAY be `null` if an SDP transport file is not supported by the transport. Otherwise the SDP transport file MUST comply with the transport specific requirements. There is no SDP format-specific parameters requirements for transports other than RTP.

- [Parameter Sets Flow Mode](https://specs.amwa.tv/nmos-parameter-registers/branches/main/sender-attributes/#parameter-sets-flow-mode)  
  A Sender MUST set the `parameter_sets_flow_mode` attribute to `strict` if operating within the necessary restrictions for this mode, or `static` if operating within the necessary restrictions for that mode. Otherwise it MAY omit or set the `parameter_sets_flow_mode` attribute to `dynamic`. If unspecified the default value is `dynamic`. See the [Parameter Sets](#parameter-sets) section for more details.

- [Parameter Sets Transport Mode](https://specs.amwa.tv/nmos-parameter-registers/branches/main/sender-attributes/#parameter-sets-transport-mode)  
  A Sender operating with out-of-band parameter sets MUST set the `parameter_sets_transport_mode` attribute to either `out_of_band` or `in_and_out_of_band`. Otherwise it MAY omit or set the `parameter_sets_transport_mode` attribute to `in_band`. If unspecified the default value is `in_band`. See the [Parameter Sets](#parameter-sets) section for more details.

  Informative note: The out of band mechanism used to transmit parameter sets is transport specific and out of the scope of this specification.

## H.265 IS-04 Receivers

Nodes capable of receiving H.265 video streams MUST have Receiver resources in the IS-04 Node API.

This section applies to a Receiver directly or indirectly associated with an H.265 stream.

Informative note: When an H.265 stream is directly associated with a Receiver, the Receiver has `format` set to `urn:x-nmos:format:video` and `media_types` of the `caps` attribute contains `video/H265`. When an H.265 stream is part of a multiplexed stream and is indirectly associated with a Receiver, the Receiver has `format` set to `urn:x-nmos:format:mux`, `media_types` of the `caps` attribute does not contains `video/H265` and `constraint_sets` of the `caps` attribute contains `video/H265`.

Informative note: In the following text the word "stream" is used to indicate either an H.265 stream or an H.265 sub-stream depending on the direct verus indiret asssociation with the Receiver.

For a Receiver directly associated with an H.265 stream, the Receiver resource MUST indicate `urn:x-nmos:format:video` for the `format` attribute and MUST list `video/H265` in the `media_types` array within the `caps` object. This has been permitted since IS-04 v1.1.

For a Receiver indirectly associated with an H.265 stream part a multiplexed stream, the Receiver resource MUST indicate `urn:x-nmos:format:mux` for the `format` attribute, MUST list the mux media type in the `media_types` array within the `caps` object and MUST list a constraint set indicating support for the media type `video/H265` in the `constraint_sets` array within the `caps` object.

If the Receiver has limitations on or preferences regarding the H.265 video streams that it supports, the Receiver resource MUST indicate constraints in accordance with the [BCP-004-01][] Receiver Capabilities specification. The Receiver SHOULD express its constraints as precisely as possible, to allow a Controller to determine with a high level of confidence the Receiver's compatibility with the available streams. It is not always practical for the constraints to indicate every type of stream that a Receiver can or cannot consume successfully; however, they SHOULD describe as many of its commonly used operating points as practical and any preferences among them.

The `constraint_sets` parameter within the `caps` object MUST be used to describe combinations of frame rates, width and height, and other parameters which the receiver can support, using the parameter constraints defined in the [Capabilities register](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/) of the NMOS Parameter Registers.

When the H.265 decoder has no restrictions on the value of some parameter, the Receiver can indicate that the parameter is unconstrained, as described in BCP-004-01. 

The following parameter constraints can be used to express limits or preferences specifically defined by Rec. ITU-T H.265 for H.265 decoders:

- [Profile](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#profile)  
  Some H.265 profiles are superset of other profiles. The H.265 specification describe the relationship among the profiles. From the point of view of the H.265 specification, supporting such superset profile is required to also be supporting the associated subset profiles. To assist a Controller not having knowledge of the H.265 profiles relationship, the Receiver Capabilities SHOULD enumerate subset profiles in addition to the superset profile.

- [Level](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#level)  
  Some H.265 levels are superset of other levels. The H.265 specification describe the relationship among the levels. From the point of view of the H.265 specification, supporting such superset level is required to also be supporting the associated subset levels. To assist a Controller not having knowledge of the H.265 levels relationship, the Receiver Capabilities SHOULD enumerate all the subset levels in addition to the superset level.

- [Bit Rate](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#format-bit-rate)
- [Constant Bit Rate](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#format-constant-bit-rate)

A Receiver MUST be able to decode bitstreams conforming to the profiles and levels declared in the Receiver Capabilities. A Receiver MAY have preferences and more optimal profiles and levels that MAY be declared through Receiver Capabilities. A preferred constraint set MAY indicate such preferences while another constraint set MAY indicate full support of some profiles and levels. A Receiver MAY further constrain the support of a coded bitstream compliant with a profile and level using other constraints in its Receiver Capabilities.

Other existing parameter constraints, such as the following, are also appropriate to express limitations on supported H.265 video streams:

- [Frame Width](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#frame-width)
- [Frame Height](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#frame-height)
- [Grain Rate](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#grain-rate)
- [Color Sampling](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#color-sampling)
- [Component Depth](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#component-depth)
- [Colorspace](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#colorspace)
- [Transfer Characteristic](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#transfer-characteristic)
- [ST 2110-21 Sender Type](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#st-2110-21-sender-type)

An example Receiver resource is provided in the [Examples](../examples/).

### RTP transport based on RFC 7798

For Nodes consuming H.265 using the RTP payload mapping defined by RFC 7798, the Receiver resource MUST indicate `urn:x-nmos:transport:rtp` or one of its subclassifications for the `transport` attribute.

The following parameter constraints can be used to express limits or preferences specifically defined for H.265 decoders:

- [Bit Rate](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#transport-bit-rate)

- [Packet Transmission Mode](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#packet-transmission-mode)  
  A Receiver based on RTP transport declares the `packet_transmission_mode` capability to indicate the NAL units packetization modes that it supports.

- [Parameter Sets Flow Mode](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#parameter-sets-flow-mode)  
  A Receiver declares the `parameter_sets_flow_mode` capability to indicate that it supports bitstreams using parameter sets associated with strictly one (`strict`), one (`static`) or multiple (`dynamic`) Flows. Considering that active parameter sets are associated with a specific Flow, this capability indicates that a Receiver is capable or not of decoding an H.265 bitstream where the associated Flow attributes change dynamically. 
  
  A Receiver supporting the `dynamic` mode MUST also support the `strict` and `static` modes. Such Receiver SHOULD have `strict`, `static` and `dynamic` values enumerated in the Receiver Capability in order to allow Senders operating in any `parameter_sets_flow_mode`.

- [Parameter Sets Transport Mode](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#parameter-sets-transport-mode)  
  A Receiver declares the `parameter_sets_transport_mode` capability to indicate that it supports bitstreams using parameter sets provided either only out-of-band, only in-band or in-and-out-of-band. The in-band parameter sets MAY update, augment or duplicate the parameter sets received out-of-band. A Receiver declaring the `in_band` or `in_and_out_of_band` capabilities MUST be capable of decoding in-band parameter sets that update, augment or duplicate the parameter sets received out-of-band. A Receiver declaring the `out_of_band` capability MUST be capable of decoding in-band parameter sets that duplicate the parameter sets received out-of-band.

  All the parameter sets used by the bitstream MUST be compliant with the `profile-space`, `profile-id`, `profile-compatibility-indicator`, `interop-constraints`, `level-id` and `tier-flag` explicitly or implicitly declared in the stream's associated SDP transport file. The parameter sets MAY be specified out-of-band using the `sprop-vps`, `sprop-sps` and `sprop-pps` parameters of an SDP transport file, in-band through the H.265 bitstream or in-and-out-of-band using both mechanisms. See the [Parameter Sets](#parameter-sets) section for more details.

  A Receiver supporting `in_and_out_of_band` MUST also support the `in_band` and `out_of_band` modes. Such Receiver SHOULD have all "in_band", "out_of_band" and "in_and_out_of_band" values enumerated in the Receiver Capabilities in order to allow Senders operating in any `parameter_sets_transport_mode`.

### RTP transport based on RFC 2250

For Nodes consuming H.265 using the RTP payload mapping defined by RFC 2250, the Receiver resource MUST indicate `urn:x-nmos:transport:rtp` or one of its subclassifications for the `transport` attribute.

The following parameter constraints can be used to express limits or preferences specifically defined for H.265 decoders:

- [Parameter Sets Flow Mode](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#parameter-sets-flow-mode)  
  A Receiver declares the `parameter_sets_flow_mode` capability to indicate that it supports bitstreams using parameter sets associated with strictly one (`strict`), one (`static`) or multiple (`dynamic`) Flows. Considering that active parameter sets are associated with a specific Flow, this capability indicates that a Receiver is capable or not of decoding an H.265 bitstream where the associated Flow attributes change dynamically. 
  
  A Receiver consuming H.265 using the RTP payload mapping defined by RFC 2250 MUST support the `dynamic` mode or be unconstrained.

- [Parameter Sets Transport Mode](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#parameter-sets-transport-mode)  
  A Receiver declares the `parameter_sets_transport_mode` capability to indicate that it supports bitstreams using parameter sets provided either only out-of-band, only in-band or in-and-out-of-band. The in-band parameter sets MAY update, augment or duplicate the parameter sets received out-of-band. A Receiver declaring the `in_band` or `in_and_out_of_band` capabilities MUST be capable of decoding in-band parameter sets that update, augment or duplicate the parameter sets received out-of-band. A Receiver declaring the `out_of_band` capability MUST be capable of decoding in-band parameter sets that duplicate the parameter sets received out-of-band.

  All the parameter sets used by the bitstream MUST be compliant with the profile and level explicitly or implicitly declared in the members profile_space, profile_idc, profile_compatibility_indication, level_idc, tier_flag, progressive_source_flag, interlaced_source_flag, non_packed_constraint_flag, frame_only_constraint_flag and copied_44bits of the HEVC_video_descriptor of an MPEG2-TS transport stream. The parameter sets MUST be specified in-band through the H.265 bitstream. See the [Parameter Sets](#parameter-sets) section for more details.

  A Receiver consuming H.265 using the RTP payload mapping defined by RFC 2250 MUST support the `in_band` mode or be unconstrained.

### Other transports

For Nodes consuming H.265 using other transports, the Receiver resource MUST indicate the associated `urn:x-nmos:transport:` or `urn:x-matrox:transport:` label of the transport or one of its subclassifications for the `transport` attribute.

For Receivers indicating `urn:x-nmos:format:video` for the `format` attribute, the following parameter constraints can be used to express limits or preferences specifically defined for H.265 decoders:

- [Parameter Sets Flow Mode](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#parameter-sets-flow-mode)  
  A Receiver declares the `parameter_sets_flow_mode` capability to indicate that it supports bitstreams using parameter sets associated with strictly one (`strict`), one (`static`) or multiple (`dynamic`) Flows. Considering that active parameter sets are associated with a specific Flow, this capability indicates that a Receiver is capable or not of decoding an H.265 bitstream where the associated Flow attributes change dynamically. 

  A Receiver supporting the `dynamic` mode MUST also support the `strict` and `static` modes. Such Receiver SHOULD have `strict`, `static` and `dynamic` values enumerated in the Receiver Capability in order to allow Senders operating in any `parameter_sets_flow_mode`.

- [Parameter Sets Transport Mode](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#parameter-sets-transport-mode)  
  A Receiver declares the `parameter_sets_transport_mode` capability to indicate that it supports bitstreams using parameter sets provided either only out-of-band, only in-band or in-and-out-of-band. The in-band parameter sets MAY update, augment or duplicate the parameter sets received out-of-band. A Receiver declaring the `in_band` or `in_and_out_of_band` capabilities MUST be capable of decoding in-band parameter sets that update, augment or duplicate the parameter sets received out-of-band. A Receiver declaring the `out_of_band` capability MUST be capable of decoding in-band parameter sets that duplicate the parameter sets received out-of-band.

  Informative note: The out of band mechanism used to transmit parameter sets is transport specific and out of the scope of this specification.

  All the parameter sets used by the bitstream MUST be compliant with the profile and level explicitly or implicitly declared using an out-of-band transport specific mechanism. The parameter sets MAY be specified in-band through the H.265 bitstream, out-of-band using an unspecified mechanism or in-and-out-of-band using both mechanisms. See the [Parameter Sets](#parameter-sets) section for more details.

  A Receiver supporting `in_and_out_of_band` MUST also support the `in_band` and `out_of_band` modes. Such Receiver SHOULD have all "in_band", "out_of_band" and "in_and_out_of_band" values enumerated in the Receiver Capabilities in order to allow Senders operating in any `parameter_sets_transport_mode`.

For Receivers indicating `urn:x-nmos:format:mux` for the `format` attribute, the following parameter constraints can be used to express limits or preferences specifically defined for H.265 decoders:

- [Parameter Sets Flow Mode](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#parameter-sets-flow-mode)  
  A Receiver declares the `parameter_sets_flow_mode` capability to indicate that it supports bitstreams using parameter sets associated with strictly one (`strict`), one (`static`) or multiple (`dynamic`) Flows. Considering that active parameter sets are associated with a specific Flow, this capability indicates that a Receiver is capable or not of decoding an H.265 bitstream where the associated Flow attributes change dynamically. 

  A Receiver consuming H.265 from a multiplexed stream MUST support the `dynamic` mode or be unconstrained.

- [Parameter Sets Transport Mode](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#parameter-sets-transport-mode)  
  A Receiver declares the `parameter_sets_transport_mode` capability to indicate that it supports bitstreams using parameter sets provided either only out-of-band, only in-band or in-and-out-of-band. The in-band parameter sets MAY update, augment or duplicate the parameter sets received out-of-band. A Receiver declaring the `in_band` or `in_and_out_of_band` capabilities MUST be capable of decoding in-band parameter sets that update, augment or duplicate the parameter sets received out-of-band. A Receiver declaring the `out_of_band` capability MUST be capable of decoding in-band parameter sets that duplicate the parameter sets received out-of-band.

  All the parameter sets used by the bitstream MUST be compliant with the profile and level explicitly or implicitly declared in the transport stream. The parameter sets MUST be specified in-band through the H.265 bitstream. See the [Parameter Sets](#parameter-sets) section for more details.

  A Receiver consuming H.265 from a multiplexed stream MUST support the `in_band` mode or be unconstrained.

## H.265 IS-05 Senders and Receivers

### RTP transport

Connection Management using IS-05 proceeds in exactly the same manner as for any other stream format carried within RTP.

If IS-04 Sender `manifest_href` is not `null`, the SDP transport file at the **/transportfile** endpoint on an IS-05 Sender MUST comply with the same requirements described for the SDP transport file at the IS-04 Sender `manifest_href`.

A `PATCH` request on the **/staged** endpoint of an IS-05 Receiver can contain an SDP transport file in the `transport_file` attribute. The SDP transport file for a H.265 stream is expected to comply with RFC 7798 and, if appropriate, ST 2110-22 or IPMX. It need not comply with the additional requirements specified for SDP transport files at Senders.

If the Receiver is not capable of consuming the stream described by a `PATCH` on the **/staged** endpoint, it SHOULD reject the request. If it is unable to assess the stream compatibility because some parameters are not included `PATCH` request, it MAY accept the request and postpone stream compatibility assessment.

### Other transports

Connection Management using IS-05 proceeds in exactly the same manner as for any other stream format carried within other transports.

If IS-04 Sender `manifest_href` is not `null`, the SDP transport file at the **/transportfile** endpoint on an IS-05 Sender MUST comply with the same requirements described for the SDP transport file at the IS-04 Sender `manifest_href`.

If the Receiver is not capable of consuming the stream described by a `PATCH` on the **/staged** endpoint, it SHOULD reject the request. If it is unable to assess the stream compatibility because some parameters are not included `PATCH` request, it MAY accept the request and postpone stream compatibility assessment.

## Parameter Sets

The active parameter sets of an H.265 stream are made of the active sequence and picture parameter sets. The parameter sets of an H.265 stream are transmitted by a Sender to a number of Receivers either out-of-band through an SDP transport file or other out-of-band transport specific mechanism, or in-band through the coded stream. The active parameter sets of an H.265 coded stream MUST reference valid out-of-band or in-band parameter sets, the stream is invalid otherwise.

The `sprop-vps`, `sprop-sps` and `sprop-pps` parameters of an SDP transport file MAY contain a collection of out-of-band parameter sets. Those parameter sets provide initial parameter sets for the H.265 stream before the decoding starts.

An H.265 stream MAY transport in-band parameter sets to update or duplicate parameter sets received out-of-band, to define additional parameter sets or to update or duplicate parameter sets received in-band. The `parameter_sets_transport_mode` Receiver Capability indicates when set to `in_band` or `in_and_out_of_band` that a Receiver supports getting updated, duplicated or additional parameter sets in-band. When set to `out_of_band` a Receiver only supports getting initial parameter sets from the SDP transport file. In all the cases the Receiver MUST support getting duplicated parameter sets in-band.

The `sprop-vps`, `sprop-sps` and `sprop-pps` parameters MAY be used by the Receiver to assert the `parameter_sets_transport_mode` in use by the Sender. The in-and-out-of-band mode is signaled if `sprop-vps`, `sprop-sps` and `sprop-pps` are present and not empty, and terminate by an empty NAL unit (i.e. an empty byte sequence that is base64 encoded). An `sprop-vps`, `sprop-sps` and `sprop-pps` parameters terminate by an empty NAL unit if it ends by a comma ','. The terminating colon ',' indicates that more parameter sets will be received in-band, indicating the in-and-out-of-band mode. The out-of-band mode is signaled when `sprop-vps`, `sprop-sps` and `sprop-pps` are present and not empty, and not terminated by a comma ','. The in-band mode is signaled when `sprop-vps`, `sprop-sps` and `sprop-pps` are not present or empty. A Sender MUST terminate the `sprop-vps`, `sprop-sps` and `sprop-pps` parameters by a comma ',' if it operates in in-and-out-of-band mode and MUST not terminate it by a comma ',' in out-of-band mode.

Informative note: It results that an H.265 Sender operating in in-and-out-of-band mode that is not sending parameter sets out-of-band will set the `sprop-vps`, `sprop-sps` and `sprop-pps` parameters to a single comma ',' value.

Informative note: The in-and-out-of-band mode implies that the Sender can optionally use the in-band path, the out-band path or both paths to transmit parameter sets. There is no requirement to use both paths simultaneously.

### Receivers

A Receiver MUST verify that the active parameter sets comply with the Receiver's Capabilities. If a Receiver support only out-of-band parameter sets it SHOULD perform the verification when a Controller PATCH the **/staged** endpoint for activation. In this situation, all the out-of-band parameter sets MUST be compliant with the Receiver Capabilities. Otherwise if a Receiver supports both out-of-band and in-band parameter sets it SHOULD perform the verification of the out-of-band parameter sets when a Controller PATCH the **/staged** endpoint for activation and it MUST perform the verification of the in-band parameter sets just-in-time as it decodes the stream. In this situation, all the out-of-band and in-band parameter sets MUST be compliant with the Receiver Capabilities.

The `parameter_sets_flow_mode` Receiver Capability indicates when set to `dynamic` that a Receiver supports decoding an H.264 stream where the active parameter sets values associated with Flow attributes may changes dynamically. The Flow attributes that are allowed to change correspond to the following attributes of a coded video Flow: `grain_rate`, `frame_width`, `frame_height`, `colorspace`, `interlace_mode`, `transfer_characteristic`, `components`, `profile`, `level`, `bit_rate` and `constant_bit_rate`. The `static` mode is more restrictive, requiring active parameter sets values associated with Flow attributes to be constant, with the exception of the Flow's `bit_rate` attribute that MAY change. The `strict` mode has the further restriction that at most one SPS be used by the coded stream.

Informative note: The Flow `bit_rate` attribute is not included in the previous criterion to allow changing HRD parameters to adapt to IP usable bandwidth changing conditions in `static` mode.

A Receiver with the `parameter_sets_flow_mode` capability set to `strict` requires that a coded stream uses picture parameter sets that are defined once and associated with at most one Flow and at most one sequence parameter set that is defined once. Such parameter sets MAY be obtained out-of-band or in-band depending on the Receiver `parameter_sets_transport_mode` capability. When obtained out-of-band the `sprop-vps`, `sprop-sps` and `sprop-pps` parameters of an SDP transport file or the parameter sets from a transport specific out-of-band mechanism MUST contain picture parameter sets associated with only one Flow and one sequence parameter set. When obtained in-band the `sprop-vps`, `sprop-sps` and `sprop-pps` parameters of an SDP transport file or the parameter sets from a transport specific out-of-band mechanism MUST be empty or omitted and the Sender transmits the picture parameter sets associated with the Flow in-band along with a sequence parameter set. At all time, the Sender MAY transmit in-band parameter sets that are duplicates of the parameter sets obtained either out-of-band or in-band. When obtained in-and-out-of-band, in-band parameter sets have priority over out-of-band parameters sets.

A Receiver with this capability set to `static` requires that a coded stream uses parameter sets associated with at most one Flow. Such parameter sets MAY be obtained out-of-band or in-band depending on the Receiver `parameter_sets_transport_mode` capability. When obtained out-of-band the `sprop-vps`, `sprop-sps` and `sprop-pps` parameters of an SDP transport file or the parameter sets from a transport specific out-of-band mechanism MUST contain parameter sets associated with only one Flow. When obtained in-band the `sprop-vps`, `sprop-sps` and `sprop-pps` parameters of an SDP transport file or the parameter sets from a transport specific out-of-band mechanism MUST be empty or omitted and the Sender transmits the parameter sets associated with the Flow in-band. At all time, the Sender MAY transmit in-band parameter sets that are duplicates of the parameter sets obtained either out-of-band or in-band. When obtained in-and-out-of-band, in-band parameter sets have priority over out-of-band parameters sets.

Informative note: The `static` mode allows multiple VPS, SPS and PPS to be used by the coded bitstream as long as the active values associated with Flow attributes do not change. For example scaling list are allowed to change when the profile allows it.

A Receiver with this capability set to `dynamic` supports that a coded stream uses parameter sets that MAY be associated with multiple Flows on the Sender. Such parameter sets MAY be obtained out-of-band or in-band according to the Receiver `parameter_sets_transport_mode` capability. When obtained out-of-band the `sprop-vps`, `sprop-sps` and `sprop-pps` parameters of an SDP transport file or the parameter sets from a transport specific out-of-band mechanism MAY contain parameter sets associated with multiple Flows. When obtained in-band the `sprop-vps`, `sprop-sps` and `sprop-pps` parameters of an SDP transport file or the parameter sets from a transport specific out-of-band mechanism MUST be empty or omitted and the Sender MAY transmit in-band parameter sets to update parameter sets initially received out-of-band or to add and update new ones. At all time, the Sender MAY transmit in-band parameter sets that are duplicates of the parameter sets obtained either out-of-band or in-band. When obtained in-and-out-of-band, in-band parameter sets have priority over out-of-band parameters sets.

### Senders

A Sender MAY, unless constrained by IS-11, produce any H.265 coded stream that is compliant with the `profile` and `level` of the associated Flow. Such a Sender MAY use one or multiple active parameter sets as per the [H.265][] specification. A Sender MAY seamlessly change dynamically the coded stream's active parameter sets, provided that the Flow associated with the Sender changes accordingly and the content of the SDP transport file does not change. If the content of the SDP transport file changes, the Sender MUST comply with IS-04, IS-05. A Sender indicates its mode of operation with the `parameter_sets_flow_mode` and `parameter_sets_transport_mode` attributes.

For the purpose of not changing the SDP transport file, a Sender MAY keep an SDP transport file `b=` bitrate attribute unchanged if the actual value is lower than the one published in the SDP transport file. Similarly a Sender MAY keep the SDP transport file format parameters `profile-space`, `profile-id`, `profile-compatibility-indicator`, `interop-constraints`, `level-id` and `tier-flag` unchanged if the actual values are a subset of the ones published in the SDP transport file.

A Sender MUST transport parameter sets `in_band` when the H.265 stream is transmitted over an MPEG2-TS based transport as per the [H.222.0][] specification.

A Sender operating with `parameter_sets_flow_mode` set to `strict` MUST produce a coded bitstream using at most one VPS, one SPS and MAY use a number of PPS associated with at most one Flow. The parameter sets MUST be defined once in-band or out-of-band and MAY be refreshed by in-band duplicates.

A Sender operating with `parameter_sets_flow_mode` set to `static` MAY produce a coded bitstream using a number of VPS, SPS and PPS that MUST be associated with at most one Flow. The parameter sets MAY be defined in-band or out-of-band and MAY be refreshed by in-band duplicates or updated, replaced or augmented by in-band ones.

A Sender operating with `parameter_sets_flow_mode` set to `dynamic` MAY produce a coded bitstream using a number of VPS, SPS and PPS that MAY be associated with multiple Flows. The parameter sets MAY be defined in-band or out-of-band and MAY be refreshed by in-band duplicates or updated, replaced or augmented by in-band ones.

The parameter sets MUST convey, so far as the VPS, SPS, and PPS syntax elements allow, the same information about the stream as conveyed by the Source and Flow attributes defined by this specification and IS-04.

Informative note: When encoding a video described as RGB 4:4:4 in the [Components](https://specs.amwa.tv/nmos-parameter-registers/branches/main/flow-attributes/#components) Flow attribute, the encoder might use an intermediate 4:4:4 format optimized for H.265 compression, and the VPS, SPS, and PPS syntax elements would represent this intermediate color representation. The coded bitstream is expected to include a `colour remapping information` SEI message to ensure that the final video output correctly represents the original RGB 4:4:4 colors.

## H.265 IS-11 Senders and Receivers

### RTP transport

### Other transports

## Controllers

[H.265]: https://www.itu.int/rec/T-REC-H.265 "High efficiency video coding"
[H.222.0]: https://www.itu.int/rec/T-REC-H.222.0 "Generic coding of moving pictures and associated audio information: Systems"
[RFC-2119]: https://tools.ietf.org/html/rfc2119 "Key words for use in RFCs"
[RFC-7798]: https://tools.ietf.org/html/rfc7798 "RTP Payload Format for High Efficiency Video Coding (HEVC)"
[RFC-2250]: https://tools.ietf.org/html/rfc2250 "RTP Payload Format for MPEG1/MPEG2 Video"
[RFC-5576]: https://tools.ietf.org/html/rfc5576 "Source-Specific Media Attributes in the Session Description Protocol (SDP)"
[IS-04]: https://specs.amwa.tv/is-04/ "AMWA IS-04 NMOS Discovery and Registration Specification"
[IS-05]: https://specs.amwa.tv/is-05/ "AMWA IS-05 NMOS Device Connection Management Specification"
[NMOS Parameter Registers]: https://specs.amwa.tv/nmos-parameter-registers/ "Common parameter values for AMWA NMOS Specifications"
[TR-10-11]: https://vsf.tv/download/technical_recommendations/VSF_TR-10-11_2024-02-23.pdf "Constant Bit-Rate Compressed Video"
[TR-10-7]: https://vsf.tv/download/technical_recommendations/VSF_TR-10-7_2023-09-26.pdf "Compressed Video"
[VSF]: https://vsf.tv/ "Video Services Forum"
[SMPTE]: https://www.smpte.org/ "Society of Media Professionals, Technologists and Engineers"
[ST-2110-22]: https://ieeexplore.ieee.org/document/9893780 "ST 2110-22:2022 - SMPTE Standard - Professional Media Over Managed IP Networks: Constant Bit-Rate Compressed Video"
[BCP-004-01]: https://specs.amwa.tv/bcp-004-01/ "AMWA BCP-004-01 NMOS Receiver Capabilities"

---
  
  ***This document is a modification of the original BCP-006-03 document from AMWA, which was drafted after the Matrox proposal document.***
  
   Copyright 2021 AMWA

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
   
