# Matrox: NMOS With USB
{:.no_toc}  
Copyright 2024, Matrox Graphics Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
  
---
  
{:toc}

## Introduction

The VSF/IPMX [TR-10-14][] technical recommendation defines the transport of USB multiplexed streams over TCP/IP. It allows the transport of multiplexed keyboard, mouse, data, audio and video sub-streams over TCP/IP. Senders and Receivers using the USB transport have their `format` attribute set to `urn:x-nmos:format:data` and their `transport` attribute set to  `urn:x-matrox:transport:usb`. The `media_type` attribute of an USB Receiver is `application/usb`. The `media_type` of a data Flow connected with an USB Sender is `application/usb`.

The content of a USB stream is not exposed at the NMOS level and as such a USB stream is not exposed as a multiplexed stream but as an opaque data stream. A USB Receiver connecting to a USB Sender is granted access to the various USB devices accessible at the Sender. For each device there is a corresponding multiplexed data sub-stream. Such devices may be plugged and unplugged dynamically without impacting the connection of a Receiver to the Sender, without impacting the associated Source, Flow and Sender resources.

Using USB Senders and Receivers may be counter intuitive at first because of the location of such Senders and Receivers in actual devices. For example, let consider a KVM device facing a User, connected to a remote computer through the network. The remote computer provides video and audio signals and as such the audio and video Senders reside on the remote computer side. The KVM device provides keyboard, mouse and storage devices and as such the USB Sender resides on the KVM device side. The USB Receiver resides on the remote computer side. In this example the KVM side would have audio and video Receivers for the displays and speakers connected to the KVM device.

## Use of Normative Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY",
and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119][RFC-2119].

## Definitions

