# Matrox: NMOS With Node Reservation
{:.no_toc}  
Copyright 2024, Matrox Graphics Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
  
---
  
{:toc}

## Introduction

It is sometimes required to reserve the use of a group of NMOS Nodes for a single Controller or entity. This document presents a vendor specific API that is used for reserving the use of a group of NMOS Nodes.

The owner of the Nodes is the only one with the ability to change the state of the Node through the NMOS RestAPIs POST, PUT, DELETE and PATCH verbs. Anyone MAY use the read-only verbs and get information from the Nodes. The owner of the Nodes provides a 128 bit key that is used to seclude the Nodes in a private group when privacy encryption is used. The owner of the Nodes is responsible for keeping its session alive.

> Note: The POST verb on some RestAPI path MAY be allowed for anyone if such request does not change the state of the Node.

## Use of Normative Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119][RFC-2119].

## Definitions

The NMOS terms 'Controller', 'Node', 'Source', 'Flow', 'Sender', 'Receiver' are used as defined in the [NMOS Glossary](https://specs.amwa.tv/nmos/main/docs/Glossary.html).

The 'Session Lifetime' determines the amount of time, after being acquired or renewed, that a session and its token remain valid. A session SHOULD be renewed after half of its lifetime. A session MUST expire a) after its lifetime if not renewed or, b) after its alivetime if unused and an NMOS RestAPI PUT, POST, PATCH or DELETE request changing the state of the Node is performed without a bearer token. By default the lifetime of a session is 60 minutes.

The 'Session AliveTime' determines the amount of time, after being used, that a session and its token remain alive. A session is used when an NMOS RestAPI is accessed using the `Authorization` header and that the bearer token proves to be the owner of the session. A session that is not alive becomes expired if an NMOS RestAPI PUT, POST, PATCH or DELETE request changing the state of the Node is performed without a bearer token. There is a special keepalive endpoint that MAY be used for keeping a session alive. By default the AliveTime of a session is 60 seconds. The AliveTime MAY be configured by an administrator from 60 seconds to 120 seconds, based on a global enterprise policy. Implementations MUST NOT use other values for the AliveTime.

## Using Reservation along with OAuth2.0 authorizations

If accesses to the NMOS APIs are authorized by OAuth2.0, the OAuth2.0 Bearer token MUST be stored in the `Authorization` HTTP header and the exclusive session Bearer token MUST be stored in the `PEP-Exclusive-Authorization` HTTP header. Otherwise when OAuth2.0 authorizations are not used, the exclusive session Bearer token MUST be stored in the `Authorization` HTTP header.

In subsequent sections, references to the `Authorization` header for the exclusive session Bearer token MUST be understood as referring to the `PEP-Exclusive-Authorization` header when OAuth2.0 is in use.

When OAuth2.0 authorizations are used alongside Node Reservation, read-only requests MUST be authorized by the OAuth2.0 Bearer token only. State-changing requests MUST be authorized by the OAuth2.0 Bearer token first, and then by the exclusive session Bearer token, and if enabled, by the mutual TLS (mTLS) client certificate authentication. The Node MUST validate the OAuth2.0 Bearer token first. If OAuth2.0 validation fails, the Node MUST return the appropriate OAuth2.0 error response without evaluating the exclusive session token. If OAuth2.0 validation succeeds, the Node MUST then authorize requests based on the exclusive session Bearer token first, and if enabled, by the mutual TLS (mTLS) client certificate authentication.

When OAuth2.0 authorizations are not used, read-only requests MUST be authorized without restrictions. State-changing requests MUST be authorized by the exclusive session Bearer token first, and then if enabled, by the mutual TLS (mTLS) client certificate authentication.

When neither OAuth2.0 authorizations nor an exclusive session are used, read-only requests MUST be authorized without restrictions. State-changing requests MUST be authorized by the mutual TLS (mTLS) client certificate authentication if enabled.

## Session Lifetime versus AliveTime

