# Matrox NMOS Extended Transport Parameters
{:.no_toc}

This document describes additional transport parameters and their permitted values which may be used in the IS-05.

{:toc}

### audio_layers_remapping, video_layers_remapping, data_layers_remapping
- **Name:** `ext_audio_layers_remapping`, `ext_video_layers_remapping`, `ext_data_layers_remapping`
- **Description:** For a Receiver, it indicates, for a given format, the sub-Stream of a multipleed stream corresponding to a Receiver's sub-Stream layer. It corresponds to a string of coma separated unsigned integers values indicating, for each layer of the Receiver, which sub-Stream of the multiplexed stream provides the essence. The length of the coma separated list is within the range of the `audio_layers`, `video_layers`, `data_layers` capabilities of the Receiver.
- **Specification:** 
- **Applicability:** AMWA IS-05 since v1.1
