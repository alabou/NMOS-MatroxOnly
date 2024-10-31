# Matrox: NMOS With IS-11
{:.no_toc}  
Copyright 2024, Matrox Graphics Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
  
---
  
{:toc}

## Introduction

The IS-11 API provides mechanisms to configure Senders for making sure that the streams transmitted over IP are compatible with the Receivers consuming them. It also provides a generic mechanism to configure Senders for controlling the parameters of the streams transmitted over IP, while still allowing a Controller to verify that Receivers are capable of consuming them. A Sender describes its capabilities and which one can be configured and to waht extents through IS-11.

The IS-11 API is available and useful for essences originating from input connectors (HDMI, SDI, AES3, etc.) and for essences originating from sensors, generators, files and other means. For essences originating from an HDMI input, IS-11 provides functions for managing the EDID given to a connected HDMI source device. For essences transmitted to an HDMI output, IS-11 provides functions for retrieving the EDID from a connected HDMI sink device. When the essence is not flowing through HDMI connectors or the device does not support the EDID functionality, the `edid_support` attribute of an input/output is false.

The IS-11 API can be used in scenarios where a Sender is configured based on a set of Receivers to be connected to the Sender. It could also be used in scenarios where a Sender is configured without considering any Receiver initially and compatibility with Receivers is verified on a per-Receiver basis without changing the already configured Sender.

Configuring a Sender with IS-11 implies defining and applying a set of active constraints to such Sender. Most IS-11 implementations require the Sender to ba inactive for applying/removing constraints. The status 423 (Locked) is returned by such implementations when attempting to apply/remove constraint for an active Sender. Matrox products mostly require an inative Sender for managing active constraints.

IS-11 constaints are based on the BCP-004-01 Receiver capabilities framework that support adding nmos and vendor capabilities and meta attributes. Current JSON schema constraint_set.json used by IS-04 and IS-11 and constraints_supported.json used by IS-11 (see https://github.com/alabou/NMOS-MatroxOnly/blob/main/Capabilities.md#updated-json-schemas) require a modificiation to align with [NMOS Capabilities](https://specs.amwa.tv/nmos-parameter-registers/branches/main/capabilities/) and allow vendor specific capabilities. 

IS-11 is compatible with fully described multiplexed Flows/Streams offered by Matrox products.

Without [Sender Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/SenderCapabilities.md) and only using [Receiver Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/ReceiverCapabilities.md) configuration through IS-11 operates on a trial-and-error basis. An NMOS Controller does not know what a Sender supports but only what it is currently doing. A Sender returns the status 422 (UnprocessableContent) when it cannot adhere to the given constraints. With Sender Capabilities an NMOS Controller knows much more about what a Sender is capable of and less likely to receive a 422 status (UnprocessableContent). As Sender Capabilities are not meant to be 100% complete and precise there still remain areas where an NMOS Controller would not know that a set of constraints is not unsupported by a given Sender.

A Sender can be strictly constrained to a very specific set of parameters, allowing only one value for each such parameters. On the contrary a Sender can be lightly constrained for a small set of parameters, allowing multiple values for such parameters. It is always possible to unconstrain a Sender by deleting the active constraints.

The IS-11 API provides `state` attribute for both IS-11 Senders and Receivers. On the Sender side the state is one of "unconstrained", "constrained", "active_constraints_violation", "no_essence", "awaiting_essence". On the Receiver side the state may is one of "unknown", "compliant_stream", "non_compliant_stream". If the `state` of a Sender becomes "active_constraints_violation" it indicates that such Sender is not capable of producing a stream that is compliant with the active constraints and unless this state is transitional, it could result in the Sender `master_enable` attribute to became false. If the `state` of a Receiver becomes "non_compliant_stream" it indicates that such Receiver detects that the stream is not compliant with the Receiver Capabilities or with internal capabilities. Unlike the Sender a Receiver is not required to become inactive if the "non_compliant_stream" state remains.

This documents presents various ways to use IS-11 with Matrox products offering the Stream Compatibility Management API.

## Use of Normative Language

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY",
and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119][RFC-2119].

## Definitions

