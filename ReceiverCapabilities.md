  
Copyright 2023, Matrox Graphics Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
  
---
  
# AMWA BCP-004-01r: Matrox NMOS Receiver Capabilities

In [IS-04][], a Receiver resource expresses the capabilities of a Receiver through attributes that identify constraints on streams and sub-Streams of compatible Senders.

Receivers indicate their `transport` and `format`. These attributes express constraints that can be evaluated against the related attributes of a Sender and its Flow.

The Receiver `caps` object is provided as an extensible mechanism to define finer-grained constraints.

IS-04 itself defines `caps` attributes for `media_types` (since v1.1) and, for data Receivers, also  `event_types` (since v1.3). Both these attributes express constraints that can be evaluated against Flow attributes, as arrays whose elements define the alternatives that are acceptable. In each case, the constraint is satisfied when the target Flow attribute matches **any of** the enumerated alternatives.  

When `caps` contains multiple attributes, i.e. both `media_types` and `event_types`, the Receiver indicates that it only accepts streams that satisfy **all of** (both!) the constraints.

The `media_types` and  `event_types` attributes are not used to express sub-Flow/sub-Stream constraints or to evaluate the compatibility of sub-Flows/sub-Streams. When a Receiver is of format `urn:x-nmos:format:mux`, those attributes are used for expressing and evaluating the constraints of the mux Receiver only. They are ignored when evaluating the constraints of the Receiver's sub-Streams.

This specification defines a new `constraint_sets` attribute for the Receiver `caps` object, which can also be combined with the existing ones. In common with the existing attributes, its value is an array of alternatives; this constraint is satisfied when **any of** its enumerated Constraint Sets are satisfied.

When evaluating constraints for sub-Flows/sub-Streams, only the Constraint Sets alternatives of matching `urn:x-matrox:format` and `urn:x-matrox:layer` are to be considered. The remaining Constraints Sets of the `constraint_sets` are ignored.

This specification defines a generic JSON syntax to express Constraint Sets made up of individual Parameter Constraints. The Constraint Set is satisfied if **all of** its Parameter Constraints are satisfied.

The representation of individual Parameter Constraints resembles the mechanism defined by [IS-05][] to constrain Sender and Receiver transport parameters at the **/constraints** endpoints, which Nodes and Controllers may also support.

This specification also defines a `version` attribute to indicate when changes to the `caps` object took place.

The `constraints_set` and `version` attributes are listed in the Capabilities parameter register in the [NMOS Parameter Registers][].

## Use of Normative Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119][RFC-2119].

## Defining Parameter Constraints

A specification for each Parameter Constraint is strongly RECOMMENDED to be listed in the Capabilities register in the [NMOS Parameter Registers][] and [Matrox Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md). Each specification defines a unique identifier, the constraint type, and the target parameter, as follows.

### Parameter Constraint Identifiers

Each Parameter Constraint is given a unique identifier - a URN. Parameter Constraints defined by the AMWA have the form:
```
urn:x-nmos:cap:<category>:<constraint>
```

Two `<category>` names are initially defined, `format` for media-related constraints, and `transport` for transport-related constraints.

For example, `urn:x-nmos:cap:format:grain_rate` is a Parameter Constraint relating to the Grain rate of the stream, for example by targeting the  `grain_rate` attribute of an IS-04 Flow. (The concept of Grains is defined in the [JT-NM Reference Architecture][].)