A session is associated with a lifetime to protect against compromised Bearer tokens. A session is associated with an alivetime to quickly terminate a previous session when no longer used. 

An entity MUST acquire Nodes to exclusively use them and it MUST prove that it is alive and actively using them to keep its ownership. The 'Session Lifetime' of all the devices MAY be changed by an administrator to better fit the objective of a given deployment to a maximum of 24 hours. The 'Session AliveTime' MUST be 60 or 120 seconds as configured by an administrator. The current values have been chosen to allow a quick turnaround when an entity that reserved a Node becomes dead after a malfunction, power down or other reasons.

The owner of an exclusive session regularly renews its session to obtain a new Bearer token to prevent its session to expire. Between the renewing intervals, the owner of an exclusive session regularly keeps its session alive by calling the KeepAlive endpoint or by using its Bearer token in an access to a Node RestAPI to keep its session alive.

## Reservation RestAPI

This RestAPI MUST use the HTTPS protocol with TLS v1.2 or TLS v1.3. The bare HTTP protocol MUST NOT be used.

The Reservation RestAPI MUST be published as a Node service of type `urn:x-matrox:service:exclusive/v1.0`. The service declaration indicates the URL where the service is accessible and if OAuth2.0 authorizations are required to access the service.

The requests and responses MUST use `Content-Type: application/json`.

In addition to the endpoint-specific status codes defined below, implementations MAY return any standard HTTP error status code (e.g., `405 Method Not Allowed`, `415 Unsupported Media Type`, `429 Too Many Requests`, `500 Internal Server Error`, `501 Not Implemented`) as appropriate.

### Acquire

The acquire endpoint MAY be protected by one or more of the following authentication mechanisms: mutual TLS (mTLS) client certificate authentication, OAuth2.0 Bearer token authentication, or HTTP Basic authentication (RFC 7617). An implementation MUST support at least one of these mechanisms. A Node returning a `401 Unauthorized` status MUST include a `WWW-Authenticate` response header advertising the supported authentication scheme(s). If OAuth2.0 is not used, the acquire endpoint SHOULD NOT be accessed with an `Authorization` header. Otherwise if OAuth2.0 is used, the acquire endpoint SHOULD NOT be accessed with a `PEP-Exclusive-Authorization` header.

This operation MUST be atomic on a per Node basis. The Node Reservation API MUST NOT allow reserving multiple Nodes simultaneously. 

