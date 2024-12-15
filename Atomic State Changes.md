# Matrox: Atomic State Changes
{:.no_toc}  
Copyright 2023, Matrox Graphics Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
  
---
  
{:toc}

## Introduction

The NMOS IS-04 registration process is not atomic. A Node provides updates to the Registry by sending independent updates in the following order: Node, then Devices, then Sources, then Flows, then Senders, and finally Receivers. Each type of resource is updated independently in the Registry. Therefore, an atomic update to multiple resources within a Node will not appear atomically in the Registry.
 
The NMOS IS-04 query process is also not atomic. A Registry provides updates to Controllers for each resource type independently and asynchronously. As a result, an atomic update to multiple resources within a Node will not be visible atomically to a Controller.
 
As the Node's resources are not updated atomically within the Registry through the Registration interface and are not presented atomically to a Controller through the Query interface, Controllers may observe an incomplete or inconsistent view of a Node's state. This document proposes a method for ensuring consistent state updates by using immutable Source and Flow resources and focusing atomic updates on mutable Sender and Receiver resources. This approach preserves compatibility with IS-04 while enhancing reliability and predictability in dynamic update scenarios.

> Note: Note: This issue is also observed when a Controller queries the Node interface directly, instead of using the Registry.

## Use of Normative Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY",
and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119][RFC-2119].

## Definitions

**Immutable resource:** A resource where a resource ID is associated with a fixed and immutable set of attributes. Neither the values of these attributes nor the set of attributes itself can change after the resource is created. 

**Mutable resource:**  A resource where a resource ID is associated with a mutable set of attributes. Both the values of these attributes and the set of attributes itself can change after the resource is created.

## Immutable Sources and Flows

To address the atomicity issue of the IS-04 Registration, Query and Node interfaces, a Node supporting atomic state changes use immutable Source and Flow resources to ensure atomic updates to a mutable Sender resource.

IS-04 Source and Flow resources MUST be immutable and once created MUST become read-only resources until deleted by the Node and garbage collected by the Registry. The ID of such immutable resources MUST be unique among all the Node resources and not be reused by the Node before previous resources are deleted and garbage collected by the Registry. A Controller MUST access/process Sources and Flows in the context of a given Sender, following the `flow_id` attribute of the Sender, the `source_id` and `parents` attributes of the Flows, the `receiver_id` and `parents` attributes of the Sources.

## Mutable Senders and Receivers

IS-04 Sender and Receiver resources MUST be mutable. The ID of such mutable resources MUST be unique among all the Node resources and remain the same for the lifetime of the associated resource. A Controller SHOULD assume that Senders and Receivers id are persistent. A Controller MUST use Senders and Receivers as anchors to discover the state of a Node. As only Senders and Receivers resources are mutable, a Node performs an atomic update of a Sender's `flow_id` to atomically update the associated Flows and Sources.
 
This approach ensures that a Controller has an accurate view of a Node's Sources, Flows, and Senders state and configuration

## Resource Management in the Registry

To avoid excessive resource growth in the Registry due to immutable Sources and Flows Nodes MUST implement garbage collection for unused resources by deleting obsolete Sources and Flows from the Registry once they are no longer directly or indirectly referenced by any Sender or Receiver.

## Example with JPEG-XS BCP-006-01 (informative)

[BCP-006-01][] describes the requirements for having a `bit_rate` attribute on a Flow of `media_type` equal to `video_jxsv` and for having a `bit_rate` attribute on a Sender referencing such Flow through its `flow_id` attribute. Assuming that a User through some configuration API changes the `bit_rate` attribute of a JPEG-XS coded Flow to a larger value. An implementation using mutable Sources, Flows and Senders would simultaneously update the `bit_rate` attribute of both the Flow and the associated Sender.

