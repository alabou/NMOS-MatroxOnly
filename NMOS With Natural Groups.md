# Matrox: NMOS With Natural Groups
{:.no_toc}  
Copyright 2024, Matrox Graphics Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
  
---
  
{:toc}

## Introduction

[BCP-002-01][] Describes a method for grouping Sender and Receiver resources into natural groups in a very generic way. This specification strengthen the requirements and provides a very precise definition of natural grouping in Matrox products. The objective is to make natural grouping of Senders and Receivers compatible and homogeneous with the concept of sub-Flows/sub-Streams of multiplexed Senders and Receivers. A Controller should be able to process and connect a group of independent Senders/Receivers in the same way it processes a group of multiplexed Flows/Streams.

## Use of Normative Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119][RFC-2119].

## Definitions

The NMOS terms 'Controller', 'Node', 'Source', 'Flow', 'Sender', 'Receiver' are used as defined in the [NMOS Glossary](https://specs.amwa.tv/nmos/main/docs/Glossary.html).

A 'sub-Flow' is defined as a Flow of format `urn:x-nmos:format:audio`, `urn:x-nmos:format:video` or `urn:x-nmos:format:data` which is part of a MPEG2-TS Stream produced by a Sender.

A 'sub-Stream' is defined as a Stream of format `urn:x-nmos:format:audio`, `urn:x-nmos:format:video` or `urn:x-nmos:format:data` which is part of a MPEG2-TS Stream consumed by a Receiver.

## Group Hint
Senders and Receivers MUST declare a "urn:x-nmos:tag:grouphint/v1.0" tag in their `tags` attribute.

The "urn:x-nmos:tag:grouphint/v1.0" tag array MUST comprise a single string formatted as one of the following options:

`"<group-name> <group-index>:<role-in-group> <role-index>"`  
`"<group-name> <group-index>:<role-in-group>"`

The `<group-name>`, `<group-index>`, `<role-in-group>`, `<role-index>` sequences MUST be replaced with the proper value as defined in the following sections. The `<group-name>` MUST be a sequence of the letters [a-zA-Z]. The `<group-index>` MUST be a decimal number where the leftmost digit MUST not be '0' unless the value is zero. The `<group-name>` and `<group-index>` sequences MUST be separated by a single space. The `<role-in-group>` MUST be a sequence of the letters [a-zA-Z]. The `<role-index>` MUST be a decimal number where the leftmost digit MUST not be '0' unless the value is zero. The `<role-in-group>` and `<role-index>` sequences MUST be separated by a single space. The `<group-index>` and `<role-in-group>` MUST be separated by a colon ':'.

The scope is always `device` which is the default value as per [Group Hint](https://specs.amwa.tv/nmos-parameter-registers/branches/main/tags/grouphint.html#group-hint-urn).

## Transport

A `<group-name>` is associated with a transport and describes a grouping over IP. For the base transports `urn:x-nmos:transport:rtp`, `urn:x-nmos:transport:mqtt`, `urn:x-nmos:transport:websocket`, `urn:x-matrox:transport:ndi`, `urn:x-matrox:transport:srt`, `urn:x-matrox:transport:usb`, `urn:x-matrox:transport:udp`, `urn:x-matrox:transport:tcp` and their sub-classes the `<group-name>` is the base transport name. The `<group-name>` SHOULD be using uppercase letters.

For the base transports `urn:x-nmos:transport:rtp`, `urn:x-nmos:transport:mqtt`, `urn:x-nmos:transport:websocket`, `urn:x-matrox:transport:ndi`, `urn:x-matrox:transport:srt`, `urn:x-matrox:transport:usb`, `urn:x-matrox:transport:udp`, `urn:x-matrox:transport:tcp` the `<group-name>` MUST be "RTP", "MQTT", "WS", "NDI","SRT", "USB", "UDP" and "TCP" respectively.

A generic `<group name>` such as "IP", "IPMX", or "ST2110", or any other valid `<group name>`, MAY be used in place of a more specific transport name.

## Format

A `<role-in-group>` is associated with the format of a Sender or Receiver. For the formats `urn:x-nmos:format:video`, `urn:x-nmos:format:audio`, `urn:x-nmos:format:data`, and `urn:x-nmos:format:mux`, the `<role-in-group>` MUST be "VIDEO", "AUDIO", "DATA", and "MUX" respectively. Alternatively, "ANC" MAY be used instead of "DATA" when the data is ancillary data. Any variation in capitalization is permitted, as `<role-in-group>` MUST always be compared using a case-insensitive comparison.

## Layer

The `<role-index>` is associated with the concept of "layer" of sub-Flows/sub-Streams. For independent Senders/Receivers it describes an ordering of the independent Senders/Receivers for a given role/format. The `<role-index>` MUST start at 0 and increment for each successive layer of the same format. The `<role-index>` values MUST be consecutive integer values starting at 0. When `<role-index>` is not present it MUST be assumed as being 0.

## Senders

The `<group-name> <group-index>` value for a Sender "urn:x-nmos:tag:grouphint/v1.0" tag MUST be unique among the various groups of Senders within a Device. The groups of Senders SHOULD be considered independent of the groups of Receivers within a Device. Identical `<group-name> <group-index>` groups for Senders and Receivers have no special meaning and are allowed.

## Receivers

The `<group-name> <group-index>` value for a Receiver "urn:x-nmos:tag:grouphint/v1.0" tag MUST be unique among the various groups of Receivers within a Device. The groups of Receivers SHOULD be considered independent of the groups of Senders within a Device. Identical `<group-name> <group-index>` groups for Senders and Receivers have no special meaning and are allowed.

## Controllers

Controllers SHOULD present to a User a group of Senders/Receivers in a similar way that a group of sub-Flows/sub-Streams would be presented for a multiplexed Sender/Receiver, using the same concepts of format and layer associated with sub-Flow/sub-Streams.

## Group Compatibility

Senders and Receivers MUST declare a "urn:x-matrox:tag:groupcompatibility/v1.0" tag in their `tags` attribute.

The "urn:x-matrox:tag:groupcompatibility/v1.0" tag array MUST comprise entries formatted as the string representation of a decimal positive integer, where the leftmost digit MUST NOT be '0' unless the value is zero.

A Sender MAY be member of multiple groups. A Sender  that does not include the "urn:x-matrox:tag:groupcompatibility/v1.0" tag MUST be assumed to belong to all groups. Senders that are members a common group are considered compatible and MAY be used simultaneously; otherwise they are not compatible and MUST be used exclusively.

A Receiver MAY be member of multiple groups. A Receiver that does not include the "urn:x-matrox:tag:groupcompatibility/v1.0" tag MUST be assumed to belong to all groups. Receivers that are members a common group are considered compatible and MAY be used simultaneously; otherwise they are not compatible and MUST be used exclusively.

> Note: The groupcompatibility tag is intended to express exclusivity or compatibility among Senders or Receivers that reside within a single device and may share internal hardware or processing resources. Certain combinations of Senders or Receivers on the same device may not be usable simultaneously due to bandwidth limitations, hardware pipeline conflicts, or configuration constraints. By declaring group membership, a device can expose these limitations declaratively, allowing an NMOS Controller to enforce compatibility rules without requiring detailed, device-specific knowledge. Devices that omit the tag are assumed to have no such internal restrictions, ensuring compatibility with existing NMOS behaviors.

## Display Walls

While the "urn:x-nmos:tag:grouphint/v1.0" tag allows grouping Senders and Receivers from a given Device, the "urn:x-nmos:tag:wallhint/v1.0" tag allows grouping Receivers across multiple Devices. The wallhint does not apply to Senders. It allows grouping all the Receivers of a given group associated to a given wall, connecting to Senders of the same group to be processed at once.

The "urn:x-nmos:tag:wallhint/v1.0" tag array MUST comprise a single string formatted as follow:

`"WALL <wall-index>"`

The `<wall-index>` sequences MUST be replaced with the proper value as defined in the following sections. The `<wall-index>` MUST be a decimal number where the leftmost digit MUST not be '0' unless the value is zero. The `WALL` and `<wall-index>` sequences MUST be separated by a single space.

The `<wall-index>` MUST correspond to the `<group-index>` of the Receiver summed with a large integer value identifying the wall. Such a large integer value SHOULD be N multiplied by a power of 10 larger than the largest `<group-index>` of all the devices part of an NMOS deployment. N MUST be an integer in the range [1, maxInt] identifying a wall. For example if there are at most 100 groups per Device then a choice for the power of ten could be 100, having walls identified as 100, 200, 300, etc.


[RFC-2119]: https://tools.ietf.org/html/rfc2119 "Key words for use in RFCs"
[IS-04]: https://specs.amwa.tv/is-04/ "AMWA IS-04 NMOS Discovery and Registration Specification"
[IS-05]: https://specs.amwa.tv/is-05/ "AMWA IS-05 NMOS Device Connection Management Specification"
[NMOS Parameter Registers]: https://specs.amwa.tv/nmos-parameter-registers/ "Common parameter values for AMWA NMOS Specifications"
[BCP-002-01]:https://specs.amwa.tv/bcp-002-01 "AMWA BCP-002-01: Natural Grouping of NMOS Resources"