The NMOS terms 'Controller', 'Node', 'Source', 'Flow', 'Sender', 'Receiver' are used as defined in the [NMOS Glossary](https://specs.amwa.tv/nmos/main/docs/Glossary.html).

## Receivers

Initialy a Controller MUST verify if the IS-11 API is supported for a given Receiver by a `GET` to `/x-nmos/streamcompatibility/v1.0/receivers/{receiverId}/status`. If the response status is 200 the Receiver supports the IS-11 API, otherwise it does not support the IS-11 API.

Next a Controller MUST verify if the Receiver is associated with Outputs by a `GET` to `/x-nmos/streamcompatibility/v1.0/receivers/{receiverId}/outputs`. If the response status is not 200 or the length of the response's array of string is 0 then the Receiver does not have associated Outputs. Otherwise it has a non-zero count of associated Outputs.

> Note: A receiver that is not associated with an Output could be providing the essence that is further transmitted over IP by a Sender. Such Receivers can be identified looking at the `receiver_id` attribute of the Sources in the Flow and parent Flows of a given Sender. 

### With Outputs

For Receivers associated with Outputs, a Controller MUST verify if such Outputs support the EDID feature of HDMI by a `GET` to `/x-nmos/streamcompatibility/v1.0/outputs/{outputId}/properties`. The `edid_suport` property indicates if the device supports EDID.

A Controller SHOULD use the `connected` and `status` properties to get information about the Output. The `status` takes one of "no_signal", "default_signal", "signal_present". A non-connected Output SHOULD not further be investigated. A connected Output indicates that either a) there is no signal, possibly because the Output is not able to generate a signal matching the requirements of the Output, b) there is a default signal, possibly because there is no essence from the Receiver, b) there is a signal originating from an essence.

If more than one Output is associated with a Receiver the current IS-11 API does not provide further insights about the relationship (topology) between the essence consumed by the Receiver and the Outputs. Even in the case of one Output, IS-11 does not define of the essence is composited on the Output signal or is the Output signal.

The Output resource is not part of the Registry. A controller MAY observe changes of the Output resource through the associated Device resource `version` attribute and then do a `GET` to `/x-nmos/streamcompatibility/v1.0/outputs/{outputId}/properties` or `/x-nmos/streamcompatibility/v1.0/outputs/{outputId}/edid`.

A Device SHOULD use descriptive labels on the Output resources to associate a physical connector with the Output.

#### With EDID

If a connected Output supports EDID and such Output is the only one associated with a Receiver, a Controller SHOULD get the EDID of the monitor by a `GET` to `/x-nmos/streamcompatibility/v1.0/outputs/{outputId}/edid`. If multiple Outputs are associated with a Receiver, a Controller with insights on the topology MAY get the EDID of each monitor and through an unspecified process, obtain an EDID representative of the topology of the Outputs.

### Capabilities

Receivers express their capabilities using the formalism of [BCP-004-01][]. Matrox products implement an enhanced version of the [Receiver Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/ReceiverCapabilities.md) which is a backward compatible extension of [BCP-004-01][].

The capabilities of a Receiver MAY change as a result of a configuration change from vendor specific methods, internal resources usage and various other vendor specific reasons. A Controller SHOULD monitor the `version` and `caps.version` attributes of Receivers resources in the Registry to assess if the Receiver capabilities have changed and then re-evaluate the Receiver state based on the latest information.

For a Receiver with HDMI Outputs supporting EDID, the information from the EDID of the device connected to the HDMI Output MAY influence the capabilities of the Receiver. For example a connected monitor suporting a maximum resolution of 1080p could change the maximum resolution supported by the associated Receiver to max 1080p. 

## Senders

Initialy a Controller MUST verify if the IS-11 API is supported for a given Sender by a `GET` to `/x-nmos/streamcompatibility/v1.0/senders/{senderId}/status`. If the response status is 200 the Sender supports the IS-11 API, otherwise it does not support the IS-11 API.

Next a Controller MUST verify if the Sender is associated with Inputs by a `GET` to `/x-nmos/streamcompatibility/v1.0/senders/{senderId}/inputs`. If the response status is not 200 or the length of the response's array of string is 0 then the Sender does not have associated Inputs. Otherwise it has a non-zero count of associated Inputs.

An IS-11 Sender has a `state` attribute that takes one of "unconstrained", "constrained", "active_constraints_violation", "no_essence", "awaiting_essence" values. The "awaiting_essence" state is a transitional state that will not persist. When a Sender is constrained by a new set of active constraints or when a new base EDID is set on an associated Input, it is expected that the Sender `state` may transition among the various possibilities until settling to a state. A controller SHOULD allow the state to settle before considering it as stable. A Controller SHOULD first wait for a change of the Sender's resource `version` and then verify the IS-11 Sender's `state`. For Senders associated with HDMI Inputs, the state of an Input and the associated Sender MAY require more time to settle as a new EDID is to be produced for the connected HDMI device that will then adapt its signal to the new EDID information.

