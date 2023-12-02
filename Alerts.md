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

Mv   Multi-vendors class prefix.

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
#### refreshPeriod
#### clearPeriod
#### alertCapabilities
#### alertDescriptors
#### alert

### Methods
#### GetActivealerts()
#### GetEventCounters()
#### ClearActiveAlert()

### Notifications
