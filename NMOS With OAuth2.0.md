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

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119][RFC-2119].

## Definitions

The NMOS terms 'Controller', 'Node', 'Source', 'Flow', 'Sender', 'Receiver' are used as defined in the [NMOS Glossary](https://specs.amwa.tv/nmos/main/docs/Glossary.html).

## Registry

An NMOS Registry MUST NOT enable OAuth2.0 authorizations on its registration API. It SHOULD instead enforce the use of TLS v1.2 or v1.3, with client-server mutual authentication if restricting access to the Registry is required, with server authentication otherwise.

## Authorization Server (AS)

This section specifies requirements for an OAuth 2.0 Authorization Server (AS) that issues access tokens intended to be used with this specification.

### Audience policy

The Authorization Server MUST issue access tokens whose `aud` claim contains the complete set of audiences (NMOS Nodes / Resource Servers) that the client/user is authorized to access for the requested API scopes, unless the access token request provides Resource Indicators ([RFC-8707][]) in which case the Authorization Server MAY issue access tokens whose `aud` claim contains only the requested audience. The set MAY be expressed either as an explicit list of entries or using wildcards as per [RFC-4592][].

The Authorization Server MUST validate any requested Resource Indicators ([RFC-8707][]) against the permissions of the client/user.

When Resource Indicators ([RFC-8707][]) are used with this specification, each requested resource is expected to be an absolute URI (typically an HTTPS URL) identifying an NMOS API endpoint. The Authorization Server MUST derive the corresponding `aud` entries from the resources by extracting the host name (FQDN) component, and MUST include that FQDN as an `aud` entry in the issued access token. If the resource URI does not contain a host name, the Authorization Server MUST reject the request.

> Note: Support for [RFC-8707][] by Controllers and Authorization Servers is optional.

## Scope
The scope of an OAuth2.0 authorization is usually the name of the NMOS API used in the path to access the API. For example, accessing the IS-05 ConnectionAPI at `http://api.example.com/x-nmos/connection/{version}` implies the "connection" scope. For IS-04 NodeAPI, QueryAPI, RegistrationAPI, IS-05 ConnectionAPI, IS-08 ChannelMappingAPI, IS-11 StreamCompatibilityManagementAPI and the IS-14 ConfigurationAPI the scope MUST be "node", "query", "registration", "connection", "channelmapping", "streamcompatibility" and "configuration" respectively. For IS-12 the scope for accessing MS-05-02 API / Objects MUST use either the "nc" or "control" scope. For accessing an "x-manufacturer" based API the scope MUST be "manufacturer".

Matrox IS-12 RestAPI is accessible through the IS-12 endpoint and MUST use either the "nc" or "control" scope as for the IS-12 WebSocket accesses.

## Paths

Access to "/" and "/x-nmos" MUST use the "node" API scope.
Access to "/x-manufacturer" and "/x-manufacturer/*" MUST use the "manufacturer" scope.

Access to an endpoint of the `urn:x-nmos:control:ncp` control type MUST use either the "nc" or "control" API scope.

## Behaviour

### Time Synchronization

The requirements on the clock used by NMOS Nodes of the NMOS system are relaxed. An NMOS Node is not required to be capable of synchronizing its clock to an external source of time. The Node's estimation of the true time MUST be within 30 minutes of the true NTP / PTP time used by the OAuth2.0 authorization server. The time used by the Node to validate the claims of a token MUST comply with this requirement. The time used by the Node to schedule the fetch / update of the OAuth2.0 authorization server public keys MUST comply with this requirement.

### Public Keys

An NMOS Node MUST cache the OAuth2.0 authorization server Public Keys. An NMOS Node MUST fetch an initial set of Public Keys after it boots/resets/restarts or an explicit administrative request and it MUST update them every 23 hours plus X seconds, where X is a random number in the range 0 to 3600. If an NMOS Node cannot obtain an initial set of the Public Keys, it MUST refuse access to the NMOS APIs until it retries and obtains an initial set of Public Keys. An NMOS Node MUST invalidate the Public Keys from a previous fetch / update operation 36 hours after obtaining them. It MUST then refuse access to NMOS APIs until it retries and is able to obtain a new set of Public Keys. An NMOS Node SHOULD use an exponential backoff, from 1 to 64 seconds, when retrying a fetch / update operation.

An NMOS Node MUST log an event if it invalidates the Public Keys and it SHOULD log an event when it gets a set of Public Keys. An NMOS Node MAY log an event when it starts refusing access because of a lack of Public Keys. An NMOS Node MAY log an event when it stops refusing access because of a lack of Public Keys.

An NMOS Node MUST discover through DNS-SD the OAuth2.0 authorization server URL(s) from the standard IS-10 `_nmos-auth._tcp` service or it MAY be configured with a list of URLs. An NMOS Node MUST NOT use the `iss` claim of a Bearer token to get Public Keys. The OAuth2.0 authorization servers MUST publish the same set of Public Keys such that any OAuth2.0 authorization server MAY be used by an NMOS Node to obtain the Public Keys and validate access tokens.

An NMOS Node MUST use TLS v1.2 or v1.3 when fetching / updating Public Keys from an OAuth2.0 authorization server. It MUST validate that the authorization server certificate has been signed by a trusted Certificate Authority. An NMOS Node MUST be configured with a set of trusted Certificate Authorities for validating access to OAuth2.0 authorization servers.

### Access Token 

#### Lifetime

Authorizations are not meant to be provided for short periods of time. An authorization is expected to be delivered for an immediate need for a complete work day. An OAuth2.0 Bearer token MUST have a minimum expiration time (`exp` claim) of 1 hour and a maximum of 24 hours from its creation time (`iat` claim).

### Type and Algorithms

The token type `typ` MUST be `JWT`.

The algorithm `alg` used for signing the Bearer token MUST be one of `RS256`, `RS512`, `ES256` or `ES512`. When `ES256` is used, the elliptic curve MUST be `P-256`. When `ES512` is used, the elliptic curve MUST be `P-521`.

### Grants

NMOS Controllers and similar NMOS sub-systems MUST obtain Bearer tokens to access the APIs of NMOS Nodes. 

NMOS Controllers and similar NMOS sub-systems SHOULD obtain Bearer tokens with `client_credentials` grants to access the APIs of NMOS Nodes. 
NMOS Controllers, similar NMOS sub-systems, users and tools MAY obtain Bearer tokens with `authorization_code` grants to access the APIs of NMOS Nodes. 

The `sub` and `client_id` claims of a Bearer token MUST be equal for the `client_credentials` grant and MUST NOT be equal for the `authorization_code` and other grants.

An NMOS Node MAY be configured to only accept Access Tokens with `client_credentials` grants or both `client_credentials` and `authorization_code` grants.

### Claims

The claims `iss`, `aud`, `sub`, `exp`, `scope`, `client_id` MUST be present in the Bearer token. 

The `nbf` claim SHOULD NOT be present in the Bearer token. If it is present it MUST be ignored.

The private claims `x-nmos-*` SHOULD be placed in an `ext` claim to separate them from standard claims. An NMOS Node MUST support having the private claims `x-nmos-*` either in the `ext` claim or along with the standard claims. An Access Token SHOULD either have the private claims `x-nmos-*` in the `ext` claim or along with the standard claims. If the private `x-nmos-*` claims are duplicated they MUST be identical.

#### Validation

An NMOS Node MUST require TLS v1.2 or v1.3 when serving HTTP requests. An NMOS Node MUST only accept Access Tokens from the `Authorization` HTTP header of a request.

ReadOnly access to a Node's API MUST be blocked if one of the following claims reject Read accesses.
ReadWrite access to a Node's API MUST be blocked if one of the following claims reject Read or Write accesses.

By default the `aud` claim MUST NOT allow access to the current API if it is not ["\*"] and no entry contains a DNS name that includes, possibly as a sub-string, the [BCP-002-02][] `Instance Identifier` of the NMOS Node. There MAY be additional characters before and after the `Instance Identifier` in the DNS name. Authorizations SHOULD be delivered to OAuth2.0 Clients for specific NMOS Nodes based on their serial number, as defined in the [BCP-002-02][] `Instance Identifier`. The DNS name of the `aud` clause matching the `Instance Identifier` of the Node MUST additionally be either the `CN` name or one of the alternates `DNS` names of the TLS server certificate associated with the NMOS endpoint.

Alternatively, if configured by an administrator to operate in an environment where OAuth2.0 Authorizations are not delivered based on a serial number, the `aud` claim MUST NOT allow access to the current API if it is not ["\*"] and no entry corresponds to the `CN` name or one of the alternates `DNS` names of the TLS server certificate associated with the NMOS endpoint. The `aud` entries may contain wild-card characters in order to target a subset of devices on a network. Such wild-carding of domain names is documented in [RFC-4592][]. For example, `*.example.com` MUST match `subdomain.example.com` but not `example.com` or `other.example.com`. Implementations MUST support RFC 4592 DNS wildcard matching when evaluating audience entries.

The ordering of the `aud` array is significant only for the purpose of interpreting the private `x-nmos-*` claims that reference `aud` entries by index (see `read` and `write` processing below). For generic audience validation, the `aud` claim is processed as usual, with no specific ordering requirement.

An implementation MUST maintain the `aud` ordering consistently within the processing of a given access token. For example, an implementation MAY internally map `aud` entries to stable identifiers (tags) while preserving the association between each JSON array position (index) and the corresponding `aud` entry.

> Note: Referencing `aud` entries by index (rather than repeating DNS names or instance identifiers by value inside each `x-nmos-*` claim) is intended to keep access tokens compact. This enables an authorization server to issue a single access token that can authorize a Controller to operate on behalf of a user across multiple NMOS Nodes (Resource Servers) without duplicating `aud` strings across multiple per-API claims.

The indexing of the `aud` array is zero-based so the first entry of the `aud` array has index 0.

The `scope` claim MUST NOT allow access to the current API if the API name is not an element of the space separated list of API(s) of the claim. Otherwise the `scope` claim MUST provide read access to the complete hierarchy of the current API which MAY further be restricted by a private `x-nmos-*` claim for the current API. An NMOS Node MUST provide such read access independently of the path being accessed. The presence of an `x-nmos-*` claim MUST remove the default read access from the `scope` claim for the associated API.

Note: As opposed to the AMWA/NMOS specification, the presence of an `x-nmos-*` claim matching an NMOS API does not grant implicit read only access. In fact it does the opposite by removing the implicit read only access from the `scope` claim for that NMOS API.

The `read` attribute of an `x-nmos-*` claim, if present, MUST provide read access if the array of paths is ["\*"] and MUST prevent read access if the array of paths is [""]. The absence of a `read` attribute prevents read access. An NMOS Node MUST provide such read access independently of the path being accessed. Values other than ["\*"], [""], or an array of signed integers MUST NOT be used. Implementations MUST support all three forms of the `read` and `write` attributes: `["*"]` for allow, `[""]` for deny, and arrays of signed integers for indexed allow/deny. The array of signed integers MUST NOT be empty and MUST be sorted to have positive integers first then negative integers. The integer value 0 MUST be considered as a positive integer. If the absolute value of any array entry is outside the bounds of the `aud` claim array, the access token is invalid and access MUST be denied.

The array of signed integers is split in two sub-arrays, one for non-negative integers and one for negative integers, keeping the same ordering as in the original array. The non-negative integer array is an allow-list while the negative integer array is a deny-list.

If the allow-list is not empty, read access MUST be denied unless, for at least one allow-list entry `i`, the associated `aud` claim array entry `aud[i]` considered alone allows access. If the allow-list processing allows read access, such access MUST be denied if, for any deny-list entry `i` (a negative integer), the associated `aud` claim array entry `aud[abs(i)]` considered alone allows access; otherwise read access MUST be allowed.

If the allow-list is empty, the deny-list is a deny-only list: read access MUST be denied if, for any deny-list entry `i` (a negative integer), the associated `aud` claim array entry `aud[abs(i)]` considered alone allows access; otherwise read access MUST be allowed.

The `write` attribute of an `x-nmos-*` claim, if present, MUST provide write access if the array of paths is ["\*"] and MUST prevent write access if the array of paths is [""]. The absence of a `write` attribute prevents write access. Both read and write accesses MUST be allowed in order to get write access. An NMOS Node MUST provide such read and write access independently of the path being accessed. Values other than ["\*"], [""], or an array of signed integers MUST NOT be used. Implementations MUST support all three forms of the `read` and `write` attributes: `["*"]` for allow, `[""]` for deny, and arrays of signed integers for indexed allow/deny. The array of signed integers MUST NOT be empty and MUST be sorted to have positive integers first then negative integers. The integer value 0 MUST be considered as a positive integer. If the absolute value of any array entry is outside the bounds of the `aud` claim array, the access token is invalid and access MUST be denied.

The array of signed integers is split in two sub-arrays, one for non-negative integers and one for negative integers, keeping the same ordering as in the original array. The non-negative integer array is an allow-list while the negative integer array is a deny-list.

If the allow-list is not empty, write access MUST be denied unless, for at least one allow-list entry `i`, the associated `aud` claim array entry `aud[i]` considered alone allows access. If the allow-list processing allows write access, such access MUST be denied if, for any deny-list entry `i` (a negative integer), the associated `aud` claim array entry `aud[abs(i)]` considered alone allows access; otherwise write access MUST be allowed.

If the allow-list is empty, the deny-list is a deny-only list: write access MUST be denied if, for any deny-list entry `i` (a negative integer), the associated `aud` claim array entry `aud[abs(i)]` considered alone allows access; otherwise write access MUST be allowed.

If the current API access is having side-effects on the state of the NMOS Node, read and write access MUST be allowed. Otherwise the API request MUST fail with HTTP 403 (`Forbidden`) if the token is valid but permissions are insufficient, or HTTP 401 (`Unauthorized`) with a `WWW-Authenticate` response header if the token is invalid or missing.

If the current API access is not having side-effects on the state of the NMOS Node, read access MUST be allowed. Otherwise the API request MUST fail with HTTP 403 (`Forbidden`) if the token is valid but permissions are insufficient, or HTTP 401 (`Unauthorized`) with a `WWW-Authenticate` response header if the token is invalid or missing.

An NMOS Node SHOULD increment a status counter a) when a ReadOnly access is denied: a.1) based on the `sub` claim, a.2) based on the `aud` claim, a.3) based on the `scope` claim, a.4) based on the `x-nmos-*` claim, b) when a ReadWrite access is denied: b.1) based on the `sub` claim, b.2) based on the `aud` claim, b.3) based on the `scope` claim, b.4) based on the `x-nmos-*` claim, c) when an access without an Access Token is performed, d) when an access with an invalid/corrupted token is performed.

