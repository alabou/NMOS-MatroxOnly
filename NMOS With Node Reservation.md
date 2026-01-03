# Matrox: NMOS With Node Reservation
{:.no_toc}  
Copyright 2024, Matrox Graphics Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
  
---
  
{:toc}

## Introduction

It is sometime required to reserve the use of a group of NMOS Nodes for a single Controller or entity. This document presents a vendor specific API that is used for reserving the use of a group of NMOS Nodes.

The owner of the Nodes is the only one with the ability change the state of the Node through the NMOS RestAPIs POST, PUT, DELETE and PATCH verbs. Anyone can use the read-only verbs and get information from the Nodes. The owner of the Nodes provides a 128 bit key that is used to seclude the Nodes in a private group when privacy encryption is used. The owner of the Nodes is responsible for keeping its session alive.

> Note: The POST verb on some RestAPI path MAY be allowed for anyone if such request does not change the state of the Node.

## Use of Normative Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119][RFC-2119].

## Definitions

The NMOS terms 'Controller', 'Node', 'Source', 'Flow', 'Sender', 'Receiver' are used as defined in the [NMOS Glossary](https://specs.amwa.tv/nmos/main/docs/Glossary.html).

The 'Session Lifetime' determines the amount of time, after being acquired or renewed, that a session and its token remain valid. A session can be renewed after half of its lifetime. A session expires after its lifetime if not renewed or after its alivetime if unused and an NMOS RestAPI PUT, POST, PATCH or DELETE request changing the state of the Node is performed without a bearer token. By default the lifetime of a session is 60 minutes.

The 'Session AliveTime' determines the amount of time, after being used, that a session and its token remain alive. A session is used when an NMOS RestAPI is accessed using the `Authorization` header and that the bearer token proves to be the owner of the session. A session that is not alive becomes expired if an NMOS RestAPI PUT, POST, PATCH or DELETE request changing the state of the Node is performed without a bearer token. There is a special keepalive endpoint that MAY be used for keeping a session alive. By default the alivetime of a session is 60 seconds.

> Note: it is possible to change, based on a global enterprise policy, the default alivetime of 60 seconds to 120 seconds. No other values are allowed.

## Using Reservation along with OAuth2.0 authorizations

If accesses to the NMOS APIs are authorized by OAuth2.0, the OAuth2.0 Bearer token MUST be stored in the `Authorization` HTTP header and the exclusive session Bearer token MUST be store in the `PEP-Exclusive-Authorization` HTTP header. Otherwise when OAuth2.0 authorizations are not used, the exclusive session Bearer token MUST be stored in the `Authorization` HTTP header.

In this document, references to the `Authorization` HTTP header MUST be replaced by references to the `PEP-Exclusive-Authorization` HTTP header when OAuth2.0 authorizations are used by a Node to authorize access to the NMOS RestAPIs.

## Session Lifetime versus AliveTime

A session is associated with a lifetime to protect against compromised Bearer tokens. A session is associated with an alivetime to quickly terminate a previous session when no longer used. 

An entity MUST acquire Nodes to exclusively used them and it MUST prove that it is alive and actively using them to keep its ownership. The 'Session Lifetime' of all the devices MAY be changed by an administrator to better fit the objective of a given deployment to a maximum of 24 hours. The 'Session AliveTime' MUST remain 60 seconds. The current values have been chosen to allow a quick turnaround when an entity that reserved Node becomes dead after a malfunction, power down or other reasons.

The owner of an exclusive session regularly Renew its session to obtain a new Bearer token to prevent its session to expire. Between the renewing intervals, the owner of an exclusive session regularly keeps its session alive by calling the KeepAlive endpoint or by using its Bearer token in an access to a Node RestAPI to keep its session alive.

## Reservation RestAPI

This RestAPI MUST use the HTTPS protocol with TLS v1.2 or TLS v1.3. It is not allowed to use the bare HTTP protocol.

The Reservation RestAPI MUST be published as a Node service of type `urn:x-matrox:service:exclusive/v1.0`. The service declaration indicate the URL where the service is accessible and if OAuth2.0 authorizations are required to access the service.

### Acquire

The acquire endpoint MAY be protected by either the use of an HTTPS server certificate, an HTTPS client certificate with mutual authentication or using credentials in some form of username and password. It is up to the vendor to decide of the exact mechanism and possibly return a `WWW-Authenticate` header with the proper authentication information. If OAuth2.0 is not used, the acquire endpoint SHOULD NOT be accessed with an `Authorization` header. Otherwise if OAuth2.0 is used, the acquire endpoint SHOULD NOT be accessed with an `PEP-Exclusive-Authorization` header.

This operation is atomic on a per Node basis. It is not possible to reserve multiple Nodes simultaneously. 

This operation attempts to acquire an exclusive session and obtain an associated bearer token. The session expires in 60 minutes unless it is renewed. A session is "alive" for 60 seconds after being acquired or used. The `exclusive_key` is used on activation of Senders and Receivers as additional keying material to derive the privacy encryption key. The privacy encryption key remains valid even if the session expires until a new owner activate a Sender / Receiver. See [PEP](https://github.com/alabou/NMOS-MatroxOnly/blob/main/NMOS%20With%20Privacy%20Encryption.md) for more details about the Privacy Encryption Protocol.

The operation fail with a status `BadRequest` if the posted JSON is invalid. The operation fail with a status `Locked` if there is an active session. Otherwise a status `Ok` and a bearer token are returned. The token MUST be used to access the NMOS RestAPIs that may change the Node state.

The client receiving a `Locked` status MUST use an exponential back-off mechanism when retrying to obtain an exclusive session. Such a mechanism MUST consider the lifetime of 60 minutes and alivetime of 60 seconds of an exclusive session.

An Implementation of the Node Reservation API MAY return a HTTP `Link` response header along with a `Locked` status to provide a mean of contacting the owner of the exclusive session through some unspecified protocol. The `Link` header MUST be `Link: <https://owner>` with the `owner` string corresponding to the percent-encoded `owner` string provided to `Acquire` by the owner of the exclusive session. In the absence of a `Link` response header the identity / information about the `owner` of the exclusive session is confidential.

```
POST /x-manufacturer/exclusive/acquire

input to ACQUIRE:
{
    owner: <string>,          // free form string indicating the owner of the Node
    exclusive_key: <string>   // 16 bytes big-endian value in hexadecimal (without 0x prefix) => total of 32 hexadecimal characters
}

output from ACQUIRE:
    <string>                  // bearer token as a base64 string
```
### Renew

The renew endpoint MUST be accessed with an `Authorization` header and a token of the form "Bearer <base64>" where <base64> is the token as a base64 string obtained from the acquire or renew endpoint. The renew endpoint MAY be protected by either the use of an HTTPS server certificate, an HTTPS client certificate with mutual authentication. Other methods of authentication MUST NOT be used.

This operation is atomic on a per Node basis. It is not possible to renew multiple Nodes simultaneously. 

This operation attempts to renew an exclusive session and obtain an associated bearer token. The session expires in 60 minutes unless it is renewed. A session is "alive" for 60 seconds after being acquired or used. 

This operation fails with a status `Unauthorized` if the bearer token of an `Authorization` header is invalid or the session has expired.

This operation fails with a status `TooEarly` if attempted before 1/3 of the session lifetime.

This operation returns a new bearer token to be used subsequently.

```
POST /x-manufacturer/exclusive/renew

output from RENEW:
    string                  // bearer token as a base64 string
```

### Release

The release endpoint MUST be accessed with an `Authorization` header and a token of the form "Bearer <base64>" where <base64> is the token as a base64 string obtained from the acquire or renew endpoints. The renew endpoint MAY be protected by either the use of an HTTPS server certificate, an HTTPS client certificate with mutual authentication. Other methods of authentication MUST NOT be used.

This operation is atomic on a per Node basis. It is not possible to release multiple Nodes simultaneously. 

This operation attemps to release an exclusive session, making it expired. 

This operation fails with a status `Unauthorized` if the bearer token of an `Authorization` header is invalid or the session has expired.

```
POST /x-manufacturer/exclusive/release
```

### KeepAlive

The keepalive endpoint MUST be accessed with an `Authorization` header and a token of the form "Bearer <base64>" where <base64> is the token as a base64 string obtained from the acquire or renew endpoints. The keepalive endpoint MAY be protected by either the use of an HTTPS server certificate, an HTTPS client certificate with mutual authentication. Other methods of authentication MUST NOT be used.

This operation is atomic on a per Node basis. It is not possible to keepalive multiple Nodes simultaneously. 

This operation attempts to keep alive an exclusive session, updating its alive time. The owner SHOULD call this endpoint before the 60 seconds alive timeout of a session is reached.

This operation fails with a status `Unauthorized` if the bearer token of an `Authorization` header is invalid or the session has expired.

```
POST /x-manufacturer/exclusive/keepalive
```

## NMOS RestAPIs

Unless there is no currently active session or stated otherwise, a client MUST use a previously acquired bearer token to access NMOS RestAPIs that may change the state of a Node. The `Authorization` header MUST be used along with a token of the form "Bearer <base64>" where <base64> is the token as a base64 string obtained from the acquire endpoint. Nodes MAY be used without reservation if there is no currently active session.

An `Unauthorized` status is returned if a) the session associated with a bearer token is expired or b) if a bearer token is not used and there is an alive session, and the verb is one of PUT, POST, PATCH, DELETE and the operation may change the state of the Node.

