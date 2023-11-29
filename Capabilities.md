# Matrox NMOS Capabilities
{:.no_toc}

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
