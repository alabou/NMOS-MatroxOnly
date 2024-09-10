# Matrox: IS-12 RestAPI
{:.no_toc}  
Copyright 2023, Matrox Graphics Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
  
---
  
{:toc}

## Introduction
This document describes a RestAPI for accessing IS-12 / MS-05-02 objects through an HTTP(S) RestAPI instead of a WebSocket API. 

A Device publishes the IS-12 protocol availability through the declaration of control endpoints.
```
"controls": [
  {
    "type": "urn:x-nmos:control:ncp/v1.0",
    "href": "<protocol>://<address>/ncWebSocket/v1.0"
  }
],
```
The `<protocol>` is either `ws` or `wss ` for accessing IS-12 / MS-05-02 objects using the WebSocket protocol (ws or wss). This is the standard method for accessing IS-12 / MS-05-02 and this is how an `ncp` endpoint is registered in IS-04. This document supports accessing IS-12 / MS-05-02 objects with the HTTP protocol (http or https) using the IS-12 JSON schemas with minor modifications.

A Device MAY also declare a "ncWebSocketGuest" control endpoint in addition or instead of the "ncWebSocket" endpoint for read-only access to the IS-12 / MS-05-02 objects.

## Use of Normative Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY",
and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119][RFC-2119].

## Definitions

## IS-04 Interactions
The IS-12 RestAPI MUST be accessible at the same `ncp` control endpoints published in IS-04 by replacing the `<protocol>` with "http" if the control endpoint is published with the "ws" protocol or "https" if the control endpoint is published with the "wss" protocol. The "http" or "https" protocols MUST NOT be published in IS-04 for an `ncp` endpoint. An implementation MUST support the WebSocket interface and optionally it MAY support the RestAPI interface.

Note: The availability of the IS-12 RestAPI can be verified using the `OPTIONS` verb.

An implementation of the IS-12 RestAPI MAY provide read-only access to objects and require a `Bearer` token to allow read-write access. The read-only `ncp` endpoint MUST have the suffix "Guest" in the control path. For example using "ncWebSocketGuest" for the read-only endpoint and "ncWebSocket" for the read-write endpoint. An implementation MAY support either or both read-only and read-write `ncp` endpoints.

Note: The WebSocket IS-12 `ncp` endpoints uses the same approach for declaring read-only and read-write endpoints.

In the following sections of this document we will use one of the following paths to access the IS-12 RestAPI `http://<address>/ncWebSocket/v1.0`, `https://<address>/ncWebSocket/v1.0`, `http://<address>/ncWebSocketGuest/v1.0` and `https://<address>/ncWebSocketGuest/v1.0`. The string "ncWebSocket" MAY be replaced by a vendor specific string.

## JSON Schemas
The followign schema modifies the IS-12 command-message.json schema slightly to allow the `object` and `method` attributes instead of the usual `oid` and `methodId` ones.

command-message-reatapi.json
```
{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "description": "Command protocol message structure",
  "title": "Command protocol message",
  "allOf": [
    {
      "$ref": "base-message.json"
    },
    {
      "type": "object",
      "required": [
        "commands",
        "messageType"
      ],
      "properties": {
        "commands": {
          "description": "Commands being transmited in this transaction",
          "type": "array",
          "items": {
            "type": "object",
            "oneOf": [
              { "required": [
                    "handle",
                    "oid",
                    "methodId"
                  ]
              },
              { "required": [
                    "handle",
                    "object",
                    "method"
                  ]
              }
            ],
            "properties": {
              "handle": {
                "type": "integer",
                "description": "Integer value used for pairing with the response",
                "minimum": 1,
                "maximum": 65535
              },
              "oid": {
                "type": "integer",
                "description": "Object id containing the method",
                "minimum": 1
              },
              "object": {
                "type": "string",
                "description": "Object containing the method provided as a role path where `/` represent the root",
                "minimum": 1
              },
              "methodId": {
                "type": "object",
                "description": "ID structure for the target method",
                "required": [
                  "level",
                  "index"
                ],
                "properties": {
                  "level": {
                    "type": "integer",
                    "description": "Level component of the method ID",
                    "minimum": 1
                  },
                  "index": {
                    "type": "integer",
                    "description": "Index component of the method ID",
                    "minimum": 1
                  }
                }
              },
              "method": {
                "type": "string",
                "description": "Name of the target method",
                "minimum": 1
              },
              "arguments": {
                "type": "object",
                "description": "Method arguments"
              }
            }
          }
        },
        "messageType": {
          "description": "Protocol message type",
          "type": "integer",
          "enum": [
            0
          ]
        }
      }
    }
  ]
}
```
The following schema modifies the IS-12 subscription-message.json schema slightly to allow an object to be specified either as an integer object id as a string role path.

