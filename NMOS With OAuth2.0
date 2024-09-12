# Matrox: NMOS With OAuth2.0
{:.no_toc}  
Copyright 2024, Matrox Graphics Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
  
---
  
{:toc}

## Introduction

This document presents the modifications / changes to the AMWA/NMOS IS-10 and BCP-003-02 specifications in Matrox NMOS Node devices implementing OAuth2.0 authentication.

The AMWA/NMOS IS-10 and BCP-003-02 specifications are overly generic and complex for implementation across all device classes. In particular, the overhead associated with these specifications, as currently written, is too demanding for smaller devices. This document proposes a balanced approach, offering a compromise between full specification support and the practical need for managing read/write access authorizations to NMOS APIs of an NMOS Node.

An NMOS Node configured to perforn OAuth2.0 Bearer token validation on its NMOS API endpoints implements, as a Resource Server, the modified specification. An NMOS Node is not expected to behave as an OAuth2.0 Client, the NMOS Registry registration API being expected to be secured by TLS client/server certificates only.

## Use of Normative Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY",
and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119][RFC-2119].

## Definitions

The NMOS terms 'Controller', 'Node', 'Source', 'Flow', 'Sender', 'Receiver' are used as defined in the [NMOS Glossary](https://specs.amwa.tv/nmos/main/docs/Glossary.html).

## Registry

An NMOS Registry MUST NOT enable OAuth2.0 authorizations on its registration API. It SHOULD instead enforces the use of TLS v1.2 or v1.3, with client-server mutual authentication if restricting access to the Registry is required, with server authentication otherwise.

## Behaviour

### Time Synchronization

The requirements on the clock used by Nmos Nodes of the NMOS system is relaxed. An NMOS Node is not required be capable of synchronizing their clocks to an external source of time. The Node estimation of the true time MUST be within 30 minutes of the true NTP / PTP time used by the OAuth2.0 authorisation server. The time used by the Node to validate the claims of a token MUST comply with this requirement. The time used by the Node to schedule the fetch / update of the OAuth2.o authorization server public keys MUST comply with this requirement.

### Public Keys

An NMOS Node MUST cache the OAuth2.0 authorization server Public Keys. An NMOS Node MUST fetch the Public Keys at boot time and it MUST update them every 24 hours plus X seconds, where X is a random number in the range 0 to 3600. If an MMOS Node cannot obtain an initial set of the Public Keys, it MUST refuse access to the NMOS APIs until it is able to obtain an initial set of Public Keys. An NMOS Node MUST invalidate the Public Keys from a fetch / update operation at most 48 hours after obtaining them. It MUST then refuse access to the NMOS APIs until it is able to obtain an new set of Public Keys. An NMOS Node MUST use an exponential backoff from 1 to 64 seconds when retrying an initial fetch or an update operation.

An NMOS Node MUST discover through DNS-SD the OAuth2.0 authorization servers URL from the standard IS-10 _nmos-auth._tcp service or it MAY be configured with an list of URLs. An NMOS Node MUST NOT use the `iss` claim of a Bearer token to get Public Keys. The OAuth2.0 authorization servers MUST publish the same set of Public Keys such that any OAuth2.0 authorization server MAY be use by an NMOS Node to obtain the Public Keys and validate access token.

An NMOS Node MUST use TLS v1.2 or v1.3 when fetching / updating Public Keys from an OAuth2.0 authorization server. It MUST validate that the authorization server certificate has been signed by a trusted Certificate Authority. An NMOS Node MUST be configured with a set of trusted Certificate Authorities for validating accesses OAuth2.o authorization servers.

### Access Token 

#### Lifetime

Authorizations are not meant to be provided for short periods of time. An authorization is expected to be delivered for an immediate need for a complete work day. An OAuth2.0 Bearer token MUST have a minimum expiration time (`exp1` claim) of 12 hours and a maximum of 24 hours from its creation time (`iat` claim).

### Type and Algorithms

The token type `typ` MUST be `JWT`.

The algorithm `alg` used for signing the Bearer token MUST be one of `RS256`, `RS512`, `EC256` or `EC512`. When `EC256` is used, the elleptic curve MUST be `P256`. When `EC512` is used, the elleptic curve MUST be `P521`.

### Grants

NMOS Controllers and similar NMOS Tools MUST obtain Bearer tokens with "client credentials" grants to access the APIs of NMOS Nodes. The `sub` and `client_id` claims of a Bearer token MUST be equal for the `client credentials` grant and MUST NOT be equal for the `authorization_code` and other grants.

### Claims

The claims `iss`, `aud`, `sub`, `exp`, `scope`, `client_id` MUST be present in the Bearer token. 

The `nbf` claim SHOULD NOT be present in the Bearer token. If it is present is MUST be ignored.

#### Validation

An NMOS Node MUST require TLS v1.2 or v1.3 when serving HTTP requests. An NMOS Node MUST only accept Access Tokens from the Authorization HTTP Header of a request.

ReadOnly access to a Node's API MUST be blocked if one of the following claims reject Read accesses.
ReadWrite access to a Node's API MUST be blocked if one of the following claims reject Read or Write accesses.

The `sub` and `client_id` claims MUST be equal which indicate "client credentials", otherwise access to the current API MUST NOT be allowed.

The `aud` claim MUST NOT allow access to the current API if it not ["*"] and it does not contain a DNS name that include the [BCP-002-02][] `Instance Identifier` string of the NMOS Node. There MAY be additional characters before and after the `Instance Identifier` in the DNS name. Authorizations SHOULD be delivered to OAuth2.0 Client for specific NMOS Nodes based on their serial number, as defined in the [BCP-002-02][] `Instance Identifier`.

The `scope` claim MUST NOT allow access to the current API if the API name is not an element of the space separated list of API(s) of the claim. Otherwise the `scope` claim MUST provide read access to the complete hierarchy of the current API which MAY further be restricted by a private `x-nmos-*` claim for the current API. An NMOS Node MUST provide such read access independently of the path being accessed. The presence of an `x-nmos-*` claim MUST remove the default read access from the `scope` claim for the associated API.

Note: As opposed to the AMWA/NMOS specification, the presence of an `x-nmos-*` claim matching an NMOS API does not grant implicit read only access. In fact is does the opposite of removing the implicit read only access from the `scope` claim for that NMOS API.

The `read` attribute of an  `x-nmos-*` claim, if present, MUST provides read access if the array of paths is ["*"] and MUST prevent read access if the array of paths is [""]. The absence of a `read` attribute prevent read access. An NMOS Node MUST provide such read access independently of the path being accessed. Values other than "*" and "" MUST NOT be used in the array of paths.

The `write` attribute of an  `x-nmos-*` claim, if present, MUST provides write access if the array of paths is ["*"] and MUST prevent write access if the array of paths is [""]. The absence of a `write` attribute prevent write access. Both read and write accesses MUST be allowed in order to get write access. An NMOS Node MUST provide such read and write access independently of the path being accessed.  Values other than "*" and "" MUST NOT be used in the array of paths.

If the current API access is having side-effects on the state of the NMOS Node, read and write access MUST be allowed. Otherwise the API request MUST fail with a "WWW-Authenticate" status.

If the current API access is not having side-effects on the state of the NMOS Node, read access MUST be allowed. Otherwise the API request MUST fail with a "WWW-Authenticate" status.

#### WebSocket

An NMOS Node SHOULD provide endpoints for getting a WebSocket upgrade that are specific for ReadOnly access and ReadWrite access. If a ReadOnly access endpoint (having the suffix "Guest") is not provided, the endpoint is qualified as having ReadWrite access and causing side-effects on the state of the NMOS Node. So although a `GET` verb is used to get an upgrade to a WebSocket, the request cannot be qualified as ReadOnly unless explicitly qualified.


[RFC-2119]: https://tools.ietf.org/html/rfc2119 "Key words for use in RFCs"
[BCP-002-02]: https://specs.amwa.tv/bcp-002-02/ "AMWA BCP-002-02: NMOS Asset Distinguishing Information"
[IS-04]: https://specs.amwa.tv/is-04/ "AMWA IS-04 NMOS Discovery and Registration Specification"
[IS-05]: https://specs.amwa.tv/is-05/ "AMWA IS-05 NMOS Device Connection Management Specification"
[NMOS Parameter Registers]: https://specs.amwa.tv/nmos-parameter-registers/ "Common parameter values for AMWA NMOS Specifications"
