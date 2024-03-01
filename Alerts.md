# Matrox: Alerts
{:.no_toc}  
Copyright 2023, Matrox Graphics Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
  
---
  
{:toc}

## Introduction

This document describes MvAlertManager IS-12 / MS-05-02 object and the IS-12 and RestAPI methods for accessing it.

The MvAlertManager is a fully IS-12 / MS-05-02 compliant object that can be used to configure alerts from various Interfaces, Senders and Receivers events. The object can be accessed as any IS-12 / MS-05-02 object through a WebSocket interface exposed as the IS-12 standard control endpoint of type "urn:x-nmos:control:ncp/v1.0". The MVAlertManager obejct can also be accessed as a simpler RestAPI at the same endpoint using the POST verb instead of the usual GET upgrading the connection from HTTP(S) to WebSocket. The HTTP(s) RestAPI allows an easier access to the MvAlertManager while still allowing asynchronous alerts to propagate to the RestAPI client through chunked responses.

The alerts provide statistics, states and events about the network interfaces and the streaming engines of Senders and Receivers. By default the MVAlertManager provide a comprehensible set of pre-configured alerts allowing a client to quickly get monitoring alerts without requiring anything but a subscription to the MvAlertManager. More advanced use of the MvAlertManager allow a client to configure its own alerts or reconfigure the existing ones within the capabilities expressed by the MvAlertManager.

The MvAlertManager allows configuring alert for specific Senders and Receiver by providing the associated IS-04 UUID of the resource to monitor. It is also possible to configure alerts for specific network interfaces by providing the associated IS-04 interface name.

This document describes the implementation and the use of compliant MvAlertManager objects.

## Use of Normative Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY",
and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119][RFC-2119].

## Definitions

Mv   Matrox Video class prefix or Multi-vendors class prefix.

## Alert Domains
The alerts are categorized into a limited number of domains. The `link`, `transport`, `essence`, `application` and `clock` domains represent the domains of standard, multi-vendors events. Those domains are also available on a per-vendor basis to provide additional vendor specific events. Finally there is a `vendor` domain for vendor specific events that do not categorized into the 5 base `link`, `transport`, `essence`, `application` and `clock` domains.

The `link`, `transport`, `essence`, `application` and `clock` domains MUST be supported by all implementations of the MvAlertManager. The `vendor`, `vendorLink`, `vendorTransport`, `vendorEssence`, `vendorApplication` and `vendorClock` domains are optional.

Each alert domain has an associated per-domain event identifier and events counter, counting all the events of a given domain. An alert is triggered when a domain events counter of an alert descriptor changes value. Each event within a domain has an associated event identifier and events counter, counting all the identified events within the domain. The events counters of the identified events within a given domain are collectively described as the detailed events counters of the domain.

The domains are defined according to the OSI model when possible. A failure at a lower level MAY cause failures at higher levels. A User SHOULD look at events from lower levels first before considering events at higher level. In some scenarios, failure at a lower level will not prevent a higher level from functioning normally. For example when using redundancy, a `transport` domain packet lost event on one network interface will not prevent a Receiver from consuming a stream if the packet is recovered on the alternate network interface. In this example the higher level `essence` domain would not register invalid stream events.

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
The alert scope indicates how the events associated with an alert are monitored. The scope MAY be `device`, `sender`, `senderAudio`, `senderVideo`, `senderData`, `senderMux`, `receiver`, `receiverAudio`, `receiverVideo`, `receiverData`, `receiverMux`, `input` or `output`.
The `device` scope MUST be supported by all implementations of the MvAlertManager. The `sender`, `senderAudio`, `senderVideo`, `senderData`, `senderMux`, `receiver`, `receiverAudio`, `receiverVideo`, `receiverData`, `receiverMux`, `input` or `output` scopes are optional.

### device
- The alert applies to events at the Device scope. The events monitored are those of all the Senders, Receivers, Inputs and Outputs associated with the Device.
### sender
- The alert applies to events at the Sender scope.  The events monitored are those of all the Senders associated with the Device.
### senderAudio, senderVideo, senderData, senderMux
- The alert applies to events at the format-specific Sender scope. The events monitored are those of all the Senders of a given `format` associated with the Device.
### receiver
- The alert applies to events at the Receiver scope. The events monitored are those of all the Receivers associated with the Device.
### receiverAudio, receiverVideo, receiverData, receiverMux
- The alert applies to events at the format-specific Receiver scope. The events monitored are those of all the Receivers of a given `format` associated with the Device.
### input
- The alert applies to events at the Input scope. The events monitored are those of all the Inputs associated with the Device.
### output
- The alert applies to events at the Output scope. The events monitored are those of all the Outputs associated with the Device.

It is possible to reduce the scope of an alert by specifying a list of resource id to restrict to those resources within the scope of matching id. For scopes other than `device` the resource id MUST correspond to a resources of the scope resource type. There is no list of resource id for the `device` scope as by definition the MvAlertManager operate at the device level.