subscription-message-restapi.json
```
{
  "$schema": "http://json-schema.org/draft-04/schema#",
  "type": "object",
  "description": "Subscription protocol message structure",
  "title": "Subscription protocol message",
  "allOf": [
    {
      "$ref": "base-message.json"
    },
    {
      "type": "object",
      "required": [
        "subscriptions",
        "messageType"
      ],
      "properties": {
        "subscriptions": {
          "description": "Array of OIDs or object role path desired for subscription",
          "type": "array",
          "items": {
            "type": ["integer", "string"]
          }
        },
        "messageType": {
          "description": "Protocol message type",
          "type": "integer",
          "enum": [
            3
          ]
        }
      }
    }
  ]
}
```

## RestAPI
The IS-12 ResteAPI MUST be accessible using the `POST` and `OPTIONS` verbs at the `ncp` endpoint using `http` or `https` as the `<protocol>`. The `GET` verb MUST be used for upgrading the HTTP (http/https) connection to a WebSocket (ws/wss) connection and MUST NOT be used for the RestAPI.

The IS-12 RestAPI MUST support the `OPTIONS` verb as sepecified in the IS-04 specification [IS-04-CORS](https://specs.amwa.tv/is-04/releases/v1.3.2/docs/APIs_-_Server_Side_Implementation_Notes.html#cross-origin-resource-sharing-cors). An `OPTION` request MUST NOT be subject to read-only / read-write constraints.

The body of a `POST` request MUST be one of the following IS-12 schema: command-message-restapi.json, subscription-message-restapi.json. Either the `object` and `method` attributes or the `oid` and `methodId` attributes of a command MUST be used. Those attributes MUST NOT be mixed. For a subscription the object MAY be speficied either as an object id or as a role path.

The body of a `POST` response MUST be one of the following IS-12 schema: command-response-message.json, subscription-response-message.json, notification-message.json, error-message.json. The response MUST be sent using the `chunked` `Transfer-Encoding` such that the client may retrieve command-response, subscription-response, notification and error messages independently. Each response message MUST be sent in its own chunk.

The RestAPI transport the same messages that would otherwise be transported in a WebSocket interface. Enhanced messages naming objects, methods and properties are provided with the RestAPI interface to ease the use for users that usually better know the name of things rather than their hierarchical numbering.

### Object role path
The `object` attribute of a command MUST identify an object with a role path where "/" stands for the `root`.

Example: The `object` "/AlertManager" identifies Matrox mvAlertManager object which is part of the root block and have a role `AlertManager`.

### Object method name
The `method` attribute of a command MUST identify an object's method either with a class path made of class names separated by "::" and terminated by the method name or with the method name alone. In the later case it identifies the method of the most derived class.

Example: For the `object` "/AlertManager" the `method` "Get" identifies the `Get` method of the `mvAlertManager` class while the `method` "NcObject::Get" identifies the `Get` method of the `NcObject` base class.

### Object property name
The `id` argument of type `NcPropertyId` passed to object methods MAY be specified either as an `NcPropertyId` value or a string value. When a string value is used it MUST be a class path made of class names separated by "::" and terminated by the property name or a property name alone.

Example: For the `object` "/AlertManager" the property `id` "MvAlertManager::alertCapabilities" identifies the `alertCapabilities` property of the `mvAlertManager` class.

## Read-Write Authorization
A request to a read-write `ncp` endpoint MUST provide a valid `Bearer` token obtained from the device vendor specific method. An `Unauthorized` (401) error MUST be returned if the request does not have a valid `Bearer` token. A request to a read-only `ncp` endpoint MUST NOT require a valid `Bearer` token.

Note: The same is true for using the Websocket interface. When upgrading an HTTP(s) connection of a read-write `ncp` endpoint to the WebSocket protocol using the `GET` verb, the request must have a valid `Bearer` token obtained from the device vendor specific method.

## Notifications
Notifications from subscriptions MUST be returned in the `POST` response as notification messages compliant with the IS-12 notification-message.json schema. The response MUST be sent using the `chunked` `Transfer-Encoding` such that the client may retrieve notification messages independently. Each response message MUST be sent in its own chunk.

The notification messages MAY interleave with other messages in the `POST` response body.

An implementation of the RestAPI MAY close a connection at any time. It SHOULD return an error message if the connection is closed because of an error. It SHOULD close a connection at response messages boundaries. It MAY close the connection of the the last command response if there is no pending notifications.

A client of the RestAPI MAY keep the connection open indefinitely, waiting for notification messages. To limit the use of device resources, a client SHOULD use a single connection for listening to notification messages.
