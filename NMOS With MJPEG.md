# Matrox: NMOS With MJPEG
{:.no_toc}  
Copyright 2026, Matrox Graphics Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
  
---
{:toc}

---
## Introduction

Motion JPEG is a coding approach in which each video frame is encoded as an independent JPEG image.
The RTP payload format for Motion JPEG is defined in IETF [RFC 2435][].

AMWA [IS-04][] and [IS-05][] already support RTP transport and can signal the media type `video/jpeg`.

## Use of Normative Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY",
and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119][].

## Definitions

The NMOS terms 'Controller', 'Node', 'Source', 'Flow', 'Sender', 'Receiver' are used as defined in the [NMOS Glossary](https://specs.amwa.tv/nmos/main/docs/Glossary.html).

In this document, "Motion JPEG" and "RTP/JPEG" refer to streams using the RTP payload mapping defined by [RFC 2435][].

## Motion JPEG IS-04 Sources, Flows and Senders

Nodes capable of transmitting Motion JPEG video streams MUST have Source, Flow and Sender resources in the IS-04 Node API.

Nodes MUST support IS-04 v1.3 to implement all aspects of this specification.
Partial implementation can be achieved using IS-04 v1.2 and earlier.

### Sources

The Source resource MUST indicate `urn:x-nmos:format:video` for the `format`.
Source resources can be associated with many Flows at the same time.
The Source is therefore unaffected by the use of Motion JPEG compression.

### Flows

The Flow resource MUST indicate `video/jpeg` in the `media_type` attribute, and `urn:x-nmos:format:video` for the `format`.
This has been permitted since IS-04 v1.1.

For Nodes implementing IS-04 v1.3 or higher, the following additional requirements on the Flow resource apply.

In addition to those attributes defined in IS-04 for all coded video Flows, the following attributes defined in the [Flow Attributes register](https://specs.amwa.tv/nmos-parameter-registers/branches/main/flow-attributes/) of the [NMOS Parameter Registers][] are used for Motion JPEG.

These attributes provide information for Controllers and Users to evaluate stream compatibility between Senders and Receivers.

- [Components](https://specs.amwa.tv/nmos-parameter-registers/branches/main/flow-attributes/#components)  
  The Flow resource MUST indicate color component sampling in `components`.
  The corresponding [RFC 2435][] type value is inferred from this sampling mode (type 0 for 4:2:2, type 1 for 4:2:0), with restart-marker variants 64 and 65 as applicable.
  For interoperability, Senders and Receivers complying with this specification MUST support [RFC 2435][] type 0 (4:2:2) and type 1 (4:2:0), and SHOULD support corresponding restart-marker types 64 and 65.
- [Quantization](https://specs.amwa.tv/nmos-parameter-registers/branches/main/flow-attributes/#quantization)  
  The Flow resource MUST indicate `quantization`, corresponding to the [RFC 2435][] `Q` field used for the stream.
  For type values 0/1/64/65, `quantization` values below 128 other than 1-99 are reserved and SHOULD NOT be used.
  A value in the range 128-255 indicates explicit quantization table signaling as defined by [RFC 2435][].

The Flow `frame_width` and `frame_height` MUST be consistent with the displayed image dimensions signaled by RTP/JPEG ([RFC 2435][] width/height fields, in 8-pixel units).
The Flow `quantization` value MUST match the RTP/JPEG `Q` value used by the stream.
For `quantization` values 1-99 (types 0/1/64/65), quantization tables MUST follow [RFC 2435][] Section 4.2.
For `quantization` values 128-255, a Quantization Table header MUST be present in the first packet of each frame (`fragment offset = 0`) per [RFC 2435][] Section 3.1.8.
For quality/bandwidth tradeoff, [RFC 2435][] `Q` is the primary coding control.

### Senders

For Nodes transmitting Motion JPEG using the RTP payload mapping defined by [RFC 2435][], the Sender resource MUST indicate `urn:x-nmos:transport:rtp` or one of its subclassifications for the `transport` attribute.
Sender resources provide no indication of media type or format, since this is described by the associated Flow resource.

The SDP file at the `manifest_href` MUST comply with the requirements of [RFC 2435][] and the following additional requirements.

Senders MUST apply [RFC 2435][] `Q` handling consistent with the Flow `quantization` value and the Flow requirements above.

Additionally, the SDP file needs to convey, so far as the defined parameters allow, the same information about the stream as conveyed by the Source, Flow and Sender attributes (or their defaults, when omitted) defined by this specification and IS-04 using the following parameters:

- depth:
  Determines the number of bits per sample. This is an integer limited by [RFC 2435][] to the value 8 for interoperability profile types 0, 1, 64, and 65.
- width:
  Determines the number of pixels per line. This is an integer between 8 and 2040, inclusive.
- height:
  Determines the number of lines per video frame. This is an integer between 8 and 2040, inclusive.
- exactframerate:
  Signals the video frame rate in frames per second. Integer frame rates MUST be signaled as a single decimal number (e.g., "25") whilst non-integer frame rates MUST be signaled as a ratio of two integer decimal numbers separated by a "forward-slash" character (e.g., "30000/1001"), utilizing the numerically smallest numerator value possible.
- interlace:
  If this parameter name is present, it indicates that the video is interlaced, or that the video is Progressive segmented Frame (PsF). If this parameter name is not present, the progressive video format MUST be assumed.
- sampling:
  Signals the color difference signal sub-sampling structure.
  For interoperability with [RFC 2435][] types 0/1/64/65, this parameter MUST be one of:
  - YCbCr-4:2:2 (corresponding to type 0 or 64)
  - YCbCr-4:2:0 (corresponding to type 1 or 65)

- colorimetry:
  Specifies the system colorimetry used by the image samples. Valid values and their specification are the following:

  - BT601-5: [BT.601-5][]  
  - BT709-2: [BT.709-2][]  
  - SMPTE240M: [SMPTE240M][]  
  - BT601: [BT.601-7][]  
  - BT709: [BT.709-6][]  
  - BT2020: [BT.2020-2][]  
  - BT2100: [BT.2100-2][]  
  - UNSPECIFIED: Colorimetry is signaled in the payload, or it must be manually coordinated between sender and receiver.  

  Signals utilizing the [BT.2100-2][] colorimetry SHOULD also signal the representational range using the optional parameter RANGE defined below. Signals utilizing the UNSPECIFIED colorimetry might require manual coordination between the sender and the receiver.

- TCS:
  Transfer Characteristic System. This parameter specifies the transfer characteristic system of the image samples. Valid values and their specification are the following:

  - SDR:
    Standard Dynamic Range video streams that utilize the Optical Electrical Transfer Function (OETF) of [BT.709-6][] or [BT.2020-2][]. Such streams MUST be assumed to target the Electro-Optical Transfer Function (EOTF) specified in [BT.1886-0][].

  - PQ:
    High dynamic range video streams that utilize the Perceptual Quantization system of [BT.2100-2][].

  - HLG:
    High dynamic range video streams that utilize the Hybrid Log-Gamma system of [BT.2100-2][].

  - UNSPECIFIED:
    Video streams whose transfer characteristics are signaled by the payload, or that must be manually coordinated between sender and receiver.

- RANGE:
  This parameter SHOULD be used to signal the encoding range of the sample values within the stream. When paired with [BT.2100-2][] colorimetry, this parameter has two allowed values, NARROW and FULL, corresponding to the ranges specified in TABLE 9 of [BT.2100-2][]. In any other context, this parameter has three allowed values: NARROW, FULLPROTECT, and FULL, which correspond to the ranges specified in [SMPTE2077][]. In the absence of this parameter, and for all but the UNSPECIFIED colorimetry, NARROW MUST be the assumed value. When paired with the UNSPECIFIED colorimetry, FULL MUST be the default assumed value.

For interoperability in NMOS systems, Senders SHOULD use [RFC 2435][] type values 0, 1, 64, or 65. Type values 128-255 require additional session-level agreement outside [RFC 2435][] and SHOULD NOT be used unless Sender and Receiver behavior is explicitly coordinated.

## Motion JPEG IS-04 Receivers

Nodes capable of receiving Motion JPEG video streams MUST have a Receiver resource in the IS-04 Node API, which lists `video/jpeg` in the `media_types` array within the `caps` object.

If the Receiver has limitations on or preferences regarding the Motion JPEG streams that it supports, the Receiver resource MUST indicate constraints in accordance with the [BCP-004-01][] Receiver Capabilities specification.
The Receiver SHOULD express its constraints as precisely as possible, to allow a Controller to determine with a high level of confidence the Receiver's compatibility with the available streams.
It is not always practical for the constraints to indicate every type of stream that a Receiver can or cannot consume successfully; however, they SHOULD describe as many of its commonly used operating points as practical and any preferences among them.

The `constraint_sets` parameter within the `caps` object can be used to describe combinations of frame rates, width and height, and other parameters which the Receiver can support, using the parameter constraints defined in the [Capabilities register](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/) of the NMOS Parameter Registers.

The following parameter constraints are appropriate to express limitations on supported Motion JPEG streams:

- [Quantization](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#quantization)

Other existing parameter constraints, such as the following, are also appropriate to express limitations on supported MJPEG video streams:

- [Frame Width](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#frame-width)
- [Frame Height](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#frame-height)
- [Color Sampling](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#color-sampling)
- [Component Depth](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/#component-depth)

To maximize interoperability, Receivers complying with this specification MUST support [RFC 2435][] type values 0 and 1, and SHOULD support corresponding restart-marker types 64 and 65.

## Motion JPEG IS-05 Senders and Receivers

Connection Management using IS-05 proceeds in exactly the same manner as for any other stream format carried within RTP.

The SDP file at the **/transportfile** endpoint on an IS-05 Sender MUST comply with the same requirements described for the SDP file at the IS-04 Sender `manifest_href`.

A `PATCH` request on the **/staged** endpoint of an IS-05 Receiver can contain an SDP file in the `transport_file` attribute.
The SDP file for a Motion JPEG stream is expected to comply with [RFC 2435][].
It need not comply with the additional requirements specified for SDP files at Senders.

If the Receiver is not capable of consuming the stream described by the SDP file, it SHOULD reject the request.
If it is unable to assess stream compatibility (for example, due to session-specific behavior associated with dynamically defined type values), it MAY accept the request.

## Controllers

Controllers MUST use IS-04 to discover Motion JPEG Senders and Receivers and IS-05 to manage connections between them.
Controllers MUST support IS-04 v1.3 to implement all aspects of this specification.
Partial implementation can be achieved using IS-04 v1.2 and earlier.

Controllers MUST support the BCP-004-01 Receiver Capabilities mechanism and all parameter constraints listed in this specification in order to evaluate stream compatibility between Motion JPEG Senders and Receivers.

[BCP-004-01]: https://specs.amwa.tv/bcp-004-01/ "AMWA BCP-004-01 NMOS Receiver Capabilities"
[RFC 2119]: https://tools.ietf.org/html/rfc2119 "Key words for use in RFCs"
[RFC 2435]: https://tools.ietf.org/html/rfc2435 "RTP Payload Format for JPEG-compressed Video"
[IS-04]: https://specs.amwa.tv/is-04/ "AMWA IS-04 NMOS Discovery and Registration Specification"
[IS-05]: https://specs.amwa.tv/is-05/ "AMWA IS-05 NMOS Device Connection Management Specification"
[MJPEG]: https://en.wikipedia.org/wiki/Motion_JPEG "Overview of Motion JPEG"
[NMOS Parameter Registers]: https://specs.amwa.tv/nmos-parameter-registers/ "Common parameter values for AMWA NMOS Specifications"
[BT.1886-0]: https://www.itu.int/rec/R-REC-BT.1886-0-201103-I/en "ITU-R Recommendation BT.1886-0 (March 2011)"
[BT.2020-2]: https://www.itu.int/rec/R-REC-BT.2020-2-201510-I/en "ITU-R Recommendation BT.2020-2 (October 2015)"
[BT.2100-2]: https://www.itu.int/rec/R-REC-BT.2100-2-201807-I/en "ITU-R Recommendation BT.2100-2 (July 2018)"
[BT.601-5]: https://www.itu.int/rec/R-REC-BT.601-5-199510-S/en "ITU-R Recommendation BT.601-5 (October 1995)"
[BT.601-7]: https://www.itu.int/rec/R-REC-BT.601-7-201103-I/en "ITU-R Recommendation BT.601-7 (March 2011)"
[BT.709-2]: https://www.itu.int/rec/R-REC-BT.709-2-199510-S/en "ITU-R Recommendation BT.709-2 (October 1995)"
[BT.709-6]: https://www.itu.int/rec/R-REC-BT.709-6-201506-I/en "ITU-R Recommendation BT.709-6 (June 2015)"
[SMPTE2077]: https://ieeexplore.ieee.org/document/7290588 "SMPTE RP 2077:2013, Full-Range Image Mapping"
[SMPTE240M]: https://ieeexplore.ieee.org/document/7291461 "SMPTE ST 240M:1999, 1125-Line High-Definition Production Systems - Signal Parameters"