The `<category>` name `meta` is reserved for [metadata related to Constraint Sets](#constraint-set-metadata). These attributes are not constraints themselves.

Manufacturers MAY use their own namespaces to indicate Parameter Constraints which are not currently defined within the NMOS namespace (`urn:x-nmos:cap:`).

### Parameter Constraint Types

The specification defines the JSON value type to which the constraint relates, which MUST be one of:
* `string`
* `integer`
* `number`
* `boolean`
* `rational`
  * as per IS-04, a JSON object with an integer `numerator` and optional integer `denominator` (default: 1)

The type of the constraint defines which [Constraint Keywords](#constraint-keywords) are allowed when the Parameter Constraint is instantiated.

### Parameter Constraint Target

The specification defines the target parameter against which the constraint is to be evaluated, for example, the specific IS-04 Flow attribute or [SDP][] format-specific parameter.

Especially in the case of parameters carried in non-JSON formats, such as a transport file, the specification MUST also describe how to map the parameter value to one of the [supported JSON types](#parameter-constraint-types).

## Instantiating Parameter Constraints

The Receiver expresses its capabilities with respect to a particular Parameter Constraint by including the constraint's unique identifier as an attribute in a [Constraint Set](#constraint-sets) with an object value, the attributes of which depend on the [specified type](#parameter-constraint-types).

For example:

```json
"urn:x-nmos:cap:format:sample_depth": {
  "enum": [ 24, 20, 16 ]
}
```

## Constraint Keywords

Each Parameter Constraint is instantiated as an object with attributes that are type-specific Constraint Keywords defining how the parameter is constrained.

The Parameter Constraint is satisfied if **all of** the constraints expressed by the Constraint Keywords are satisfied.
This implies that if **any of** the constraints expressed by the Constraint Keywords are _not_ satisfied, the Parameter Constraint is not satisfied.
Equally, when there are no Constraint Keywords, the Parameter Constraint thus explicitly indicates that the target parameter is unconstrained.

Note that in some cases, the target parameter will allow future addition of new values, for example by inclusion in the Flow Attributes register in the NMOS Parameter Registers.
It could therefore be better to explicitly constrain the target parameter to all supported values, if new values could cause an issue.

### Common Constraint Keywords

The following attributes are allowed for all constraint types:
* `enum` as an array value with one or more elements of the specified type

### String Constraint Keywords

Nothing additional

### Integer and Number Constraint Keywords

The following attributes are additionally allowed for `integer` and `number` constraints:

* `minimum`, inclusive minimum, an integer or number as appropriate
* `maximum`, inclusive maximum, an integer or number as appropriate

### Boolean Constraint Keywords

Nothing additional

### Rational Constraint Keywords

The following attributes are additionally allowed for `rational` constraints:

* `minimum`, inclusive minimum, a `rational` value
* `maximum`, inclusive maximum, a `rational` value

Note that comparison between two rational values, _n<sub>1</sub> / d<sub>1</sub>_ and _n<sub>2</sub> / d<sub>2</sub>_, SHOULD be performed by cross-multiplication and comparison of the products, _n<sub>1</sub> * d<sub>2</sub>_ and _n<sub>2</sub> * d<sub>1</sub>_, taking account of negative denominators.

## Constraint Sets

Constraint Sets MUST be instantiated with one or more Parameter Constraints.
The Constraint Set is satisfied if **all of** its Parameter Constraints are satisfied.
This implies that if **any of** the Parameter Constraints are _not_ satisfied, the Constraint Set as a whole is not satisfied.

The Constraint Set is represented as a JSON object with attributes that are the Parameter Constraints.

### Constraint Set Metadata

Additional metadata about each Constraint Set MAY be included, using the metadata attributes listed in the Capabilities register in the [NMOS Parameter Registers][] and [Matrox Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md) with the following unique identifiers:
```
urn:x-nmos:cap:meta:<attribute>
```

#### Constraint Set Label

The metadata attribute `urn:x-nmos:cap:meta:label` MAY be used to provide a human-readable name for the Constraint Set as a simple string value.
If a Receiver uses this attribute, it SHOULD do so for all Constraint Sets.

A Controller MAY use this label to indicate to a user which Constraint Sets of a Receiver are satisfied by a Sender.

#### Constraint Set Preference

The metadata attribute `urn:x-nmos:cap:meta:preference` enables the Receiver to indicate its preference between the listed Constraint Sets.

A Controller MAY use Receiver preference, for example, to assist the user in choosing between multiple Senders to connect to a Receiver.

The preference is indicated as an integer value in the range from -100 to 100 inclusive.

If the Receiver has no preference, it MAY omit the attribute from all Constraint Sets.

When a Receiver wants to indicate preference, it adds the attribute either to all Constraint Sets or only to some, in which case the other Constraint Sets have an effective value of 0.
The Receiver indicates its strongest preference for one or more Constraint Sets by assigning them its highest value.
It indicates preference against, or weaker preference for, Constraint Sets by assigning them lower values.

For example:

* When a Receiver supports a few options natively, and many that require some transformation, it MAY explicitly associate a positive value just with the native options (since the many will have a lower effective value of 0).
* When a Receiver supports many options well, but a few low-quality options are provided, perhaps for wider compatibility, it MAY explicitly associate a negative value just with those options (since the many will have a higher effective value of 0).

#### Constraint Set Enabled

The metadata attribute `urn:x-nmos:cap:meta:enabled` MAY be used to indicate Constraint Sets which do not apply to the current operating configuration of a Receiver, but which can be enabled via some unspecified configuration mechanism.

A Controller MUST NOT take into consideration a Constraint Set that has this attribute set to `false`, unless the Controller is capable of making the required configuration changes. Controllers MAY use this attribute as a hint to users that a Sender and Receiver could be connected subject to a reconfiguration.

If a Constraint Set is enabled or the Receiver does not support offline capabilities then this attribute MAY be omitted.

#### Constraint Set Format, Layer and Layer Compatibility Groups

A sub-Flow is defined as a member of a multiplexed flow produced by a Flow of format `urn:x-nmos:format:mux`. A sub-Flow MUST be a member of the `parents` attribute of a mux Flow.

A sub-Stream is defined as a member of a multiplexed stream consumed by a Receiver of format `urn:x-nmos:format:mux`.

The metadata attribute `urn:x-matrox:cap:meta:format` MUST be used to indicate that a Constraint Set, associated with a sub-Flow/sub-Stream, applies to a specific format. The format MAY be one of `urn:x-nmos:format:video`, `urn:x-nmos:format:audio` or `urn:x-nmos:format:data`.

The metadata attribute `urn:x-matrox:cap:meta:layer` MUST be used to indicate that a Constraint Set, associated with a sub-Flow/sub-Stream, applies to a specific layer of a given format. The layer must be an unsigned integer in the range 0 to N-1 where N the total number of layers of a given format.

The metadata `urn:x-matrox:cap:meta:format` and `urn:x-matrox:cap:meta:layer` attributes MUST be used to filter the Constraint Sets for a target sub-Flow/sub-Stream or a target mux Flow/Stream.

A sub-Flow MUST have a `urn:x-matrox:layer` attribute matching the associated Sender Constraint Set `urn:x-matrox:cap:meta:layer` meta attribute. The sub-Flow `format` attribute MUST match the associated Sender Constraint Set `urn:x-matrox:cap:meta:format` meta attribute.

A Source associated with a Receiver sub-Stream MUST have a `urn:x-matrox:layer` attribute matching the associated Receiver Constraint Set `urn:x-matrox:cap:meta:layer` meta attribute. The Source `format` attribute MUST match the associated Receiver Constraint Set `urn:x-matrox:cap:meta:format` meta attribute.

The metadata attribute `urn:x-matrox:cap:meta:layer_compatibility_groups` MAY be used on a sub-Flow/sub-Stream to indicate that a Constraint Set applies to a number of layer compatibility groups. The layer compatibility groups must be an array of unsigned integer in the range 0 to 63. A Constraint Set MAY apply to multiple compatibility groups. A Constraint Set without a `urn:x-matrox:cap:meta:layer_compatibility_groups` attribute MUST be assumed as being part of all groups. Only Constraint Sets that are members of a common group are compatibles. A Controller SHOULD process Constraint Sets according to their compatibility group.

A sub-Flow MUST have a `urn:x-matrox:layer_compatibility_groups` attribute matching the associated Sender Constraint Set `urn:x-matrox:cap:meta:layer_compatibility_groups` meta attribute. The sub-Flow `format` attribute MUST match the associated Sender Constraint Set `urn:x-matrox:cap:meta:format` meta attribute. The intersection of the `urn:x-matrox:layer_compatibility_groups` attribute of all the sub-Flows associated with a mux Flow MUST not be empty.

A sub-Stream/sub-Flow Constraint Set MUST NOT use transport Receiver/Sender Capabilities. Such Capabilities use the `urn:x-nmos:cap:transport:` or `urn:x-matrox:cap:transport:` prefix and apply only to a Stream/Flow.

### Listing Constraint Sets

The Receiver advertises a list of Constraint Sets as a JSON array of these objects, using the key `constraint_sets` in the `caps` object.

The `constraint_sets` as a whole is satisfied if **any of** the listed Constraint Sets of matching `urn:x-matrox:format` and `urn:x-matrox:layer` are satisfied. For the purpose of filtering the list of Constraint Sets, the absence of the `urn:x-matrox:cap:meta:format` and `urn:x-matrox:cap:meta:layer` meta attributes provides the list of Constraint Sets that are not associated with sub-Flows/sub-Streams. The evaluation of the `constraint_sets` targets a Flow/Stream of one of the formats `urn:x-nmos:format:audio`, `urn:x-nmos:format:video`, `urn:x-nmos:format:data`, `urn:x-nmos:format:mux` in which the Constraint Sets do not have the `urn:x-matrox:cap:meta:format` and `urn:x-matrox:cap:meta:layer` meta attributes, or the evaluation of the `constraint_sets` targets a sub-Flow/sub-Stream of one of the formats `urn:x-nmos:format:audio`, `urn:x-nmos:format:video`, `urn:x-nmos:format:data` in which the Constraint Sets have the `urn:x-matrox:cap:meta:format` and `urn:x-matrox:cap:meta:layer` meta attributes.

When the list is empty, or none of the Constraint Sets are satisfied, the `constraint_sets` as a whole is thus not satisfied.

Several worked examples are provided in the [Examples](Examples.md) section.

## Validating Parameter Constraints and Constraint Sets

This specification includes a JSON Schema for each [Parameter Constraint Type](#parameter-constraint-types) and for Constraint Sets and the `constraint_sets` attribute as a whole, in the [APIs/schemas](../APIs/schemas) directory.

The Capabilities register in the [NMOS Parameter Registers][] and [Matrox Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md) include a supplementary schema that validates the specific requirements for every Parameter Constraint listed in the register.

## Capabilities Version

IS-04 requires that the core [resource `version`](https://specs.amwa.tv/is-04/releases/v1.3/docs/2.1._APIs_-_Common_Keys.html#version) is updated when any attributes of the `caps` object or resource as a whole are changed.

Other attributes of the Receiver resource are likely to be updated more often than `caps`, for example the `subscription` attribute is updated to reflect a new connection.
However, the capabilities of a Receiver could change over its lifetime, for example, as a result of reconfiguration by some other means.
This specification therefore defines a `version` attribute for the `caps` object itself, which reflects only when that object last changed.

## Behaviour: Receivers

In order to use the finer-grained constraints mechanism defined by this specification, Receivers MUST include both the `constraint_sets` and `version` attributes in the `caps` object.

Receivers SHOULD express their capabilities as precisely as possible, using the relevant Parameter Constraints listed in the Capabilities register in the [NMOS Parameter Registers][] and [Matrox Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md).
However, this specification may not be sufficiently expressive to indicate every type of stream or sub-Stream that a Receiver can or cannot consume successfully. It is entirely possible that a Receiver may fail to consume a stream or sub-Stream even if the Receiver's advertised Constraint Sets indicate that it can.

A Receiver SHOULD not consume a stream or sub-Stream that is incompatible with the advertised Receiver Capabilities.

The value of the `constraint_sets` attribute MUST be valid according to this specification. The value of all the Constraint Set attributes MUST be valid according to the relevant specification in the Capabilities register in the [NMOS Parameter Registers][]and [Matrox Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md).

The Receiver MUST reflect any change in its capabilities by updating the `caps` object as appropriate and modifying the [`version` attribute](#capabilities-version) of that object as well as the core resource `version`.

## Behaviour: Controllers

Controllers are strongly RECOMMENDED to support all Parameter Constraints listed in the Capabilities register in the [NMOS Parameter Registers][] and and [Matrox Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md) that are applicable for the kinds of Receiver with which they interact.
However, Controllers MAY ignore individual Parameter Constraints whose unique identifiers they do not recognize.
Some Parameter Constraints are only relevant to specific `transport` and `format` values or to particular IANA media types.
When a Controller cannot evaluate any of the Parameter Constraints in a Constraint Set, that Constraint Set SHOULD be considered to be satisfied, but the Controller MAY distinguish this case for a user.

Controllers SHOULD provide an indication to a user whether a Sender satisfies a Constraint Set of a Receiver, for example in a cross-point matrix view. Controllers MAY allow a user to attempt to make a connection to a Sender whether the Receiver's `constraint_sets` are satisfied or not.

Controllers MAY use the `version` attribute of the `caps` object to avoid unnecessary re-evaluation of Receiver capabilities.

[IS-04]: https://specs.amwa.tv/is-04/ "AMWA IS-04 NMOS Discovery and Registration Specification"

[IS-05]: https://specs.amwa.tv/is-05/ "AMWA IS-05 NMOS Device Connection Management Specification"

[JT-NM Reference Architecture]: https://jt-nm.org/reference-architecture/ "JT-NM Reference Architecture (RA) v1.0"

[NMOS Parameter Registers]: https://specs.amwa.tv/nmos-parameter-registers/ "Common parameter values for AMWA NMOS Specifications"

[RFC-2119]: https://tools.ietf.org/html/rfc2119 "Key words for use in RFCs to Indicate Requirement Levels"

[SDP]: https://tools.ietf.org/html/rfc4566 "SDP: Session Description Protocol"

  ---
  
  ***This document modifies the original document BCP-004-01 from AMWA.***
  
   Copyright 2021 AMWA

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
   
