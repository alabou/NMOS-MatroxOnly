# Matrox: NMOS With Status Reporting
{:.no_toc}  
Copyright 2024, Matrox Graphics Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
  
---
  
{:toc}

## Introduction

[BCP-008-01][] and [BCP-008-02][] Describe a method for monitoring Receiver and Sender statuses through IS-12 asynchronous WebSockets. This document defines an alternative monitoring mechanism that uses the well-known IS-04 Node API and NMOS Registry to deliver asynchronous status updates through the IS-04 Query WebSocket interface. This specification retains the semantics of [BCP-008-01][] and [BCP-008-02][] for the link, transmission, connection, essence, stream and external synchronization statuses and their associated transition counters. What differs is the reporting mechanism, which reuses the IS-04 Node API instead of the more complex IS-12 transport.

Statuses and transition counters are exposed via IS-04 Sources of type `urn:x-nmos:format:data`, each representing the health of a Sender or Receiver identified by its monitored_id.

A Controller or monitoring tool can subscribe to WebSockets notifications about updated Sources (all of them or only very specific ones) and get asynchronous notifications when the status information of the target Sender or Receiver changes.

This mechanism provides a lightweight alternative to IS-12-based status reporting, retaining the same status semantics as BCP-008-01 and BCP-008-02 while leveraging the existing IS-04 infrastructure for asynchronous notifications. It requires no additional transport protocols, reduces implementation cost, and allows uniform monitoring of Senders and Receivers via a single, well-known interface.

## Use of Normative Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119][RFC-2119].

## Definitions

The NMOS terms 'Controller', 'Node', 'Source', 'Flow', 'Sender', 'Receiver' are used as defined in the [NMOS Glossary](https://specs.amwa.tv/nmos/main/docs/Glossary.html).

## Source

The following JSON object provides an example of a Source resource with the statuses and transition counters of a parent Receiver. 

```
{
  "id": "00000000-0500-4003-ab00-4d5458005179",
  "version": "1759548376:307433877",
  "label": "Source Monitor",
  "description": "",
  "tags": { },
  "caps": { },
  "device_id": "00000000-0100-4000-ab00-4d5458005179",
  "parents": [    
  ],
  "clock_name": null,
  "format": "urn:x-nmos:format:data",

  "monitored_id": "00000000-0300-4000-ab00-4d5458005179",
  "monitored_type": "receiver",

  "overall_status": 1,
  "link_status": 1,
  "synchronization_status": 1,
  "connection_status": 1,
  "stream_status": 1,
  "link_counter": 0,
  "synchronization_counter": 0,
  "connection_counter": 0,
  "stream_counter": 0
}
```
A Source MUST have the `format` attribute set to `urn:x-nmos:format:data`.

A Source MUST provide the `overallStatus`, `linkStatus`, `transmissionStatus`, `connectionStatus`, `essenceStatus`, `streamStatus` and `externalSynchronizationStatus` of [BCP-008-01][] and [BCP-008-02][] and their associated transition counters.

The Source attributes MUST use the following names: `overall_status`, `link_status`, `transmission_status`, `connection_status`, `essence_status`, `stream_status` and `synchronization_status` for the statuses and `link_counter`, `transmission_counter`, `connection_counter`, `essence_counter`, `stream_counter` and `synchronization_counter` for the associated transition counters.

A Source associated with a Sender MUST have the attributes `overall_status`, `link_status`, `transmission_status`, `essence_status`,  `synchronization_status`,  `link_counter`, `transmission_counter`, `essence_counter` and `synchronization_counter`.

A Source associated with a Receiver MUST have the attributes `overall_status`, `link_status`, `connection_status`, `stream_status`,  `synchronization_status`,  `link_counter`, `connection_counter`, `stream_counter` and `synchronization_counter`.

The value of a `*_status` attribute is a non-negative integer value corresponding to the [BCP-008-01][] and [BCP-008-02][] statuses: AllUp (1), SomeDown (2), AllDown (3), Inactive (0), NotUsed (0), Healthy (1), PartiallyHealthy (2), Unhealthy (3).

The value of a `*_counter` attribute is an non-negative integer value.

The `id` of the monitored Sender or Receiver MUST be specified in the Source's `monitored_id` attribute and the `monitored_type` set to "sender" or "receiver" accordingly.

The `version`  attribute MUST be updated whenever the value of a source's attribute changes.

The `clock_name attribute MUST be `null`.

The state of a monitoring Source SHOULD NOT be updated more than once per second. A Source MUST NOT publish more than one update to the Registry per second. This limit applies per resource (per monitoring Source), not per Node.

## Controller

A Controller or monitoring tools MUST NOT continously poll the IS-04 Node API of a Node. A Controller SHOULD use the Registry IS-04 Query API and WebSockets asynchronous notifications to get continuous monitoring information.

