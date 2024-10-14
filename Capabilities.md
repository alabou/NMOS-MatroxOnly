# Matrox NMOS Capabilities
{:.no_toc}  
Copyright 2023, Matrox Graphics Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
  
---
  
This document describes values that may be used to identify a capability, used in the `caps` property of the resources defined in the [AMWA IS-04 NMOS Discovery and Registration Specification](https://specs.amwa.tv/is-04). Note that capabilities are defined from the Receiver Capabilities perspective but are allowed to be used as Sender Capabilities also. When Sender Capabilities are available, they become an alternate target that a Controller MAY use to verifiy compliance with Receiver Capabilities.

{:toc}

## Manufacturer defined capabilities

The [NMOS Parameter Registers](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/) allows Manufacturer to define and use their own capabilities.

>`Manufacturers MAY use their own namespaces to indicate capabilities which are not currently defined within the NMOS namespace (urn:x-nmos:cap:). In order to avoid collisions with simple names allocated by AMWA specifications, they MUST NOT use capability names that do not start with urn:.`

The JSON schemas constraint_set.json used by IS-04 and IS-11 and constraints_supported.json used by IS-11 do not adhere to the language of the [NMOS Parameter Registers](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/) by not allowing Manufacturer's namespaces. The following schemas MUST be used.

> The manufacturer namespace is expected to use lower case letters only. This seems a reasonable restriction.

### Updated JSON schemas
constraint-set.json
```
{
  ...
   "patternProperties": {
      "^urn:x-nmos:cap:(?!meta:)": {
        "$ref": "param_constraint.json"
      }
  }
  
  "patternProperties": {
      "^urn:x-[a-z]+:cap:(?!meta:)": {
        "$ref": "param_constraint.json"
      }
  }

  "patternProperties": {
      "^urn:x-[a-z]+:cap:meta:": {
          "oneOf": [
              {
                "type": [ "boolean", "integer", "number", "string", "null" ]
              },
              {
                "type": "array",
                "items": {
                    "type": [ "boolean", "integer", "number", "string" ]
                }
              }
          ]
      }
  }
  ...
}
```

constraints_supported.json
```
{
  ...
  {
    "pattern": "^urn:x-nmos:cap:"
  },
  {
    "pattern": "^urn:x-[a-z]+:cap:"
  }
  ...
}
```

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

### constant_bit_rate
- **Name:** `urn:x-matrox:cap:format:constant_bit_rate`
- **Description:** Identifies the `bit_rate` of a Flow as being constant or variable.
- **Specification:** [Matrox Sender Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/SenderCapabilities.md), [Matrox Receiver Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/ReceiverCapabilities.md)
- **Type:** boolean
- **Target:** (a) Flow's `constant_bit_rate` attribute
- **Applicability:** AMWA IS-04 v1.3

### parameter_sets_transport_mode
- **Name:** `urn:x-matrox:cap:transport:parameter_sets_transport_mode`
- **Description:** Identifies the acceptable parameter sets transport modes.
- **Specification:** [Matrox Sender Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/SenderCapabilities.md), [Matrox Receiver Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/ReceiverCapabilities.md)
  - **Type:** string (enumerated values as per the specifications [H.264](https://github.com/alabou/NMOS-MatroxOnly/blob/main/NMOS%20With%20H.264.md), [H.265](https://github.com/alabou/NMOS-MatroxOnly/blob/main/NMOS%20With%20H.265.md), [AAC](https://github.com/alabou/NMOS-MatroxOnly/blob/main/NMOS%20With%20AAC.md))
  - **Target:** (a) Sender `parameter_sets_transport_mode`, (b) SDP attribute `a=fmtp:` format-specific parameter `sprop-parameter-sets`, per [RFC 6184][RFC-6184], (c) SDP attribute `a=fmtp:` format-specific parameters `sprop-vps`, `sprop-sps` and `sprop-pps`, per [RFC 7798][RFC-7798], (d) SDP attribute `a=fmtp:` format-specific parameter `config` per [RFC 6416][RFC-6416]
- **Applicability:** AMWA IS-04 v1.3

### parameter_sets_flow_mode
- **Name:** `urn:x-matrox:cap:transport:parameter_sets_flow_mode`
- **Description:** Identifies the acceptable parameter sets flow modes.
- **Specification:** [Sender Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/SenderCapabilities.md), [Receiver Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/ReceiverCapabilities.md)
  - **Type:** string (enumerated values as per the specifications [H.264](https://github.com/alabou/NMOS-MatroxOnly/blob/main/NMOS%20With%20H.264.md), [H.265](https://github.com/alabou/NMOS-MatroxOnly/blob/main/NMOS%20With%20H.265.md), [AAC](https://github.com/alabou/NMOS-MatroxOnly/blob/main/NMOS%20With%20AAC.md))
  - **Target:** (a) Sender `parameter_sets_flow_mode`
- **Applicability:** AMWA IS-04 v1.3

### clock_ref_type
- **Name:** `urn:x-matrox:cap:transport:clock_ref_type`
- **Description:** Identifies the acceptable clock reference supported by a Receiver. The clock associated with a Flow is identified by the `clock_name` attribute of the Source associated with the Flow. The value `internal` implies recovering the Sender's internal clock, while the value `ptp` implies using the common reference clock. 
- **Specification:** [Sender Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/SenderCapabilities.md), [Receiver Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/ReceiverCapabilities.md)
  - **Type:** string (enumerated values as per IS-04 schema clock_internal.json `internal` and clock_ptp.json `ptp`)
  - **Target:** (a) `ref_type` of Source's associated `clock_name` clock. (b) SDP a=ts-refclk attributes
- **Applicability:** AMWA IS-04 v1.3

### synchronous_media
- **Name:** `urn:x-matrox:cap:transport:synchronous_media`
- **Description:** Identifies the acceptable media types supported by a Receiver. A media is either synchronous or asynchronous to the reference clock. A receiver may support either or both types.
- **Specification:** [Sender Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/SenderCapabilities.md), [Receiver Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/ReceiverCapabilities.md)
  - **Type:** boolean
  - **Target:** (a) `urn:x-matrox:synchronous_media` attribute of a Source. (b) SDP a=mediaclk attribute (`sender` implies asynchronous, `direct` implies synchronous)
- **Applicability:** AMWA IS-04 v1.3

### info_block
- **Name:** `urn:x-matrox:cap:transport:info_block`
- **Description:** Identifies if the Receiver supports in-band dynamic updates of some of the media stream attributes from Media Info Blocks. The info block mechanism is standard for IPMX Senders but it is optional for Receivers. A list of supported Media Info Block types is provided. En empty list indicate that the info block mechanism is not supported at all. A list having only the value 0, which is an invalid media info block type identifier, serves the same purpose. A partial list indicate the Media Info Block types that are supported. When media stream attributes associated with a Sender change, a Controller may let the Receiver handle the media stream attributes changes from the media info blocks produced by the Sender, if all of media info block types produced by a Sender are supported by the Receiver. Note that for coded Flows the Sender `parameter_sets_flow_mode` attribute allows for a similar functionality when the content of the SDP transport file does not change. The `info_block` capability allows for more flexibility when the SDP transport file changes are transmitted as part of the IPMX info block.
- **Specification:** [Sender Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/SenderCapabilities.md), [Receiver Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/ReceiverCapabilities.md)
  - **Type:** array of integer (Media Info Block type identifiers)
  - **Target:** (a) `transport_file` activation attribute of the Receiver.
- **Applicability:** AMWA IS-04 v1.3, AMWA IS-05 v1.1
