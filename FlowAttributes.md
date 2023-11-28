# Matrox NMOS Flow Attributes
{:.no_toc}

This document describes additional Flow attributes and their permitted values which may be used in Flow resources within the [AMWA IS-04 NMOS Discovery and Registration Specification](https://specs.amwa.tv/is-04).

{:toc}

### layer
- **Name:** `urn:x-matrox:layer`
- **Description:** This attributes identifies a sub-Flow providing an essence to a multiplexed Sender. It is valid and allowed only for a sub-Flow. A sub-Flow is a member of the `parents` attribute of a Flow of format `urn:x-nmos:format:mux`. The mux Flow is associated with a Sender providing Sender Capabilities.
- **Specification:** [AMWA IS-04](https://specs.amwa.tv/IS-04/v1.3), [Matrox Sender Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/SenderCapabilities.md)
- **Applicability:** 
- **Permitted Values:**
  - The layer value matching a sub-Flow Constraint Set of the Sender's Capabilities. It corresponds to an unsigned integer inthe range 0 to N-1 where N is the total number of layers of a given format.

### layer_compatibility_groups
- **Name:** `urn:x-matrox:layer_compatibility_groups`
- **Description:** This attributes identifies the compatibility groups of a sub-Flow providing an essence to a multiplexed Sender. It is valid and allowed only for a sub-Flow. A sub-Flow is a member of the `parents` attribute of a Flow of format `urn:x-nmos:format:mux`. The mux Flow is associated with a Sender providing Sender Capabilities.
- **Specification:** [AMWA IS-04](https://specs.amwa.tv/IS-04/v1.3), [Matrox Sender Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/SenderCapabilities.md)
- **Applicability:** 
- **Permitted Values:**
  - The layer_compatibility_groups value matching a sub-Flow Constraint Set of the Sender's Capabilities. It corresponds to an array of unsigned integers in the range 0 to 63 inclusively.
