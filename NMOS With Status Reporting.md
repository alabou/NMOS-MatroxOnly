# Matrox: NMOS With Status Reporting
{:.no_toc}  
Copyright 2024, Matrox Graphics Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
  
---
  
{:toc}

## Introduction

This document may be described as an “IS-04 Binding for BCP-008 Monitoring.”

[BCP-008-01][] and [BCP-008-02][] describe a method for monitoring Receiver and Sender statuses using IS-12 asynchronous WebSockets.
This document defines an alternative reporting mechanism that uses the existing IS-04 Node API and NMOS Registry to deliver the same monitoring information asynchronously through the IS-04 Query WebSocket interface.

This specification retains the complete semantics of [BCP-008-01][] and [BCP-008-02][] for the link, transmission, connection, essence, stream, and external synchronization statuses and their associated transition counters. Only the transport mechanism differs, reusing the widely deployed IS-04 infrastructure rather than introducing a separate IS-12 layer.

Statuses and transition counters are exposed via IS-04 Sources of type `urn:x-nmos:format:data`, each representing the health of a Sender or Receiver within the same Device.
A Controller or monitoring application can subscribe to WebSocket notifications from the IS-04 Query API for "monitoring" Sources to receive asynchronous updates whenever the monitor state of a Sender or Receiver changes.

This mechanism provides a lightweight and implementation-friendly alternative to IS-12-based status reporting. It preserves the established BCP-008 semantics while leveraging the mature IS-04 discovery and subscription model. As such, it requires no additional transport protocols, reduces implementation cost, and enables uniform monitoring of Senders and Receivers through a single, well-known interface.

The IS-04 reporting mechanism defined in this document is fully compatible with the implementation defined by [BCP-008-01][] and [BCP-008-02][].
An implementation may support both mechanisms concurrently, providing broader interoperability between IS-12 and IS-04 reporting models.

## Use of Normative Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119][RFC-2119].

## Definitions

