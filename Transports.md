# Matrox NMOS Transports
{:.no_toc}

This document describes various transport protocols and defines the identifier used in the `transport` property of the Sender and Receiver resources defined in the [AMWA IS-04 NMOS Discovery and Registration Specification](https://specs.amwa.tv/is-04).

{:toc}

### NDI
- **Name:** `urn:x-matrox:transport:ndi`
- **Description:** Identifies the NDI Transport Protocol.
- **Specification:** [AMWA IS-04 v1.3](https://specs.amwa.tv/is-04/v1.3)
- **Applicability:** AMWA IS-04 since v1.3, IS-05 since v1.1

- The NDI transport is a multiplexed transport protocol comprised of video, audio and data sub-streams.

### SRT
- **Name:** `urn:x-matrox:transport:srt`
- **Description:** Identifies the SRT Transport Protocol.
- **Specification:** [AMWA IS-04 v1.3](https://specs.amwa.tv/is-04/v1.3)
- **Applicability:** AMWA IS-04 since v1.3, IS-05 since v1.1

- The SRT transport is by default an MPEG2-TS multiplexed transport protocol comprised of video, audio and data sub-streams.

- The protocol supports the `.mp2t` and `.rtp` subclassifications. The `mp2t` subclassification is the default one being used when a subclassification is not povided. It corresponds to an MPEG2-TS multiplexed stream being sent through the SRT protocol. The `.rtp` subclassification corresponds to an RTP stream being sent through the SRT protocol.

### USB
- **Name:** `urn:x-matrox:transport:usb`
- **Description:** Identifies the IPMX USB Transport Protocol.
- **Specification:** [AMWA IS-04 v1.3](https://specs.amwa.tv/is-04/v1.3)
- **Applicability:** AMWA IS-04 since v1.3, IS-05 since v1.1

- The USB transport is a multiplexed transport protocol comprised of data sub-streams.

### UDP
- **Name:** `urn:x-matrox:transport:udp`
- **Description:** Identifies the UDP Transport Protocol.
- **Specification:** [AMWA IS-04 v1.3](https://specs.amwa.tv/is-04/v1.3)
- **Applicability:** AMWA IS-04 since v1.3, IS-05 since v1.1

- The UDP transport protocol is an MPEG2-TS multiplexed transport protocol comprised of video, audio and data sub-streams.

### RTP.TCP
- **Name:** `urn:x-matrox:transport:rtp.tcp`
- **Description:** Identifies the RTP Transport Protocol over TCP
- **Specification:** [AMWA IS-04 v1.3](https://specs.amwa.tv/is-04/v1.3)
- **Applicability:** AMWA IS-04 since v1.3, IS-05 since v1.1

- The RTP.TCP transport is the RTP transport protocol over TCP instead of UDP.