This operation attempts to acquire an exclusive session and obtain an associated bearer token. The session MUST expire in 60 minutes unless it is renewed. A session MUST remain "alive" for AliveTime seconds after being acquired or used. The `exclusive_key` MUST be used on activation of Senders and Receivers as additional keying material to derive the privacy encryption key. The privacy encryption key MUST remain valid even if the session expires until a new owner activates a Sender / Receiver. See [PEP](https://github.com/alabou/NMOS-MatroxOnly/blob/main/NMOS%20With%20Privacy%20Encryption.md) for more details about the Privacy Encryption Protocol.

> Note: "no owner" is also considered a new owner in the previous paragraph.

The operation MUST fail with a status `400 Bad Request` if the posted JSON is invalid. The operation MUST fail with a status `423 Locked` if there is an active session. Otherwise a status `200 Ok` MUST be returned along with a bearer token. The token MUST be used to access the NMOS RestAPIs changing the state of a Node.

The client receiving a `423 Locked` status MUST use an exponential back-off mechanism when retrying to obtain an exclusive session. Such a mechanism MUST consider the Lifetime of 60 minutes and the AliveTime of an exclusive session.

An implementation of the Node Reservation API MAY return a HTTP `Link` response header along with a `423 Locked` status to provide a means of contacting the owner of the exclusive session through some unspecified protocol. The `Link` header MUST be `Link: <https://owner>` with the `owner` string corresponding to the percent-encoded `owner` string provided to `Acquire` by the owner of the exclusive session. In the absence of a `Link` response header the identity / information about the `owner` of the exclusive session is confidential.

```
POST /x-manufacturer/exclusive/acquire

input to ACQUIRE:
{
    owner: <string>,         // A string identifying the owner of the exclusive session.
                             // MUST be a valid URI authority with an optional path as per
                             // RFC 3986 (e.g., "controller.example.com/session/42").
                             // MUST NOT exceed 256 bytes. When used in the Link response
                             // header, it is percent-encoded and prepended with "https://"

    exclusive_key: <string>  // 16 bytes big-endian value in hexadecimal (without 0x prefix) => total of 32 hexadecimal characters
}

output from ACQUIRE:
    <string>                  // bearer token as a base64 string
```

In an NMOS Node, a successful `Acquire` operation MUST set the hidden `key_xcl` IS-05 transport parameter to the value of `exclusive_key` for all Senders and Receivers of the Node supporting Privacy Encryption. When such a Sender or Receiver is activated under the corresponding Node Reservation session with `master_enable` set to `true`, the active `key_xcl` parameter MUST take the value of the staged `key_xcl` parameter for that Sender and MUST be used as additional keying material in the Privacy Encryption key derivation process. A Sender that is activated with `master_enable` set to `true` without an associated Node Reservation session MUST set both the staged and active `key_xcl` hidden transport parameters to an empty octet string, in which case `key_xcl` MUST NOT be used in the Privacy Encryption key derivation process.

### Renew

The renew endpoint MUST be accessed with an `Authorization` header and an opaque token of the form "Bearer <base64>" where <base64> is the token as a base64 string obtained from the acquire or renew endpoint. The renew endpoint MAY be protected by either the use of an HTTPS server certificate, an HTTPS client certificate with mutual authentication. Other methods of authentication MUST NOT be used.

This operation MUST be atomic on a per Node basis. It MUST NOT be possible to renew multiple Nodes simultaneously. 

This operation attempts to renew an exclusive session and obtain an associated bearer token. The session MUST expire in 60 minutes unless it is renewed. A session MUST remain "alive" for AliveTime seconds after being acquired or used. 

This operation MUST fail with a status `401 Unauthorized` and MUST include a `WWW-Authenticate: Bearer` response header if the bearer token of an `Authorization` header is invalid or the session has expired.

This operation MUST fail with a status `425 Too Early` if attempted before 1/3 of the session lifetime.

A successful operation MUST return a status `200 Ok` and a new bearer token to be used subsequently.

The Renew request MUST NOT include a request body.

```
POST /x-manufacturer/exclusive/renew

output from RENEW:
    string                  // bearer token as a base64 string
```

### Release

The release endpoint MUST be accessed with an `Authorization` header and an opaque token of the form "Bearer <base64>" where <base64> is the token as a base64 string obtained from the acquire or renew endpoints. The release endpoint MAY be protected by either the use of an HTTPS server certificate, an HTTPS client certificate with mutual authentication. Other methods of authentication MUST NOT be used.

This operation MUST be atomic on a per Node basis. The Node Reservation API MUST NOT allow releasing multiple Nodes simultaneously. 

This operation attempts to release an exclusive session, making it expired. 

This operation MUST fail with a status `401 Unauthorized` and MUST include a `WWW-Authenticate: Bearer` response header if the bearer token of an `Authorization` header is invalid or the session has expired. Otherwise it MUST return `200 Ok` with no response body after setting the exclusive session as expired.

```
POST /x-manufacturer/exclusive/release
```

In an NMOS Node, a successful `Release` operation MUST set the hidden `key_xcl` IS-05 active and staged transport parameters to an empty octet string for all Senders and Receivers of the Node supporting Privacy Encryption.

Releasing an exclusive session MUST NOT affect the operational state of active Senders and Receivers. The privacy encryption key derived during the previous activation remains valid until the next activation.

### KeepAlive

The keepalive endpoint MUST be accessed with an `Authorization` header and an opaque token of the form "Bearer <base64>" where <base64> is the token as a base64 string obtained from the acquire or renew endpoints. The keepalive endpoint MAY be protected by either the use of an HTTPS server certificate, an HTTPS client certificate with mutual authentication. Other methods of authentication MUST NOT be used.

This operation MUST be atomic on a per Node basis. It MUST NOT be possible to keepalive multiple Nodes simultaneously. 

This operation attempts to keep alive an exclusive session, updating its alive time. The owner SHOULD call this endpoint before the alive timeout of AliveTime seconds of the session is reached.

This operation MUST fail with a status `401 Unauthorized` and MUST include a `WWW-Authenticate: Bearer` response header if the bearer token of an `Authorization` header is invalid or the session has expired. Otherwise it MUST return `200 Ok` with no response body after updating the exclusive session's alive time.

```
POST /x-manufacturer/exclusive/keepalive
```

The KeepAlive operation MUST NOT extend the session Lifetime. Only the Renew operation extends the session Lifetime.

## NMOS RestAPIs

Unless there is no currently active session or stated otherwise, a client MUST use a previously acquired bearer token to access NMOS RestAPIs that may change the state of a Node. The `Authorization` header MUST be used along with an opaque token of the form "Bearer <base64>" where <base64> is the token as a base64 string obtained from the acquire or renew endpoints. Nodes MAY be used without reservation if there is no currently active session.

A `401 Unauthorized` status MUST be returned and MUST include a `WWW-Authenticate: Bearer` response header if a) the session associated with a bearer token is expired or b) if a bearer token is not used and there is an alive session, and the verb is one of PUT, POST, PATCH, DELETE and the operation may change the state of the Node.