#### Mutual TLS Client Certificate Binding

When a Node API endpoint is accessed using mutual TLS (mTLS) and an OAuth 2.0 access token is presented, the Node MUST enforce an additional client identity check as specified below:

- The Node MUST authorize the request only if the `client_id` claim value matches the `CN` name or one of the alternates `DNS` names of the TLS client certificate accessing the NMOS endpoint. 
- The comparison MUST be case-insensitive. 
- Wildcards MUST NOT be considered a match. If a wildcard is present in any SAN entry the Node MUST treat it as non-matching for the purpose of this check. If no match is found, the Node MUST reject the request.

This check binds the access token to the identity of the OAuth 2.0 client (the Controller), as identified by the `client_id` claim. The `sub` claim identifies the end user (where applicable) and MUST NOT be used for this binding.

When mTLS is used, OAuth 2.0 clients (Controllers) MUST be provisioned such that their `client_id` value matches (case-insensitively) the `CN` name or one of the alternates `DNS` names of their TLS client certificate. Wildcards MUST NOT be used for this purpose. An OAuth 2.0 Authorization Server SHOULD enforce this requirement at client registration time and/or when issuing access tokens.

#### WebSocket

An NMOS Node SHOULD provide endpoints for getting a WebSocket upgrade that are specific for ReadOnly access and ReadWrite access. If a ReadOnly access endpoint (having the suffix "Guest") is not provided, the endpoint is qualified as having ReadWrite access and causing side-effects on the state of the NMOS Node. So although a `GET` verb is used to get an upgrade to a WebSocket, the request cannot be qualified as ReadOnly unless explicitly qualified.

