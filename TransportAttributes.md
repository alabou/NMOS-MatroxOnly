# Matrox NMOS Extended Transport Parameters
{:.no_toc}

This document describes additional transport parameters and their permitted values which may be used in the IS-05.

{:toc}

### audio_layers_mapping, video_layers_mapping, data_layers_mapping
- **Name:** `ext_audio_layers_mapping`, `ext_video_layers_mapping`, `ext_data_layers_mapping`
- **Description:** For a Receiver of format `urn:x-nmos:format:mux`, it indicates, for a given format, the sub-Stream of a multipleed stream corresponding to a Receiver's sub-Stream layer. It corresponds to a string of coma separated unsigned integers values indicating, for each layer of the Receiver, which sub-Stream of the multiplexed stream provides the essence. The length of the coma separated list is within the range of the `audio_layers`, `video_layers`, `data_layers` capabilities of the Receiver. An empty string indicates that no re-mapping is to be performed.
- **Specification:** [Matrox Receiver Capabilities](https://github.com/alabou/NMOS-MatroxOnly/blob/main/ReceiverCapabilities.md)
- **Applicability:** AMWA IS-05 since v1.1
