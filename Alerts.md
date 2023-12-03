# Matrox: Alerts
{:.no_toc}  
Copyright 2023, Matrox Graphics Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
  
---
  
{:toc}

## Introduction

This document describes MvAlertManager IS-12 / MS-05 object and the IS-12 and RestAPI methods for accessing it.

The MvAlertManager is a fully IS-12 / MS-05 compliant object that can be used to configure alerts from various Interfaces, Senders and Receivers events. The object can be accessed as any IS-12 / MS-05 object through a WebSocket interface exposed as the IS-12 standard control endpoint of type "urn:x-nmos:control:ncp/v1.0". The MVAlertManager obejct can also be accessed as a simpler RestAPI at the same endpoint using the POST verb instead of the usual GET upgrading the connection from HTTP(S) to WebSocket. The HTTP(s) RestAPI allows an easier access to the MvAlertManager while still allowing asynchronous alerts to propagate to the RestAPI client through chunked responses.

The alerts provide statistics, states and events about the network interfaces and the streaming engines of Senders and Receivers. By default the MVAlertManager provide a comprehensible set of pre-configured alerts allowing a client to quickly get monitoring alerts without requiring anything but a subscription to the MvAlertManager. More advanced use of the MvAlertManager allow a client to configure its own alerts or reconfigure the existing ones within the capabilities expressed by the MvAlertManager.

The MvAlertManager allows configuring alert for specific Senders and Receiver by providing the associated IS-04 UUID of the resource to monitor. It is also possible to configure alerts for specific network interfaces by providing the associated IS-04 interface name.

This document describes the implementation and the use of compliant MvAlertManager objects.

## Use of Normative Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY",
and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119][RFC-2119].

## Definitions

Mv   Matrox Video class prefix or Multi-vendors class prefix.

## Alert Domains
The alerts are categorized into a limited number of domains. The `link`, `transport`, `essence`, `application` and `clock` domains represent the domains of standards, multi-vendors events. Those domains are also available on a per-vendor basis to provide additional vendor specific events. Finally there is a `vendor` domain for vendor specific events that do not categorized into the 5 base `link`, `transport`, `essence`, `application` and `clock` domains.

The `link`, `transport`, `essence` and `clock` domains MUST be supported by all implementations of the MvAlertManager. The `application`, `vendor`, `vendorLink`, `vendorTransport`, `vendorEssence`, `vendorApplication` and `vendorClock` domains are optional.

Each alert domain has an associated per-domain event counter, counting all the events of a given domain. An alert is triggered when a domain counter of an active alert descriptor changes value.

### link, vendorLink
- ISO level 1 and 2 (physical, data link)
- Ethernet, WiFi, 802.1x 
- Notion of “frame”

### transport, vendorTransport
- ISO level 3 and 4 (network, transport)
- IPv4, IPv6, UDP, TCP, SRT, USB
- IGMP, MLD
- RTP, MPEG2-TS
- Notion of “packet”, raw messages, raw streams

### essence, vendorEssence
- ISO level 5, 6 and 7 (session, presentation, application)
- HTTP, WebSocket, HDCP, TLS, PEP, NMOS
- RTP format, media stream
- Notion of media stream and messages

### application, vendorApplication
- ISO level 7 (application)
- DNS, mDNS, DNS-SD, DHCP, OAuth2, Proxy, Radius, NMOS Registry, etc.

### clock, vendorClock
- PTP, NTP, media clock recovery, reference clock recovery

### vendor
- vendor specific events like temperature, battery charge, etc.

## Alert Scopes
The alert scope indicates if the events associated with an alert have to be monitored at the Device, Sender, Receiver, Input or Output level.
The Device scope MUST be supported by all implementations of the MvAlertManager. The Sender, Receiver, Input and Output scopes are optional.

### device
- The alert applies to events at the Device scope
### sender
- The alert applies to events at the Sender scope
### senderAudio, senderVideo, senderData, senderMux
- The alert applies to events at the format-specific Sender scope
### receiver
- The alert applies to events at the Receiver scope
### receiverAudio, receiverVideo, receiverData, receiverMux
- The alert applies to events at the format-specific Receiver scope
### input
- The alert applies to events at the Input scope
### output
- The alert applies to events at the Output scope

## MvAlertManager class

```
interface MvAlertManager : NcManager {

	attribute NcUint32 alertPeriod;
	attribute NcUint32 refreshPeriod;
	attribute NcUint32 clearPeriod;
	attribute readonly sequence<MvAlertCapabilityDescriptor> alertCapabilities;
	attribute sequence<MvAlertDescriptor> alertDescriptors;

	MvMethodResultActiveAlerts GetActiveAlerts();
	MvMethodResultEventCounters GetEventCounters(NcUint16 alertDescriptorIndex);
	NcMethodResult ClearActiveAlert(NcUint16 alertDescriptorIndex);
	
	attribute readonly MvAlertEventData alert;
};
```


### Attributes
#### alertPeriod
Defines the rate at which the device issues active alerts notifications (i.e. every N seconds).
- Integer [0, N] (runtime NcPropertyConstraintsNumber)
- Units of seconds
- 0 is the DEFAULT value
	- Means “do not limit the rate”
	- Does not provide a perfect per-event notification scheme because events may arise faster than the alert can be generated by the device.

#### refreshPeriod
Defines the rate at which the device re-issue active alerts notifications (i.e. every N seconds).
- Integer [0, N] (runtime NcPropertyConstraintsNumber)
- Units of seconds
- 0 is the DEFAULT value
	Means “do not re-issue” 

#### clearPeriod
Defines the period after which the device automatically clear active alerts (i.e. after N seconds). The method ClearAlert() is available to explicitly clear an alert.
- Integer [0, N] (runtime NcPropertyConstraintsNumber)
- Units of seconds
- 0 is the DEFAULT value
	- Means “clear immediately”
- A value larger than 86400 (1 day) means do not auto-clear

#### alertCapabilities
#### alertDescriptors
#### alert

### Methods
#### GetActivealerts()
#### GetEventCounters()
#### ClearActiveAlert()

### Notifications