Subscribing to notification messages MUST be considered a read-only operation. Registering a websocket for receiving notification messages from objects MAY cause side-effects on the state of the websocket connection. This MUST NOT be considered as causing side-effects on the state of the NMOS Node. The Read-Only versus Read-Write qualifiers relate to objects in the [MS-005-02][] framework, not to the IS-12 mechanisms for accessing, controlling and monitoring those objects.

#### HTTP Status Codes

Implementations MUST use appropriate HTTP status codes for access failures:
- **401 Unauthorized**: Returned when the access token is missing, expired, malformed, has an invalid signature, or fails the Mutual TLS Client Certificate Binding check. Include a `WWW-Authenticate` response header as per RFC 6750.
- **403 Forbidden**: Returned when the token is valid but the requested operation is denied due to insufficient permissions (e.g., scope mismatch, audience restrictions, or explicit deny via `x-nmos-*` claims).

##### Examples (Informative)

The following examples illustrate access tokens for a Controller operating on behalf of a user across multiple NMOS Nodes (for example in mux and independent-stream topologies such as MPEG2-TS over RTP/SRT/UDP/RTSP).

**Example 1: complete token using `["*"]` for multiple APIs and multiple Nodes**

This example follows a simple pattern where the Authorization Server grants full read/write access for the listed APIs on all targeted Nodes.

