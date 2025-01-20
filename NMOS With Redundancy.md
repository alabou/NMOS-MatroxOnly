# Matrox: NMOS With Redundancy
{:.no_toc}  
Copyright 2024, Matrox Graphics Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
  
---
  
{:toc}

## Introduction

This document presents various aspects associated with using redundancy / routing with NMOS and Matrox products. It covers the cases of UDP red/blue network redundancy and Multipath TCP  (MPTCP) network redundancy. It also covers the case of using multiple network interfaces to perform routing.

## Use of Normative Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119][RFC-2119].

## Definitions

The NMOS terms 'Controller', 'Node', 'Source', 'Flow', 'Sender', 'Receiver' are used as defined in the [NMOS Glossary](https://specs.amwa.tv/nmos/main/docs/Glossary.html).

## Redundancy

The IS-04 `interface_bindings` and IS-05 `transport_params` attributes define arrays of interface name and transport parameters set respectively. The size of those arrays MUST match the number of redundant paths (legs). The use of redundancy for given Senders and Receivers MUST be configured through a vendor specific mechanism. Under this assumption it MUST NOT be possible through NMOS to add or remove redundant legs and change the size of the `interface_bindings` and `transport_params` arrays.  With redundancy those arrays MUST have more than one entry and usually have two entries.

It MUST NOT be possible to activate or deactivate specific redundant legs of a Sender through the IS-05 transport parameters. A Sender SHOULD use transport parameter constraints to indicate those restrictions.

It MAY be possible to activate or deactivate some of the redundant legs of a Receiver through the IS-05 transport parameters or an SDP transport file. The inactive legs MUST NOT be removed from the `interface_bindings` and `transport_params` arrays. A Receiver SHOULD use transport parameter constraints to indicate any restrictions.

A Sender MAY silently ignore an attempt by a Controller to disable a leg through the IS-05 transport parameters. In that scenario a Sender MAY silently ignore an attempt by a Controller to set a transport parameter to a value that violate the associated parameter constraints.

A Receiver MAY silently ignore an attempt by a Controller to disable a leg through the IS-05 transport parameters. In that scenario a Receiver MAY silently ignore an attempt by a Controller to set a transport parameter to a value that violate the associated parameter constraints.

A Receiver that is not configured for using redundancy MAY connect to a Sender that is configured for using redundancy and connect or subscribe to media from either path (leg). The method used by such Receiver for selecting the stream of a redundant pair that is accessible to the Receiver is unspecified.

A Receiver that is configured for using redundancy MAY connect to a Sender that is not configured for using redundancy, and connect or subscribe to media using either path (leg) and disable the other unused paths (legs). A device MAY disallow disabling redundancy paths (legs) and in this case the Receiver SHOULD NOT be allowed to connect to a Sender not configured for using redundancy.

A Receiver that is configured for using redundancy MAY connect to a Sender that is not configured for using redundancy, and connect or subscribe to media using multiple paths provided by a mean out of the control of the Sender. In that case the information about the redundant paths, if any, MAY be provided by a Controller through the IS-05 transport parameters or an SDP transport file.

This redundancy "logic" applies to all transports, push or pull protocols, connection oriented or not. Temporal redundancy is not allowed to add entries to the `interface_bindings` and `transport_params` arrays. For example FEC have its own transport mechanism.

## Routing

IS-05 transport parameters MAY allow the selection of a specific network interface for a path (leg) by selecting an IP address. The interface names in the `interface_bindings` array MUST be updated to match the IS-05 interface selections. This operation is allowed with and without redundancy. Without redundancy the `interface_bindings` and `transport_params` arrays MUST have a single entry.

In routing scenarios, it is possible to associate a Sender with a specific network interface through the IS-05 transport parameters. This operation allows a Sender to be routed a specific network interface. For connection oriented protocols this approach does not allow the Sender to listen to more than one interface. With redundancy, connection oriented protocol can listen to multiple interfaces. An example of this approach is MPTCP.


[RFC-2119]: https://tools.ietf.org/html/rfc2119 "Key words for use in RFCs"
[IS-04]: https://specs.amwa.tv/is-04/ "AMWA IS-04 NMOS Discovery and Registration Specification"
[IS-05]: https://specs.amwa.tv/is-05/ "AMWA IS-05 NMOS Device Connection Management Specification"
[NMOS Parameter Registers]: https://specs.amwa.tv/nmos-parameter-registers/ "Common parameter values for AMWA NMOS Specifications"
