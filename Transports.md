# Matrox NMOS Transports
{:.no_toc}

This document describes various transport protocols and defines the identifier used in the `transport` property of the Sender and Receiver resources defined in the [AMWA IS-04 NMOS Discovery and Registration Specification](https://specs.amwa.tv/is-04).

{:toc}

### NDI
- **Name:** `urn:x-matrox:transport:ndi`
- **Description:** Identifies the NDI Transport Protocol.
- **Specification:** [AMWA IS-04 v1.3](https://specs.amwa.tv/is-04/v1.3)
- **Applicability:** AMWA IS-04 since v1.3, IS-05 since v1.1

- The `ndi` transport is a multiplexed transport protocol comprising video, audio and data sub-streams. A Sender using the `ndi` transport must be associated with a Flow of format `urn:x-nmos:format:mux`. A Receiver using the `ndi` transport must be of format `urn:x-nmos:format:mux`.

### SRT
- **Name:** `urn:x-matrox:transport:srt`
- **Description:** Identifies the SRT Transport Protocol.
- **Specification:** [AMWA IS-04 v1.3](https://specs.amwa.tv/is-04/v1.3)
- **Applicability:** AMWA IS-04 since v1.3, IS-05 since v1.1

-The `srt` transport is, by default, an MPEG2-TS multiplexed transport protocol comprising video, audio, and data sub-streams.

- The protocol supports the `.mp2t` and `.rtp` subclassifications.
  -- The `mp2t` subclassification is the default one, being implicit when a subclassification is not povided. It corresponds to an MPEG2-TS multiplexed stream being sent through the `srt` protocol. A Sender using the `srt` or `srt.mp2t` transport must be associated with a Flow of format `urn:x-nmos:format:mux`. A Receiver using the `srt` or `srt.mp2t` transport must be of format `urn:x-nmos:format:mux`.
  --The `.rtp` subclassification corresponds to an RTP stream being sent through the `srt` protocol. The RTP stream be be an MPEG2-TS stream but this is signaled at the RTP level, not as a subclassification.

### USB
- **Name:** `urn:x-matrox:transport:usb`
- **Description:** Identifies the IPMX USB Transport Protocol.
- **Specification:** [AMWA IS-04 v1.3](https://specs.amwa.tv/is-04/v1.3)
- **Applicability:** AMWA IS-04 since v1.3, IS-05 since v1.1

- The `usb` transport is a data transport protocol comprising data sub-streams. A Sender using the `usb` transport must be associated with a Flow of format `urn:x-nmos:format:data`. A Receiver using the `ndi` transport must be of format `urn:x-nmos:format:data`.

### UDP
- **Name:** `urn:x-matrox:transport:udp`
- **Description:** Identifies the UDP Transport Protocol.
- **Specification:** [AMWA IS-04 v1.3](https://specs.amwa.tv/is-04/v1.3)
- **Applicability:** AMWA IS-04 since v1.3, IS-05 since v1.1

- The `udp` transport protocol is an MPEG2-TS multiplexed transport protocol comprising video, audio and data sub-streams. A Sender using the `usb` transport must be associated with a Flow of format `urn:x-nmos:format:mux`. A Receiver using the `udp` transport must be of format `urn:x-nmos:format:mux`.

### RTP.TCP
- **Name:** `urn:x-matrox:transport:rtp.tcp`
- **Description:** Identifies the RTP Transport Protocol over TCP
- **Specification:** [AMWA IS-04 v1.3](https://specs.amwa.tv/is-04/v1.3)
- **Applicability:** AMWA IS-04 since v1.3, IS-05 since v1.1

- The `rtp.tcp` transport is the RTP transport protocol over TCP instead of UDP.