```json
{
  "iss": "https://oauth2.matrox.com/v1.0",
  "scope": "offline node connection streamcompatibility",
  "sub": "user@matrox.com",
  "aud": ["MTXCIP-CC91629", "MTXCIP-CC91699"],
  "client_id": "nmosController-54321",
  "exp": 1.720538859e+09,
  "x-nmos-node": { "read": ["*"], "write": [""] },
  "x-nmos-connection": { "read": ["*"], "write": ["*"] },
  "x-nmos-streamcompatibility": { "read": ["*"], "write": ["*"] }
}
```

**Example 2: compact token using `aud` indices**

This example illustrates how the same token can remain compact by referencing `aud` entries by index. In this example, the Controller is authorized for write accesses only on node MTXCIP-CC91699. The "x-nmos-node" claim is not present because the "scope" claim already provides read access.

```json
{
  "iss": "https://oauth2.matrox.com/v1.0",
  "scope": "offline node connection streamcompatibility",
  "sub": "user@matrox.com",
  "aud": ["MTXCIP-CC91629", "MTXCIP-CC91699"],
  "client_id": "nmosController-54321",
  "exp": 1.720538859e+09,
  "x-nmos-connection": { "read": [0, 1], "write": [1] },
  "x-nmos-streamcompatibility": { "read": ["*"], "write": [1] }
}
```

