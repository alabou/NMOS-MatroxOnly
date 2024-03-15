# Matrox NMOS Source Attributes
{:.no_toc}  
Copyright 2023, Matrox Graphics Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
  
---
  
This document describes additional Source attributes and their permitted values which may be used in Source resources within the [AMWA IS-04 NMOS Discovery and Registration Specification](https://specs.amwa.tv/is-04).

{:toc}

### receiver_id
- **Name:** `urn:x-matrox:receiver_id`
- **Description:** This attributes indicates the Receiver providing the essence to the Source.
- **Specification:** [AMWA IS-04](https://specs.amwa.tv/IS-04/v1.3)
- **Applicability:** 
- **Permitted Values:**
  - The UUID of a Receiver.

### layer
- **Name:** `urn:x-matrox:layer`
- **Description:** This attributes indicates the Receiver's sub-Stream providing the essence to the Source.
- **Specification:** [AMWA IS-04](https://specs.amwa.tv/IS-04/v1.3), [Matrox Receiver Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/ReceiverCapabilities.md)
- **Applicability:** 
- **Permitted Values:**
  - The layer value matching a sub-Stream Constraint Set of the Receiver's Capabilities.

### synchronous_media
- **Name:** `urn:x-matrox:synchronous_media`
- **Description:** This attributes indicates the media is synchronous (true) or asynchronous (false) to the source reference clock. An unspecified attribute shall be interpreted according to the operational environment. For an ST-2110 environment an unspecified attribute must be interpreted as synchronous media. For an IPMX environment an unspecified attribute must be interpreted as an asynchronous media. If this attribute is not specified for a Source then the SDP transport file a=mediaclk attribute should be used to know about the media being synchronous or asynchronous.
- **Specification:** [AMWA IS-04](https://specs.amwa.tv/IS-04/v1.3)
- **Applicability:** 
- **Permitted Values:** true, false
