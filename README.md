# Matrox NMOS Extended Features

This repository describes the extended features of the NMOS Advanced Streaming Architecture developped by Matrox.

# Purpose and Key Features

## Purpose

The NMOS Advanced Streaming Architecture extends and defines IP-based media streaming for the professional AV (proAV) market. Designed to address the growing demand for flexible, secure, and scalable streaming workflows, these specifications extend the NMOS framework with advanced features that enhance configurability, interoperability, security, and resource management in both small-scale and large-scale systems.

### Key objectives include:

1. **Unprecedented Configurability**:
   - Leverage the power of IS-11 to configure independent audio, video, data, and multiplexed (mux) streams, including fine-grained per-audio, per-video, and per-data sub-stream configuration within multiplexed streams. This enables precise control over individual media essences, perfectly tailored to suit complex workflows.
   - Leverage stream and sub-stream capabilities on both the sender and receiver sides to dynamically adapt stream parameters such as resolution, bitrate, and format in real time. This ensures seamless compatibility with receiver requirements and infrastructure constraints.

2. **Unified Management**:
   - Establish a unified, adaptable framework for managing independent and multiplexed streams under a single, extensible model, enabling consistent configuration, seamless interoperability, comprehensive configurability, and operational efficiency across diverse protocols, transport layers, media types, and system scales.

3. **Comprehensive Protocol and Media Support**:
   - Provide extensive compatibility with industry-standard transport protocols, including RTP, SRT, NDI, RTSP, MPEG2-TS over UDP, USB, and IPMX.
   - Provide support for a wide range of media formats, including compressed (JPEG-XS, H.264, H.265, AAC), uncompressed (raw video, PCM audio), and multiplexed (MPEG2-TS, NDI, RTSP, AES3, AM824) streams.

4. **Enhanced Security**:
   - Integrate robust security protocols to protect content and workflows across all supported transports, including the integration of the IPMX Privacy Encryption Protocol (PEP) extended to secure non-IPMX flows.
   - Strengthen access control with OAuth2.0-based authorizations, ensuring secure authentication and granular permission management for devices and workflows.
   - Safeguard system resources with the Node Reservation protocol, mitigating conflicts and optimizing resource allocation in complex deployments.
   - Enable comprehensive content protection with advanced HDCP support, covering both baseband HDMI and HDCP-over-IP workflows via the IPMX HDCP Key Exchange Protocol (HKEP), ensuring compatibility with protected media workflows.

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

The `nmos-testing` branch [MatroxOnly](https://github.com/alabou/nmos-testing/tree/MatroxOnly) provides the Matrox-Transports, Matrox-Capabilities, Matrox-Privacy, Matrox-AAC, Matrox-H264, Matrox-H265, Matrox-USB test suites for testing the extended transports, capabilities, privacy encryption and AAC audio, H.264 video, H.265 video formats.

The `nmos-parameter-registers` branch [MatroxOnly](https://github.com/alabou/nmos-parameter-registers/tree/MatroxOnly) provides the parameter registers for the NMOS Advanced Streaming Architecture.
