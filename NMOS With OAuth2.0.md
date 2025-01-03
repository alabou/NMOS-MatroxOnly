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

An NMOS Node configured to perform OAuth2.0 Bearer token validation on its NMOS API endpoints implements, as a Resource Server, the modified specification. An NMOS Node is not expected to behave as an OAuth2.0 Client, the NMOS Registry registration API being expected to be secured by TLS client/server certificates only.

## Use of Normative Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY",
and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119][RFC-2119].

## Definitions

The NMOS terms 'Controller', 'Node', 'Source', 'Flow', 'Sender', 'Receiver' are used as defined in the [NMOS Glossary](https://specs.amwa.tv/nmos/main/docs/Glossary.html).

## Registry

An NMOS Registry MUST NOT enable OAuth2.0 authorizations on its registration API. It SHOULD instead enforces the use of TLS v1.2 or v1.3, with client-server mutual authentication if restricting access to the Registry is required, with server authentication otherwise.

## Scope
The scope of an OAuth2.0 authorization is usually the name of the NMOS API used in the path to access the API. For example accessing the IS-05 ConnectionAPI at http://api.example.com/x-nmos/connection/{version} implies the "connection" scope. For IS-04 NodeAPI, QueryAPI, RegistrationAPI, IS-05 ConnectionAPI, IS-08 ChannelMappingAPI and IS-11 StreamCompatibilityManagementAPI the scope MUST be "node", "query", registration", "connection", "channelmapping" and "streamcompatibility" respectively. For IS-12 the scope for accessing MS-05-02 API / Objects MUST use the "nc" scope. For accessing an "x-manufacturer" based API the scope MUST be "manufacturer".

Matrox IS-12 RestAPI is accessible through the IS-12 endpoint and MUST use the "nc" scope as for the IS-12 WebSocket accesses.

## Paths

Access to "/" and "/x-nmos" MUST use the "node" API scope.
Access to "/x-manufacturer" and "/x-manufacturer/*" MUST use the "manufacturer" scope.

Access to an endpoint of the `urn:x-nmos:control:ncp` control type MUST use the "nc" API scope.

## Behaviour

### Time Synchronization

The requirements on the clock used by Nmos Nodes of the NMOS system is relaxed. An NMOS Node is not required to be capable of synchronizing their clocks to an external source of time. The Node estimation of the true time MUST be within 30 minutes of the true NTP / PTP time used by the OAuth2.0 authorisation server. The time used by the Node to validate the claims of a token MUST comply with this requirement. The time used by the Node to schedule the fetch / update of the OAuth2.0 authorization server public keys MUST comply with this requirement.

### Public Keys

An NMOS Node MUST cache the OAuth2.0 authorization server Public Keys. An NMOS Node MUST fetch an initial set of Public Keys after it boots/resets/restarts or an explicit administrative request and it MUST update them every 23 hours plus X seconds, where X is a random number in the range 0 to 3600. If an NMOS Node cannot obtain an initial set of the Public Keys, it MUST refuse access to the NMOS APIs until it retries and obtains an initial set of Public Keys. An NMOS Node MUST invalidate the Public Keys from a previous fetch / update operation 36 hours after obtaining them. It MUST then refuse access to NMOS APIs until it retries and is able to obtain an new set of Public Keys. An NMOS Node MUST use an exponential backoff, from 1 to 64 seconds, when retrying a fetch / update operation.

An NMOS Node MUST log an event if it invalidates the Public Keys and it SHOULD log an event when it gets a set of Public Keys. An NMOS Node MAY log an event when it start refusing access because of a lack of Public Keys. An NMOS Node MAY log an event when it stop refusing access because of a lack of Public Keys.

An NMOS Node MUST discover through DNS-SD the OAuth2.0 authorization servers URL from the standard IS-10 _nmos-auth._tcp service or it MAY be configured with an list of URLs. An NMOS Node MUST NOT use the `iss` claim of a Bearer token to get Public Keys. The OAuth2.0 authorization servers MUST publish the same set of Public Keys such that any OAuth2.0 authorization server MAY be use by an NMOS Node to obtain the Public Keys and validate access token.

An NMOS Node MUST use TLS v1.2 or v1.3 when fetching / updating Public Keys from an OAuth2.0 authorization server. It MUST validate that the authorization server certificate has been signed by a trusted Certificate Authority. An NMOS Node MUST be configured with a set of trusted Certificate Authorities for validating accesses OAuth2.0 authorization servers.

### Access Token 

#### Lifetime

Authorizations are not meant to be provided for short periods of time. An authorization is expected to be delivered for an immediate need for a complete work day. An OAuth2.0 Bearer token MUST have a minimum expiration time (`exp` claim) of 1 hours and a maximum of 24 hours from its creation time (`iat` claim).

### Type and Algorithms

The token type `typ` MUST be `JWT`.

The algorithm `alg` used for signing the Bearer token MUST be one of `RS256`, `RS512`, `EC256` or `EC512`. When `EC256` is used, the elliptic curve MUST be `P256`. When `EC512` is used, the elliptic curve MUST be `P521`.

### Grants

NMOS Controllers and similar NMOS sub-systems MUST obtain Bearer tokens to access the APIs of NMOS Nodes. 

NMOS Controllers and similar NMOS sub-systems SHOULD obtain Bearer tokens with `client_credentials` grants to access the APIs of NMOS Nodes. 
NMOS Controllers, similar NMOS sub-systems, users and tools MAY obtain Bearer tokens with `authorization_code` grants to access the APIs of NMOS Nodes. 

The `sub` and `client_id` claims of a Bearer token MUST be equal for the `client_credentials` grant and MUST NOT be equal for the `authorization_code` and other grants.

An NMOS Node MAY be configured to accept Access Tokens with either `client_credentials` grants or `authorization_code` grants or both.

### Claims

The claims `iss`, `aud`, `sub`, `exp`, `scope`, `client_id` MUST be present in the Bearer token. 

The `nbf` claim SHOULD NOT be present in the Bearer token. If it is present is MUST be ignored.

The private claims `x-nmos-*` SHOULD be placed in an `ext` claim to separate them from standard claims. An NMOS Node MUST support having the private claims `x-nmos-*` either in the `ext` claim or along with the standard claims. An Access Token SHOULD either have the private claims `x-nmos-*` in the `ext` claim or along with the standard claims. If the private `x-nmos-*` claims are duplicated they MUST be identical.

#### Validation

An NMOS Node MUST require TLS v1.2 or v1.3 when serving HTTP requests. An NMOS Node MUST only accept Access Tokens from the Authorization HTTP Header of a request.

ReadOnly access to a Node's API MUST be blocked if one of the following claims reject Read accesses.
ReadWrite access to a Node's API MUST be blocked if one of the following claims reject Read or Write accesses.

The `sub` and `client_id` claims MUST be equal which indicate `client_credentials`, otherwise access to the current API MUST NOT be allowed.

The `aud` claim MUST NOT allow access to the current API if it not ["\*"] and it does not contain a DNS name that include the [BCP-002-02][] `Instance Identifier` string of the NMOS Node. There MAY be additional characters before and after the `Instance Identifier` in the DNS name. Authorizations SHOULD be delivered to OAuth2.0 Client for specific NMOS Nodes based on their serial number, as defined in the [BCP-002-02][] `Instance Identifier`.

The `scope` claim MUST NOT allow access to the current API if the API name is not an element of the space separated list of API(s) of the claim. Otherwise the `scope` claim MUST provide read access to the complete hierarchy of the current API which MAY further be restricted by a private `x-nmos-*` claim for the current API. An NMOS Node MUST provide such read access independently of the path being accessed. The presence of an `x-nmos-*` claim MUST remove the default read access from the `scope` claim for the associated API.

Note: As opposed to the AMWA/NMOS specification, the presence of an `x-nmos-*` claim matching an NMOS API does not grant implicit read only access. In fact is does the opposite of removing the implicit read only access from the `scope` claim for that NMOS API.

The `read` attribute of an  `x-nmos-*` claim, if present, MUST provides read access if the array of paths is ["\*"] and MUST prevent read access if the array of paths is [""]. The absence of a `read` attribute prevent read access. An NMOS Node MUST provide such read access independently of the path being accessed. Values other than "\*" and "" MUST NOT be used in the array of paths.

The `write` attribute of an  `x-nmos-*` claim, if present, MUST provides write access if the array of paths is ["\*"] and MUST prevent write access if the array of paths is [""]. The absence of a `write` attribute prevent write access. Both read and write accesses MUST be allowed in order to get write access. An NMOS Node MUST provide such read and write access independently of the path being accessed.  Values other than "\*" and "" MUST NOT be used in the array of paths.

If the current API access is having side-effects on the state of the NMOS Node, read and write access MUST be allowed. Otherwise the API request MUST fail with a "WWW-Authenticate" status.

If the current API access is not having side-effects on the state of the NMOS Node, read access MUST be allowed. Otherwise the API request MUST fail with a "WWW-Authenticate" status.

An NMOS Node SHOULD increment a status counter a) when a ReadOnly access is denied: a.1) based on the `sub` claim, a.2) based on the `aud` claim, a.3) based on the `scope` claim, a.4) based on the `x-nmos-*` claim, b) when a ReadWrite access is denied: b.1) based on the `sub` claim, b.2) based on the `aud` claim, b.3) based on the `scope` claim, b.4) based on the `x-nmos-*` claim, c) when an access without an Access Token is performed, d) when an acess with an invalid/corrupted token is performed.

#### WebSocket

An NMOS Node SHOULD provide endpoints for getting a WebSocket upgrade that are specific for ReadOnly access and ReadWrite access. If a ReadOnly access endpoint (having the suffix "Guest") is not provided, the endpoint is qualified as having ReadWrite access and causing side-effects on the state of the NMOS Node. So although a `GET` verb is used to get an upgrade to a WebSocket, the request cannot be qualified as ReadOnly unless explicitly qualified.


[RFC-2119]: https://tools.ietf.org/html/rfc2119 "Key words for use in RFCs"
[BCP-002-02]: https://specs.amwa.tv/bcp-002-02/ "AMWA BCP-002-02: NMOS Asset Distinguishing Information"
[IS-04]: https://specs.amwa.tv/is-04/ "AMWA IS-04 NMOS Discovery and Registration Specification"
[IS-05]: https://specs.amwa.tv/is-05/ "AMWA IS-05 NMOS Device Connection Management Specification"
[NMOS Parameter Registers]: https://specs.amwa.tv/nmos-parameter-registers/ "Common parameter values for AMWA NMOS Specifications"