### With Inputs

For Senders associated with Inputs, a Controller MUST verify if such Inputs support the EDID feature of HDMI by a `GET` to `/x-nmos/streamcompatibility/v1.0/inputs/{inputId}/properties`. The `edid_suport` property indicates if the device supports EDID.

A Controller SHOULD use the `connected` and `status` properties to get information about the Input. The `status` takes one of "no_signal", "awaiting_signal", "signal_present". A non-connected Input SHOULD not further be investigated. A connected Input indicates that either a) there is no signal, possibly because the Input is not connected or the signal is corrupted or out-of-specifications, b) the acquisition of the signal is in progress, b) there is a signal originating from the connected device. A Controller SHOULD get the state of the Sender by a `GET` to `/x-nmos/streamcompatibility/v1.0/senders/{senderId}/status` which takes one of "unconstrained", "constrained", "active_constraints_violation", "no_essence", "awaiting_essence". If the Sender `status` is none of "no_essence", "awaiting_essence" and the Input is not connected or the Input `status` is not "signal_present", it indicates that a default essence is produced by the Input as a substitute to an essence from a connected device.

If more than one Input is associated with a Sender the current IS-11 API does not provide further insights about the relationship (topology) between the essence produced by the Sender and the Inputs. Even in the case of one Input, IS-11 does not define of the essence is composited on the Sender stream or is the Sender stream.

The Input resource is not part of the Registry. A controller MAY observe changes of the Input resource through the associated Device resource `version` attribute and then do a `GET` to `/x-nmos/streamcompatibility/v1.0/inputs/{inputId}/properties`.

A Device SHOULD use descriptive labels on the Input resources to associate a physical connector with the Input.

#### With EDID

If a connected Input supports EDID and such Input is the only one associated with a Sender and the Input property `base_edid_support` is true, a Controller SHOULD provide an EDID from at least one Receiver to the Input by a `PUT` to `/x-nmos/streamcompatibility/v1.0/inputs/{inputId}/edid/base`. If multiple Inuts are associated with a Sender, a Controller with insights on the topology MAY through an unspecified process, obtain an EDID representative of the topology for each such Input.

> If the Input property `adjust_to_caps` is present and true, the EDID `PUT` to `/x-nmos/streamcompatibility/v1.0/inputs/{inputId}/edid/base` MAY be modified by the device prior to be used as the Input Base EDID.

### Capabilities

Senders express their capabilities using the formalism of [BCP-004-01][]. Matrox products implement an enhanced version of the [Sender Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/SenderCapabilities.md) which is a backward compatible extension of [BCP-004-01][]. Matrox products implement Sender capabilities in addition to the usual Receiver capabilities. Using Sender capabilities allows Matrox products to express to which extents a Sender can be configured and what Flows can be produced by the Sender.

The capabilities of a Sender MAY change as a result of a configuration change from vendor specific methods, internal resources usage and various other vendor specific reasons. A Controller SHOULD monitor the `version` and `caps.version` attributes of Senders resources in the Registry to assess if the Sender capabilities have changed and then re-evaluate the Sender state based on the latest information.

Sender capabilities SHOULD NOT change when a Sender is active (active `master_enable` is true) as this could make the active constraints invalid and/or the current Flow/sub-Flows non-compliant.

### Active Constraints

The active constraints applied to a Sender MUST be within the capabilities of the Sender and a Sender SHOULD return a 422 (UnprocessableEntity) response status. Constraints cannot enhance the Sender capabilities.

If the Sender capabilities change while there are active constraints, the Sender MUST only consider the intersection the new Sender capabilities with the active constraints, ignoring the space of active constraints outside the new Sender capabilities.

### Propagating the preferred capabilities

For a Sender associated with an Input, the application of active constraints to a Sender propagate to the EDID of the Input as a preferred mode, indicating to the connected HDMI device the preferred mode for the HDMI signal. The device processes the active constraints and extract a preferred mode from them. If the constraints are strict then the resulting preferred mode is obvious. Otherwise it is up to the device to produce a preferred mode out of the various possibilities. The propagation of a preferred mode to the EDID MUST be performed such that it is within the capabilities of the effective EDID.

