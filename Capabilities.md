# Matrox NMOS Capabilities
{:.no_toc}  
Copyright 2023, Matrox Graphics Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
  
---
  
This document describes values that may be used to identify a capability, used in the `caps` property of the resources defined in the [AMWA IS-04 NMOS Discovery and Registration Specification](https://specs.amwa.tv/is-04).

{:toc}

## Constraint Set Metadata
### format
- **Name:** `urn:x-matrox:cap:meta:format`
- **Description:** Indicates the format associated with the Constraint Set
- **Specification:** [Sender Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/SenderCapabilities.md), [Receiver Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/ReceiverCapabilities.md)
  - **Type:** string
- **Applicability:** AMWA IS-04 v1.3

### layer
- **Name:** `urn:x-matrox:cap:meta:layer`
- **Description:** Indicates the layer associated with the Constraint Set
- **Specification:** [Sender Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/SenderCapabilities.md), [Receiver Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/ReceiverCapabilities.md)
  - **Type:** integer
- **Applicability:** AMWA IS-04 v1.3

### layer_compatibility_groups
- **Name:** `urn:x-matrox:cap:meta:layer_compatibility_groups`
- **Description:** Indicates the layer compatibility groups associated with the Constraint Set
- **Specification:** [Sender Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/SenderCapabilities.md), [Receiver Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/ReceiverCapabilities.md)
  - **Type:** array of integer
- **Applicability:** AMWA IS-04 v1.3

## Parameter Constraints
### audio_layers
- **Name:** `urn:x-matrox:cap:format:audio_layers`
- **Description:** Provide a minimum, maximum or list of layers allowed for multiplexed stream.
- **Specification:** [Sender Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/SenderCapabilities.md), [Receiver Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/ReceiverCapabilities.md), [Flow Attributes](https://github.com/alabou/NMOS-MatroxOnly/blob/main/FlowAttributes.md)
  - **Type:** integer
  - **Target:** (a) Flow `urn:x-matrox:audio_layers` attribute of a mux Flow, (b) Number of audio sub-streams of a mux Receiver.
- **Applicability:** AMWA IS-04 v1.3

### video_layers
- **Name:** `urn:x-matrox:cap:format:video_layers`
- **Description:** Provide a minimum, maximum or list of layers allowed for multiplexed stream.
- **Specification:** [Sender Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/SenderCapabilities.md), [Receiver Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/ReceiverCapabilities.md), [Flow Attributes](https://github.com/alabou/NMOS-MatroxOnly/blob/main/FlowAttributes.md)
  - **Type:** integer
  - **Target:** (a) Flow `urn:x-matrox:video_layers` attribute of a mux Flow, (b) Number of video sub-streams of a mux Receiver.
- **Applicability:** AMWA IS-04 v1.3

### data_layers
- **Name:** `urn:x-matrox:cap:format:data_layers`
- **Description:** Provide a minimum, maximum or list of layers allowed for multiplexed stream.
- **Specification:** [Sender Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/SenderCapabilities.md), [Receiver Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/ReceiverCapabilities.md), [Flow Attributes](https://github.com/alabou/NMOS-MatroxOnly/blob/main/FlowAttributes.md)
  - **Type:** integer
  - **Target:** (a) Flow `urn:x-matrox:data_layers` attribute of a mux Flow, (b) Number of data sub-streams of a mux Receiver.
- **Applicability:** AMWA IS-04 v1.3

### hkep
- **Name:** `urn:x-matrox:cap:transport:hkep`
- **Description:** Indicate that the Receiver / Sender supports HDCP / HKEP protected streams. A value false means that HDCP / HKEP streams are not supported, a value true means that only HDCP / HKEP streams are supported, a value { true, false } or {} indicate that both HDCP / HKEP protected streams and non-protected streams are supported.
- **Specification:** [Sender Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/SenderCapabilities.md), [Receiver Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/ReceiverCapabilities.md), [HKEP](https://vsf.tv/download/technical_recommendations/VSF_TR-10-5_2022-03-22.pdf)
  - **Type:** boolean
  - **Target:** (a) SDP attribute `a=hkep:` parameter 
- **Applicability:** AMWA IS-04 v1.3

### privacy
- **Name:** `urn:x-matrox:cap:transport:privacy`
- **Description:** Indicate that the Receiver / Sender supports Privacy Encryption Protocol (PEP) protected streams. A value false means that PEP streams are not supported, a value true means that only PEP streams are supported, a value { true, false } or {} indicate that both PEP protected streams and non-protected streams are supported.
- **Specification:** [Sender Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/SenderCapabilities.md), [Receiver Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/ReceiverCapabilities.md), [PEP](https://vsf.tv/download/technical_recommendations/VSF_TR-10-13_2024-02-13.pdf)
  - **Type:** boolean
  - **Target:** (a) SDP attribute `a=privacy:` parameter (b) IS-05 `ext_privacy` transport parameters
- **Applicability:** AMWA IS-04 v1.3
- 
### channel_order
- **Name:** `urn:x-matrox:cap:transport:channel_order`
- **Description:** Provides the ordering of channels into groups as per ST 2110-30 and ST 2110-31 channel grouping symbols for PCM streams and opaque AM824 streams. This capability should not be used for fully described AM824 streams as the sub-streams capabilities are much more expressive. The SMPTE2110 channel-order convention is used as in the following example "SMPTE2110.(51,ST)" having two groups for a total of 8 channels.
- **Specification:** SMPTE ST 2110-30 and ST 2110-31, [Sender Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/SenderCapabilities.md), [Receiver Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/ReceiverCapabilities.md), [NMOS With AES3](https://github.com/alabou/NMOS-MatroxOnly/blob/main/NMOS%20With%20AES3.md)
  - **Type:** string
  - **Target:** (a) SDP channel-order parameter of PCM streams and opaque AM824 streams.
- **Applicability:** AMWA IS-04 v1.3

### parameter_sets_transport_mode
- **Name:** `urn:x-matrox:cap:transport:parameter_sets_transport_mode`
- **Description:** Identifies the acceptable parameter sets transport modes.
- **Specification:** per AMWA BCP-004-01
  - **Type:** string (enumerated values as per the specifications [H.264](https://github.com/alabou/NMOS-MatroxOnly/blob/main/NMOS%20With%20H.264.md), [H.265](https://github.com/alabou/NMOS-MatroxOnly/blob/main/NMOS%20With%20H.265.md), [AAC](https://github.com/alabou/NMOS-MatroxOnly/blob/main/NMOS%20With%20AAC.md))
  - **Target:** (a) Sender `parameter_sets_transport_mode`, (b) SDP attribute `a=fmtp:` format-specific parameter `sprop-parameter-sets`, per [RFC 6184][RFC-6184], (c) SDP attribute `a=fmtp:` format-specific parameters `sprop-vps`, `sprop-sps` and `sprop-pps`, per [RFC 7798][RFC-7798], (d) SDP attribute `a=fmtp:` format-specific parameter `config` per [RFC 6416][RFC-6416]
- **Applicability:** AMWA IS-04

### parameter_sets_flow_mode
- **Name:** `urn:x-matrox:cap:transport:parameter_sets_flow_mode`
- **Description:** Identifies the acceptable parameter sets flow modes.
- **Specification:** per AMWA BCP-004-01
  - **Type:** string (enumerated values as per the specifications [H.264](https://github.com/alabou/NMOS-MatroxOnly/blob/main/NMOS%20With%20H.264.md), [H.265](https://github.com/alabou/NMOS-MatroxOnly/blob/main/NMOS%20With%20H.265.md), [AAC](https://github.com/alabou/NMOS-MatroxOnly/blob/main/NMOS%20With%20AAC.md))
  - **Target:** (a) Sender `parameter_sets_flow_mode`
- **Applicability:** AMWA IS-04
