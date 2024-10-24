# Matrox NMOS Transports
{:.no_toc}  
Copyright 2023, Matrox Graphics Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
  
---
  
This document describes various transport protocols and defines the identifier used in the `transport` property of the Sender and Receiver resources defined in the [AMWA IS-04 NMOS Discovery and Registration Specification](https://specs.amwa.tv/is-04).

{:toc}

## Transports

This document summarize the various transports available.

### NDI
- **Name:** `urn:x-matrox:transport:ndi`
- **Description:** Identifies the NDI Transport Protocol.
- **Specification:** [AMWA IS-04 v1.3](https://specs.amwa.tv/is-04/v1.3)
- **Applicability:** AMWA IS-04 since v1.3, IS-05 since v1.1

- The `ndi` transport is a multiplexed transport protocol comprising video, audio and data sub-streams. A Sender using the `ndi` transport MUST be associated with a Flow of format `urn:x-nmos:format:mux`. A Receiver using the `ndi` transport MUST be of format `urn:x-nmos:format:mux`.

### SRT
- **Name:** `urn:x-matrox:transport:srt`
- **Description:** Identifies the SRT Transport Protocol.
- **Specification:** [AMWA IS-04 v1.3](https://specs.amwa.tv/is-04/v1.3)
- **Applicability:** AMWA IS-04 since v1.3, IS-05 since v1.1

-The `srt` transport is, by default, an MPEG2-TS multiplexed transport protocol comprising video, audio, and data sub-streams.

- The protocol supports the `.mp2t` and `.rtp` subclassifications.
  - The `mp2t` subclassification is the default one, being implicit when a subclassification is not povided. It corresponds to an MPEG2-TS multiplexed stream being sent through the SRT protocol. A Sender using the `srt` or `srt.mp2t` transport MUST be associated with a Flow of format `urn:x-nmos:format:mux`. A Receiver using the `srt` or `srt.mp2t` transport MUST be of format `urn:x-nmos:format:mux`.
  -The `.rtp` subclassification corresponds to an RTP stream being sent through the SRT protocol. The RTP stream MAY be an MPEG2-TS stream but this is signaled at the RTP level, not as a subclassification.

### USB
- **Name:** `urn:x-matrox:transport:usb`
- **Description:** Identifies the IPMX USB Transport Protocol.
- **Specification:** [AMWA IS-04 v1.3](https://specs.amwa.tv/is-04/v1.3)
- **Applicability:** AMWA IS-04 since v1.3, IS-05 since v1.1

- The `usb` transport is a data transport protocol comprising data sub-streams. A Sender using the `usb` transport MUST be associated with a Flow of format `urn:x-nmos:format:data`. A Receiver using the `usb` transport MUST be of format `urn:x-nmos:format:data`.

### UDP
- **Name:** `urn:x-matrox:transport:udp`
- **Description:** Identifies the UDP Transport Protocol.
- **Specification:** [AMWA IS-04 v1.3](https://specs.amwa.tv/is-04/v1.3)
- **Applicability:** AMWA IS-04 since v1.3, IS-05 since v1.1

- The `udp` transport protocol is, by default, an MPEG2-TS multiplexed transport protocol comprising video, audio and data sub-streams.

- The protocol supports the `.mcast`, `.ucast`, `.mp2t`, `.mp2t.mcast` and `.mp2t.ucast` subclassifications.
  - The `mp2t` subclassification is the default one, being implicit when a subclassification is not povided. It corresponds to an MPEG2-TS multiplexed stream being sent through the UDP protocol. A Sender using the `udp`, `udp.mp2t`, `udp.mcast`, `udp.ucast`, `udp.mp2t.mcast` or `udp.mp2t.ucast` transport MUST be associated with a Flow of format `urn:x-nmos:format:mux`. A Receiver using those transports MUST be of format `urn:x-nmos:format:mux`.

### RTP.TCP
- **Name:** `urn:x-matrox:transport:rtp.tcp`
- **Description:** Identifies the RTP Transport Protocol over TCP
- **Specification:** [AMWA IS-04 v1.3](https://specs.amwa.tv/is-04/v1.3)
- **Applicability:** AMWA IS-04 since v1.3, IS-05 since v1.1

- The `rtp.tcp` transport is the RTP transport protocol over TCP instead of UDP.

### RTSP
- **Name:** `urn:x-matrox:transport:rtsp`, `urn:x-matrox:transport:rtsp.tcp`
- **Description:** Identifies the RTSP Control Protocol over TCP (media transport as per SDP transport file from DESCRIBE)
- **Specification:** [AMWA IS-04 v1.3](https://specs.amwa.tv/is-04/v1.3)
- **Applicability:** AMWA IS-04 since v1.3, IS-05 since v1.1

## Multiplexing

A Flow of format `urn:x-nmos:format:mux` MUST have parents Flows of the `urn:x-nmos:format:audio`, `urn:x-nmos:format:video` or `urn:x-nmos:format:data` format. 

Informative Note: An opaque MPEG2-TS stream scenario is still possible using a Flow of format `urn:x-nmos:format:video` with the `video/MP2T` media type. This is similar to the opaque AES3 stream scenario using `urn:x-nmos:format:audio` as the Flow format and `audio/AM824` as the media type.

## Testing

The previous transports, along with the `urn:x-matrox:transport:rtp` transport can be tested using the forked [nmos-testing repository](https://github.com/alabou/nmos-testing.git) with the `MatroxOnly` branch. The `Matrox-Transports` testsuite provides the tests for the various transports.

Note: Currently the testsuite does not activate the Senders and Receivers to perform live/activation testing.
