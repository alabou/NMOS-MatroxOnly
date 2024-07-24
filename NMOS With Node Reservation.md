# Matrox: NMOS With Node Reservation
{:.no_toc}  
Copyright 2024, Matrox Graphics Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
  
---
  
{:toc}

## Introduction

It is sometime required to reserve the use of a group of NMOS Nodes for a single Controler or entity. This document presents a vendor specific API that is used for reserving the use of a group of NMOS Nodes.

The owner of the Nodes is the only one with the ability change the state of the Node through the NMOS RestAPIs POST, PUT, DELETE and PATCH verbs. Anyone can use the read-only verbs and get informations from the Nodes. The owner of the Nodes provides a 128 bit key that is used to seclude the Nodes in a private group when privacy encryption is used. The owner of the Nodes is responsible for keeping its session alive.

> Note: The POST verb on some RestAPI path MAY be allowed for anyone if such request does not change the state of the Node.

## Use of Normative Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY",
and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119][RFC-2119].

## Definitions

The NMOS terms 'Controller', 'Node', 'Source', 'Flow', 'Sender', 'Receiver' are used as defined in the [NMOS Glossary](https://specs.amwa.tv/nmos/main/docs/Glossary.html).

The 'Session Lifetime' determines the amount of time, after being acquired or renewed, that a session and its token remain valid. A session can be renewed after half of its lifetime. A session expires after its lifetime if not renewed or after its alivetime if unused and an NMOS RestAPI PUT, POST, PATCH or DELETE request changing the state of the Node is performed without a bearer token. By default the lifetime of a session is 5 minutes.

The 'Session AliveTime' determine the amount of time, after being used, that a session and its token remain alive. A session is used when an NMOS RestAPI is accessed using the `Authorization` header and that the bearer token proves to be the owner of the session. A session that is not alive becomes expired if an NMOS RestAPI PUT, POST, PATCH or DELETE request changing the state of the Node is performed without a bearer token. There is a special keepalive endpoint that MAY be used for keeping a session alive. By default the alivetime of a session is 60 seconds.

## Reservation RestAPI

This RestAPI MUST use the HTTPS protocol with TLS v1.2 or TLS v1.3. It is not allowed to use the bare HTTP protocol.

### Acquire

The acquire endpoint MAY be protected by either the use of an HTTPS server certificate, an HTTPS client certificate with mutual authentication or using credential in some form of username and password. It is up to the vendor to decide of the exact mechanism and possibly return a `WWW-Authenticate` header with the proper authentication information. 

This operation is atomic on a per Node basis. It is not possible to reserve multiple Nodes simultaneously. 

This operation attemps to acquire an exclusive session and obtain an associated bearer token. The session expires in 5 minutes unless it is renewed. A session is "alive" for 60 seconds after being acquired or used. The `exclusive_key` is used on activation of Senders and Receivers as additional keying material to derive the privacy encryption key. The privacy encryption key remains valid even if the session expires until a new owner activate a Sender / Receiver.

The operation fail with a status `BadRequest` if the posted JSON is invalid. The operation fail with a status `Locked` if there is an active session. Otherwise a status `Ok` and a bearer token are returned. The token MUST be used to access the NMOS RestAPIs that may change the Node state.

POST /x-manufacturer/exclusive/acquire

input to ACQUIRE:
{
    owner: <string>,          // free form string indicating the owner
    exclusive_key: <string>   // 16 bytes big-endian value in hexadecimal (without 0x prefix) => total of 32 hexadecimal characters
}

output from ACQUIRE:
    <string>                  // bearer token as a base64 string

### Renew

The renew endpoint MUST be accessed with an `Authorization` header and a token of the form "Bearer <base64>" where <base64> is the token as a base64 string obtained from the acquire or renew endpoint. The renew endpoint MAY be protected by either the use of an HTTPS server certificate, an HTTPS client certificate with mutual authentication. Other methods of authentication MUST NOT be used.

This operation is atomic on a per Node basis. It is not possible to renew multiple Nodes simultaneously. 

This operation attemps to renew an exclusive session and obtain an associated bearer token. The session expires in 5 minutes unless it is renewed. A session is "alive" for 60 seconds after being acquired or used. 

This operation fails with a status `Unauthorized` if the bearer token of an `Authorization` header is invalid or the session has expired or if an `Authorization` header is not used and there is an alive session. This operation fails with a status `Locked` if an `Authorization` header is not used and there is no alive session.

This operation fails if attempted before 1/3 of the session lifetime.

This operation returns a new bearer token to be used subsequently.

POST /x-manufacturer/exclusive/renew

output from RENEW:
    string                  // bearer token as a base64 string

### Release

The release endpoint MUST be accessed with an `Authorization` header and a token of the form "Bearer <base64>" where <base64> is the token as a base64 string obtained from the acquire or renew endpoints. The renew endpoint MAY be protected by either the use of an HTTPS server certificate, an HTTPS client certificate with mutual authentication. Other methods of authentication MUST NOT be used.

This operation is atomic on a per Node basis. It is not possible to release multiple Nodes simultaneously. 

This operation attemps to release an exclusive session, making it expired. 

This operation fails if the bearer token is invalid or the session has expired.

POST /x-manufacturer/exclusive/release

### KeepAlive

The keepalive endpoint MUST be accessed with an `Authorization` header and a token of the form "Bearer <base64>" where <base64> is the token as a base64 string obtained from the acquire or renew endpoints. The keepalive endpoint MAY be protected by either the use of an HTTPS server certificate, an HTTPS client certificate with mutual authentication. Other methods of authentication MUST NOT be used.

This operation is atomic on a per Node basis. It is not possible to keepalive multiple Nodes simultaneously. 

This operation attemps to keep alive an exclusive session, updating its alive time. The owner SHOULD call this endpoint before the 60 seconds alive timeout of a session is reached.

This operation fails if the bearer token is invalid or the session has expired.

POST /x-manufacturer/exclusive/keepalive

## NMOS RestAPIs

Unless there is no currently active session, a client MUST use a previously acquired bearer token to access NMOS RestAPIs that may change the state of a Node. The `Authorization` header MUST be used along with a token of the form "Bearer <base64>" where <base64> is the token as a base64 string obtained from the acquire endpoint. Nodes may be used without reservation if there is no currently active session.

An `Unauthorized` status is returned if the session associated with a bearer token is expired or alive, and the verb is one of PUT, POST, PATCH, DELETE and the operation may change the state of the Node.

Nodes reservation SHOULD be used in environments where multiple Controllers and/or entities compete for using the Nodes. The Node's exclusivity extend to the exclusive privacy of the streaming. Knowlege of the PEP Pre-Shared Key (PSK) and all the related parameters is not enough for accessing the content. The session exclusive key used in the privacy key derivation process ensures that only the owner of the exclusive session can access the content, providing further privacy in 1-to-N scenarios (note: peer-to-peer ECDH provides a similar exclusivity in a 1-to-1 scenario).


[RFC-2119]: https://tools.ietf.org/html/rfc2119 "Key words for use in RFCs"
[IS-04]: https://specs.amwa.tv/is-04/ "AMWA IS-04 NMOS Discovery and Registration Specification"
[IS-05]: https://specs.amwa.tv/is-05/ "AMWA IS-05 NMOS Device Connection Management Specification"
[NMOS Parameter Registers]: https://specs.amwa.tv/nmos-parameter-registers/ "Common parameter values for AMWA NMOS Specifications"
