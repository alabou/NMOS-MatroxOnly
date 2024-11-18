# NMOS Advanced Streaming Architecture

This repository describes the extended features of the NMOS Advanced Streaming Architecture developped by Matrox.

# Purpose and Key Features

## Purpose

The NMOS Advanced Streaming Architecture redefines IP-based media streaming for the professional AV (proAV) market. Designed to address the growing demand for flexible, secure, and scalable streaming workflows, these specifications extend the NMOS framework with advanced features that enhance configurability, interoperability, security, and resource management in both small-scale and large-scale systems.

**Key objectives include:**

1. **Unprecedented Configurability**:
   - Enable configuration through IS-11 of independent audio, video, data, and multiplexed (mux) streams, along with per-audio, per-video, and per-data sub-streams within multiplexed streams, allowing fine-grained control of individual media essences.
   - Leverage streams and sub-streams, sender and receiver capabilities, to dynamically adapt stream parameters such as resolution, bitrate, and format to match receiver and infrastructure requirements in real time.

2. **Unified Management**:
   - Unify the handling of both independent and multiplexed streams, streamlining configuration and simplifying operation in complex systems.

3. **Comprehensive Protocol and Media Support**:
   - Provide extensive compatibility with industry-standard transport protocols, including RTP, SRT, NDI, RTSP, MPEG2-TS over UDP, USB, and IPMX.
   - Ensure support for a wide range of media formats, including compressed (JPEG-XS, H.264, H.265, AAC), uncompressed (raw video, PCM audio), and multiplexed (MPEG2-TS, NDI, RTSP, AES3, AM824) streams.

4. **Enhanced Security**:
   - Integrate advanced security measures, including the IPMX Privacy Encryption Protocol (PEP) extended to non-IPMX flows, OAuth2.0-based authorization, and Node Reservation protocols.
   - Provide advanced HDCP support for baseband HDMI and HDCP over IP workflows with the IPMX HDCP Key Exchange Protocol (HKEP).

---

## Key Features

### 1. Stream and Sub-stream Configurability with IS-11

- **Fine-Grained Control**: IS-11 introduces the ability to configure individual streams and sub-streams within multiplexed flows, enabling precise control over each media essence.
- **Dynamic Adaptation**: Dynamic constraint-based negotiation ensures optimal configurations for varying network conditions and receiver capabilities.

### 2. Sender and Receiver Capabilities

- **Sender Capabilities**: Describe the range of supported formats, profiles, and parameters (e.g., supported resolutions, audio channels).
- **Receiver Capabilities**: Ensure the system dynamically selects the best configuration based on the receiver's capabilities and constraints.

### 3. Unified Group Management

- **Simplified Workflows**: Unifies the management of groups of independent streams and multiplexed streams under a common operational model.
- **Efficient Relationships**: Leverages compatibility groups and hierarchical structures to manage complex relationships between streams efficiently.

### 4. Advanced Security Framework

- **Extended Encryption**: The IPMX Privacy Encryption Protocol (PEP) extends beyond IPMX-compliant flows, securing non-IPMX streams with robust encryption.
- **Secure Access Control**: OAuth2.0 authorization provides secure access control for devices and workflows.
- **Resource Protection**: Node Reservation Protocol protects resources and prevents conflicts in shared environments.
- **HDCP Support**: The IPMX HDCP Key Exchange Protocol (HKEP) provides advanced HDCP support for baseband HDMI and HDCP over IP workflows.

### 5. Comprehensive Protocol and Media Type Support

- **Protocol Compatibility**: Supports an extensive range of transport protocols, including RTP, SRT, NDI, RTSP, MPEG2-TS over UDP, USB, and IPMX.
- **Media Format Versatility**: Accommodates a wide variety of media formats, such as compressed (JPEG-XS, H.264, H.265, AAC), uncompressed (raw video, PCM audio), and multiplexed (MPEG2-TS, NDI, RTSP, AES3, AM824) streams.

---

## Setting Expectations

These specifications represent a significant evolution in NMOS technology, offering unmatched configurability, interoperability, security, and resource management for proAV workflows. By enabling configuration of independent streams and per-sub-stream configuration within multiplexed flows, leveraging sender and receiver capabilities, and integrating advanced security protocols, they provide a state-of-the-art framework for the professional AV market. Whether managing small-scale systems or large distributed networks, these specifications ensure efficiency, reliability, and future-proof operation.

---

## Testing

The nmos-testing branch [MatroxOnly](https://github.com/alabou/nmos-testing/tree/MatroxOnly) provides the Matrox-Transports and Matrox-Capabilities test suites for testing the extended transports and capabilities.