For a Sender that is not associated with an Input but instead is associated with a Receiver, the application of active constraints to a Sender propagate to the capabilities of the Receiver as a preferred constraint set for the Stream or sub-Streams, indicating to a Controller the preferred constraint set for the Stream and sub-Streams. The device processes the active constraints and extract a preffered constraint set from them. If the constraints are strict then the resulting preferred constraint set is obvious. Otherwise it is up to the device to produce a preferred constraint set out of the various possibilities. The propagation of a preferred constraint set to the Receiver MUST be performed such that it is within the capabilities of the Receiver.

## Peer-to-Peer HDMI use-case

In this use-case there is one Receiver producing an HDMI output, such Receiver is connected to a Sender capturing an HDMI input. In order to have the device connected to the HDMI input associated with the Sender behave as if it is directly connected through HDMI to the device connected to the HDMI output associated with the Receiver, a Controller MUST get the EDID from the Receiver's Output and put it as the Sender's Input base EDID.

Assuming the Sender has no active constraints, it is free to stream the essence from the device connected to the HDMI Input in any way it wants. The base EDID from the Output MUST be provided to the connected HDMI device, which is not absolutely required to use the preferred mode from the EDID, but a mode from all the modes expressed in the EDID. Even if the device connected to the HDMI Input produces a signal matching the preferred mode of the EDID, the Sender is still free to process/convert such signal in anyway it wants. It is only under IS-11 active constraints that a Sender is required to follow the constraints. The Sender device MAY have vendor specific configuration settings that force a particular behavior such as to follow the HDMI input signal or produce a stream with a fixed parameters.

With IS-11 it is not possible to contrain a Sender to produce a stream that precisely match the input signal. A vendor SHOULD offer such "follow input" configuration in order to enable the peer-to-peer use-case. A Sender with the Input property `adjust_to_caps` present and true MAY modify the base EDID to match the internal constraints of the device even if there are IS-1 active constraints applied to the Sender. Those edits SHOULD be minimal to truly allow the peer-to-peer use-case.

## Static streaming parameters

In this use-case a Controller set a fixed format for the streams produced by a Sender, requiring the Sender to convert the source essences to the fixed format. It implies, as a minimum, setting active constraints allowing a single value for all of the existing `urn:cap:format:` capabilities. In other words, all the format parameters associated with a Flow/Stream and sub-Flow/sub-Stream are not allowed to change.

When active constraints are set for a given Sender, the IS-11 API MAY respond with a 422 status (UnprocessableEntity) if it is not capable of producing a stream compliant with the specified set of constaints. If the IS-11 API respond with a 200 status (Ok), the Sender is required to either produce a stream compliant with the applied constraints or stop streaming and become inactive with `master_enable` becoming false and its state becoming "active_constraints_violation".

Using IS-11 active constraints, a Controller get either a compliant stream or nothing (no streaming at all). An IS-11 implementation SHOULD minimize the possibilities causing the streaming to stop and reaching the "active_constraints_violation" state. It is understood that it is not possible in some scenarios for a device to provide 100% assurance that it will always be able to produce a compliant stream independently of the essences consumed from the associated Inputs or Receivers. A device MAY, instead of stopping the streaming, produce a default compliant stream that would alert the user that the Sender is unable to comply with the active constraints.

## N-to-1 new-configured use-case

In this use-case a Sender is inactive and a Controller is processign the connection of a number of Receivers to the Sender. The Controller SHOULD get the  capabilities of all such Receivers and intersect them. The intersection of the Receivers provides the capabilities that are common to all the Receivers. Such intersection is then further itersected with the Sender capabilities (if any), resulting in the capabilities that can be achieved with this Sender. The resulting intersection with the Sender MAY be programmed as the Sender's active constraints, making sure that the Sender produces streams/sub-Streams that are compliant with all the Receivers. The Controller MAY select any subset of constraints within the intersection with the Sender and still obtain compliant Streams/sub-Streams.

An interesting approach for a Controller is to first present to a User the intersection of the capabilities of all the Receivers and then provide a list of Senders that are capable of operating within those constraints. Once the User selects a specific Sender, the Controller performs the intersection with the Sender and presents the resulting capability sets to the User which then selects a configuration within all those possibles that satisfies both the Sender and all the Receivers capabilities.

Once the Controller observes that the Sender `state` is "constrained", the Controller MAY activate the Sender and then all the Receivers.

## N-to-1 pre-configured use-case

