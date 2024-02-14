# Matrox: NMOS With AAC
{:.no_toc}  
Copyright 2023, Matrox Graphics Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
  
---
  
{:toc}

## Introduction

Advanced Audio Coding (AAC) is a technology standardized in [AAC][AAC] | ISO/IEC 14496-3.
A companion RTP payload format specification was developed through the IETF Payloads working group, IETF [RFC 3640][RFC-3640]. Another RTP payload format specification IETF [RFC 6416][RFC-6416] also exist and may be used as an alternate method for transporting the audio stream payload in RTP.

> RFC 3640 only support passing configuration information out-of-band while RFC 6416 support both in-band and out-of-band methods. When targetting MPEG2-TS transport the configuration information is provided in-band as per the H.222 specification.

> RFC 6416 is used in declarative mode as per RFC 6116 section 7.4.1 "Declarative SDP Usage for MPEG-4 Audio".

The [Video Services Forum][VSF] developed Technical Recommendation [TR-??][TR-??] and [TR-??][TR-??] of the IPMX suite of protocols, which cover the end-to-end application use of constant and variable bitrate compression for audio, using the SMPTE ST 2110 and IPMX suite of protocols.

TR-?? and TR-?? mandate the use of the AMWA [IS-04][IS-04] and [IS-05][IS-05] NMOS Specifications in IPMX compliant systems.  

AMWA IS-04 and IS-05 already have support for RTP transport and can signal the media type `audio/mpeg4-generic` as defined in RFC 3640 or `audio/MP4A-LATM` as defined in RFC 6416. For MPEG2-TS transport the AAC codec is signaled as `audio/MP4A-ADTS`.

> MPEG4 audio is a synonym for Advanced Audio Coding, corresponding to the AAC codec. The media type `audio/mpeg4-generic` indicates MPEG4 audio, hence the AAC codec. The media type `audio/MP4A-LATM` indicates MPEG4 audio framed using the LATM multiplexor to transport configuration information along with the audio stream. It indicates the AAC codec. The media type `audio/MP4A-ADTS` indicates MPEG4 audio framed using the ADTS multiplexor to transport configuration information along with the audio stream. Once again it indicates the AAC codec.

- [ ] TODO: The MP4A-ADTS is not registered to IANA but as it does not appear in any SDP transport file it may not be required.

In this document the concept of parameter sets usually associated with coded video streams is reused for coded audio streams to maintain as much as possible a common programming model for coded video streams. For an audio stream the concept of parameter sets maps to the concept of configs that define the parameters of a coded audio stream.

## Use of Normative Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY",
and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119][RFC-2119].

## Definitions

