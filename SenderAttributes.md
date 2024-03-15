# Matrox NMOS Sender Attributes
{:.no_toc}  
Copyright 2023, Matrox Graphics Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
  
---
  
This document describes additional Sender attributes and their permitted values which may be used in Sender resources within the [AMWA IS-04 NMOS Discovery and Registration Specification](https://specs.amwa.tv/is-04).

{:toc}

### parameter_sets_transport_mode
- **Name:** `urn:x-matrox:parameter_sets_transport_mode`
- **Description:** Describes the parameter sets transport mode for compressed audio and video
- **Specification:** [AMWA IS-04](https://specs.amwa.tv/IS-04/v1.3), [AAC](https://github.com/alabou/NMOS-MatroxOnly/blob/main/NMOS%20With%20AAC.md), [H.264](https://github.com/alabou/NMOS-MatroxOnly/blob/main/NMOS%20With%20H.264.md), [H.265](https://github.com/alabou/NMOS-MatroxOnly/blob/main/NMOS%20With%20H.265.md)
- **Applicability:** 
- **Permitted Values:** `in-band`, `out-of-band`, `in-and-out-of-band`

### parameter_sets_flow_mode
- **Name:** `urn:x-matrox:parameter_sets_flow_mode`
- **Description:** Describes the parameter sets flow mode for compressed audio and video
- **Specification:** [AMWA IS-04](https://specs.amwa.tv/IS-04/v1.3), [AAC](https://github.com/alabou/NMOS-MatroxOnly/blob/main/NMOS%20With%20AAC.md), [H.264](https://github.com/alabou/NMOS-MatroxOnly/blob/main/NMOS%20With%20H.264.md), [H.265](https://github.com/alabou/NMOS-MatroxOnly/blob/main/NMOS%20With%20H.265.md)
- **Applicability:** 
- **Permitted Values:** `strict`, `static` and `dynamic`