In this use-case the Sender is active and has been constrained prior to being activated and a Controller is processign the connection of a current Receiver to the Sender. As the Sender is already active, the Controller can only assess if the Receiver is capable of consuming the streams/sub-Streams from the Sender. Otherwise the controller SHOULD inform the User that the Receiver is not capable of consuming the Streams/sub-Steams the Sender is currently producing.

The Controller SHOULD intersect Receiver capabilities with the Sender capabilities and further intersect the result with the Sender active constraints. The resulting intersection provides the capabilities that can be achieved with this active Sender. If the intersection is empty the Receiver cannot consume the Sender's Stream/sub-Streams based on the Sender capabilities and active constraints. In this case a Controller SHOULD perform an additional compliance verification using the Sender's Flows and sub-Flows attributes. As Sender capabilities are not required to be 100% complete and precise, doing this last verification with the actual state of the Sender could prove the Receiver to be capable of consuming the Streams/sub-Streams currently produces by a Sender.

If the Receiver cannot connect to the Sender, an interesting approach for a Controller is to intersect the Receiver capabilities with the Sender capabilities and present the intersection to the User. The resulting capabilities are those that would allow the Streams/sub-Streams from the Sender to be compliant with the actual Receiver.

> Note: An implementation of IS-11 that would support narrowing the active constraints of an active Sende could make sure that a Receiver compliant with the current Flow/sub-Flows would remain compliant with the narrowed active constaints.

> Note: The active constraints of a Sender could no longer be within the capabilities of the Sender if such Sender capabilities changed after the active constraints have been applied.

## Without Sender Capabilities

Without IS-11 and without Sender Capabilities, a Controller uses the current Flow attributes of an active Sender and the associated SDP transport file parameters to verify the compliance of the stream from a Sender with Receivers. A Controller observes the actual Flow of a Sender but it does not know what other Flows the Sender could be streaming and what else the Sender could do.

With IS-11 but without Sender Capabilities, a Controller operates on a trial-and-error basis, applying active constraints to a Sender and checking the response status and the Sender `state`. If the response status is 422 (UnprocessableEntity) or the Sender's `state` becomes "active_constraints_violation", the Controller modifies the active constraint and try again. With the exception of very simple cases this become unmanageable.

## With Sender Capabilities

With IS-11 and Sender Capabilities, a Controller uses the Sender capabilities along with the active constraints to verify the compliance of Receivers with Sender streams. In this use-case a Sender could respond with a 422 status (UnprocessableEntity) or with a `state` becoming  "active_constraints_violation" due to the fact that capabilities are not 100% complete and fully precise, only for complex and uncommon active constraints.

For example, with Sender capabilities a controller would know that a Sender may produce an H.264, H.265 or JPEG-XS coded stream. If only looking at the current Flow such Controller would only know that currently the Sender is producing a JPEG-XS stream.

## Advanced sub-Flow constaints

[BCP-004-01][] provides a framework to describe the capabilities of a Receiver regarding the Streams it can consume. If the Receiver is of format `video`, the capabilities relate to a video stream. If the Receiver is of format `audio`, the capabilities relate to an audio stream. If the Receiver is of format `data`, the capabilities relate to a data stream. Finaly if the Receiver is of format `mux`, the capabilities relate to a mux stream which excludes the content of the mux stream.

Matrox extended [Receiver Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/ReceiverCapabilities.md) and [Sender Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/SenderCapabilities.md) are backward compatible with [BCP-004-01][] while adding support for fully described multiplexed streams.

### Backward compatibility

The `media_types` array of a Receiver `caps` attribue contains allowed media types for the Receiver format. A Receiver of format `mux` would list a number of mux media types. For backward compatibility the `media_types` array MUST NOT list non-mux media types. The constraint sets for the mux sub-Streams MUST have a `media_type` capability with values that are not in the `media_types` array. It results that constraint sets related to sub-Streams are automatically rejected by a Controller evaluationg the Receiver capabilities because their `media_type` capability is not within the `media_types` array.

### Natural Groups