The [IS-04][] [registration rules](https://specs.amwa.tv/is-04/releases/v1.3.3/docs/Behaviour_-_Registration.html#referential-integrity) state that a Node should update the Registry first with the Flow and then with the Sender. At the Registry level, after the mutable Flow is updated, the combined state of the updated Flow and old Sender is invalid as the Sender's bitrate cannot be lower than the Flow's bit rate. This inconsistency may cause a Controller to raise false alarms or interpret the state incorrectly.

A Node using immutable Sources and Flows and mutable Senders would simultaneously create a new Flow for the updated `bit_rate` attribute, update the Sender's `bit_rate` attribute and `flow_id` attribute to reference the new Flow. At the Registry level, after the new immutable Flow is added to the Registry, the combined state of the old Flow and old Sender remains the same. Then after the mutable Sender is updated in the Registry, the combined state of the new Flow and old Sender describe larger value of both `bit_rate` attributes and the combined state remains valid. Ultimately the Node delete the old Flow which is garbage collected from the Registry and no longer used/referenced by any resource.

This is a very simple example where a Controller may observe a transient invalid state of a Node. There are numerous others.

## Compliance with IS-04 

The [IS-04][] section [Identifier Persistence & Generation](https://specs.amwa.tv/is-04/releases/v1.3.3/docs/Data_Model_-_Identifier_Mapping.html#identifier-persistence--generation) only has an absolute requirement (`MUST`) for the Node ID. This requirement is "For physical Nodes, the Node ID MUST be universally unique to that Node, and remain the same for all time (much in the same way as a serial number).".

For Device, Source, Flow, Sender and Receiver resources the `SHOULD` and `SHOULD NOT` compliance words are used. A requirement for a Flow is "SHOULD NOT change if: a) Configuration parameters associated with the Flow are changed, such as its operating resolution or bitrate, b) Labels, descriptions or other metadata associated with the Flow resource are modified"

Using immutable Flows does not comply with this requirement, but a Controller MUST NOT assume that the Flow ID will never change, as the normative word used is `SHOULD NOT`. This specification estimates that the atomicity issues of the IS-05 Registration, Query and Node interfaces justify using a different behavior in favor of immutable Flows.

The requirement of this specification for using immutable Sources and Flows update the associated [Identifier Persistence & Generation](https://specs.amwa.tv/is-04/releases/v1.3.3/docs/Data_Model_-_Identifier_Mapping.html#identifier-persistence--generation) rules as follow:

### Source ID
Owned by:
  Device ID

MUST change if:
  - Device ID changes
  - A different physical interface (such as an SDI input) is used to retrieve essence
  - Format URN changes between video, audio, data and mux variants
  - Configuration parameters associated with the Source are changed, such as its operating resolution or bitrate
  - Labels, descriptions or other metadata associated with the Source resource are modified
  - Anything of an immutable Source changes

### Flow ID
Owned by:
  Source ID

MUST Change if:
  - Source ID changes
  - Format URN changes between video, audio, data and mux variants (including between two codec types)
  - Configuration parameters associated with the Flow are changed, such as its operating resolution or bitrate
  - Labels, descriptions or other metadata associated with the Flow resource are modified
  - Anything of an immutable Flow changes

According to the [Data Model: Identifier Mapping](https://specs.amwa.tv/is-04/releases/v1.3.2/docs/Data_Model_-_Identifier_Mapping.html) section, a Flow ID **SHOULD** change if:

- The Source ID changes.  
- The Format URN changes between video, audio, data, and mux variants (including between two codec types).  

This indicates that Controllers MUST be prepared for Flow IDs to change under these circumstances, acknowledging that Flows are not entirely static. Therefore, Controllers should not assume permanent Flows and must handle scenarios where new Flow IDs are generated due to changes in codec types.

Controllers prepared for such scenarios would already be compliant with the approach of using immutable Flows and very likely to also handle properly immutable Sources.

## Compliance with MS-04

The approach described in this document is compliant with [MS-04][] [Basic Media Operations](https://specs.amwa.tv/ms-04/releases/v1.0.0/docs/3.1._Basic_Media_Operations.html) section.

For example, assume a device captures an SDI input video signal and transmits an associated uncompressed video stream over RTP. The NMOS resource model would have a Source (representing the SDI-captured signal), a Flow associated with that Source, and a Sender associated with that Flow. The Source has an ID value of 's0', the Flow an ID value of 'f0', and the Sender an ID value of 'snd0'. The SDI video signal is 1080p60, which is represented at the Source with a `grain_rate` of 60 Hz, and at the Flow with a frame width and height of 1920 and 1080, and a `grain_rate` of 60 Hz.

Now assume that the device also has a Flow 'f1' scaling up the incoming video signal to 2160p60. According to [MS-04][], the Flow with ID 'f1' would be associated with the same Source with ID 's0'. The Sender 'snd0' could be associated with either Flow to stream a 1080p60 version of the Source or a 2160p60 version of it. A Controller MUST track the `flow_id` used by Sender 'snd0' to determine whether the stream produced by Sender 'snd0' is 1080p60 or 2160p60.

[MS-04][] does not specify whether Flow 'f1' is created at the same time as Flow 'f0', or at some later time. It is safe to assume that Flow 'f1' can be created after Flow 'f0', such as when a User configures the device to stream a 2160p60 signal over IP. At this point, Flow 'f1' would be created and associated with Sender 'snd0'.

The immutable Flow approach described in this document goes beyond the [MS-04][] transform/process requirement by treating all Flow attributes as immutable, without impacting the required behavior of Controllers. 

The same conclusion applies to Source resources that are created when the content is fundamentally modified. Stopping and starting the capture of a signal fundamentally alter the content as it create time discontinuities and could also result in changing other characteristics of the captured signal. A Controller MUST be ready at any time to have a different Flows and Sources associated with a Sender.



[RFC-2119]: https://tools.ietf.org/html/rfc2119 "Key words for use in RFCs"
[IS-04]: https://specs.amwa.tv/is-04/ "AMWA IS-04 NMOS Discovery and Registration Specification"
[BCP-006-01]: https://specs.amwa.tv/bcp-006-01/releases/v1.0.0/docs/NMOS_With_JPEG_XS.html "NMOS With JPEG XS"