The NMOS terms 'Controller', 'Node', 'Source', 'Flow', 'Sender', 'Receiver' are used as defined in the [NMOS Glossary](https://specs.amwa.tv/nmos/main/docs/Glossary.html).

## Source

The following JSON object provides an example of a Source resource with the status and transition counters of a sibling Receiver. 

```
{
  "id": "00000000-0500-4003-ab00-4d5458005179",
  "version": "1759597033:934345807",
  "label": "Source Monitor",
  "description": "",
  "tags": {  },
  "caps": {  },
  "receiver_id": null,
  "device_id": "00000000-0100-4000-ab00-4d5458005179",
  "parents": [  ],
  "clock_name": null,
  "format": "urn:x-nmos:format:data",
  "monitor_type": "receiver",
  "monitor_sibling_id": "00000000-0300-4000-ab00-4d5458005179",
  "monitor_auto_reset_counters": true,
  "monitor_status_reporting_delay": 3,
  "monitor_state": {
    "overall_status": 1,
    "overall_message": ""
    "link_status": 1,
    "synchronization_status": 1,
    "connection_status": 1,
    "stream_status": 1,
    "link_counter": 0,
    "synchronization_counter": 0,
    "connection_counter": 0,
    "stream_counter": 0
  }
}
```
A Source MUST have the `format` attribute set to `urn:x-nmos:format:data`.

A Source MUST have a `monitor_type` attribute indicating the resource type of the sibling and MUST be either "sender" or "receiver".

A Source MUST have a `monitor_sibling_id` attribute indicating the resource `id` of the sibling. The `monitor_sibling_id` MUST identify a Sender or Receiver belonging to the same `device_id`. A monitoring Source MUST NOT reference its monitored resource using the `parents` attribute.

A Source MUST provide the `monitor_state` object attribute along with the corresponding `overallStatus`, `linkStatus`, `transmissionStatus`, `connectionStatus`, `essenceStatus`, `streamStatus` and `externalSynchronizationStatus` properties of [BCP-008-01][] and [BCP-008-02][] and their associated transition counters. A Source MAY provide the `overallStatusMessage` property of [BCP-008-01][] and [BCP-008-02][].

> Note: The SynchronizationSourceId is not retained in the IS-04 binding as it can be obtained from the Node's `clocks` attribute.

The Source's `monitor_state` object attributes MUST have all the following attributes: `overall_status`, `link_status`, `transmission_status`, `connection_status`, `essence_status`, `stream_status` and `synchronization_status` for the status and `link_counter`, `transmission_counter`, `connection_counter`, `essence_counter`, `stream_counter` and `synchronization_counter` for the associated transition counters. The Source's `monitor_state` object attributes MAY have an `overall_message` attribute.

> Note: The attributes name of the IS-04 binding are simplified to favor a small JSON footprint while stil being easily associated with the [BCP-008-01][] and [BCP-008-02][] properties.

A Source associated with a Sender, having `monitor_type` set to "sender", MUST have the following attributes in the `monitor_state` object: `overall_status`, `link_status`, `transmission_status`, `essence_status`,  `synchronization_status`,  `link_counter`, `transmission_counter`, `essence_counter` and `synchronization_counter`. It MAY have an `overall_message` attribute.

A Source associated with a Receiver, having `monitor_type` set to "receiver", MUST have the following attributes in the `monitor_state` object: `overall_status`, `link_status`, `connection_status`, `stream_status`,  `synchronization_status`,  `link_counter`, `connection_counter`, `stream_counter` and `synchronization_counter`. It MAY have an `overall_message` attribute.

The value of a `*_status` attribute is a non-negative integer value corresponding to the [BCP-008-01][] and [BCP-008-02][] status definitions: AllUp (1), SomeDown (2), AllDown (3), Inactive (0), NotUsed (0), Healthy (1), PartiallyHealthy (2), Unhealthy (3).

The value of a `*_counter` attribute is a non-negative integer value.

The value of the `overall_message` attribute is a string describing the overall status of a SEnder or Receiver. The length of the string SHOULD be kept to a minimum.

> Note: A higher level standard is likely to impose a maximum length for such string in order to minimize the impact on the Registry at large scales. The per-domain optional messages of [BCP-008-01][] and [BCP-008-02][] are not part of the IS-04 binding to favor the smallest footprint.

The Source’s `monitor_state` attribute MUST reflect the effective state of the underlying Sender or Receiver Monitor as determined by the state-reporting behavior defined in [BCP-008-01][] and [BCP-008-02][]. In particular, implementations MUST apply the default `statusReportingDelay` of 3 seconds, which functions as a low-pass filter on status transitions, and this delay MUST NOT be modified nor permitted to be modified by the associated [BCP-008-01][] and [BCP-008-02][] implementation.

The `version` attribute MUST be updated whenever one or more values in `monitor_state` change, and MUST NOT be updated otherwise.

The `clock_name` attribute MUST be `null`.

The `monitor_auto_reset_counters` attribute indicates whether the implementation automatically resets transition counters at activation of the associated Sender or Receiver.
Its Boolean value MUST correspond to the `autoResetCountersAndMessages` property defined in [BCP-008-01][] and [BCP-008-02][].

> Note: Under the immutable default settings defined by [BCP-008-01][] and [BCP-008-02][] (statusReportingDelay = 3 seconds), devices typically emit no more than one update approximately every three seconds per monitored entity, with occasional immediate updates on deterioration.

> Note: The various messages defined by [BCP-008-01][] and [BCP-008-02][] are out of scope of this specification in order to maintain the most compact representation of the monitoring states.

## Transport

The primary purpose of this specification is to define an IS-04-only transport binding for the monitoring state model defined by [BCP-008-01][] and [BCP-008-02][].

A Node or Device claiming compliance with this specification MUST implement the IS-04 transport described herein. Support for the IS-12 / IS-14 based transports defined in [BCP-008-01][] and [BCP-008-02][] is OPTIONAL. Implementations that provide only the IS-04 transport MUST be considered fully compliant with this specification.

## Controller

A Controller or monitoring tools MUST NOT continuously poll the IS-04 Node API of a Node. A Controller SHOULD use the Registry IS-04 Query API and WebSockets asynchronous notifications to get continuous monitoring information.

[BCP-008-01]: https://specs.amwa.tv/bcp-008-01
[BCP-008-02]: https://specs.amwa.tv/bcp-008-02
[RFC-2119]: https://datatracker.ietf.org/doc/html/rfc2119