Let consider a non-multiplexed scenarios where a one video, two audio and one data streams are transmitted in parallel by 4 Senders using the RTP transport. Each Sender is associated with a grouphint tag providing the `<group-name> <group-index>:<role-in-group> <role-index>` information as per [NMOS with Natural Groups](https://github.com/alabou/NMOS-MatroxOnly/blob/main/NMOS%20With%20Natural%20Groups.md). For our current example the video stream would be tagged as "RTP 0:VIDEO 0", the two audio streams would be tagged as "RTP 0:AUDIO 0" and "RTP 0:AUDIO 1" and the data stream would be tagged as "RTP 0:DATA 0".

### Formats and Layers

The natural group's `<role-in-group>` value, as illustrated before, corresponds to the `format` of a Flow/Stream. So instead of using the concept of `<role-index` we use the concept of `layer`. A Sender grouphint "RTP 0:AUDIO 0" becomes "format: urn:x-nmos:format:audio, layer: 0". The objective is to identify a sub-Flow/sub-Stream with a (format, layer) pair. As a Flow already has a `format` attribute, a new `layer` attribute is added to a Flow such that it can be properly identified, as was the case for the separate Senders of the example above.

In order to associate capabilities to a specific sub-Flow/sub-Stream, the meta attributes `urn:x-matrox:cap:meta:format` and `urn:x-matrox:cap:meta:layer` are added to a constraint set. A constraint set without those meta attributes is associated with a mux Flow/Stream or a non-multiplexed audio, video or data stream. A `urn:x-matrox:cap:meta:layer` attribute is also available on a Source in order to associate it with a sub-Stream of a Receiver.

Now let consider a multiplexed MPEG2-TS scenarios where a one video, two audio and one data streams are multiplexed and transmitted by 1 Sender using the RTP transport. The Sender is associated with a grouphint tag "RTP 0:MUX 0". The Flow associated with the Sender is of format `urn:x-nmos:format:mux` and has 4 parents Flows (a one video, two audio and one data Flows). For our current example the video Flow would be tagged as "format: urn:x-nmos:format:video, layer: 0", the two audio Flows would be tagged as "format: urn:x-nmos:format:audio, layer: 0" and "format: urn:x-nmos:format:audio, layer: 1" and the data Flow would be tagged as "format: urn:x-nmos:format:data, layer: 0". The constaint sets of the Sender and Receiver Capabilities would also be tagged accordingly. The constraints sets of the Sender's active constraints would also be tagged accordingly.

To obtain the constraint sets corresponding to a specific (format, layer) it is very easy to filter the constraint sets, keeping only those matching the required format and layer or absence of such. It is similarly easy to filter the constraint set for those associated with the mux or non-multiplexed audio, video and data streams, which are those not having the `urn:x-matrox:cap:meta:format` and `urn:x-matrox:cap:meta:layer` meta attributes.

### Compatibility Groups

In complex scenarios it becomes necessary to describe that some capabilities are compatible among themselves but incompatible with other capabilities. Let take as an example a mux where you could either send a) RAW video and PCM audio or b) HEVC video and AAC audio. Without compatibility groups the evaluation of the capabilities could not resolve that only a) and b) are possible and that a Receiver is not capable of consuming a mux stream having RAW video and AAC audio.

A new Flow attribute `urn:x-matrox:layer_compatibility_groups` and associated meta attribute `urn:x-matrox:cap:meta:layer_compatibility_groups` are added to the model and allow indicating in which, out of a maximum of 64, the Flow and constraint set are members. For a given mux Flow, the intersection of the `urn:x-matrox:layer_compatibility_groups` attribue of the Flow and all the parent Flows MUST NOT be empty as otherwise it would indicate an invalid configuration. Similarly the intersection of the `urn:x-matrox:cap:meta:layer_compatibility_groups` meta attribtue of all the constaint sets of the active constraints of a Sender MUST not be empty.

When a Controller presents the capabilities of a Receiver or Sender to a User, it is appropriate to filter the constraint sets based on a given compatibility group. For a User the compatibility groups represent various alternatives of what a Receiver or Sender support.

Although the `urn:x-matrox:layer_compatibility_groups` and `urn:x-matrox:cap:meta:layer_compatibility_groups` attributes has the word `layer` in their name, they also apply to mux constraints sets and Flows. This allows for a Receiver of format `urn:x-nmos:format:mux` to support multiple flavor of muxes of various media types, each possibly having dedicated constraint sets.


[RFC-2119]: https://tools.ietf.org/html/rfc2119 "Key words for use in RFCs"
[IS-11]: https://specs.amwa.tv/is-11/ "AMWA IS-11 NMOS Stream Compatibility Management"
[BCP-004-01]: https://specs.amwa.tv/bcp-004-01/ "AMWA BCP-004-01 NMOS Receiver Capabilities"