The NMOS terms 'Controller', 'Node', 'Source', 'Flow', 'Sender', 'Receiver' are used as defined in the [NMOS Glossary](https://specs.amwa.tv/nmos/main/docs/Glossary.html).

## USB IS-04 Sources, Flows and Senders

Nodes implementing IS-04 v1.3 or higher, that are capable of transmitting USB data streams, MUST have Source, Flow and Sender resources in the IS-04 Node API.

### Sources

A USB Source resource MUST indicate `urn:x-nmos:format:data` for the `format` attribute and it MUST be associated with a Flow of the same `format` through the `source_id` attribute of the Flow. 

Examples Source resources are provided in [Examples](../examples/).

### Flows

A USB Flow resource MUST indicate `application/usb` in the `media_type` attribute and `urn:x-nmos:format:data` for the `format` attribute. A USB Flow MUST have a `source_id` attribute referencing a Source of the same `format`.

Examples Flow resources are provided in [Examples](../examples/).

### Senders

An USB Sender resource MUST indicate `urn:x-matrox:transport:usb` for the `transport` attribute.

A Sender associated with a USB Flow through the `flow_id` attribute MUST provide Sender's Capabilities for the data Flow.

The Sender MUST express its limitations or preferences regarding the USB streams that it supports indicating constraints in accordance with the [Sender Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/SenderCapabilities.md) Sender Capabilities specification. The Sender SHOULD express its constraints as precisely as possible, to allow a Controller to determine with a high level of confidence the Sender's stream capabilities. It is not always practical for the constraints to indicate every type of stream that a Sender can or cannot produce; however, they SHOULD describe as many of its commonly used operating points as practical and any preferences among them.

The `constraint_sets` parameter within the `caps` object MUST be used to describe combinations of parameters which the sender can support, using the parameter constraints defined in the [Capabilities register](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/) of the NMOS Parameter Registers and [Matrox Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md).

A USB Sender is a TCP/IP server. A USB Sender accept connections from connecting USB Receivers. The underlying protocol used by the `urn:x-nmos:transport:usb` transport is TCP, optionally using the MPTCP (multi-patsh TCP) scheme for redundancy.

An example Sender resource is provided in the [Examples](../examples/).

#### SDP format-specific parameters

The `manifest_href` attribute of the Sender MUST provide the URL to an SDP transport file compliant with the requirements of [TR-10-14][] and the following:

- The media description line `m=<media> <port> <proto> <fmt> ...` MUST have <media> set to `application`, <proto> set to `TCP` and <fmt> set to `usb` to express that the `media_type` is `application/usb` and the TCP protocol is used by the `urn:x-nmos:transport:usb` transport.

- The connection information lines `c=<nettype> <addrtype> <connection-address>` MUST have <connection-address> set to the IP address of the Sender's TCP server.

- The attribute `a=setup:passive` MUST be specifified.

- If redundancy is used at most two paths MUST be specified using two media descriptors. The <connection-address> of each media descriptor specify a different path for reaching the TCP server of the Sender. A `a=group:DUP` session attribute MUST specify the two media paths identified using the `a=mid:` media attribute. The first identifier of the `a=group:DUP` session attribute MUST specify the first leg (path) and the other identifier the second leg. The first leg corresponds to entry 0 of the IS-05 transport parameters array while the second leg corresponds to entry 1.

## USB IS-04 Receivers

Nodes implementing IS-04 v1.3 or higher that are capable of receiving USB data streams MUST have Receiver resources in the IS-04 Node API.

A USB Receiver resource MUST indicate `urn:x-matrox:transport:usb` for the `transport` attribute.

A USB Receiver MUST indicate `urn:x-nmos:format:data` for the `format` attribute and MUST provide Receiver's Capabilities for the data Stream.

The Receiver MUST express its limitations or preferences regarding the USB streams that it supports indicating constraints in accordance with the [Receiver Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/ReceiverCapabilities.md) Receiver Capabilities specification. The Receiver SHOULD express its constraints as precisely as possible, to allow a Controller to determine with a high level of confidence the Receiver's compatibility with the available stream. It is not always practical for the constraints to indicate every type of stream that a Receiver can or cannot consume successfully; however, they SHOULD describe as many of its commonly used operating points as practical and any preferences among them.

The `constraint_sets` parameter within the `caps` object MUST be used to describe combinations of parameters which the receiver can support, using the parameter constraints defined in the [Capabilities register](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/) of the NMOS Parameter Registers and [Matrox Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md).

A USB Receiver is a TCP/IP client. A USB Sender accept connections from connecting USB Receivers. The underlying protocol used by the `urn:x-nmos:transport:usb` transport is TCP, optionally using the MPTCP (multi-patsh TCP) scheme for redundancy.

An example Receiver resource is provided in the [Examples](../examples/).

### Grouping of Receivers
In some scenarios a group of Receivers control the USB sub-system of a Device. 

The grouping scheme described in [NMOS With Natural Groups](https://github.com/alabou/NMOS-MatroxOnly/blob/main/NMOS%20With%20Natural%20Groups.md) MUST be used. All those Receivers MUST be in the same `<group-name> <group-index>` group and each MUST use a different `<role-index>` in the `DATA` role.

With this grouping convention a Controller can identify the number of Senders that can simultaneously control the USB sub-system of a Device. 

## USB IS-05 Senders and Receivers

Connection Management using IS-05 proceeds in exactly the same manner as for any other transport using the USB specific transport parameters defined in [USB Sender transport parameters](https://github.com/alabou/NMOS-MatroxOnly/blob/main/schemas/sender_transport_params_usb.json) and [USB Receiver transport parameters](https://github.com/alabou/NMOS-MatroxOnly/blob/main/schemas/receiver_transport_params_usb.json).

Redundancy MUST be implemented using MPTCP. At most two sets of transport parameters MUST be specified for Senders and Receivers supporting redundancy with the `urn:x-nmos:transport:usb` transport. The trhsport parameters of the first leg are provided as entry 0 of the transport parameters array while those of the second leg are provided as entry 1.

### Receivers

A `PATCH` request on the **/staged** endpoint of an IS-05 Receiver can contain an SDP transport file in the `transport_file` attribute. The SDP transport file for a USB stream is expected to comply with IPMX [TR-10-14][]. It need not comply with the additional requirements specified for SDP transport files at Senders.

If the Receiver is not capable of consuming the stream described by a `PATCH` on the **/staged** endpoint, it SHOULD reject the request. If it is unable to assess the stream compatibility because some parameters are not included `PATCH` request, it MAY accept the request and postpone stream compatibility assessment.

A Controller MAY connect a Receiver not supporting redundancy to either leg of a Sender supporting redundancy. A Controller MUST set the `source_ip` and `source_port` attributes of the second leg of a Receiver supporting redundancy to `null` when connecting to a Sender not supporting redundancy.

### Senders

If the IS-04 Sender `manifest_href` attribute is not `null`, the SDP transport file at the **/transportfile** endpoint MUST comply with the same requirements described for the SDP transport file at the IS-04 Sender `manifest_href`.

A Sender MAY, unless constrained by IS-11, produce any USB stream that is compliant with the associated Flow.

## USB IS-11 Senders and Receivers

### RTP transport

### Other transports

## Controllers

[RFC-2119]: https://tools.ietf.org/html/rfc2119 "Key words for use in RFCs"
[IS-04]: https://specs.amwa.tv/is-04/ "AMWA IS-04 NMOS Discovery and Registration Specification"
[IS-05]: https://specs.amwa.tv/is-05/ "AMWA IS-05 NMOS Device Connection Management Specification"
[NMOS Parameter Registers]: https://specs.amwa.tv/nmos-parameter-registers/ "Common parameter values for AMWA NMOS Specifications"
[VSF]: https://vsf.tv/ "Video Services Forum"
[SMPTE]: https://www.smpte.org/ "Society of Media Professionals, Technologists and Engineers"
[BCP-004-01]: https://specs.amwa.tv/bcp-004-01/ "AMWA BCP-004-01 NMOS Receiver Capabilities"
[TR-10-8]: https://vsf.tv/download/technical_recommendations/VSF_TR-10-8_2023-04-14.pdf "NMOS Requirements"
[TR-10-14]: https://vsf.tv/download/technical_recommendations/VSF_TR-10-14_2024-09-24.pdf "IPMX	USB"
