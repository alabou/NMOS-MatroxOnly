# Matrox NMOS Extended Transport Parameters
{:.no_toc}

This document describes additional transport parameters and their permitted values which may be used in the IS-05.

{:toc}

### audio_layers_mapping, video_layers_mapping, data_layers_mapping
- **Name:** `ext_audio_layers_mapping`, `ext_video_layers_mapping`, `ext_data_layers_mapping`
- **Description:** For a Receiver of format `urn:x-nmos:format:mux`, it indicates, for a given format, the sub-Stream of a multiplexed stream corresponding to a Receiver's sub-Stream layer. It corresponds to a string of coma separated unsigned integer values indicating, for each layer of the Receiver, which sub-Stream of the multiplexed stream provides the essence. The length of the coma separated list must be within the min/max range of the `audio_layers`, `video_layers`, `data_layers` capabilities of the Receiver. An empty string indicates that no re-mapping is to be performed. These attributes are optional and may not be supported as transport parameters in which case no re-mapping is performed. A Controller must not specify indices of sub-Streams that are not part of the multiplexed stream.

**Example 1**
Sender multiplexed stream [v0, v1, a0, a1, a2, d0]
Sender video_layers: 2
Sender audio_layers: 3
Sender data_layers: 1

Receiver multiplexed stream [v0, v1, v2, a0, a1, a2, a3, a4, d0, d1]
Recceiver video_layers: min 1, max 3
Recceiver audio_layers: min 0, max 5
Recceiver data_layers: min 0, max 2

video_layers_mapping [a, b]   length is min(max(sender_video_layers, receiver_video_layers_min), receiver_video_layers_max)
audio_layers_mapping [d, e, f] length is min(max(sender_audio_layers, receiver_audio_layers_min), receiver_audio_layers_max)
data_layers_mapping [i] length is min(max(sender_data_layers, receiver_data_layers_min), receiver_data_layers_max)

[a,b] is a 2-shuffle of [0,1]
[d,e,f] is a 3-shuffle of [0,1,2]
[i] is 0

**Example 2**
Sender multiplexed stream [v0, v1, v2, v3, a0, a1, a2, a3, a4, a5, a6, d0, d1, d2, d3]
Sender video_layers: 4
Sender audio_layers: 7
Sender data_layers: 4

Receiver multiplexed stream [v0, v1, v2, a0, a1, a2, a3, a4, d0, d1]
Recceiver video_layers: min 1, max 3
Recceiver audio_layers: min 0, max 5
Recceiver data_layers: min 0, max 2

video_layers_mapping [a, b, c]   length is min(max(sender_video_layers, receiver_video_layers_min), receiver_video_layers_max)
audio_layers_mapping [d, e, f, g, h] length is min(max(sender_audio_layers, receiver_audio_layers_min), receiver_audio_layers_max)
data_layers_mapping [i,j] length is min(max(sender_data_layers, receiver_data_layers_min), receiver_data_layers_max)

[a,b,c] is a 3-shuffle of [0,1,2,3]
[d,e,f,g,h] is a 5-shuffle of [0,1,2,3,4,5,6]
[i,j] is a 2-shuffle of [0,1,2,3]


- **Specification:** [Matrox Receiver Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/ReceiverCapabilities.md)
- **Applicability:** AMWA IS-05 since v1.1