Nodes reservation SHOULD be used in environments where multiple Controllers and/or entities compete for using the Nodes. The Node's exclusivity extends to the exclusive privacy of the streaming. Knowledge of the PEP Pre-Shared Key (PSK) and all the related parameters is not enough for accessing the content. The session exclusive key used in the privacy key derivation process ensures that only the owner of the exclusive session having knowledge of the session exclusive key can access the content, providing further privacy in 1-to-N scenarios (note: peer-to-peer ECDH provides a similar exclusivity in a 1-to-1 scenario).

## Verifying Ownership

If an entity in possession of an exclusive session token lost track of the renewal and keep-alive schedules it SHOULD first attempt to KeepAlive its token and if successful it SHOULD then attempt to renew the token. If the renewal returns a `425 Too Early` status, the token SHOULD be considered to be still valid for at least half of its 'Session Lifetime'.

## Additional Applications

### MLS
The `exclusive_key` MAY be used to carry epoch-specific keying material derived by an external Messaging Layer Security (MLS) mechanism as specified by RFC 9420 and RFC 9750. When such usage is supported, a change of MLS epoch secret MUST result in a change of the active `exclusive_key`, and an encrypting device using an in-band dynamic `key_version` protocol MUST change the `key_version` value when the new exclusive_key becomes active. Receivers provisioned with the updated MLS-derived `exclusive_key` MUST be able to derive the corresponding privacy decryption key for the new epoch. Receivers that have not received the updated MLS-derived `exclusive_key` MUST be unable to derive the correct decryption state and, when an authenticated PEP mode is used, MUST detect this condition through authentication failure. The Reservation API acts only as a provisioning mechanism for MLS-derived keying material and does not by itself define MLS group control, membership changes, or epoch distribution.


[RFC-2119]: https://tools.ietf.org/html/rfc2119 "Key words for use in RFCs"
[IS-04]: https://specs.amwa.tv/is-04/ "AMWA IS-04 NMOS Discovery and Registration Specification"
[IS-05]: https://specs.amwa.tv/is-05/ "AMWA IS-05 NMOS Device Connection Management Specification"
[RFC-7617]: https://tools.ietf.org/html/rfc7617 "The 'Basic' HTTP Authentication Scheme"
[NMOS Parameter Registers]: https://specs.amwa.tv/nmos-parameter-registers/ "Common parameter values for AMWA NMOS Specifications"