It is possible to reduce the scope of an alert by specifying a list of interface name to restrict to those resources within the scope of matching interface name. This does not apply to the `input` and `output` scopes as there is no associated network interfaces.

For a `vendor` domain alert, it is possible to reduce the scope of the alert by specifying a list of events in the `vendor` domain to restrict to those matching events within the scope.

## State
An events counter is associated with a state of the sub-system(s) producing the identified event, indicating the severity of the event on the sub-system(s) or the actual state of the sub-system(s). A domain events counter registers the state of the event that triggered an alert. A detailed events counter registers the state of the last event cumulated in the events counter or the last state change of the sub-system(s). The state associated with a detailed events counter is more useful when a single entity is associated with the alert descriptor, for example when a single interface name is specified in `interfaceNames` or a single resource id is specified in `resourceIds`. When multiple resources or interfaces are cumulated in a detailed events counter, the state canont be associated to a specific resource and represent a random sampling the resources/interfaces.

It is important to note that only events can trigger an alert such that the state associated with a domain events counter always correspond to an event severity state. It is only when getting the events counters using the `GetEventCounters()` that the state represents either an event severity or an actual state of the sub-system(s).

### unknown
This state can represent situations where the system's state cannot be determined or is in an indeterminate state. It's a useful state to account for scenarios where the system's condition is unclear.
### inactive
This state signifies that the system is currently not actively engaged in its primary functions or operations. It represents a deliberate state of non-use or idleness, distinct from normal operation. The system is intentionally not performing its usual tasks during this state.
### waiting
In this state, the system awaits a specific condition before actively engaging or continuing its primary functions or operations. It signifies a state of non-use or idleness, distinct from normal operation, triggered by the absence of a necessary condition. During this phase, the system deviates from its regular tasks as it awaits the fulfillment of the necessary condition.
### normal
This state represents the ideal, expected operational state where everything is functioning correctly, and there are no errors or issues.
### warning
This state indicates that the system is not in a critical error state but has encountered issues or conditions that require attention or monitoring. It serves as an early warning before more severe errors occur.
### error
This state represents a more severe issue or error that needs immediate attention. It signifies a significant problem that may impact the system's functionality.
### malfunction
This state suggests that the system is experiencing a critical failure or is not functioning as intended. It typically implies that the system's core functionality is compromised.

## Info
An events counter is associated with textual information from the sub-system producing the identified event. A domain events counter registers the textual information of the event that triggered an alert. A detailed events counter registers the textual information of the last event cumulated in the events counter.

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
	- It means “do not limit the rate”
	- It does not provide a perfect per-event notification scheme because events may arise faster than the alert can be generated by the device.

#### refreshPeriod
Defines the rate at which the device re-issue active alerts notifications (i.e. every N seconds).
- Integer [0, N] (runtime NcPropertyConstraintsNumber)
- Units of seconds
- 0 is the DEFAULT value
	- It means “do not re-issue” 

#### clearPeriod
Defines the period after which the device automatically clear active alerts (i.e. after N seconds). The method ClearAlert() is available to explicitly clear an alert.
- Integer [0, N] (runtime NcPropertyConstraintsNumber)
- Units of seconds
- 0 is the DEFAULT value
	- It means “clear immediately”
- A value larger than 86400 (1 day) means do not auto-clear

#### alertCapabilities (readonly)
```
interface MvAlertCapabilityDescriptor {
	attribute MvAlertDomain alertDomain;
	attribute sequence<MvAlertScope> alertScope;
	attribute sequence<NcUuid> resourceIds;
	attribute sequence<NcString> interfaceNames;
	attribute sequence<MvEvent> events;
};
```

This attribute provides the alerts and events reporting capabilities of the device. Each capability descriptor of the sequence provides information about how a compliant alert decriptor for a given domain can be created and added to the alertDescriptors sequence.

- An empty `alertScope`, `resourceIds`, `interfaceNames` or `events` sequence indicates that the associated MvAlertDescriptor attribute may be given any value.
- A sequence of values for those attributes indicates all the possible values that the associated MvAlertDescriptor attribute may be given. All or a subset of the value can be used.

#### alertDescriptors
```
interface MvAlertDescriptor {
	attribute NcBoolean enabled;
	attribute MvAlertDomain alertDomain;
	attribute MVAlertScope alertScope;
	attribute sequence<NcUuid> resourceIds;
	attribute sequence<NcString> interfaceNames;
	attribute sequence<MvEvent> events;
};
```

This attribute provides the sequence of active alert descriptors.

- A non-empty `resourceIds`, `interfaceNames` sequence MAY be used to narrow the scope of the alert which by default applies to all the events of a given domain within the specified scope.

	- A non-empty sequence of `resourceIds` MAY be used to narrow the scope to those resources of matching resource id within the scope.
 	- A non-empty sequence of `interfaceNames` MAY be used to narrow the scope to those events of matching interface name within the scope.

