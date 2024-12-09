# Matrox NMOS Flow Attributes
{:.no_toc}  
Copyright 2023, Matrox Graphics Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
  
---
  
This document describes additional Flow attributes and their permitted values which may be used in Flow resources within the [AMWA IS-04 NMOS Discovery and Registration Specification](https://specs.amwa.tv/is-04).

{:toc}

### layer
- **Name:** `urn:x-matrox:layer`
- **Description:** This attributes identifies a sub-Flow providing an essence to a multiplexed Sender. It is valid and allowed only for a sub-Flow. A sub-Flow is a member of the `parents` attribute of a Flow of format `urn:x-nmos:format:mux`. The mux Flow is associated with a Sender providing Sender Capabilities.
- **Specification:** [AMWA IS-04](https://specs.amwa.tv/IS-04/v1.3), [Matrox Sender Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/SenderCapabilities.md)
- **Applicability:** 
- **Permitted Values:**
  - The layer value matching a sub-Flow Constraint Set of the Sender's Capabilities. It corresponds to an unsigned integer in the range 0 to N-1 where N is the total number of layers of a given format.

### layer_compatibility_groups
- **Name:** `urn:x-matrox:layer_compatibility_groups`
- **Description:** This attributes identifies the compatibility groups of a sub-Flow providing an essence to a multiplexed Sender. It is valid and allowed only for a sub-Flow. A sub-Flow without a `urn:x-matrox:layer_compatibility_groups` attribute is assumed as being part of all groups. A sub-Flow is a member of the `parents` attribute of a Flow of format `urn:x-nmos:format:mux`. The mux Flow is associated with a Sender providing Sender Capabilities. 
- **Specification:** [AMWA IS-04](https://specs.amwa.tv/IS-04/v1.3), [Matrox Sender Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/SenderCapabilities.md)
- **Applicability:** 
- **Permitted Values:**
  - The layer_compatibility_groups value matching a sub-Flow Constraint Set of the Sender's Capabilities. It corresponds to an array of unsigned integers in the range 0 to 63 inclusively.

### audio_layers, video_layers, data_layers
- **Name:** `urn:x-matrox:audio_layers`, `urn:x-matrox:video_layers`, `urn:x-matrox:data_layers`
- **Description:** This attributes identifies how many sub-Flows of a given format are providing essences to a multiplexed Sender. It is valid and allowed only for Flow of format `urn:x-nmos:format:mux`. The mux Flow is associated with a Sender providing Sender Capabilities.
- **Specification:** [AMWA IS-04](https://specs.amwa.tv/IS-04/v1.3), [Matrox Sender Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/SenderCapabilities.md)
- **Applicability:** 
- **Permitted Values:**
  - It corresponds to an unsigned integer in the range 0 to N-1 where N is the total number of layers of a given format.

### constant_bit_rate
- **Name:** `urn:x-matrox:constant_bit_rate`
- **Description:** This attributes qualifies the `bit_rate` attribute as being constant or variable.
- **Specification:** [AMWA IS-04](https://specs.amwa.tv/IS-04/v1.3), [Matrox Sender Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/SenderCapabilities.md)
- **Applicability:** 
- **Permitted Values:** true, false