Nodes reservation SHOULD be used in environments where multiple Controllers and/or entities compete for using the Nodes. The Node's exclusivity extend to the exclusive privacy of the streaming. Knowledge of the PEP Pre-Shared Key (PSK) and all the related parameters is not enough for accessing the content. The session exclusive key used in the privacy key derivation process ensures that only the owner of the exclusive session having knowledge of the session exclusive key can access the content, providing further privacy in 1-to-N scenarios (note: peer-to-peer ECDH provides a similar exclusivity in a 1-to-1 scenario).

## Verifying Ownership

If an entity in possession of a exclusive session token lost track of the renewal and keep-alive schedules it SHOULD first attempt to KeepAlive its token and if successful it SHOULD then attempt to renew the token. If the renewal returns a `TooEarly` status, the token SHOULD be considered to be still valid for at least half of its 'Session Lifetime'.


[RFC-2119]: https://tools.ietf.org/html/rfc2119 "Key words for use in RFCs"
[IS-04]: https://specs.amwa.tv/is-04/ "AMWA IS-04 NMOS Discovery and Registration Specification"
[IS-05]: https://specs.amwa.tv/is-05/ "AMWA IS-05 NMOS Device Connection Management Specification"
[NMOS Parameter Registers]: https://specs.amwa.tv/nmos-parameter-registers/ "Common parameter values for AMWA NMOS Specifications"