**Example 3: compact token using `aud` indices with universal read-only**

This example illustrates how the same token can remain compact by referencing `aud` entries by index. In this example, the Controller is authorized for write accesses only on nodes MTXCIP-CC91629 and MTXCIP-CC91699. The "x-nmos-node" claim is not present because the "scope" claim already provides read access. ReadOnly access is allowed on any node.

```json
{
  "iss": "https://oauth2.matrox.com/v1.0",
  "scope": "offline node connection streamcompatibility",
  "sub": "user@matrox.com",
  "aud": ["*", "MTXCIP-CC91629", "MTXCIP-CC91699"],
  "client_id": "nmosController-54321",
  "exp": 1.720538859e+09,
  "x-nmos-connection": { "read": ["*"], "write": [1, 2] },
  "x-nmos-streamcompatibility": { "read": ["*"], "write": [1, 2] }
}
```

##### Pseudocode (Informative)

The pseudocode below illustrates the normative requirements of this section for evaluating read/write access for a single HTTP request.

```python
# Inputs:
# - claims: decoded JWT access token claims (signature already validated)
# - read_write: True if the request has side-effects on the state of the NMOS Node
# - api_name: current NMOS API name (e.g. "node", "connection", "query", ...)
# - node_instance_id: BCP-002-02 Instance Identifier of the NMOS Node (if used in aud)
# - tls_server_cert_names: set of DNS names from TLS server certificate (CN + SANs)
# - use_client_credentials_grant_only: bool (policy switch)
# - use_serial_number_in_aud: bool
#     - True: aud entries contain the Instance Identifier (serial number) and MUST also match TLS server certificate identity
#     - False: aud entries are (wildcard-capable) TLS server certificate names
#
# Output:
# - allow: boolean
# - otherwise the request fails with HTTP 401 and includes a WWW-Authenticate response header

def validate_access(
    claims,
    read_write,
    api_name,
    node_instance_id,
    tls_server_cert_names,
    use_client_credentials_grant_only,
    use_serial_number_in_aud,
):
    # ---- required claims ----
    required = ["iss", "sub", "aud", "client_id", "exp", "scope"]
    for k in required:
        if k not in claims:
            return DENY  # invalid token

    # ---- exp check ----
    exp = claims["exp"]
    if not is_number(exp):
        return DENY  # invalid token
    if now() > unix_time(exp):
        return DENY

    # ---- grant policy (optional) ----
    sub = claims["sub"]
    client_id = claims["client_id"]
    if not is_string(sub) or not is_string(client_id):
        return DENY  # invalid token
        
    if use_client_credentials_grant_only:
        if sub != client_id:
            return DENY  # invalid token

    # ---- scope gating ----
    scope = claims["scope"]
    if not is_string(scope):
        return DENY  # invalid token
    if api_name not in split_by_spaces(scope):
        return DENY

    # ---- aud gating ----
    aud = claims["aud"]
    if not is_array(aud) or any(not is_string(a) for a in aud):
        return DENY  # invalid token

    if not any(aud_entry_allows_current_node(a, node_instance_id, tls_server_cert_names, use_serial_number_in_aud) for a in aud):
        return DENY

    # ---- locate private claim x-nmos-<api> (it may be in ext or at top-level) ----
    priv = None
    access_key = "x-nmos-" + api_name

    if "ext" in claims:
        if not is_object(claims["ext"]):
            return DENY  # invalid token
        if access_key in claims["ext"]:
            priv = claims["ext"][access_key]
    else:
        if access_key in claims:
            priv = claims[access_key]

    # ---- no private claim: RO allowed, RW denied ----
    if priv is None:
        return ALLOW if not read_write else DENY

    if not is_object(priv):
        return DENY  # invalid token

    # Presence of x-nmos-<api> removes default implicit read access from scope.
    # Read must be granted explicitly by the private claim.
    read_allowed = eval_indexed_attr(priv.get("read", MISSING), aud, node_instance_id, tls_server_cert_names, use_serial_number_in_aud)
    if read_allowed is INVALID:
        return DENY  # invalid token
    if read_allowed is not ALLOW:
        return DENY

    write_allowed = eval_indexed_attr(priv.get("write", MISSING), aud, node_instance_id, tls_server_cert_names, use_serial_number_in_aud)
    if write_allowed is INVALID:
        return DENY  # invalid token

    # Consistency rule: it is invalid for a token to grant write access without also granting read access.
    if (write_allowed is ALLOW) and (read_allowed is not ALLOW):
        return DENY  # invalid token

    if read_write:
        return ALLOW if ((read_allowed is ALLOW) and (write_allowed is ALLOW)) else DENY
    else:
        return ALLOW if (read_allowed is ALLOW) else DENY


def aud_entry_allows_current_node(aud_entry, node_instance_id, tls_server_cert_names, use_serial_number_in_aud):
    if aud_entry == "*":
        return True

    if use_serial_number_in_aud:
        # aud_entry must contain node_instance_id as a substring
        if node_instance_id not in aud_entry:
            return False
        # and must also match TLS server certificate identity (CN or SAN)
        return aud_entry in tls_server_cert_names

    # use_serial_number_in_aud == False: aud entries are TLS cert names (with RFC 4592 wildcards)
    return matches_dns_wildcard(aud_entry, tls_server_cert_names)

def matches_dns_wildcard(pattern, cert_names):
    # Implement RFC 4592 DNS wildcard matching (e.g., *.example.com matches sub.example.com)
    for name in cert_names:
        if dns_wildcard_matches(pattern, name):
            return True
    return False

def dns_wildcard_matches(pattern, target):
    # Simplified: pattern like *.domain matches sub.domain
    # Full RFC 4592 implementation needed in real code
    if pattern.startswith("*."):
        domain = pattern[2:]
        return target.endswith("." + domain) and "." not in target[:-len("." + domain)]
    return pattern == target


def eval_indexed_attr(attr, aud, node_instance_id, tls_server_cert_names, use_serial_number_in_aud):
    # Returns one of {ALLOW, DENY, INVALID}
    #
    # Supported forms:
    # - ["*"]  => ALLOW
    # - [""]   => DENY
    # - [signed integers...] referencing aud indices:
    #     i >= 0: allow if aud[i] alone allows
    #     i <  0: deny  if aud[abs(i)] alone allows
    # - missing => DENY
    if attr is MISSING:
        return DENY

    if is_array(attr) and len(attr) == 1 and is_string(attr[0]):
        if attr[0] == "*":
            return ALLOW
        if attr[0] == "":
            return DENY
        return INVALID

    if not is_array_of_signed_integers(attr):
        return INVALID

    if len(attr) == 0:
        return INVALID

    # The array MUST be sorted to have positive integers first then negative integers (0 is positive).
    # Do not auto-sort; treat ordering violations as INVALID.
    list_pos = []
    list_neg = []
    seen_negative = False
    for i in attr:
        if i < 0:
            seen_negative = True
            list_neg.append(i)
        else:
            if seen_negative:
                return INVALID
            list_pos.append(i)

    # Evaluate allowlist/denylist semantics.
    #
    # - If there is at least one non-negative index, the list is an allowlist with optional deny exceptions:
    #     * DENY unless at least one non-negative index matches.
    #     * If allowed, DENY if any negative index matches (deny exception).
    # - If the list contains only negative indices, it is a denylist:
    #     * ALLOW unless a negative index matches.

    def idx_matches(i):
        if abs(i) >= len(aud):
            return INVALID
        aud_entry = aud[abs(i)]
        return aud_entry_allows_current_node(aud_entry, node_instance_id, tls_server_cert_names, use_serial_number_in_aud)

    # Phase 1: allow-list (if present)
    if len(list_pos) > 0:
        allowed = False
        for i in list_pos:
            m = idx_matches(i)
            if m is INVALID:
                return INVALID
            if m:
                allowed = True
                break
        if not allowed:
            return DENY

    # Phase 2: deny-list exceptions (applies both to allowlist and denylist-only)
    for i in list_neg:
        m = idx_matches(i)
        if m is INVALID:
            return INVALID
        if m:
            return DENY

    return ALLOW
```


[RFC-2119]: https://tools.ietf.org/html/rfc2119 "Key words for use in RFCs"
[BCP-002-02]: https://specs.amwa.tv/bcp-002-02/ "AMWA BCP-002-02: NMOS Asset Distinguishing Information"
[IS-04]: https://specs.amwa.tv/is-04/ "AMWA IS-04 NMOS Discovery and Registration Specification"
[IS-05]: https://specs.amwa.tv/is-05/ "AMWA IS-05 NMOS Device Connection Management Specification"
[NMOS Parameter Registers]: https://specs.amwa.tv/nmos-parameter-registers/ "Common parameter values for AMWA NMOS Specifications"
[MS-005-02]: https://specs.amwa.tv/ms-05-02/ "AMWA MS-05-02 NMOS Control Framework"
[RFC-4592]: https://tools.ietf.org/html/rfc4592 "The Role of Wildcards in the Domain Name System"
[RFC-8707]: https://tools.ietf.org/html/rfc8707 "Resource Indicators for OAuth 2.0"