The NMOS terms 'Controller', 'Node', 'Source', 'Flow', 'Sender', 'Receiver' are used as defined in the [NMOS Glossary](https://specs.amwa.tv/nmos/main/docs/Glossary.html).

## AAC IS-04 Sources, Flows and Senders

Nodes capable of transmitting AAC audio streams MUST have Source, Flow and Sender resources in the IS-04 Node API.

### Sources

The Source resource MUST indicate `urn:x-nmos:format:audio` for the `format` attribute.
- Source resources MAY be associated with many Flows at the same time. The Source is therefore unaffected by the use of AAC compression.

- IS-08 MAY be used to re-arrange the audio channels of the Source feeding an AAC coded Flow.

### Flows

The Flow resource MUST indicate `audio/mpeg4-generic` or `audio/MP4A-LATM` or `audio/MP4A-ADTS` in the `media_type` attribute, and `urn:x-nmos:format:audio` for the `format` attribute. This has been permitted since IS-04 v1.1. 
- AAC Flow resources MAY be associated with many Senders at the same time through the Senders' `flow_id` attributes. The AAC Flow is therefore unaffected by the use of a specific transport.
- AAC Flow resources MAY be associated with many Flows at the same time through the Flows' `parents` attributes. The AAC Flow is therefore unaffected by being the parent of some other Flows.

For Nodes implementing IS-04 v1.3 or higher, the following additional requirements on the Flow resource apply.

In addition to those attributes defined in IS-04 for all coded audio Flows, the following attributes defined in the [Flow Attributes Register](https://specs.amwa.tv/nmos-parameter-registers/branches/main/flow-attributes/) of the [NMOS Parameter Registers][] are used for AAC.

These attributes provide information for Controllers and Users to evaluate stream compatibility between Senders and Receivers.

- [Profile](https://specs.amwa.tv/nmos-parameter-registers/branches/main/flow-attributes/#profile)  
  The Flow resource MUST indicate the AAC profile, which defines algorithmic features and limits that MUST be supported by all decoders conforming to that profile. The stream's active config MUST be compliant with the `profile` attribute of the Flow. The permitted `profile` values are strings, defined as per ISO ISO/IEC 14496-3

  - "Speech"
  - "Synthetic"
  - "Scalable"
  - "Main"
  - "HighQuality"
  - "LowDelay"
  - "Natural"
  - "Mobile"
  - "AAC"
  - "HighEfficiencyAAC"
  - "HighEfficiencyAACv2"
  - "LowDelayAAC"
  - "LowDelayAACv2"
  - "ExtendedHighEfficiencyAAC"
  
  The profile strings in this specification are included in the [NMOS Parameter Registers][]. Additional strings may be added there in the future.
  
- [Level](https://specs.amwa.tv/nmos-parameter-registers/branches/main/flow-attributes/#level)  
  The Flow resource MUST indicate the AAC level, which defines a set of limits on the values that may be taken by the syntax elements of an AAC bitstream. The stream's active config MUST be compliant with the `level` attribute of the Flow.The permitted `level` values are strings, defined as per ISO ISO/IEC 14496-3

  - "1"
  - "2"
  - "3"
  - "4"
  - "5"
  - "6"
  - "7"
  - "8"
  
  The level strings in this specification are included in the [NMOS Parameter Registers][]. Additional strings may be added there in the future.

The Flow's `profile` and `level` attributes map to the `profile-level-id` parameter of the SDP transport file. See the [SDP format-specific parameters](#sdp-format-specific-parameters) section.

The Flow's `profile` and `level` attributes map to the member MPEG-4_audio_profile_and_level of the MPEG-4_audio_descriptor of an MPEG2-TS transport stream. See the [RTP transport based on RFC 2250](#rtp-transport-based-on-rfc-2250) section.

Informative note: The Flow's `profile` and `level` attributes are always required. The `profile-level-id` parameter of the SDP transport file is REQUIRED according to RFC 3640, OPTIONAL according to RFC 6416 is REQUIRED by this specification. There is no default value defied by RFC 3640 or RFC 6416.

- [Bit Rate](https://specs.amwa.tv/nmos-parameter-registers/branches/main/flow-attributes/#bit-rate)  
  The Flow resource MUST indicate the target encoding bit rate (kilobits/second) of the AAC bitstream. The stream's active config MUST be compliant with the `bit_rate` attribute of the Flow. The `bit_rate` integer value is expressed in units of 1000 bits per second, rounding up.

  Informative note: The Flow's `bit_rate` attribute map to the `bitrate` parameter of the SDP transport file which is OPTIONAL according to RFC 6416, not specified by RFC 3640 and REQUIRED and by this specification.

- [Constant Bit Rate](https://specs.amwa.tv/nmos-parameter-registers/branches/main/flow-attributes/#constant-bit-rate)
  The Flow resource MUST indicate if it operates in constant bit rate (CBR) mode or variable bit rate mode (VBR or other). When operating in constant bit rate mode the `bit_rate` corresponds to the constant encoding bit rate. Otherwise it corresponds to the maximum encoding bit rate. Since the default value of this attribute is `false`, a Flow MAY omit this attribute when using a variable bit rate mode.

Informative note: The maximum bit rate information relates to the codec profile / level limits and the Bit Reservoir buffering model. It corredponds to the maximum bitrate in any time window of one second duration as per ISO/IEC 14496-1. The CBR versus VBR mode of operation of the encoder provide essential clues about the coded bitstream produced.

Informative note: The target bitrate is propably more specifically the maximum bitrate that is used to calculate the buffering model between the encoder and the decoder, aka bit reservoir, etc. In variable bitrate mdoes, this would more precisely describe the stream. For constant bitrate it is the target, for variable bitrate it is the maximum.

Informative note: AAC specification indicates: 4.5.3.3 Maximum bit rate: The maximum bitrate depends on the audio sampling rate. It can be calculated based on the minimum input buffer size according to the formula: *** Table 4.126 Maximum bitrate depending on the sampling frequency sampling_frequency maximum bitrate / NCC, 48 kHz => 288 kbit/s, 44.1 kHz => 264.6 kbit/s, 32 kHz => 192 kbit/s

Informative note: The RFC 3640 standard does not define a bitrate SDP transport file parameter. RFC 6416 defines an OPTIONAL bitrate parameter in bits per seconds.  RFC 3890 propose an SDP bitrate attribute that does not include transport overhead for media type mpeg4-generic. EBU TECH 3326 require specifying the coding bitrate using the TIAS bandwidth modifier of RFC-3890 and recommend adding a `bitrate` parameter in bits per second to the fmtp attribute. As RFC 3640 indicates "Applications MAY use more parameters, in addition to those defined above." it seems acceptable to include the bitrate parameter to the SDP transport file for both RFC 3640 and RFC 6416 in a uniform way in bits per seconds (Flow property remain in Kbps units).

The AAC encoder associated with the Flow MUST produce an AAC bitstream that is compliant with the `profile` and `level` attributes.

Examples Flow resources are provided in [Examples](../examples/).

### Senders

This section applies to a Sender directly associated with an AAC Flow through the Sender's `flow_id` attribute.

Informative note: When an AAC Flow is not directly associated with a Sender but with a multiplexed Flow through the Flow's parents attribute, the Sender does not provide AAC format-specific attributes. A Sender provides such attributes only when the AAC Flow is directly associated with it. The attributes `parameter_sets_flow_mode` and `parameter_sets_transport_mode` associated with an AAC Flow that are described in this section get their respective default value of `dynamic` and `in_band`.  

For multiplexed AAC Flows, the Sender MUST conform to the behaviour dictated by the `dynamic` and `in_band` modes described in this specification.

Sender resources provide no indication of media type or format, since this is described by the associated Flow resource.

#### RTP transport based on RFC3640 or RFC 6416

For Nodes transmitting AAC using the RTP payload mapping defined by RFC 3640 or RFC 6416, the Sender resource MUST indicate `urn:x-nmos:transport:rtp` or one of its subclassifications for the `transport` attribute.

For Nodes implementing IS-04 v1.3 or higher, the following additional requirements on the Sender resource apply.

In addition to those attributes defined in IS-04 for Senders, the following attributes defined in the [Sender Attributes Register](https://specs.amwa.tv/nmos-parameter-registers/branches/main/sender-attributes/) of the NMOS Parameter Registers are used for AAC.

- [Bit Rate](https://specs.amwa.tv/nmos-parameter-registers/branches/main/sender-attributes/#bit-rate)  
  The Sender resource SHOULD indicate the target bit rate (kilobits/second) including the transport overhead of the AAC stream. The value is for the IP packets, so for the RTP payload format per RFC 3640 or RFC 6416, that includes the RTP, UDP and IP packet headers and the payload. The `bit_rate` integer value is expressed in units of 1000 bits per second, rounding up. The Sender's transport `bit_rate` indicates a constant bit rate or a maximum bit rate depending on the `constant_bit_rate` attribute of the associated Flow. 

- [Packet Transmission Mode](https://specs.amwa.tv/nmos-parameter-registers/branches/main/sender-attributes/#packet-transmission-mode)  
  A Sender MUST include the `packet_transmission_mode` attribute and set it to either `non_interleaved_access_units` or `interleaved_access_units`. The parameters of the SDP transport file for RFC 3640 MUST describe the use of the interleaved mode and provide all the necessary information required by the decoder to reconstruct the audio stream.

  Informative note: The interleaved mode is not supported by RFC 6416.
  
- [Parameter Sets Flow Mode](https://specs.amwa.tv/nmos-parameter-registers/branches/main/sender-attributes/#parameter-sets-flow-mode)
  A Sender MUST set the `parameter_sets_flow_mode` attribute to `strict` if operating within the necessary restrictions for this mode, or `static` if operating within the necessary restrictions for that mode. Otherwise it MAY omit or set the `parameter_sets_flow_mode` attribute to `dynamic`. If unspecified the default value is `dynamic`. See the [Parameter Sets](#parameter-sets) section for more details.

- [Parameter Sets Transport Mode](https://specs.amwa.tv/nmos-parameter-registers/branches/main/sender-attributes/#parameter-sets-transport-mode)  
  A Sender operating with out-of-band parameter sets MUST set the `parameter_sets_transport_mode` attribute to either `out_of_band` or `in_and_out_of_band`. Otherwise it MAY omit or set the `parameter_sets_transport_mode` attribute to `in_band`. If unspecified the default value is `in_band`. See the [Parameter Sets](#parameter-sets) section for more details.

  RFC 3640 does not support the `in_band` mode such that `parameter_sets_transport_mode` MUST be set to `out_of_band`.

  Informative note: From ISO/IEC 14496-3 "The header streams are transported via MPEG-4 systems. These streams contain configuration information, which is necessary for the decoding process and parsing of the raw data streams. However, an update is only necessary if there are changes in the configuration." AudioSpecificConfig is part of the header streams.

An example Sender resource is provided in the [Examples](../examples/).

The AAC encoder of a Sender MUST produces an AAC bitstream that is compliant with the `profile-level-id` explicitely declared in the stream's associated SDP transport file or the MPEG-4_audio_profile_and_level of the MPEG-4_audio_descriptor of an MPEG2-TS transport stream.

##### SDP format-specific parameters

The SDP file at the `manifest_href` MUST comply with the requirements of RFC 3640 or RFC 6416.

Additionally, the SDP transport file needs to convey, so far as the defined format-specific parameters allow, the same information about the stream as conveyed by the Source, Flow and Sender attributes defined by this specification and IS-04, unless such information is conveyed through in-band configs.

Therefore:

- The `profile-level-id` format-specific parameter MUST be included with the correct value.
  
- The `config` format-specific parameter MUST always be included if the Sender `parameter_sets_transport_mode` property is `out_of_band`. The hexadecimal value of the "config" parameter is the AudioSpecificConfig(), as defined in ISO/IEC 14496-3. Ex config=AB8902. To explicitly indicate that `parameter_sets_transport_mode` property is `in_band` the value "" MUST be used with RFC 3640. Ex config=""

- The `mode` format-specific parameter MUST be included with the correct value for RFC 3640. Actually only the `AAC-hbr` mode is supported.

- The `streamType` format-specific parameter MUST be included with the value 5 for RFC 3640. Actually only the `audio` stream type is supported.

- The `maxDisplacement`, `constantDuration` and `de-interleaveBufferSize` format-specific parameters SHOULD be included with the correct value for RFC 3640 if the `packetization-mode` equals one of the interleaved modes.

- The `sizeLength`, `indexLength` and `indexDeltaLength` MUST always be included for RFC 3640 as only mode AAC-hbr is supported. Expected values for AAC-hbr are `sizeLength` = 13, `indexLength` = 3 and `indexDeltaLength` = 3.

Informative note: The Flow bit_rate information is assumed to be conveyed according to the rules of the standards being implemented by the device. In some scenarios the encoding is not declared out-of-band through the SDP transport file but in-band through the coded stream.

Examples of SDP transport file are provided in the [Examples](../examples/).

#### Other transports

For Nodes transmitting AAC using other transports, the Sender resource MUST indicate the associated `urn:x-nmos:transport:` or `urn:x-matrox:transport:` label of the transport or one of its subclassifications for the `transport` attribute.

Sender resources provide no indication of media type or format, since this is described by the associated Flow resource.

The `manifest_href` attribute MAY be `null` if an SDP transport file is not supported by the transport. Otherwise the SDP transport file MUST comply with the transport specific requirements. There is no SDP format-specific parameters requirements for transports other than RTP.

- [Parameter Sets Flow Mode](https://specs.amwa.tv/nmos-parameter-registers/branches/main/sender-attributes/#parameter-sets-flow-mode)  
  A Sender MUST set the `parameter_sets_flow_mode` attribute to `strict` if operating within the necessary restrictions for this mode, or `static` if operating within the necessary restrictions for that mode. Otherwise it MAY omit or set the `parameter_sets_flow_mode` attribute to `dynamic`. If unspecified the default value is `dynamic`. See the [Parameter Sets](#parameter-sets) section for more details.

- [Parameter Sets Transport Mode](https://specs.amwa.tv/nmos-parameter-registers/branches/main/sender-attributes/#parameter-sets-transport-mode)  
  A Sender operating with out-of-band parameter sets MUST set the `parameter_sets_transport_mode` attribute to either `out_of_band` or `in_and_out_of_band`. Otherwise it MAY omit or set the `parameter_sets_transport_mode` attribute to `in_band`. If unspecified the default value is `in_band`. See the [Parameter Sets](#parameter-sets) section for more details.

  Informative note: The out of band mechanism used to transmit configs is transport specific and out of the scope of this specification.

## AAC IS-04 Receivers

Nodes capable of receiving AAC audio streams MUST have Receiver resources in the IS-04 Node API.

This section applies to a Receiver directly or indirectly associated with an AAC stream.

Informative note: When an AAC stream is directly associated with a Receiver, the Receiver has `format` set to `urn:x-nmos:format:audio` and `media_types` of the `caps` attribute contains `audio/mpeg4-generic`, `audio/MP4A-LATM` or `audio/MP4A-ADTS`. When an AAC stream is part of a multiplexed stream and is indirectly associated with a Receiver, the Receiver has `format` set to `urn:x-nmos:format:mux`, `media_types` of the `caps` attribute does not contains `audio/mpeg4-generic`, `audio/MP4A-LATM` or `audio/MP4A-ADTS` and `constraint_sets` of the `caps` attribute contains `audio/mpeg4-generic`, `audio/MP4A-LATM` or `audio/MP4A-ADTS`.

For a Receiver directly associated with an AAC stream, the Receiver resource MUST indicate `urn:x-nmos:format:audio` for the `format` attribute and MUST list `audio/mpeg4-generic`, `audio/MP4A-LATM` or `audio/MP4A-ADTS` in the `media_types` array within the `caps` object. This has been permitted since IS-04 v1.1.

For a Receiver indirectly associated with an AAC stream part a multiplexed stream, the Receiver resource MUST indicate `urn:x-nmos:format:mux` for the `format` attribute, MUST list the mux media type in the `media_types` array within the `caps` object and MUST list a constraint set indicating support for the media type `audio/mpeg4-generic`, `audio/MP4A-LATM` or `audio/MP4A-ADTS` in the `constraint_sets` array within the `caps` object.

If the Receiver has limitations on or preferences regarding the AAC audio streams that it supports, the Receiver resource MUST indicate constraints in accordance with the [BCP-004-01][] Receiver Capabilities specification. The Receiver SHOULD express its constraints as precisely as possible, to allow a Controller to determine with a high level of confidence the Receiver's compatibility with the available streams. It is not always practical for the constraints to indicate every type of stream that a Receiver can or cannot consume successfully; however, they SHOULD describe as many of its commonly used operating points as practical and any preferences among them.

The `constraint_sets` parameter within the `caps` object MUST be used to describe combinations of frame rates, width and height, and other parameters which the receiver can support, using the parameter constraints defined in the [Capabilities register](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/) of the NMOS Parameter Registers.

When the AAC decoder has no restrictions on the value of some parameter, the Receiver can indicate that the parameter is unconstrained, as described in BCP-004-01. 

The following parameter constraints can be used to express limits or preferences specifically defined by Standard ISO/IEC 14496-3 and RFC 3640 for AAC decoders:

- [Profile](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#profile)
  Some AAC profiles are superset of other profiles. The AAC specification describe the relationship among the profiles. From the point of view of the AAC specification, supporting such superset profile is required to also be supporting the associated subset profiles. To assist a Controller not having knowledge of the AAC profiles relationship, the Receiver Capabilities SHOULD enumerate subset profiles in addition to the superset profile.

- [Level](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#level)
  Some AAC levels are superset of other levels. The AAC specification describe the relationship among the levels. From the point of view of the AAC specification, supporting such superset level is required to also be supporting the associated subset levels. To assist a Controller not having knowledge of the AAC levels relationship, the Receiver Capabilities SHOULD enumerate all the subset levels in addition to the superset level.

- [Bit Rate](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#format-bit-rate)
- [Constant Bit Rate](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#format-constant-bit-rate)

A Receiver MUST be able to decode bitstreams conforming to the profiles and levels declared in the Receiver Capabilities. A Receiver MAY have preferences and more optimal profiles and levels that MAY be declared through Receiver Capabilities. A preferred constraint set MAY indicate such preferences while another constraint set MAY indicate full support of some profiles and levels. A Receiver MAY further constrain the support of a coded bitstream compliant with a profile and level using other constraints in its Receiver Capabilities.

Other existing parameter constraints, such as the following, are also appropriate to express limitations on supported AAC audio streams:

- [Channel Count](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#channel-count)
- [Sample Rate](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#sample-rate)
- [Sample Depth](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#sample-depth)
- [Packet Time](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#packet-time)
- [Max Packet Time](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#max-packet-time)
- [Format Bit Rate](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#format-bit-rate)
- [Format Constant Bit Rate](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#format-constant-bit-rate)
- [Transport Bit Rate](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#transport-bit-rate)

An example Receiver resource is provided in the [Examples](../examples/).

## RTP transport based on RFC 3640 or RFC 6416

For Nodes consuming AAC using the RTP payload mapping defined by RFC 3640 or RFC 6416, the Receiver resource MUST indicate `urn:x-nmos:transport:rtp` or one of its subclassifications for the `transport` attribute.

The following parameter constraints can be used to express limits or preferences specifically defined for AAC decoders:

- [Bit Rate](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#transport-bit-rate)

- [Packet Transmission Mode](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#packet-transmission-mode)  
  A Receiver based on RTP transport declares the `packet_transmission_mode` capability to indicate the access units packetization modes that it supports.   
  RFC 3640 for the AAC-hbr mode require the `non_interleaved_access_units` and `interleaved_access_units` packetization modes to be supported by all the AAC Receivers. A constrained Receiver MUST have `packet_transmission_mode` capabilities indicating support for both the "non_interleaved_access_units" and "interleaved_access_units" modes and optionally it MAY use the preference property to indicate which mode it prefers while still being required to support both.  
  RFC 6416 only supports the `non_interleaved_access_units` mode. A Receiver MUST have `packet_transmission_mode` capabilities indicating support for the `non_interleaved_access_units` mode.

- [Parameter Sets Flow Mode](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#parameter-sets-flow-mode)  
  A Receiver declares the `parameter_sets_flow_mode` capability to indicate that it supports bitstreams using parameter sets associated with strictly one (`strict`), one (`static`) or multiple (`dynamic`) Flows. Considering that active parameter sets are associated with a specific Flow, this capability indicates that a Receiver is capable or not of decoding an AAC bitstream where the associated Flow attributes change dynamically. 
  
  A Receiver supporting the `dynamic` mode MUST also support the `strict` and `static` modes. Such Receiver SHOULD have `strict`, `static` and `dynamic` values enumerated in the Receiver Capability in order to allow Senders operating in any `parameter_sets_flow_mode`.

- [Parameter Sets Transport Mode](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#parameter-sets-transport-mode)  
  A Receiver declares the `parameter_sets_transport_mode` capability to indicate that it supports bitstreams using parameter sets provided either only out-of-band, only in-band or in-and-out-of-band. The in-band parameter sets MAY update, augment or duplicate the parameter sets received out-of-band. A Receiver declaring the `in_band` or `in_and_out_of_band` capabilities MUST be capable of decoding in-band parameter sets that update, augment or duplicate the parameter sets received out-of-band. A Receiver declaring the `out_of_band` capability MUST be capable of decoding in-band parameter sets that duplicate the parameter sets received out-of-band.

  The config used by the bitstream MUST be compliant with the `profile-level-id` parameter explicitly or implicitly declared in the stream's associated SDP transport file. The config MAY be specified out-of-band using the `config` parameter of an SDP transport file, in-band through the AAC bitstream or in-and-out-of-band using both mechanisms. See the [Parameter Sets](#parameter-sets) section for more details.

  A Receiver supporting `in_and_out_of_band` MUST also support the `in_band` and `out_of_band` modes. Such Receiver SHOULD have all "in_band", "out_of_band" and "in_and_out_of_band" values enumerated in the Receiver Capabilities in order to allow Senders operating in any `parameter_sets_transport_mode`.
 
## RTP transport based on RFC 2250

For Nodes consuming AAC using the RTP payload mapping defined by RFC 2250, the Receiver resource MUST indicate `urn:x-nmos:transport:rtp` or one of its subclassifications for the `transport` attribute.

The following parameter constraints can be used to express limits or preferences specifically defined for AAC decoders:

- [Parameter Sets Flow Mode](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#parameter-sets-flow-mode)  
  A Receiver declares the `parameter_sets_flow_mode` capability to indicate that it supports bitstreams using parameter sets associated with strictly one (`strict`), one (`static`) or multiple (`dynamic`) Flows. Considering that active parameter sets are associated with a specific Flow, this capability indicates that a Receiver is capable or not of decoding an AAC bitstream where the associated Flow attributes change dynamically. 

  A Receiver consuming AAC using the RTP payload mapping defined by RFC 2250 MUST support the `dynamic` mode or be unconstrained.

- [Parameter Sets Transport Mode](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#parameter-sets-transport-mode)  
  A Receiver declares the `parameter_sets_transport_mode` capability to indicate that it supports bitstreams using parameter sets provided either only out-of-band, only in-band or in-and-out-of-band. The in-band parameter sets MAY update, augment or duplicate the parameter sets received out-of-band. A Receiver declaring the `in_band` or `in_and_out_of_band` capabilities MUST be capable of decoding in-band parameter sets that update, augment or duplicate the parameter sets received out-of-band. A Receiver declaring the `out_of_band` capability MUST be capable of decoding in-band parameter sets that duplicate the parameter sets received out-of-band.

  The config used by the bitstream MUST be compliant with the profile and level explicitly or implicitly declared in the member `profile-level-id` of the MPEG-4_audio_profile_and_level of the MPEG-4_audio_descriptor of an MPEG2-TS transport stream. The config MUST be specified in-band through the AAC bitstream. See the [Parameter Sets](#parameter-sets) section for more details.

  A Receiver consuming AAC using the RTP payload mapping defined by RFC 2250 MUST support the `in_band` mode or be unconstrained.

### Other transports

For Nodes consuming AAC using other transports, the Receiver resource MUST indicate the associated `urn:x-nmos:transport:` or `urn:x-matrox:transport:` label of the transport or one of its subclassifications for the `transport` attribute.

For Receivers indicating `urn:x-nmos:format:video` for the `format` attribute, the following parameter constraints can be used to express limits or preferences specifically defined for AAC decoders:

- [Parameter Sets Flow Mode](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#parameter-sets-flow-mode)  
  A Receiver declares the `parameter_sets_flow_mode` capability to indicate that it supports bitstreams using parameter sets associated with strictly one (`strict`), one (`static`) or multiple (`dynamic`) Flows. Considering that active parameter sets are associated with a specific Flow, this capability indicates that a Receiver is capable or not of decoding an AAC bitstream where the associated Flow attributes change dynamically. 

  A Receiver supporting the `dynamic` mode MUST also support the `strict` and `static` modes. Such Receiver SHOULD have `strict`, `static` and `dynamic` values enumerated in the Receiver Capability in order to allow Senders operating in any `parameter_sets_flow_mode`.

- [Parameter Sets Transport Mode](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#parameter-sets-transport-mode)  
  A Receiver declares the `parameter_sets_transport_mode` capability to indicate that it supports bitstreams using parameter sets provided either only out-of-band, only in-band or in-and-out-of-band. The in-band parameter sets MAY update, augment or duplicate the parameter sets received out-of-band. A Receiver declaring the `in_band` or `in_and_out_of_band` capabilities MUST be capable of decoding in-band parameter sets that update, augment or duplicate the parameter sets received out-of-band. A Receiver declaring the `out_of_band` capability MUST be capable of decoding in-band parameter sets that duplicate the parameter sets received out-of-band.

  Informative note: The out of band mechanism used to transmit parameter sets is transport specific and out of the scope of this specification.

  The config used by the bitstream MUST be compliant with the profile and level explicitly or implicitly declared using an out-of-band transport specific mechanism. The config MAY be specified in-band through the AAC bitstream, out-of-band using an unspecified mechanism or in-and-out-of-band using both mechanisms. See the [Parameter Sets](#parameter-sets) section for more details.

  A Receiver supporting `in_and_out_of_band` MUST also support the `in_band` and `out_of_band` modes. Such Receiver SHOULD have all "in_band", "out_of_band" and "in_and_out_of_band" values enumerated in the Receiver Capabilities in order to allow Senders operating in any `parameter_sets_transport_mode`.

For Receivers indicating `urn:x-nmos:format:mux` for the `format` attribute, the following parameter constraints can be used to express limits or preferences specifically defined for AAC decoders:

- [Parameter Sets Flow Mode](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#parameter-sets-flow-mode)  
  A Receiver declares the `parameter_sets_flow_mode` capability to indicate that it supports bitstreams using parameter sets associated with strictly one (`strict`), one (`static`) or multiple (`dynamic`) Flows. Considering that active parameter sets are associated with a specific Flow, this capability indicates that a Receiver is capable or not of decoding an AAC bitstream where the associated Flow attributes change dynamically. 

  A Receiver consuming AAC from a multiplexed stream MUST support the `dynamic` mode or be unconstrained.

- [Parameter Sets Transport Mode](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#parameter-sets-transport-mode)  
  A Receiver declares the `parameter_sets_transport_mode` capability to indicate that it supports bitstreams using parameter sets provided either only out-of-band, only in-band or in-and-out-of-band. The in-band parameter sets MAY update, augment or duplicate the parameter sets received out-of-band. A Receiver declaring the `in_band` or `in_and_out_of_band` capabilities MUST be capable of decoding in-band parameter sets that update, augment or duplicate the parameter sets received out-of-band. A Receiver declaring the `out_of_band` capability MUST be capable of decoding in-band parameter sets that duplicate the parameter sets received out-of-band.

  The config used by the bitstream MUST be compliant with the profile and level explicitly or implicitly declared in the transport stream. The config MUST be specified in-band through the AAC bitstream. See the [Parameter Sets](#parameter-sets) section for more details.

  A Receiver consuming AAC from a multiplexed stream MUST support the `in_band` mode or be unconstrained.
  
## AAC IS-05 Senders and Receivers

### RTP transport

Connection Management using IS-05 proceeds in exactly the same manner as for any other stream format carried within RTP.

If IS-04 Sender `manifest_href` is not `null`, the SDP transport file at the **/transportfile** endpoint on an IS-05 Sender MUST comply with the same requirements described for the SDP transport file at the IS-04 Sender `manifest_href`.

A `PATCH` request on the **/staged** endpoint of an IS-05 Receiver can contain an SDP transport file in the `transport_file` attribute. The SDP transport file for a AAC stream is expected to comply with RFC 3640 or RFC 6416 and, if appropriate IPMX. It need not comply with the additional requirements specified for SDP transport files at Senders.

If the Receiver is not capable of consuming the stream described by a `PATCH` on the **/staged** endpoint, it SHOULD reject the request. If it is unable to assess the stream compatibility because some parameters are not included in the `PATCH` request, it MAY accept the request and postpone stream compatibility assessment.

### Other transports

Connection Management using IS-05 proceeds in exactly the same manner as for any other stream format carried within other transports.

If IS-04 Sender `manifest_href` is not `null`, the SDP transport file at the **/transportfile** endpoint on an IS-05 Sender MUST comply with the same requirements described for the SDP transport file at the IS-04 Sender `manifest_href`.

If the Receiver is not capable of consuming the stream described by a `PATCH` on the **/staged** endpoint, it SHOULD reject the request. If it is unable to assess the stream compatibility because some parameters are not included `PATCH` request, it MAY accept the request and postpone stream compatibility assessment.

## Parameter Sets

The config of an AAC stream is transmitted by a Sender to a number of Receivers either out-of-band through an SDP transport file or in-band through the coded stream.

The `config` parameter of an SDP transport file MAY contain an out-of-band config. This config provide initial parameters for the AAC stream before the decoding starts.

An AAC stream using LATM or ADTS MAY transport in-band configs to update or duplicate a config received out-of-band, to define additional config or to update or duplicate a config received in-band. The `parameter_sets_transport_mode` Receiver Capability indicates when set to `in_band` or `in_and_out_of_band` that a Receiver supports getting updated, duplicated or additional configs in-band. When set to `out_of_band` a Receiver supports only getting initial config from the SDP transport file. In all the cases the Receiver MUST support getting duplicated config in-band (if any).

Informative note: Using RFC 3640, there will never be in-band configs.

The `config` parameter MAY be used by the Receiver to assert the `parameter_sets_transport_mode` in use by the Sender. The in-and-out-of-band mode is signaled if `config` is present and not empty, and terminates by a comma ','. The terminating colon ',' indicates that more configs will be received in-band, indicating the in-and-out-of-band mode. The out-of-band mode is signaled when `config` is present and not empty and not terminated by a comma ','. The in-band mode is signaled when `config` is not present or empty. A Sender MUST terminate the `conifig` parameter by a comma ',' if it operates in in-and-out-of-band mode and MUST not terminate it by a comma ',' in out-of-band mode.

Informative note: It results that an AAC Sender operating in in-and-out-of-band mode that is not sending parameter sets out-of-band will set the  `config` parameter to a single comma ',' value.

Informative note: The in-and-out-of-band mode implies that the Sender can optionally use the in-band path, the out-band path or both paths to transmit parameter sets. There is no requirement to use both paths simultaneously.

### Receivers

A Receiver MUST verify that the active config comply with the Receiver's Capabilities. If a Receiver support only out-of-band config it SHOULD perform the verification when a Controller PATCH the **/staged** endpoint for activation. In this situation, all the out-of-band config MUST be compliant with the Receiver Capabilities. Otherwise if a Receiver supports both out-of-band and in-band configs it SHOULD perform the verification of the out-of-band config when a Controller PATCH the **/staged** endpoint for activation and it MUST perform the verification of the in-band configs just-in-time as it decodes the stream. In this situation, all the out-of-band and in-band configs MUST be compliant with the Receiver Capabilities.

The `parameter_sets_flow_mode` Receiver Capability indicates when set to `dynamic` that a Receiver supports decoding an AAC stream where the active config values associated with Flow properties may changes dynamically. The Flow properties that are allowed to change correspond to the following attributes of a coded audio Flow: `sample_rate`, `format`, `media_type`, `profile`, `level`, `bit_rate`, `constant_bit_rate` and audio Source: `channels`. The "static" mode is more restrictive, requiring active config values associated with Flow attributes to be constant with the exception of the Flow's `bit_rate` attribute that MAY change.The `strict` mode has the further restriction that at most one SPS be used by the coded stream.

Informative note: The Flow bit_rate attribute is not included in the previous criterion to allow adapting to IP usable bandwidth changing conditions in `static` mode. The Source channels is considered part of the information associated with a Flow.

A Receiver with the `parameter_sets_flow_mode` capability set to `strict` requires that a coded stream uses a config defined once and associated with at most one Flow. Such config MAY be obtained out-of-band or in-band depending on the Receiver `parameter_sets_transport_mode` capability. When obtained out-of-band the `config` parameter of an SDP transport file or the parameter sets from a transport specific out-of-band mechanism MUST contain a config associated with only one Flow. When obtained in-band the `config` parameter of an SDP transport file or from a transport specific out-of-band mechanism MUST be empty or omitted and the Sender transmits the config associated with the Flow in-band. At all time, the Sender MAY transmit in-band configs that are duplicates of the configs obtained either out-of-band or in-band. When obtained in-and-out-of-band, in-band configs have priority over the out-of-band ones.

A Receiver with this capability set to `static` requires that a coded stream uses configs associated with at most one Flow. Such configs MAY be obtained out-of-band or in-band depending on the Receiver `parameter_sets_transport_mode` capability. When obtained out-of-band the `config` parameter of an SDP transport file or a transport specific out-of-band mechanism MUST contain a config associated with only one Flow. When obtained in-band the `config` parameter of an SDP transport file or a transport specific out-of-band mechanism MUST be empty or omitted and the Sender transmits the config associated with the Flow in-band. At all time, the Sender MAY transmit in-band configs that are duplicates of the configs obtained either out-of-band or in-band. When obtained in-and-out-of-band, in-band configs have priority over out-of-band ones.

Informative note: RFC 3640 does not allow in-band configs.

A Receiver with this capability set to `dynamic` supports that a coded stream uses configs that MAY be associated with multiple Flows on the Sender. Such configs MAY be obtained out-of-band or in-band according to the Receiver `parameter_sets_transport_mode` capability. When obtained out-of-band the `config` parameter of an SDP transport file or a transport specific out-of-band mechanism MAY contain a config associated with multiple Flows. When obtained in-band the `config` parameter of an SDP transport file or a transport specific out-of-band mechanism MUST be empty or omitted and the Sender MAY transmit in-band configs to update configs initially received out-of-band or to add and update new ones. At all time, the Sender MAY transmit in-band configs that are duplicates of the configs obtained either out-of-band or in-band. When obtained in-and-out-of-band, in-band configs have priority over out-of-band ones.

### Senders

A Sender MAY, unless constrained by IS-11, produce any AAC coded stream that is compliant with the `profile` and `level` of the associated Flow. Such a Sender MAY use one or multiple active parameter sets as per the [AAC][] specification. A Sender MAY seamlessly change dynamically the coded stream's active parameter sets, provided that the Flow associated with the Sender changes accordingly and the content of the SDP transport file does not change. If the content of the SDP transport file changes, the Sender MUST comply with IS-04, IS-05. A Sender indicates its mode of operation with the `parameter_sets_flow_mode` and `parameter_sets_transport_mode` attributes.

A Sender MUST transport configs `in_band` when the AAC stream is transmitted over an MPEG2-TS based transport as per the [H.222] specification.

A Sender operating with `parameter_sets_flow_mode` set to `strict` MUST produce a coded bitstream using at most one config associated with at most one Flow. The config MUST be defined once in-band or out-of-band and MAY be refreshed by in-band duplicates.

A Sender operating with `parameter_sets_flow_mode` set to `static` MAY produce a coded bitstream using a number of configs that MUST be associated with at most one Flow. The configs MAY be defined in-band or out-of-band and MAY be refreshed by in-band duplicates or updated, replaced or augmented by in-band ones.

A Sender operating with `parameter_sets_flow_mode` set to `dynamic` MAY produce a coded bitstream using a number of configs that MAY be associated with multiple Flows. The configs MAY be defined in-band or out-of-band and MAY be refreshed by in-band duplicates or updated, replaced or augmented by in-band ones.

## AAC IS-11 Senders and Receivers

### RTP transport

### Other transports

## Controllers

[AAC]: https://www.iso.org/standard/76383.html "ISO/IEC 14496-3 Coding of audio-visual objects"
[H.222.0]: https://www.itu.int/rec/T-REC-H.222.0 "Generic coding of moving pictures and associated audio information: Systems"
[RFC-2119]: https://tools.ietf.org/html/rfc2119 "Key words for use in RFCs"
[RFC-3640]: https://datatracker.ietf.org/doc/html/rfc3640 "RTP Payload Format for Transport of MPEG-4 Elementary Streams"
[RFC-6416]: https://datatracker.ietf.org/doc/html/rfc6416 "RTP Payload Format for MPEG-4 Audio/Visual Streams"
[RFC-2250]: https://tools.ietf.org/html/rfc2250 "RTP Payload Format for MPEG1/MPEG2 Video"
[IS-04]: https://specs.amwa.tv/is-04/ "AMWA IS-04 NMOS Discovery and Registration Specification"
[IS-05]: https://specs.amwa.tv/is-05/ "AMWA IS-05 NMOS Device Connection Management Specification"
[NMOS Parameter Registers]: https://specs.amwa.tv/nmos-parameter-registers/ "Common parameter values for AMWA NMOS Specifications"
[VSF]: https://vsf.tv/ "Video Services Forum"
[SMPTE]: https://www.smpte.org/ "Society of Media Professionals, Technologists and Engineers"
[BCP-004-01]: https://specs.amwa.tv/bcp-004-01/ "AMWA BCP-004-01 NMOS Receiver Capabilities"


- [ ] TODO: consider adding channel-order as per ST2110-30/31