- A non-empty `events` sequence MAY be used to provide detailed event counters with an alert in addition to the default domain event counter. By default only the domain event counter is provided with an alert, even when calling GetEventCounters().
	- The `events` sequence attributes does not influence when an alert is triggered with the exception of the `vendor` domain where the alert descriptor domain counter only counts the events that are part of the `events` sequence.

#### alert (readonly)
```
interface MvAlertEventData {
	attribute NcUint16 alertDescriptorIndex;
	attribute MvAlertDescriptor alertDescriptor;
	attribute MvEventCounter eventCounter;
};
```
This attributes is used to propagate alert notifications. IS-12 / MS-05-02 support getting notifications about property changed events from objects. When the MvAlertManager generates an alert, the `alert` property is set to the MvAlertEventData object describing the alert descriptor that triggered the notification. An application subscribing to the MvAlertManager notifications can observe alert notifications coming from the `alert` property. The applicaiton SHOULD not read the value of the `alert` attribute as it continously change every time an alert is triggered. Instead is SHOULD get the active alerts using the GetActiveAlerts() method or get the detailed counter associated with an alert descriptor using the GetEventCounters() method.

The `eventCounter` attribute provided with the MvAlertEventData object corresponds to the domain event counter. The GetEventCounters() method MUST be used to retrieve detailed event counters.

### Methods
#### GetActiveAlerts()
```
interface MvActiveAlert {
	attribute NcUint16 alertDescriptorIndex;
	attribute MvAlertDescriptor alertDescriptor;
	attribute sequence<MvEventCounter> eventCounters
};

MvMethodResultActiveAlerts is a sequence of MvActiveAlert
```

This method return a sequence of active alerts. Note that an alert notification returns the domain counter in the `eventCounter` attribute while this method additionally returns in the `eventCounters` attribute all the detailed event counters. The `alertDescriptorIndex` value MAY be used to clear the alert using the `ClearActiveAlert()` method.

#### GetEventCounters(NcUint16 alertDescriptorIndex)
```
interface MvEventCounter {
	attribute MVEvent event;
	attribute NcUint64 eventCounter;
	attribute MvEventState eventState;
	attribute NcString eventInfo;
	attribute NcString interfaceName;
};

MvMethodResultEventCounters is a sequence of MvEventCounter
```
This method returns the sequence of detailed counters associated with the alert descriptor identified by `alertDescriptorIndex`.

#### ClearActiveAlert(NcUint16 alertDescriptorIndex)
This method clear the alert associated with the alert descriptor identifies by `alertDescriptorIndex`.

### Notifications
Notifications about alerts are obtained by subscribing to the MvAlertManager object and monitoring events on the `alert` property.

### Events
The event identifiers of the MvEvent enumeration MAY be discovered by an application using IS-11 / MS-05-02 NcDataClassManager `datatypes` attribute. An implementation of MvAlertManager MUST support the base domain events `link`, `transport`, `essence`, `application` and `clock`. The vendor specific domains are optional.

The base domain events are defined for the domain event counter (having an id corresponding to a multiple of 1000). Look at the https://github.com/alabou/NMOS-MatroxOnly/blob/main/Alerts.md#alert-domains section for more detail about the domains.

#### link (1000)
#### linkDown (1001)
This is the SRF link down event.

This event indicates that the associated network interface transitionned from the UP to the DOWN state. A network interface that is denied access to the network MUST not report a `linkDown` event because the interface is still UP and "partially" working. If the network interface becomes DOWN because the associated sub-system detected either a disconnect from the network connector, a signal integrity issue or a protocol issue, the severity state MUST be `inactive`. The interface became DOWN because of an external issue. If the network interface becomes DOWN because the associated sub-system detected an internal error the severity state MUST be `malfunction`. The interface became DOWN because of an internal issue. Textual information MAY be provided along withthe event to describe the circumstances of the network interface transitionning to the DOWN state.

#### transport (2000)
#### transportPacketLost (2001)
This is the SRF packet lost event.

#### transportPacketLate (2002)
This is the SRF packet late event.

#### transportStreamInvalid (2003)
This is the SRF stream invalid event when detected at the transport level.

#### essence (3000)
#### essenceStreamInvalid (3001)
This is the SRF stream invalid event when detected at the essence level.

#### application (4000)
#### clock (5000)
#### clockPtpLeaderChange (5001)
This is the SRF PTP leader change event.

#### clockPtpUnlock (5002)
This is the SRF PTP unlock event.

#### vendor (10000)
#### vendorTemperature (10001)

#### vendorLink (11000)

#### vendorTransport (12000)
#### vendorTransportError (12001)

#### vendorEssence (13000)
#### vendorEssenceStart (13001)
#### vendorEssenceStop (13002)
#### vendorEssenceError (13002)

#### vendorApplication (14000)
#### vendorClock (15000)
