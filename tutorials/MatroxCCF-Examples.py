import re
import json
from  MatroxCCF import *

ndi_sender = '''
{
    "id": "00000000-0202-4000-ab00-4d5458005056",
    "version": "1730486252:892492983",
    "label": "Net Stream NDI 0",
    "description": "This is the Net Stream NDI 0",
    "tags": {
        "urn:x-nmos:tag:grouphint/v1.0": [
            "NDI 0:MUX 0"
        ],
        "urn:x-nmos:tag:transport:ndi:group": [
            "Public"
        ]
    },
    "flow_id": "5530f937-0404-4000-ab00-4d5458005056",
    "transport": "urn:x-matrox:transport:ndi",
    "device_id": "00000000-0100-4000-ab00-4d5458005056",
    "manifest_href": "http://127.0.0.1:5056/x-nmos/connection/v1.1/single/senders/00000000-0202-4000-ab00-4d5458005056/transportfile",
    "interface_bindings": [
        "lo"
    ],
    "subscription": {
        "receiver_id": null,
        "active": true
    },
    "caps": {
        "version": "1730485958:301503984",
        "constraint_sets": [
            {
                "urn:x-nmos:cap:meta:label": "Native Mux constraints",
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 100,
                "urn:x-matrox:cap:format:audio_layers": {
                    "minimum": 1,
                    "maximum": 1
                },
                "urn:x-matrox:cap:format:data_layers": {
                    "minimum": 0,
                    "maximum": 0
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "application/ndi"
                    ]
                },
                "urn:x-matrox:cap:format:video_layers": {
                    "minimum": 1,
                    "maximum": 1
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "Native Video sub-constraints",
                "urn:x-matrox:cap:meta:format": "urn:x-nmos:format:video",
                "urn:x-matrox:cap:meta:layer": 0,
                "urn:x-matrox:cap:meta:layer_compatibility_groups": [
                    1
                ],
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 100,
                "urn:x-nmos:cap:format:frame_width": {
                    "enum": [
                        1920
                    ]
                },
                "urn:x-nmos:cap:format:frame_height": {
                    "enum": [
                        1080
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "4.1"
                    ]
                },
                "urn:x-nmos:cap:format:interlace_mode": {
                    "enum": [
                        "progressive"
                    ]
                },
                "urn:x-nmos:cap:format:colorspace": {
                    "enum": [
                        "BT709"
                    ]
                },
                "urn:x-nmos:cap:format:transfer_characteristic": {
                    "enum": [
                        "SDR"
                    ]
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "video/H264"
                    ]
                },
                "urn:x-nmos:cap:format:color_sampling": {
                    "enum": [
                        "YCbCr-4:2:0"
                    ]
                },
                "urn:x-nmos:cap:format:component_depth": {
                    "enum": [
                        8
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "High"
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "enum": [
                        40000
                    ]
                },
                "urn:x-nmos:cap:format:grain_rate": {
                    "enum": [
                        {
                            "numerator": 60,
                            "denominator": 1
                        }
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "Native Audio sub-constraints",
                "urn:x-matrox:cap:meta:format": "urn:x-nmos:format:audio",
                "urn:x-matrox:cap:meta:layer": 0,
                "urn:x-matrox:cap:meta:layer_compatibility_groups": [
                    1
                ],
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 100,
                "urn:x-nmos:cap:format:sample_rate": {
                    "enum": [
                        {
                            "numerator": 48000,
                            "denominator": 1
                        }
                    ]
                },
                "urn:x-nmos:cap:format:channel_count": {
                    "enum": [
                        2
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "AAC"
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "2"
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "enum": [
                        128
                    ]
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        true
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "audio/mpeg4-generic"
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "Mux constraints",
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 1,
                "urn:x-matrox:cap:format:data_layers": {
                    "minimum": 0,
                    "maximum": 0
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "application/ndi"
                    ]
                },
                "urn:x-matrox:cap:format:video_layers": {
                    "minimum": 1,
                    "maximum": 1
                },
                "urn:x-matrox:cap:format:audio_layers": {
                    "minimum": 0,
                    "maximum": 1
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "H.264 sub-constraints",
                "urn:x-matrox:cap:meta:format": "urn:x-nmos:format:video",
                "urn:x-matrox:cap:meta:layer": 0,
                "urn:x-matrox:cap:meta:layer_compatibility_groups": [
                    1
                ],
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 1,
                "urn:x-nmos:cap:format:frame_width": {
                    "enum": [
                        640,
                        1280,
                        1920
                    ]
                },
                "urn:x-nmos:cap:format:color_sampling": {
                    "enum": [
                        "YCbCr-4:2:0"
                    ]
                },
                "urn:x-nmos:cap:format:interlace_mode": {
                    "enum": [
                        "progressive"
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "minimum": 30000,
                    "maximum": 2400000
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false,
                        true
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "3",
                        "3.1",
                        "3.2",
                        "4",
                        "4.1",
                        "4.2",
                        "5",
                        "5.1",
                        "5.2",
                        "6",
                        "6.1",
                        "6.2"
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "video/H264"
                    ]
                },
                "urn:x-nmos:cap:format:frame_height": {
                    "enum": [
                        360,
                        720,
                        1080
                    ]
                },
                "urn:x-nmos:cap:format:colorspace": {
                    "enum": [
                        "BT709",
                        "BT2020"
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "High10",
                        "High10Intra"
                    ]
                },
                "urn:x-nmos:cap:format:grain_rate": {
                    "enum": [
                        {
                            "numerator": 24,
                            "denominator": 1
                        },
                        {
                            "numerator": 60,
                            "denominator": 1
                        },
                        {
                            "numerator": 6000,
                            "denominator": 1001
                        },
                        {
                            "numerator": 30,
                            "denominator": 1
                        },
                        {
                            "numerator": 3000,
                            "denominator": 1001
                        }
                    ]
                },
                "urn:x-nmos:cap:format:transfer_characteristic": {
                    "enum": [
                        "SDR"
                    ]
                },
                "urn:x-nmos:cap:format:component_depth": {
                    "enum": [
                        8
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "AAC stereo sub-constraints",
                "urn:x-matrox:cap:meta:format": "urn:x-nmos:format:audio",
                "urn:x-matrox:cap:meta:layer": 0,
                "urn:x-matrox:cap:meta:layer_compatibility_groups": [
                    1
                ],
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 1,
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "Main",
                        "Natural",
                        "LowDelayAAC",
                        "LowDelayAACv2"
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "1"
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "maximum": 576
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false,
                        true
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "audio/mpeg4-generic"
                    ]
                },
                "urn:x-nmos:cap:format:sample_rate": {
                    "enum": [
                        {
                            "numerator": 48000,
                            "denominator": 1
                        }
                    ]
                },
                "urn:x-nmos:cap:format:channel_count": {
                    "enum": [
                        2
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "H.265 sub-constraints",
                "urn:x-matrox:cap:meta:format": "urn:x-nmos:format:video",
                "urn:x-matrox:cap:meta:layer": 0,
                "urn:x-matrox:cap:meta:layer_compatibility_groups": [
                    1
                ],
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 0,
                "urn:x-nmos:cap:format:component_depth": {
                    "enum": [
                        8,
                        10
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "minimum": 6000,
                    "maximum": 4000000
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false,
                        true
                    ]
                },
                "urn:x-nmos:cap:format:interlace_mode": {
                    "enum": [
                        "progressive"
                    ]
                },
                "urn:x-nmos:cap:format:frame_width": {
                    "enum": [
                        640,
                        1280,
                        1920
                    ]
                },
                "urn:x-nmos:cap:format:transfer_characteristic": {
                    "enum": [
                        "SDR"
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "video/H265"
                    ]
                },
                "urn:x-nmos:cap:format:frame_height": {
                    "enum": [
                        360,
                        720,
                        1080
                    ]
                },
                "urn:x-nmos:cap:format:color_sampling": {
                    "enum": [
                        "YCbCr-4:2:0",
                        "YCbCr-4:4:4"
                    ]
                },
                "urn:x-nmos:cap:format:grain_rate": {
                    "enum": [
                        {
                            "numerator": 24,
                            "denominator": 1
                        },
                        {
                            "numerator": 60,
                            "denominator": 1
                        },
                        {
                            "numerator": 6000,
                            "denominator": 1001
                        },
                        {
                            "numerator": 30,
                            "denominator": 1
                        },
                        {
                            "numerator": 3000,
                            "denominator": 1001
                        }
                    ]
                },
                "urn:x-nmos:cap:format:colorspace": {
                    "enum": [
                        "BT709",
                        "BT2020"
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "Main10",
                        "Main10-444",
                        "Main10Intra",
                        "Main10Intra-444"
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "Main-3",
                        "Main-3.1",
                        "Main-4",
                        "High-4",
                        "Main-4.1",
                        "High-4.1",
                        "Main-5",
                        "High-5",
                        "Main-5.1",
                        "High-5.1",
                        "Main-5.2",
                        "High-5.2",
                        "Main-6",
                        "High-6",
                        "Main-6.1",
                        "High-6.1",
                        "Main-6.2",
                        "High-6.2"
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "RAW sub-constraints",
                "urn:x-matrox:cap:meta:format": "urn:x-nmos:format:video",
                "urn:x-matrox:cap:meta:layer": 0,
                "urn:x-matrox:cap:meta:layer_compatibility_groups": [
                    0
                ],
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 0,
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "video/raw"
                    ]
                },
                "urn:x-nmos:cap:format:grain_rate": {
                    "enum": [
                        {
                            "numerator": 24,
                            "denominator": 1
                        },
                        {
                            "numerator": 30,
                            "denominator": 1
                        },
                        {
                            "numerator": 3000,
                            "denominator": 1001
                        },
                        {
                            "numerator": 60,
                            "denominator": 1
                        },
                        {
                            "numerator": 6000,
                            "denominator": 1001
                        }
                    ]
                },
                "urn:x-nmos:cap:format:frame_width": {
                    "enum": [
                        720,
                        1280,
                        1920,
                        3840
                    ]
                },
                "urn:x-nmos:cap:format:frame_height": {
                    "enum": [
                        480,
                        720,
                        1080,
                        2160
                    ]
                },
                "urn:x-nmos:cap:format:transfer_characteristic": {
                    "enum": [
                        "SDR"
                    ]
                },
                "urn:x-nmos:cap:format:colorspace": {
                    "enum": [
                        "BT601",
                        "BT709",
                        "BT2020"
                    ]
                },
                "urn:x-nmos:cap:format:color_sampling": {
                    "enum": [
                        "YCbCr-4:2:2"
                    ]
                },
                "urn:x-nmos:cap:format:component_depth": {
                    "enum": [
                        8
                    ]
                },
                "urn:x-nmos:cap:format:interlace_mode": {
                    "enum": [
                        "progressive"
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "AAC multi-channels sub-constraints",
                "urn:x-matrox:cap:meta:format": "urn:x-nmos:format:audio",
                "urn:x-matrox:cap:meta:layer": 0,
                "urn:x-matrox:cap:meta:layer_compatibility_groups": [
                    1
                ],
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 0,
                "urn:x-nmos:cap:format:channel_count": {
                    "enum": [
                        2,
                        6
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "HighQuality",
                        "AAC",
                        "HighEfficiencyAAC",
                        "HighEfficiencyAACv2"
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "4"
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "maximum": 1728
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false,
                        true
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "audio/mpeg4-generic"
                    ]
                },
                "urn:x-nmos:cap:format:sample_rate": {
                    "enum": [
                        {
                            "numerator": 48000,
                            "denominator": 1
                        }
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "PCM sub-constraints",
                "urn:x-matrox:cap:meta:format": "urn:x-nmos:format:audio",
                "urn:x-matrox:cap:meta:layer": 0,
                "urn:x-matrox:cap:meta:layer_compatibility_groups": [
                    0
                ],
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 0,
                "urn:x-nmos:cap:format:sample_depth": {
                    "enum": [
                        16,
                        24
                    ]
                },
                "urn:x-nmos:cap:format:sample_rate": {
                    "enum": [
                        {
                            "numerator": 48000,
                            "denominator": 1
                        }
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "audio/L16",
                        "audio/L24"
                    ]
                },
                "urn:x-nmos:cap:format:channel_count": {
                    "enum": [
                        2,
                        6,
                        8
                    ]
                }
            }
        ]
    }
}
'''

mp2t_sender = '''
{
    "id": "00000000-0203-4000-ab00-4d5458005057",
    "version": "1730324051:669490368",
    "label": "Net Stream MPEG2-TS 0",
    "description": "This is the Net Stream MPEG2-TS 0",
    "tags": {
        "urn:x-nmos:tag:grouphint/v1.0": [
            "RTP 0:MUX 0"
        ]
    },
    "flow_id": "6550e13d-0406-4000-ab00-4d5458005057",
    "transport": "urn:x-nmos:transport:rtp.mcast",
    "device_id": "00000000-0100-4000-ab00-4d5458005057",
    "manifest_href": null,
    "interface_bindings": [
        "lo"
    ],
    "subscription": {
        "receiver_id": null,
        "active": false
    },
    "caps": {
        "version": "1730227257:141302953",
        "constraint_sets": [
            {
                "urn:x-nmos:cap:meta:label": "Native Audio sub-constraints",
                "urn:x-matrox:cap:meta:format": "urn:x-nmos:format:audio",
                "urn:x-matrox:cap:meta:layer": 1,
                "urn:x-matrox:cap:meta:layer_compatibility_groups": [
                    0
                ],
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 100,
                "urn:x-nmos:cap:format:bit_rate": {
                    "enum": [
                        128
                    ]
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        true
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "audio/MP4A-ADTS"
                    ]
                },
                "urn:x-nmos:cap:format:sample_rate": {
                    "enum": [
                        {
                            "numerator": 48000,
                            "denominator": 1
                        }
                    ]
                },
                "urn:x-nmos:cap:format:channel_count": {
                    "enum": [
                        2
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "AAC"
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "2"
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "Native Mux constraints",
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 100,
                "urn:x-matrox:cap:format:video_layers": {
                    "minimum": 1,
                    "maximum": 1
                },
                "urn:x-matrox:cap:format:audio_layers": {
                    "minimum": 2,
                    "maximum": 2
                },
                "urn:x-matrox:cap:format:data_layers": {
                    "minimum": 0,
                    "maximum": 0
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "application/MP2T"
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "Native Video sub-constraints",
                "urn:x-matrox:cap:meta:format": "urn:x-nmos:format:video",
                "urn:x-matrox:cap:meta:layer": 0,
                "urn:x-matrox:cap:meta:layer_compatibility_groups": [
                    0
                ],
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 100,
                "urn:x-nmos:cap:format:frame_width": {
                    "enum": [
                        1920
                    ]
                },
                "urn:x-nmos:cap:format:color_sampling": {
                    "enum": [
                        "YCbCr-4:2:2"
                    ]
                },
                "urn:x-nmos:cap:format:frame_height": {
                    "enum": [
                        1080
                    ]
                },
                "urn:x-nmos:cap:format:transfer_characteristic": {
                    "enum": [
                        "SDR"
                    ]
                },
                "urn:x-nmos:cap:format:component_depth": {
                    "enum": [
                        10
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "4"
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "High-422"
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "enum": [
                        40000
                    ]
                },
                "urn:x-nmos:cap:format:interlace_mode": {
                    "enum": [
                        "progressive"
                    ]
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "video/H264"
                    ]
                },
                "urn:x-nmos:cap:format:colorspace": {
                    "enum": [
                        "BT709"
                    ]
                },
                "urn:x-nmos:cap:format:grain_rate": {
                    "enum": [
                        {
                            "numerator": 60,
                            "denominator": 1
                        }
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "Native Audio sub-constraints",
                "urn:x-matrox:cap:meta:format": "urn:x-nmos:format:audio",
                "urn:x-matrox:cap:meta:layer": 0,
                "urn:x-matrox:cap:meta:layer_compatibility_groups": [
                    0
                ],
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 100,
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "audio/MP4A-ADTS"
                    ]
                },
                "urn:x-nmos:cap:format:sample_rate": {
                    "enum": [
                        {
                            "numerator": 48000,
                            "denominator": 1
                        }
                    ]
                },
                "urn:x-nmos:cap:format:channel_count": {
                    "enum": [
                        2
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "AAC"
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "2"
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "enum": [
                        128
                    ]
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        true
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "AAC multi-channels sub-constraints",
                "urn:x-matrox:cap:meta:format": "urn:x-nmos:format:audio",
                "urn:x-matrox:cap:meta:layer": 0,
                "urn:x-matrox:cap:meta:layer_compatibility_groups": [
                    0
                ],
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 1,
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "4"
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "maximum": 1728
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false,
                        true
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "audio/MP4A-ADTS"
                    ]
                },
                "urn:x-nmos:cap:format:sample_rate": {
                    "enum": [
                        {
                            "numerator": 48000,
                            "denominator": 1
                        }
                    ]
                },
                "urn:x-nmos:cap:format:channel_count": {
                    "enum": [
                        2,
                        6
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "HighQuality",
                        "AAC",
                        "HighEfficiencyAAC",
                        "HighEfficiencyAACv2"
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "H.264 sub-constraints",
                "urn:x-matrox:cap:meta:format": "urn:x-nmos:format:video",
                "urn:x-matrox:cap:meta:layer": 0,
                "urn:x-matrox:cap:meta:layer_compatibility_groups": [
                    0
                ],
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 1,
                "urn:x-nmos:cap:format:frame_height": {
                    "enum": [
                        480,
                        720,
                        1080,
                        2160
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "3",
                        "3.1",
                        "3.2",
                        "4",
                        "4.1",
                        "4.2",
                        "5",
                        "5.1",
                        "5.2",
                        "6",
                        "6.1",
                        "6.2"
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "video/H264"
                    ]
                },
                "urn:x-nmos:cap:format:frame_width": {
                    "enum": [
                        720,
                        1280,
                        1920,
                        3840
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "High-422",
                        "HighIntra-422"
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "minimum": 40000,
                    "maximum": 3200000
                },
                "urn:x-nmos:cap:format:grain_rate": {
                    "enum": [
                        {
                            "numerator": 24,
                            "denominator": 1
                        },
                        {
                            "numerator": 60,
                            "denominator": 1
                        },
                        {
                            "numerator": 6000,
                            "denominator": 1001
                        },
                        {
                            "numerator": 30,
                            "denominator": 1
                        },
                        {
                            "numerator": 3000,
                            "denominator": 1001
                        }
                    ]
                },
                "urn:x-nmos:cap:format:color_sampling": {
                    "enum": [
                        "YCbCr-4:2:0",
                        "YCbCr-4:2:2"
                    ]
                },
                "urn:x-nmos:cap:format:colorspace": {
                    "enum": [
                        "BT601",
                        "BT709",
                        "BT2020"
                    ]
                },
                "urn:x-nmos:cap:format:component_depth": {
                    "enum": [
                        8,
                        10
                    ]
                },
                "urn:x-nmos:cap:format:transfer_characteristic": {
                    "enum": [
                        "SDR"
                    ]
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false,
                        true
                    ]
                },
                "urn:x-nmos:cap:format:interlace_mode": {
                    "enum": [
                        "progressive"
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "Mux constraints",
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 1,
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "application/MP2T"
                    ]
                },
                "urn:x-matrox:cap:format:video_layers": {
                    "minimum": 1,
                    "maximum": 1
                },
                "urn:x-matrox:cap:format:audio_layers": {
                    "minimum": 0,
                    "maximum": 2
                },
                "urn:x-matrox:cap:format:data_layers": {
                    "minimum": 0,
                    "maximum": 0
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "AAC multi-channels sub-constraints",
                "urn:x-matrox:cap:meta:format": "urn:x-nmos:format:audio",
                "urn:x-matrox:cap:meta:layer": 1,
                "urn:x-matrox:cap:meta:layer_compatibility_groups": [
                    0
                ],
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 1,
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "audio/MP4A-ADTS"
                    ]
                },
                "urn:x-nmos:cap:format:sample_rate": {
                    "enum": [
                        {
                            "numerator": 48000,
                            "denominator": 1
                        }
                    ]
                },
                "urn:x-nmos:cap:format:channel_count": {
                    "enum": [
                        2,
                        6
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "HighQuality",
                        "AAC",
                        "HighEfficiencyAAC",
                        "HighEfficiencyAACv2"
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "4"
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "maximum": 1728
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false,
                        true
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "H.265 sub-constraints",
                "urn:x-matrox:cap:meta:format": "urn:x-nmos:format:video",
                "urn:x-matrox:cap:meta:layer": 0,
                "urn:x-matrox:cap:meta:layer_compatibility_groups": [
                    0
                ],
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 0,
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "Main10-422",
                        "Main10-444",
                        "Main10Intra-422",
                        "Main10Intra-444"
                    ]
                },
                "urn:x-nmos:cap:format:frame_width": {
                    "enum": [
                        720,
                        1280,
                        1920,
                        3840
                    ]
                },
                "urn:x-nmos:cap:format:frame_height": {
                    "enum": [
                        480,
                        720,
                        1080,
                        2160
                    ]
                },
                "urn:x-nmos:cap:format:transfer_characteristic": {
                    "enum": [
                        "SDR"
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "minimum": 10002,
                    "maximum": 4000000
                },
                "urn:x-nmos:cap:format:color_sampling": {
                    "enum": [
                        "YCbCr-4:2:0",
                        "YCbCr-4:2:2",
                        "YCbCr-4:4:4"
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "Main-3",
                        "Main-3.1",
                        "Main-4",
                        "High-4",
                        "Main-4.1",
                        "High-4.1",
                        "Main-5",
                        "High-5",
                        "Main-5.1",
                        "High-5.1",
                        "Main-5.2",
                        "High-5.2",
                        "Main-6",
                        "High-6",
                        "Main-6.1",
                        "High-6.1",
                        "Main-6.2",
                        "High-6.2"
                    ]
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false,
                        true
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "video/H265"
                    ]
                },
                "urn:x-nmos:cap:format:colorspace": {
                    "enum": [
                        "BT601",
                        "BT709",
                        "BT2020"
                    ]
                },
                "urn:x-nmos:cap:format:component_depth": {
                    "enum": [
                        8,
                        10
                    ]
                },
                "urn:x-nmos:cap:format:grain_rate": {
                    "enum": [
                        {
                            "numerator": 24,
                            "denominator": 1
                        },
                        {
                            "numerator": 60,
                            "denominator": 1
                        },
                        {
                            "numerator": 6000,
                            "denominator": 1001
                        },
                        {
                            "numerator": 30,
                            "denominator": 1
                        },
                        {
                            "numerator": 3000,
                            "denominator": 1001
                        }
                    ]
                },
                "urn:x-nmos:cap:format:interlace_mode": {
                    "enum": [
                        "progressive"
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "JPEG-XS sub-constraints",
                "urn:x-matrox:cap:meta:format": "urn:x-nmos:format:video",
                "urn:x-matrox:cap:meta:layer": 0,
                "urn:x-matrox:cap:meta:layer_compatibility_groups": [
                    0
                ],
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 0,
                "urn:x-nmos:cap:format:sublevel": {
                    "enum": [
                        "Sublev3bpp",
                        "Sublev4bpp"
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "minimum": 802161,
                    "maximum": 4278190
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "4k-1",
                        "4k-2",
                        "4k-3"
                    ]
                },
                "urn:x-nmos:cap:format:grain_rate": {
                    "enum": [
                        {
                            "numerator": 24,
                            "denominator": 1
                        },
                        {
                            "numerator": 30,
                            "denominator": 1
                        },
                        {
                            "numerator": 3000,
                            "denominator": 1001
                        },
                        {
                            "numerator": 60,
                            "denominator": 1
                        },
                        {
                            "numerator": 6000,
                            "denominator": 1001
                        }
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "Main420.12",
                        "High420.12",
                        "Main444.12",
                        "High444.12"
                    ]
                },
                "urn:x-nmos:cap:format:color_sampling": {
                    "enum": [
                        "YCbCr-4:2:0",
                        "YCbCr-4:2:2",
                        "YCbCr-4:4:4"
                    ]
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false,
                        true
                    ]
                },
                "urn:x-nmos:cap:format:frame_width": {
                    "enum": [
                        720,
                        1280,
                        1920,
                        3840
                    ]
                },
                "urn:x-nmos:cap:format:component_depth": {
                    "enum": [
                        8,
                        10
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "video/jxsv"
                    ]
                },
                "urn:x-nmos:cap:format:transfer_characteristic": {
                    "enum": [
                        "SDR"
                    ]
                },
                "urn:x-nmos:cap:format:colorspace": {
                    "enum": [
                        "BT601",
                        "BT709",
                        "BT2020"
                    ]
                },
                "urn:x-nmos:cap:format:interlace_mode": {
                    "enum": [
                        "progressive"
                    ]
                },
                "urn:x-nmos:cap:format:frame_height": {
                    "enum": [
                        480,
                        720,
                        1080,
                        2160
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "AAC stereo sub-constraints",
                "urn:x-matrox:cap:meta:format": "urn:x-nmos:format:audio",
                "urn:x-matrox:cap:meta:layer": 0,
                "urn:x-matrox:cap:meta:layer_compatibility_groups": [
                    0
                ],
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 0,
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false,
                        true
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "audio/MP4A-ADTS"
                    ]
                },
                "urn:x-nmos:cap:format:sample_rate": {
                    "enum": [
                        {
                            "numerator": 48000,
                            "denominator": 1
                        }
                    ]
                },
                "urn:x-nmos:cap:format:channel_count": {
                    "enum": [
                        2
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "Main",
                        "Natural",
                        "LowDelayAAC",
                        "LowDelayAACv2"
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "1"
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "maximum": 576
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "AM824 sub-constraints",
                "urn:x-matrox:cap:meta:format": "urn:x-nmos:format:audio",
                "urn:x-matrox:cap:meta:layer": 0,
                "urn:x-matrox:cap:meta:layer_compatibility_groups": [
                    0
                ],
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 0,
                "urn:x-nmos:cap:format:channel_count": {
                    "enum": [
                        2,
                        4,
                        8,
                        10
                    ]
                },
                "urn:x-nmos:cap:format:sample_rate": {
                    "enum": [
                        {
                            "numerator": 48000,
                            "denominator": 1
                        }
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "audio/AM824"
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "PCM sub-constraints",
                "urn:x-matrox:cap:meta:format": "urn:x-nmos:format:audio",
                "urn:x-matrox:cap:meta:layer": 0,
                "urn:x-matrox:cap:meta:layer_compatibility_groups": [
                    0
                ],
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 0,
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "audio/L16",
                        "audio/L20",
                        "audio/L24"
                    ]
                },
                "urn:x-nmos:cap:format:channel_count": {
                    "enum": [
                        2,
                        6,
                        8
                    ]
                },
                "urn:x-nmos:cap:format:sample_depth": {
                    "enum": [
                        16,
                        20,
                        24
                    ]
                },
                "urn:x-nmos:cap:format:sample_rate": {
                    "enum": [
                        {
                            "numerator": 48000,
                            "denominator": 1
                        }
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "AAC stereo sub-constraints",
                "urn:x-matrox:cap:meta:format": "urn:x-nmos:format:audio",
                "urn:x-matrox:cap:meta:layer": 1,
                "urn:x-matrox:cap:meta:layer_compatibility_groups": [
                    0
                ],
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 0,
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "1"
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "maximum": 576
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false,
                        true
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "audio/MP4A-ADTS"
                    ]
                },
                "urn:x-nmos:cap:format:sample_rate": {
                    "enum": [
                        {
                            "numerator": 48000,
                            "denominator": 1
                        }
                    ]
                },
                "urn:x-nmos:cap:format:channel_count": {
                    "enum": [
                        2
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "Main",
                        "Natural",
                        "LowDelayAAC",
                        "LowDelayAACv2"
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "AM824 sub-constraints",
                "urn:x-matrox:cap:meta:format": "urn:x-nmos:format:audio",
                "urn:x-matrox:cap:meta:layer": 1,
                "urn:x-matrox:cap:meta:layer_compatibility_groups": [
                    0
                ],
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 0,
                "urn:x-nmos:cap:format:sample_rate": {
                    "enum": [
                        {
                            "numerator": 48000,
                            "denominator": 1
                        }
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "audio/AM824"
                    ]
                },
                "urn:x-nmos:cap:format:channel_count": {
                    "enum": [
                        2,
                        4,
                        8,
                        10
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "PCM sub-constraints",
                "urn:x-matrox:cap:meta:format": "urn:x-nmos:format:audio",
                "urn:x-matrox:cap:meta:layer": 1,
                "urn:x-matrox:cap:meta:layer_compatibility_groups": [
                    0
                ],
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 0,
                "urn:x-nmos:cap:format:sample_depth": {
                    "enum": [
                        16,
                        20,
                        24
                    ]
                },
                "urn:x-nmos:cap:format:sample_rate": {
                    "enum": [
                        {
                            "numerator": 48000,
                            "denominator": 1
                        }
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "audio/L16",
                        "audio/L20",
                        "audio/L24"
                    ]
                },
                "urn:x-nmos:cap:format:channel_count": {
                    "enum": [
                        2,
                        6,
                        8
                    ]
                }
            }
        ]
    }
}
'''

video_sender = '''
{
    "id": "00000000-0200-4000-ab00-4d5458005057",
    "version": "1730479011:563002770",
    "label": "Net Stream 0 Video 0",
    "description": "This is the Net Stream 0 Video 0",
    "tags": {
        "urn:x-nmos:tag:grouphint/v1.0": [
            "RTP 0:VIDEO 0"
        ]
    },
    "flow_id": "6e50e13d-0400-4000-ab00-4d5458005057",
    "transport": "urn:x-nmos:transport:rtp.mcast",
    "device_id": "00000000-0100-4000-ab00-4d5458005057",
    "manifest_href": null,
    "interface_bindings": [
        "lo"
    ],
    "subscription": {
        "receiver_id": null,
        "active": false
    },
    "caps": {
        "version": "1730227257:139443720",
        "constraint_sets": [
            {
                "urn:x-nmos:cap:meta:label": "Native Video constraints",
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 100,
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "video/H264"
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "4"
                    ]
                },
                "urn:x-matrox:cap:transport:parameter_sets_transport_mode": {
                    "enum": [
                        "in_and_out_of_band"
                    ]
                },
                "urn:x-nmos:cap:format:frame_height": {
                    "enum": [
                        1080
                    ]
                },
                "urn:x-nmos:cap:format:interlace_mode": {
                    "enum": [
                        "progressive"
                    ]
                },
                "urn:x-nmos:cap:transport:packet_transmission_mode": {
                    "enum": [
                        "non_interleaved_nal_units"
                    ]
                },
                "urn:x-nmos:cap:format:grain_rate": {
                    "enum": [
                        {
                            "numerator": 60,
                            "denominator": 1
                        }
                    ]
                },
                "urn:x-nmos:cap:format:colorspace": {
                    "enum": [
                        "BT709"
                    ]
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false
                    ]
                },
                "urn:x-nmos:cap:format:frame_width": {
                    "enum": [
                        1920
                    ]
                },
                "urn:x-nmos:cap:format:component_depth": {
                    "enum": [
                        10
                    ]
                },
                "urn:x-nmos:cap:format:color_sampling": {
                    "enum": [
                        "YCbCr-4:2:2"
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "enum": [
                        40000
                    ]
                },
                "urn:x-matrox:cap:transport:parameter_sets_flow_mode": {
                    "enum": [
                        "strict"
                    ]
                },
                "urn:x-nmos:cap:format:transfer_characteristic": {
                    "enum": [
                        "SDR"
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "High-422"
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "H.264 constraints",
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 1,
                "urn:x-nmos:cap:format:interlace_mode": {
                    "enum": [
                        "progressive"
                    ]
                },
                "urn:x-nmos:cap:format:transfer_characteristic": {
                    "enum": [
                        "SDR"
                    ]
                },
                "urn:x-nmos:cap:format:component_depth": {
                    "enum": [
                        8,
                        10
                    ]
                },
                "urn:x-nmos:cap:format:grain_rate": {
                    "enum": [
                        {
                            "numerator": 24,
                            "denominator": 1
                        },
                        {
                            "numerator": 60,
                            "denominator": 1
                        },
                        {
                            "numerator": 6000,
                            "denominator": 1001
                        },
                        {
                            "numerator": 30,
                            "denominator": 1
                        },
                        {
                            "numerator": 3000,
                            "denominator": 1001
                        }
                    ]
                },
                "urn:x-nmos:cap:format:color_sampling": {
                    "enum": [
                        "YCbCr-4:2:0",
                        "YCbCr-4:2:2"
                    ]
                },
                "urn:x-nmos:cap:transport:packet_transmission_mode": {
                    "enum": [
                        "non_interleaved_nal_units"
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "video/H264"
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "3",
                        "3.1",
                        "3.2",
                        "4",
                        "4.1",
                        "4.2",
                        "5",
                        "5.1",
                        "5.2",
                        "6",
                        "6.1",
                        "6.2"
                    ]
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false,
                        true
                    ]
                },
                "urn:x-nmos:cap:format:frame_width": {
                    "enum": [
                        720,
                        1280,
                        1920,
                        3840
                    ]
                },
                "urn:x-nmos:cap:format:colorspace": {
                    "enum": [
                        "BT601",
                        "BT709",
                        "BT2020"
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "High-422",
                        "HighIntra-422"
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "minimum": 40000,
                    "maximum": 3200000
                },
                "urn:x-nmos:cap:format:frame_height": {
                    "enum": [
                        480,
                        720,
                        1080,
                        2160
                    ]
                },
                "urn:x-matrox:cap:transport:parameter_sets_flow_mode": {
                    "enum": [
                        "strict"
                    ]
                },
                "urn:x-matrox:cap:transport:parameter_sets_transport_mode": {
                    "enum": [
                        "in_and_out_of_band"
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "H.265 constraints",
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 0,
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "Main-3",
                        "Main-3.1",
                        "Main-4",
                        "High-4",
                        "Main-4.1",
                        "High-4.1",
                        "Main-5",
                        "High-5",
                        "Main-5.1",
                        "High-5.1",
                        "Main-5.2",
                        "High-5.2",
                        "Main-6",
                        "High-6",
                        "Main-6.1",
                        "High-6.1",
                        "Main-6.2",
                        "High-6.2"
                    ]
                },
                "urn:x-nmos:cap:transport:packet_transmission_mode": {
                    "enum": [
                        "non_interleaved_nal_units"
                    ]
                },
                "urn:x-matrox:cap:transport:parameter_sets_flow_mode": {
                    "enum": [
                        "strict"
                    ]
                },
                "urn:x-nmos:cap:format:frame_width": {
                    "enum": [
                        720,
                        1280,
                        1920,
                        3840
                    ]
                },
                "urn:x-nmos:cap:format:colorspace": {
                    "enum": [
                        "BT601",
                        "BT709",
                        "BT2020"
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "Main10-422",
                        "Main10-444",
                        "Main10Intra-422",
                        "Main10Intra-444"
                    ]
                },
                "urn:x-nmos:cap:format:transfer_characteristic": {
                    "enum": [
                        "SDR"
                    ]
                },
                "urn:x-nmos:cap:format:component_depth": {
                    "enum": [
                        8,
                        10
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "video/H265"
                    ]
                },
                "urn:x-nmos:cap:format:frame_height": {
                    "enum": [
                        480,
                        720,
                        1080,
                        2160
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "minimum": 10002,
                    "maximum": 4000000
                },
                "urn:x-matrox:cap:transport:parameter_sets_transport_mode": {
                    "enum": [
                        "in_and_out_of_band"
                    ]
                },
                "urn:x-nmos:cap:format:grain_rate": {
                    "enum": [
                        {
                            "numerator": 24,
                            "denominator": 1
                        },
                        {
                            "numerator": 60,
                            "denominator": 1
                        },
                        {
                            "numerator": 6000,
                            "denominator": 1001
                        },
                        {
                            "numerator": 30,
                            "denominator": 1
                        },
                        {
                            "numerator": 3000,
                            "denominator": 1001
                        }
                    ]
                },
                "urn:x-nmos:cap:format:color_sampling": {
                    "enum": [
                        "YCbCr-4:2:0",
                        "YCbCr-4:2:2",
                        "YCbCr-4:4:4"
                    ]
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false,
                        true
                    ]
                },
                "urn:x-nmos:cap:format:interlace_mode": {
                    "enum": [
                        "progressive"
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "JPEG-XS constraints",
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 0,
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "4k-1",
                        "4k-2",
                        "4k-3"
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "Main420.12",
                        "High420.12",
                        "Main444.12",
                        "High444.12"
                    ]
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false,
                        true
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "minimum": 802161,
                    "maximum": 4278190
                },
                "urn:x-nmos:cap:format:grain_rate": {
                    "enum": [
                        {
                            "numerator": 24,
                            "denominator": 1
                        },
                        {
                            "numerator": 30,
                            "denominator": 1
                        },
                        {
                            "numerator": 3000,
                            "denominator": 1001
                        },
                        {
                            "numerator": 60,
                            "denominator": 1
                        },
                        {
                            "numerator": 6000,
                            "denominator": 1001
                        }
                    ]
                },
                "urn:x-nmos:cap:format:color_sampling": {
                    "enum": [
                        "YCbCr-4:2:0",
                        "YCbCr-4:2:2",
                        "YCbCr-4:4:4"
                    ]
                },
                "urn:x-nmos:cap:format:transfer_characteristic": {
                    "enum": [
                        "SDR"
                    ]
                },
                "urn:x-nmos:cap:format:sublevel": {
                    "enum": [
                        "Sublev3bpp",
                        "Sublev4bpp"
                    ]
                },
                "urn:x-nmos:cap:transport:packet_transmission_mode": {
                    "enum": [
                        "codestream"
                    ]
                },
                "urn:x-nmos:cap:format:frame_width": {
                    "enum": [
                        720,
                        1280,
                        1920,
                        3840
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "video/jxsv"
                    ]
                },
                "urn:x-nmos:cap:format:frame_height": {
                    "enum": [
                        480,
                        720,
                        1080,
                        2160
                    ]
                },
                "urn:x-nmos:cap:format:component_depth": {
                    "enum": [
                        8,
                        10
                    ]
                },
                "urn:x-nmos:cap:format:interlace_mode": {
                    "enum": [
                        "progressive"
                    ]
                },
                "urn:x-nmos:cap:format:colorspace": {
                    "enum": [
                        "BT601",
                        "BT709",
                        "BT2020"
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "RAW constraints",
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 0,
                "urn:x-nmos:cap:format:colorspace": {
                    "enum": [
                        "BT601",
                        "BT709",
                        "BT2020"
                    ]
                },
                "urn:x-nmos:cap:format:component_depth": {
                    "enum": [
                        8,
                        10
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "video/raw"
                    ]
                },
                "urn:x-nmos:cap:format:frame_width": {
                    "enum": [
                        720,
                        1280,
                        1920,
                        3840
                    ]
                },
                "urn:x-nmos:cap:format:frame_height": {
                    "enum": [
                        480,
                        720,
                        1080,
                        2160
                    ]
                },
                "urn:x-nmos:cap:format:transfer_characteristic": {
                    "enum": [
                        "SDR"
                    ]
                },
                "urn:x-nmos:cap:format:color_sampling": {
                    "enum": [
                        "YCbCr-4:2:0",
                        "YCbCr-4:2:2",
                        "YCbCr-4:4:4"
                    ]
                },
                "urn:x-nmos:cap:format:interlace_mode": {
                    "enum": [
                        "progressive"
                    ]
                },
                "urn:x-nmos:cap:format:grain_rate": {
                    "enum": [
                        {
                            "numerator": 24,
                            "denominator": 1
                        },
                        {
                            "numerator": 30,
                            "denominator": 1
                        },
                        {
                            "numerator": 3000,
                            "denominator": 1001
                        },
                        {
                            "numerator": 60,
                            "denominator": 1
                        },
                        {
                            "numerator": 6000,
                            "denominator": 1001
                        }
                    ]
                }
            }
        ]
    },
    "bit_rate": 43200,
    "st2110_21_sender_type": "2110TPW",
    "packet_transmission_mode": "non_interleaved_nal_units",
    "urn:x-matrox:parameter_sets_transport_mode": "in_and_out_of_band",
    "urn:x-matrox:parameter_sets_flow_mode": "strict"
}
'''

audio_sender = '''
{
    "id": "00000000-0201-4000-ab00-4d5458005057",
    "version": "1730227257:139970732",
    "label": "Net Stream 0 Audio 0",
    "description": "This is the Net Stream 0 Audio 0",
    "tags": {
        "urn:x-nmos:tag:grouphint/v1.0": [
            "RTP 0:AUDIO 0"
        ]
    },
    "flow_id": "5650e13d-0401-4000-ab00-4d5458005057",
    "transport": "urn:x-nmos:transport:rtp.mcast",
    "device_id": "00000000-0100-4000-ab00-4d5458005057",
    "manifest_href": null,
    "interface_bindings": [
        "lo"
    ],
    "subscription": {
        "receiver_id": null,
        "active": false
    },
    "caps": {
        "version": "1730227257:139919406",
        "constraint_sets": [
            {
                "urn:x-nmos:cap:meta:label": "Native Audio constraints",
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 100,
                "urn:x-matrox:cap:transport:parameter_sets_transport_mode": {
                    "enum": [
                        "out_of_band"
                    ]
                },
                "urn:x-nmos:cap:format:channel_count": {
                    "enum": [
                        2
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "2"
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "AAC"
                    ]
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        true
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "audio/mpeg4-generic"
                    ]
                },
                "urn:x-nmos:cap:format:sample_rate": {
                    "enum": [
                        {
                            "numerator": 48000,
                            "denominator": 1
                        }
                    ]
                },
                "urn:x-matrox:cap:transport:parameter_sets_flow_mode": {
                    "enum": [
                        "strict"
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "enum": [
                        128
                    ]
                },
                "urn:x-nmos:cap:transport:packet_transmission_mode": {
                    "enum": [
                        "non_interleaved_access_units"
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "AAC multi-channels constraints",
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 1,
                "urn:x-matrox:cap:transport:parameter_sets_transport_mode": {
                    "enum": [
                        "out_of_band"
                    ]
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false,
                        true
                    ]
                },
                "urn:x-nmos:cap:transport:packet_transmission_mode": {
                    "enum": [
                        "non_interleaved_access_units"
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "4"
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "maximum": 1728
                },
                "urn:x-nmos:cap:format:sample_rate": {
                    "enum": [
                        {
                            "numerator": 48000,
                            "denominator": 1
                        }
                    ]
                },
                "urn:x-nmos:cap:format:channel_count": {
                    "enum": [
                        2,
                        6
                    ]
                },
                "urn:x-matrox:cap:transport:parameter_sets_flow_mode": {
                    "enum": [
                        "strict"
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "audio/mpeg4-generic"
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "HighQuality",
                        "AAC",
                        "HighEfficiencyAAC",
                        "HighEfficiencyAACv2"
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "AAC stereo constraints",
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 0,
                "urn:x-nmos:cap:format:bit_rate": {
                    "maximum": 576
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "Main",
                        "Natural",
                        "LowDelayAAC",
                        "LowDelayAACv2"
                    ]
                },
                "urn:x-matrox:cap:transport:parameter_sets_transport_mode": {
                    "enum": [
                        "out_of_band"
                    ]
                },
                "urn:x-nmos:cap:transport:packet_transmission_mode": {
                    "enum": [
                        "non_interleaved_access_units"
                    ]
                },
                "urn:x-matrox:cap:transport:parameter_sets_flow_mode": {
                    "enum": [
                        "strict"
                    ]
                },
                "urn:x-nmos:cap:format:sample_rate": {
                    "enum": [
                        {
                            "numerator": 48000,
                            "denominator": 1
                        }
                    ]
                },
                "urn:x-nmos:cap:format:channel_count": {
                    "enum": [
                        2
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "1"
                    ]
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false,
                        true
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "audio/mpeg4-generic"
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "AM824 constraints",
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 0,
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "audio/AM824"
                    ]
                },
                "urn:x-nmos:cap:format:channel_count": {
                    "enum": [
                        2,
                        4,
                        8,
                        10
                    ]
                },
                "urn:x-nmos:cap:format:sample_rate": {
                    "enum": [
                        {
                            "numerator": 48000,
                            "denominator": 1
                        },
                        {
                            "numerator": 96000,
                            "denominator": 1
                        },
                        {
                            "numerator": 44100,
                            "denominator": 1
                        },
                        {
                            "numerator": 88200,
                            "denominator": 1
                        }
                    ]
                },
                "urn:x-matrox:cap:transport:channel_order": {
                    "enum": [
                        "SMPTE2110.(AES3)",
                        "SMPTE2110.(AES3,ST)",
                        "SMPTE2110.(AES3,51)",
                        "SMPTE2110.(AES3,71)"
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "PCM constraints",
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 0,
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "audio/L16",
                        "audio/L20",
                        "audio/L24"
                    ]
                },
                "urn:x-nmos:cap:format:channel_count": {
                    "enum": [
                        2,
                        6,
                        8
                    ]
                },
                "urn:x-nmos:cap:format:sample_depth": {
                    "enum": [
                        16,
                        20,
                        24
                    ]
                },
                "urn:x-nmos:cap:format:sample_rate": {
                    "enum": [
                        {
                            "numerator": 48000,
                            "denominator": 1
                        },
                        {
                            "numerator": 96000,
                            "denominator": 1
                        },
                        {
                            "numerator": 44100,
                            "denominator": 1
                        },
                        {
                            "numerator": 88200,
                            "denominator": 1
                        }
                    ]
                },
                "urn:x-matrox:cap:transport:channel_order": {
                    "enum": [
                        "SMPTE2110.(ST)",
                        "SMPTE2110.(51)",
                        "SMPTE2110.(71)"
                    ]
                }
            }
        ]
    },
    "bit_rate": 138,
    "packet_transmission_mode": "non_interleaved_access_units",
    "urn:x-matrox:parameter_sets_transport_mode": "out_of_band",
    "urn:x-matrox:parameter_sets_flow_mode": "strict"
}
'''

compressed_video_sender = '''
{
    "id": "00000000-0200-4000-ab00-4d5458005057",
    "version": "1730479011:563002770",
    "label": "Net Stream 0 Video 0",
    "description": "This is the Net Stream 0 Video 0",
    "tags": {
        "urn:x-nmos:tag:grouphint/v1.0": [
            "RTP 0:VIDEO 0"
        ]
    },
    "flow_id": "6e50e13d-0400-4000-ab00-4d5458005057",
    "transport": "urn:x-nmos:transport:rtp.mcast",
    "device_id": "00000000-0100-4000-ab00-4d5458005057",
    "manifest_href": null,
    "interface_bindings": [
        "lo"
    ],
    "subscription": {
        "receiver_id": null,
        "active": false
    },
    "caps": {
        "version": "1730227257:139443720",
        "constraint_sets": [
            {
                "urn:x-nmos:cap:meta:label": "Native Video constraints",
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 100,
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "video/H264"
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "4"
                    ]
                },
                "urn:x-matrox:cap:transport:parameter_sets_transport_mode": {
                    "enum": [
                        "in_and_out_of_band"
                    ]
                },
                "urn:x-nmos:cap:format:frame_height": {
                    "enum": [
                        1080
                    ]
                },
                "urn:x-nmos:cap:format:interlace_mode": {
                    "enum": [
                        "progressive"
                    ]
                },
                "urn:x-nmos:cap:transport:packet_transmission_mode": {
                    "enum": [
                        "non_interleaved_nal_units"
                    ]
                },
                "urn:x-nmos:cap:format:grain_rate": {
                    "enum": [
                        {
                            "numerator": 60,
                            "denominator": 1
                        }
                    ]
                },
                "urn:x-nmos:cap:format:colorspace": {
                    "enum": [
                        "BT709"
                    ]
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false
                    ]
                },
                "urn:x-nmos:cap:format:frame_width": {
                    "enum": [
                        1920
                    ]
                },
                "urn:x-nmos:cap:format:component_depth": {
                    "enum": [
                        10
                    ]
                },
                "urn:x-nmos:cap:format:color_sampling": {
                    "enum": [
                        "YCbCr-4:2:2"
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "enum": [
                        40000
                    ]
                },
                "urn:x-matrox:cap:transport:parameter_sets_flow_mode": {
                    "enum": [
                        "strict"
                    ]
                },
                "urn:x-nmos:cap:format:transfer_characteristic": {
                    "enum": [
                        "SDR"
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "High-422"
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "H.264 constraints",
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 1,
                "urn:x-nmos:cap:format:interlace_mode": {
                    "enum": [
                        "progressive"
                    ]
                },
                "urn:x-nmos:cap:format:transfer_characteristic": {
                    "enum": [
                        "SDR"
                    ]
                },
                "urn:x-nmos:cap:format:component_depth": {
                    "enum": [
                        8,
                        10
                    ]
                },
                "urn:x-nmos:cap:format:grain_rate": {
                    "enum": [
                        {
                            "numerator": 24,
                            "denominator": 1
                        },
                        {
                            "numerator": 60,
                            "denominator": 1
                        },
                        {
                            "numerator": 6000,
                            "denominator": 1001
                        },
                        {
                            "numerator": 30,
                            "denominator": 1
                        },
                        {
                            "numerator": 3000,
                            "denominator": 1001
                        }
                    ]
                },
                "urn:x-nmos:cap:format:color_sampling": {
                    "enum": [
                        "YCbCr-4:2:0",
                        "YCbCr-4:2:2"
                    ]
                },
                "urn:x-nmos:cap:transport:packet_transmission_mode": {
                    "enum": [
                        "non_interleaved_nal_units"
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "video/H264"
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "3",
                        "3.1",
                        "3.2",
                        "4",
                        "4.1",
                        "4.2",
                        "5",
                        "5.1",
                        "5.2",
                        "6",
                        "6.1",
                        "6.2"
                    ]
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false,
                        true
                    ]
                },
                "urn:x-nmos:cap:format:frame_width": {
                    "enum": [
                        720,
                        1280,
                        1920,
                        3840
                    ]
                },
                "urn:x-nmos:cap:format:colorspace": {
                    "enum": [
                        "BT601",
                        "BT709",
                        "BT2020"
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "High-422",
                        "HighIntra-422"
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "minimum": 40000,
                    "maximum": 3200000
                },
                "urn:x-nmos:cap:format:frame_height": {
                    "enum": [
                        480,
                        720,
                        1080,
                        2160
                    ]
                },
                "urn:x-matrox:cap:transport:parameter_sets_flow_mode": {
                    "enum": [
                        "strict"
                    ]
                },
                "urn:x-matrox:cap:transport:parameter_sets_transport_mode": {
                    "enum": [
                        "in_and_out_of_band"
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "H.265 constraints",
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 0,
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "Main-3",
                        "Main-3.1",
                        "Main-4",
                        "High-4",
                        "Main-4.1",
                        "High-4.1",
                        "Main-5",
                        "High-5",
                        "Main-5.1",
                        "High-5.1",
                        "Main-5.2",
                        "High-5.2",
                        "Main-6",
                        "High-6",
                        "Main-6.1",
                        "High-6.1",
                        "Main-6.2",
                        "High-6.2"
                    ]
                },
                "urn:x-nmos:cap:transport:packet_transmission_mode": {
                    "enum": [
                        "non_interleaved_nal_units"
                    ]
                },
                "urn:x-matrox:cap:transport:parameter_sets_flow_mode": {
                    "enum": [
                        "strict"
                    ]
                },
                "urn:x-nmos:cap:format:frame_width": {
                    "enum": [
                        720,
                        1280,
                        1920,
                        3840
                    ]
                },
                "urn:x-nmos:cap:format:colorspace": {
                    "enum": [
                        "BT601",
                        "BT709",
                        "BT2020"
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "Main10-422",
                        "Main10-444",
                        "Main10Intra-422",
                        "Main10Intra-444"
                    ]
                },
                "urn:x-nmos:cap:format:transfer_characteristic": {
                    "enum": [
                        "SDR"
                    ]
                },
                "urn:x-nmos:cap:format:component_depth": {
                    "enum": [
                        8,
                        10
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "video/H265"
                    ]
                },
                "urn:x-nmos:cap:format:frame_height": {
                    "enum": [
                        480,
                        720,
                        1080,
                        2160
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "minimum": 10002,
                    "maximum": 4000000
                },
                "urn:x-matrox:cap:transport:parameter_sets_transport_mode": {
                    "enum": [
                        "in_and_out_of_band"
                    ]
                },
                "urn:x-nmos:cap:format:grain_rate": {
                    "enum": [
                        {
                            "numerator": 24,
                            "denominator": 1
                        },
                        {
                            "numerator": 60,
                            "denominator": 1
                        },
                        {
                            "numerator": 6000,
                            "denominator": 1001
                        },
                        {
                            "numerator": 30,
                            "denominator": 1
                        },
                        {
                            "numerator": 3000,
                            "denominator": 1001
                        }
                    ]
                },
                "urn:x-nmos:cap:format:color_sampling": {
                    "enum": [
                        "YCbCr-4:2:0",
                        "YCbCr-4:2:2",
                        "YCbCr-4:4:4"
                    ]
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false,
                        true
                    ]
                },
                "urn:x-nmos:cap:format:interlace_mode": {
                    "enum": [
                        "progressive"
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "JPEG-XS constraints",
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 0,
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "4k-1",
                        "4k-2",
                        "4k-3"
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "Main420.12",
                        "High420.12",
                        "Main444.12",
                        "High444.12"
                    ]
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false,
                        true
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "minimum": 802161,
                    "maximum": 4278190
                },
                "urn:x-nmos:cap:format:grain_rate": {
                    "enum": [
                        {
                            "numerator": 24,
                            "denominator": 1
                        },
                        {
                            "numerator": 30,
                            "denominator": 1
                        },
                        {
                            "numerator": 3000,
                            "denominator": 1001
                        },
                        {
                            "numerator": 60,
                            "denominator": 1
                        },
                        {
                            "numerator": 6000,
                            "denominator": 1001
                        }
                    ]
                },
                "urn:x-nmos:cap:format:color_sampling": {
                    "enum": [
                        "YCbCr-4:2:0",
                        "YCbCr-4:2:2",
                        "YCbCr-4:4:4"
                    ]
                },
                "urn:x-nmos:cap:format:transfer_characteristic": {
                    "enum": [
                        "SDR"
                    ]
                },
                "urn:x-nmos:cap:format:sublevel": {
                    "enum": [
                        "Sublev3bpp",
                        "Sublev4bpp"
                    ]
                },
                "urn:x-nmos:cap:transport:packet_transmission_mode": {
                    "enum": [
                        "codestream"
                    ]
                },
                "urn:x-nmos:cap:format:frame_width": {
                    "enum": [
                        720,
                        1280,
                        1920,
                        3840
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "video/jxsv"
                    ]
                },
                "urn:x-nmos:cap:format:frame_height": {
                    "enum": [
                        480,
                        720,
                        1080,
                        2160
                    ]
                },
                "urn:x-nmos:cap:format:component_depth": {
                    "enum": [
                        8,
                        10
                    ]
                },
                "urn:x-nmos:cap:format:interlace_mode": {
                    "enum": [
                        "progressive"
                    ]
                },
                "urn:x-nmos:cap:format:colorspace": {
                    "enum": [
                        "BT601",
                        "BT709",
                        "BT2020"
                    ]
                }
            }
        ]
    },
    "bit_rate": 43200,
    "st2110_21_sender_type": "2110TPW",
    "packet_transmission_mode": "non_interleaved_nal_units",
    "urn:x-matrox:parameter_sets_transport_mode": "in_and_out_of_band",
    "urn:x-matrox:parameter_sets_flow_mode": "strict"
}
'''

compressed_audio_sender = '''
{
    "id": "00000000-0201-4000-ab00-4d5458005057",
    "version": "1730227257:139970732",
    "label": "Net Stream 0 Audio 0",
    "description": "This is the Net Stream 0 Audio 0",
    "tags": {
        "urn:x-nmos:tag:grouphint/v1.0": [
            "RTP 0:AUDIO 0"
        ]
    },
    "flow_id": "5650e13d-0401-4000-ab00-4d5458005057",
    "transport": "urn:x-nmos:transport:rtp.mcast",
    "device_id": "00000000-0100-4000-ab00-4d5458005057",
    "manifest_href": null,
    "interface_bindings": [
        "lo"
    ],
    "subscription": {
        "receiver_id": null,
        "active": false
    },
    "caps": {
        "version": "1730227257:139919406",
        "constraint_sets": [
            {
                "urn:x-nmos:cap:meta:label": "Native Audio constraints",
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 100,
                "urn:x-matrox:cap:transport:parameter_sets_transport_mode": {
                    "enum": [
                        "out_of_band"
                    ]
                },
                "urn:x-nmos:cap:format:channel_count": {
                    "enum": [
                        2
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "2"
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "AAC"
                    ]
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        true
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "audio/mpeg4-generic"
                    ]
                },
                "urn:x-nmos:cap:format:sample_rate": {
                    "enum": [
                        {
                            "numerator": 48000,
                            "denominator": 1
                        }
                    ]
                },
                "urn:x-matrox:cap:transport:parameter_sets_flow_mode": {
                    "enum": [
                        "strict"
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "enum": [
                        128
                    ]
                },
                "urn:x-nmos:cap:transport:packet_transmission_mode": {
                    "enum": [
                        "non_interleaved_access_units"
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "AAC multi-channels constraints",
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 1,
                "urn:x-matrox:cap:transport:parameter_sets_transport_mode": {
                    "enum": [
                        "out_of_band"
                    ]
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false,
                        true
                    ]
                },
                "urn:x-nmos:cap:transport:packet_transmission_mode": {
                    "enum": [
                        "non_interleaved_access_units"
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "4"
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "maximum": 1728
                },
                "urn:x-nmos:cap:format:sample_rate": {
                    "enum": [
                        {
                            "numerator": 48000,
                            "denominator": 1
                        }
                    ]
                },
                "urn:x-nmos:cap:format:channel_count": {
                    "enum": [
                        2,
                        6
                    ]
                },
                "urn:x-matrox:cap:transport:parameter_sets_flow_mode": {
                    "enum": [
                        "strict"
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "audio/mpeg4-generic"
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "HighQuality",
                        "AAC",
                        "HighEfficiencyAAC",
                        "HighEfficiencyAACv2"
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "AAC stereo constraints",
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 0,
                "urn:x-nmos:cap:format:bit_rate": {
                    "maximum": 576
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "Main",
                        "Natural",
                        "LowDelayAAC",
                        "LowDelayAACv2"
                    ]
                },
                "urn:x-matrox:cap:transport:parameter_sets_transport_mode": {
                    "enum": [
                        "out_of_band"
                    ]
                },
                "urn:x-nmos:cap:transport:packet_transmission_mode": {
                    "enum": [
                        "non_interleaved_access_units"
                    ]
                },
                "urn:x-matrox:cap:transport:parameter_sets_flow_mode": {
                    "enum": [
                        "strict"
                    ]
                },
                "urn:x-nmos:cap:format:sample_rate": {
                    "enum": [
                        {
                            "numerator": 48000,
                            "denominator": 1
                        }
                    ]
                },
                "urn:x-nmos:cap:format:channel_count": {
                    "enum": [
                        2
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "1"
                    ]
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false,
                        true
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "audio/mpeg4-generic"
                    ]
                }
            }
        ]
    },
    "bit_rate": 138,
    "packet_transmission_mode": "non_interleaved_access_units",
    "urn:x-matrox:parameter_sets_transport_mode": "out_of_band",
    "urn:x-matrox:parameter_sets_flow_mode": "strict"
}
'''

video_receiver = '''
{
    "id": "00000000-0303-4000-ab00-4d5458005058",
    "version": "1730490691:18090749",
    "label": "Net Stream 1 Video 0",
    "description": "This is the Net Stream 1 Video 0",
    "tags": {
        "urn:x-nmos:tag:grouphint/v1.0": [
            "RTP 1:VIDEO 0"
        ],
        "urn:x-nmos:tag:wallhint/v1.0": [
            "WALL 21"
        ]
    },
    "transport": "urn:x-nmos:transport:rtp.mcast",
    "device_id": "00000000-0100-4000-ab00-4d5458005058",
    "interface_bindings": [
        "lo"
    ],
    "subscription": {
        "sender_id": null,
        "active": false
    },
    "format": "urn:x-nmos:format:video",
    "caps": {
        "media_types": [
            "video/raw",
            "video/H264",
            "video/H265",
            "video/jxsv"
        ],
        "version": "1730490691:18051428",
        "constraint_sets": [
            {
                "urn:x-nmos:cap:meta:label": "Native Video constraints",
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 100,
                "urn:x-nmos:cap:format:color_sampling": {
                    "enum": [
                        "YCbCr-4:2:2"
                    ]
                },
                "urn:x-nmos:cap:format:colorspace": {
                    "enum": [
                        "BT709"
                    ]
                },
                "urn:x-matrox:cap:transport:parameter_sets_transport_mode": {
                    "enum": [
                        "in_and_out_of_band",
                        "in_band",
                        "out_of_band"
                    ]
                },
                "urn:x-nmos:cap:format:interlace_mode": {
                    "enum": [
                        "progressive"
                    ]
                },
                "urn:x-nmos:cap:format:transfer_characteristic": {
                    "enum": [
                        "SDR"
                    ]
                },
                "urn:x-nmos:cap:format:component_depth": {
                    "enum": [
                        10
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "High-422"
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "enum": [
                        40000
                    ]
                },
                "urn:x-matrox:cap:transport:parameter_sets_flow_mode": {
                    "enum": [
                        "strict"
                    ]
                },
                "urn:x-nmos:cap:format:grain_rate": {
                    "enum": [
                        {
                            "numerator": 60,
                            "denominator": 1
                        }
                    ]
                },
                "urn:x-nmos:cap:transport:packet_transmission_mode": {
                    "enum": [
                        "non_interleaved_nal_units"
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "4"
                    ]
                },
                "urn:x-nmos:cap:format:frame_width": {
                    "enum": [
                        1920
                    ]
                },
                "urn:x-nmos:cap:format:frame_height": {
                    "enum": [
                        1080
                    ]
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "video/H264"
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "H.264 constraints",
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 1,
                "urn:x-nmos:cap:format:bit_rate": {
                    "minimum": 40000,
                    "maximum": 3200000
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false,
                        true
                    ]
                },
                "urn:x-nmos:cap:transport:packet_transmission_mode": {
                    "enum": [
                        "non_interleaved_nal_units",
                        "single_nal_unit"
                    ]
                },
                "urn:x-matrox:cap:transport:parameter_sets_flow_mode": {
                    "enum": [
                        "strict"
                    ]
                },
                "urn:x-nmos:cap:format:frame_width": {
                    "enum": [
                        720,
                        1280,
                        1920,
                        3840
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "High-422",
                        "HighIntra-422"
                    ]
                },
                "urn:x-nmos:cap:format:frame_height": {
                    "enum": [
                        480,
                        720,
                        1080,
                        2160
                    ]
                },
                "urn:x-nmos:cap:format:color_sampling": {
                    "enum": [
                        "YCbCr-4:2:0",
                        "YCbCr-4:2:2"
                    ]
                },
                "urn:x-nmos:cap:format:colorspace": {
                    "enum": [
                        "BT601",
                        "BT709",
                        "BT2020"
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "3",
                        "3.1",
                        "3.2",
                        "4",
                        "4.1",
                        "4.2",
                        "5",
                        "5.1",
                        "5.2",
                        "6",
                        "6.1",
                        "6.2"
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "video/H264"
                    ]
                },
                "urn:x-nmos:cap:format:interlace_mode": {
                    "enum": [
                        "progressive"
                    ]
                },
                "urn:x-nmos:cap:format:component_depth": {
                    "enum": [
                        8,
                        10
                    ]
                },
                "urn:x-matrox:cap:transport:parameter_sets_transport_mode": {
                    "enum": [
                        "in_and_out_of_band",
                        "in_band",
                        "out_of_band"
                    ]
                },
                "urn:x-nmos:cap:format:grain_rate": {
                    "enum": [
                        {
                            "numerator": 24,
                            "denominator": 1
                        },
                        {
                            "numerator": 60,
                            "denominator": 1
                        },
                        {
                            "numerator": 6000,
                            "denominator": 1001
                        },
                        {
                            "numerator": 30,
                            "denominator": 1
                        },
                        {
                            "numerator": 3000,
                            "denominator": 1001
                        }
                    ]
                },
                "urn:x-nmos:cap:format:transfer_characteristic": {
                    "enum": [
                        "SDR"
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "H.265 constraints",
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 0,
                "urn:x-nmos:cap:format:transfer_characteristic": {
                    "enum": [
                        "SDR"
                    ]
                },
                "urn:x-nmos:cap:format:component_depth": {
                    "enum": [
                        8,
                        10
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "Main-3",
                        "Main-3.1",
                        "Main-4",
                        "High-4",
                        "Main-4.1",
                        "High-4.1",
                        "Main-5",
                        "High-5",
                        "Main-5.1",
                        "High-5.1",
                        "Main-5.2",
                        "High-5.2",
                        "Main-6",
                        "High-6",
                        "Main-6.1",
                        "High-6.1",
                        "Main-6.2",
                        "High-6.2"
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "minimum": 10002,
                    "maximum": 4000000
                },
                "urn:x-nmos:cap:format:grain_rate": {
                    "enum": [
                        {
                            "numerator": 24,
                            "denominator": 1
                        },
                        {
                            "numerator": 60,
                            "denominator": 1
                        },
                        {
                            "numerator": 6000,
                            "denominator": 1001
                        },
                        {
                            "numerator": 30,
                            "denominator": 1
                        },
                        {
                            "numerator": 3000,
                            "denominator": 1001
                        }
                    ]
                },
                "urn:x-nmos:cap:format:frame_height": {
                    "enum": [
                        480,
                        720,
                        1080,
                        2160
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "Main10-422",
                        "Main10-444",
                        "Main10Intra-422",
                        "Main10Intra-444"
                    ]
                },
                "urn:x-matrox:cap:transport:parameter_sets_transport_mode": {
                    "enum": [
                        "in_and_out_of_band",
                        "in_band",
                        "out_of_band"
                    ]
                },
                "urn:x-matrox:cap:transport:parameter_sets_flow_mode": {
                    "enum": [
                        "strict"
                    ]
                },
                "urn:x-nmos:cap:format:interlace_mode": {
                    "enum": [
                        "progressive"
                    ]
                },
                "urn:x-nmos:cap:format:colorspace": {
                    "enum": [
                        "BT601",
                        "BT709",
                        "BT2020"
                    ]
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false,
                        true
                    ]
                },
                "urn:x-nmos:cap:transport:packet_transmission_mode": {
                    "enum": [
                        "non_interleaved_nal_units"
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "video/H265"
                    ]
                },
                "urn:x-nmos:cap:format:color_sampling": {
                    "enum": [
                        "YCbCr-4:2:0",
                        "YCbCr-4:2:2",
                        "YCbCr-4:4:4"
                    ]
                },
                "urn:x-nmos:cap:format:frame_width": {
                    "enum": [
                        720,
                        1280,
                        1920,
                        3840
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "JPEG-XS constraints",
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 0,
                "urn:x-nmos:cap:format:bit_rate": {
                    "minimum": 802161,
                    "maximum": 4278190
                },
                "urn:x-nmos:cap:format:grain_rate": {
                    "enum": [
                        {
                            "numerator": 24,
                            "denominator": 1
                        },
                        {
                            "numerator": 30,
                            "denominator": 1
                        },
                        {
                            "numerator": 3000,
                            "denominator": 1001
                        },
                        {
                            "numerator": 60,
                            "denominator": 1
                        },
                        {
                            "numerator": 6000,
                            "denominator": 1001
                        }
                    ]
                },
                "urn:x-nmos:cap:format:frame_width": {
                    "enum": [
                        720,
                        1280,
                        1920,
                        3840
                    ]
                },
                "urn:x-nmos:cap:format:transfer_characteristic": {
                    "enum": [
                        "SDR"
                    ]
                },
                "urn:x-nmos:cap:format:colorspace": {
                    "enum": [
                        "BT601",
                        "BT709",
                        "BT2020"
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "4k-1",
                        "4k-2",
                        "4k-3"
                    ]
                },
                "urn:x-nmos:cap:format:component_depth": {
                    "enum": [
                        8,
                        10
                    ]
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false,
                        true
                    ]
                },
                "urn:x-nmos:cap:format:sublevel": {
                    "enum": [
                        "Sublev3bpp",
                        "Sublev4bpp"
                    ]
                },
                "urn:x-nmos:cap:transport:packet_transmission_mode": {
                    "enum": [
                        "codestream"
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "video/jxsv"
                    ]
                },
                "urn:x-nmos:cap:format:interlace_mode": {
                    "enum": [
                        "progressive"
                    ]
                },
                "urn:x-nmos:cap:format:frame_height": {
                    "enum": [
                        480,
                        720,
                        1080,
                        2160
                    ]
                },
                "urn:x-nmos:cap:format:color_sampling": {
                    "enum": [
                        "YCbCr-4:2:0",
                        "YCbCr-4:2:2",
                        "YCbCr-4:4:4"
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "Main420.12",
                        "High420.12",
                        "Main444.12",
                        "High444.12"
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "RAW constraints",
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 0,
                "urn:x-nmos:cap:format:colorspace": {
                    "enum": [
                        "BT601",
                        "BT709",
                        "BT2020"
                    ]
                },
                "urn:x-nmos:cap:format:color_sampling": {
                    "enum": [
                        "YCbCr-4:2:0",
                        "YCbCr-4:2:2",
                        "YCbCr-4:4:4"
                    ]
                },
                "urn:x-nmos:cap:format:component_depth": {
                    "enum": [
                        8,
                        10
                    ]
                },
                "urn:x-nmos:cap:format:interlace_mode": {
                    "enum": [
                        "progressive"
                    ]
                },
                "urn:x-nmos:cap:format:grain_rate": {
                    "enum": [
                        {
                            "numerator": 24,
                            "denominator": 1
                        },
                        {
                            "numerator": 30,
                            "denominator": 1
                        },
                        {
                            "numerator": 3000,
                            "denominator": 1001
                        },
                        {
                            "numerator": 60,
                            "denominator": 1
                        },
                        {
                            "numerator": 6000,
                            "denominator": 1001
                        }
                    ]
                },
                "urn:x-nmos:cap:format:frame_width": {
                    "enum": [
                        720,
                        1280,
                        1920,
                        3840
                    ]
                },
                "urn:x-nmos:cap:format:frame_height": {
                    "enum": [
                        480,
                        720,
                        1080,
                        2160
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "video/raw"
                    ]
                },
                "urn:x-nmos:cap:format:transfer_characteristic": {
                    "enum": [
                        "SDR"
                    ]
                }
            }
        ]
    }
}
'''

compressed_video_receiver = '''
{
    "id": "00000000-0303-4000-ab00-4d5458005058",
    "version": "1730490691:18090749",
    "label": "Net Stream 1 Video 0",
    "description": "This is the Net Stream 1 Video 0",
    "tags": {
        "urn:x-nmos:tag:grouphint/v1.0": [
            "RTP 1:VIDEO 0"
        ],
        "urn:x-nmos:tag:wallhint/v1.0": [
            "WALL 21"
        ]
    },
    "transport": "urn:x-nmos:transport:rtp.mcast",
    "device_id": "00000000-0100-4000-ab00-4d5458005058",
    "interface_bindings": [
        "lo"
    ],
    "subscription": {
        "sender_id": null,
        "active": false
    },
    "format": "urn:x-nmos:format:video",
    "caps": {
        "media_types": [
            "video/H264",
            "video/H265"
        ],
        "version": "1730490691:18051428",
        "constraint_sets": [
            {
                "urn:x-nmos:cap:meta:label": "Native Video constraints",
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 100,
                "urn:x-nmos:cap:format:color_sampling": {
                    "enum": [
                        "YCbCr-4:2:2"
                    ]
                },
                "urn:x-nmos:cap:format:colorspace": {
                    "enum": [
                        "BT709"
                    ]
                },
                "urn:x-matrox:cap:transport:parameter_sets_transport_mode": {
                    "enum": [
                        "in_and_out_of_band",
                        "in_band",
                        "out_of_band"
                    ]
                },
                "urn:x-nmos:cap:format:interlace_mode": {
                    "enum": [
                        "progressive"
                    ]
                },
                "urn:x-nmos:cap:format:transfer_characteristic": {
                    "enum": [
                        "SDR"
                    ]
                },
                "urn:x-nmos:cap:format:component_depth": {
                    "enum": [
                        10
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "High-422"
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "enum": [
                        40000
                    ]
                },
                "urn:x-matrox:cap:transport:parameter_sets_flow_mode": {
                    "enum": [
                        "strict"
                    ]
                },
                "urn:x-nmos:cap:format:grain_rate": {
                    "enum": [
                        {
                            "numerator": 60,
                            "denominator": 1
                        }
                    ]
                },
                "urn:x-nmos:cap:transport:packet_transmission_mode": {
                    "enum": [
                        "non_interleaved_nal_units"
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "4"
                    ]
                },
                "urn:x-nmos:cap:format:frame_width": {
                    "enum": [
                        1920
                    ]
                },
                "urn:x-nmos:cap:format:frame_height": {
                    "enum": [
                        1080
                    ]
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "video/H264"
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "H.264 constraints",
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 1,
                "urn:x-nmos:cap:format:bit_rate": {
                    "minimum": 40000,
                    "maximum": 3200000
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false,
                        true
                    ]
                },
                "urn:x-nmos:cap:transport:packet_transmission_mode": {
                    "enum": [
                        "non_interleaved_nal_units",
                        "single_nal_unit"
                    ]
                },
                "urn:x-matrox:cap:transport:parameter_sets_flow_mode": {
                    "enum": [
                        "strict"
                    ]
                },
                "urn:x-nmos:cap:format:frame_width": {
                    "enum": [
                        720,
                        1280,
                        1920,
                        3840
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "High-422",
                        "HighIntra-422"
                    ]
                },
                "urn:x-nmos:cap:format:frame_height": {
                    "enum": [
                        480,
                        720,
                        1080,
                        2160
                    ]
                },
                "urn:x-nmos:cap:format:color_sampling": {
                    "enum": [
                        "YCbCr-4:2:0",
                        "YCbCr-4:2:2"
                    ]
                },
                "urn:x-nmos:cap:format:colorspace": {
                    "enum": [
                        "BT601",
                        "BT709",
                        "BT2020"
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "3",
                        "3.1",
                        "3.2",
                        "4",
                        "4.1",
                        "4.2",
                        "5",
                        "5.1",
                        "5.2",
                        "6",
                        "6.1",
                        "6.2"
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "video/H264"
                    ]
                },
                "urn:x-nmos:cap:format:interlace_mode": {
                    "enum": [
                        "progressive"
                    ]
                },
                "urn:x-nmos:cap:format:component_depth": {
                    "enum": [
                        8,
                        10
                    ]
                },
                "urn:x-matrox:cap:transport:parameter_sets_transport_mode": {
                    "enum": [
                        "in_and_out_of_band",
                        "in_band",
                        "out_of_band"
                    ]
                },
                "urn:x-nmos:cap:format:grain_rate": {
                    "enum": [
                        {
                            "numerator": 24,
                            "denominator": 1
                        },
                        {
                            "numerator": 60,
                            "denominator": 1
                        },
                        {
                            "numerator": 6000,
                            "denominator": 1001
                        },
                        {
                            "numerator": 30,
                            "denominator": 1
                        },
                        {
                            "numerator": 3000,
                            "denominator": 1001
                        }
                    ]
                },
                "urn:x-nmos:cap:format:transfer_characteristic": {
                    "enum": [
                        "SDR"
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "H.265 constraints",
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 0,
                "urn:x-nmos:cap:format:transfer_characteristic": {
                    "enum": [
                        "SDR"
                    ]
                },
                "urn:x-nmos:cap:format:component_depth": {
                    "enum": [
                        8,
                        10
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "Main-3",
                        "Main-3.1",
                        "Main-4",
                        "High-4",
                        "Main-4.1",
                        "High-4.1",
                        "Main-5",
                        "High-5",
                        "Main-5.1",
                        "High-5.1",
                        "Main-5.2",
                        "High-5.2",
                        "Main-6",
                        "High-6",
                        "Main-6.1",
                        "High-6.1",
                        "Main-6.2",
                        "High-6.2"
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "minimum": 10002,
                    "maximum": 4000000
                },
                "urn:x-nmos:cap:format:grain_rate": {
                    "enum": [
                        {
                            "numerator": 24,
                            "denominator": 1
                        },
                        {
                            "numerator": 60,
                            "denominator": 1
                        },
                        {
                            "numerator": 6000,
                            "denominator": 1001
                        },
                        {
                            "numerator": 30,
                            "denominator": 1
                        },
                        {
                            "numerator": 3000,
                            "denominator": 1001
                        }
                    ]
                },
                "urn:x-nmos:cap:format:frame_height": {
                    "enum": [
                        480,
                        720,
                        1080,
                        2160
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "Main10-422",
                        "Main10-444",
                        "Main10Intra-422",
                        "Main10Intra-444"
                    ]
                },
                "urn:x-matrox:cap:transport:parameter_sets_transport_mode": {
                    "enum": [
                        "in_and_out_of_band",
                        "in_band",
                        "out_of_band"
                    ]
                },
                "urn:x-matrox:cap:transport:parameter_sets_flow_mode": {
                    "enum": [
                        "strict"
                    ]
                },
                "urn:x-nmos:cap:format:interlace_mode": {
                    "enum": [
                        "progressive"
                    ]
                },
                "urn:x-nmos:cap:format:colorspace": {
                    "enum": [
                        "BT601",
                        "BT709",
                        "BT2020"
                    ]
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false,
                        true
                    ]
                },
                "urn:x-nmos:cap:transport:packet_transmission_mode": {
                    "enum": [
                        "non_interleaved_nal_units"
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "video/H265"
                    ]
                },
                "urn:x-nmos:cap:format:color_sampling": {
                    "enum": [
                        "YCbCr-4:2:0",
                        "YCbCr-4:2:2",
                        "YCbCr-4:4:4"
                    ]
                },
                "urn:x-nmos:cap:format:frame_width": {
                    "enum": [
                        720,
                        1280,
                        1920,
                        3840
                    ]
                }
            }
        ]
    }
}
'''

audio_receiver = '''
{
    "id": "00000000-0304-4000-ab00-4d5458005058",
    "version": "1730490691:18280852",
    "label": "Net Stream 1 Audio 0",
    "description": "This is the Net Stream 1 Audio 0",
    "tags": {
        "urn:x-nmos:tag:grouphint/v1.0": [
            "RTP 1:AUDIO 0"
        ],
        "urn:x-nmos:tag:wallhint/v1.0": [
            "WALL 21"
        ]
    },
    "transport": "urn:x-nmos:transport:rtp.mcast",
    "device_id": "00000000-0100-4000-ab00-4d5458005058",
    "interface_bindings": [
        "lo"
    ],
    "subscription": {
        "sender_id": null,
        "active": false
    },
    "format": "urn:x-nmos:format:audio",
    "caps": {
        "media_types": [
            "audio/L16",
            "audio/L20",
            "audio/L24",
            "audio/mpeg4-generic",
            "audio/MP4A-LATM"
        ],
        "version": "1730490691:18253908",
        "constraint_sets": [
            {
                "urn:x-nmos:cap:meta:label": "Native Audio constraints",
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 100,
                "urn:x-nmos:cap:format:channel_count": {
                    "enum": [
                        2
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "AAC"
                    ]
                },
                "urn:x-matrox:cap:transport:parameter_sets_transport_mode": {
                    "enum": [
                        "out_of_band"
                    ]
                },
                "urn:x-matrox:cap:transport:parameter_sets_flow_mode": {
                    "enum": [
                        "strict"
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "audio/mpeg4-generic"
                    ]
                },
                "urn:x-nmos:cap:format:sample_rate": {
                    "enum": [
                        {
                            "numerator": 48000,
                            "denominator": 1
                        }
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "2"
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "enum": [
                        128
                    ]
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        true
                    ]
                },
                "urn:x-nmos:cap:transport:packet_transmission_mode": {
                    "enum": [
                        "non_interleaved_access_units"
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "AAC multi-channels constraints",
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 1,
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "HighQuality",
                        "AAC",
                        "HighEfficiencyAAC",
                        "HighEfficiencyAACv2"
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "maximum": 1728
                },
                "urn:x-matrox:cap:transport:parameter_sets_transport_mode": {
                    "enum": [
                        "out_of_band"
                    ]
                },
                "urn:x-matrox:cap:transport:parameter_sets_flow_mode": {
                    "enum": [
                        "strict"
                    ]
                },
                "urn:x-nmos:cap:format:sample_rate": {
                    "enum": [
                        {
                            "numerator": 48000,
                            "denominator": 1
                        }
                    ]
                },
                "urn:x-nmos:cap:format:channel_count": {
                    "enum": [
                        2,
                        6
                    ]
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false,
                        true
                    ]
                },
                "urn:x-nmos:cap:transport:packet_transmission_mode": {
                    "enum": [
                        "non_interleaved_access_units"
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "audio/mpeg4-generic"
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "4"
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "AAC stereo constraints",
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 0,
                "urn:x-nmos:cap:format:channel_count": {
                    "enum": [
                        2
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "maximum": 576
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false,
                        true
                    ]
                },
                "urn:x-nmos:cap:transport:packet_transmission_mode": {
                    "enum": [
                        "non_interleaved_access_units"
                    ]
                },
                "urn:x-matrox:cap:transport:parameter_sets_flow_mode": {
                    "enum": [
                        "strict"
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "audio/mpeg4-generic"
                    ]
                },
                "urn:x-nmos:cap:format:sample_rate": {
                    "enum": [
                        {
                            "numerator": 48000,
                            "denominator": 1
                        }
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "Main",
                        "Natural",
                        "LowDelayAAC",
                        "LowDelayAACv2"
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "1"
                    ]
                },
                "urn:x-matrox:cap:transport:parameter_sets_transport_mode": {
                    "enum": [
                        "out_of_band"
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "PCM constraints",
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 0,
                "urn:x-nmos:cap:format:channel_count": {
                    "enum": [
                        2,
                        6,
                        8
                    ]
                },
                "urn:x-nmos:cap:format:sample_depth": {
                    "enum": [
                        16,
                        20,
                        24
                    ]
                },
                "urn:x-nmos:cap:format:sample_rate": {
                    "enum": [
                        {
                            "numerator": 48000,
                            "denominator": 1
                        },
                        {
                            "numerator": 96000,
                            "denominator": 1
                        },
                        {
                            "numerator": 44100,
                            "denominator": 1
                        },
                        {
                            "numerator": 88200,
                            "denominator": 1
                        }
                    ]
                },
                "urn:x-matrox:cap:transport:channel_order": {
                    "enum": [
                        "SMPTE2110.(ST)",
                        "SMPTE2110.(51)",
                        "SMPTE2110.(71)"
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "audio/L16",
                        "audio/L20",
                        "audio/L24"
                    ]
                }
            }
        ]
    }
}
'''

compressed_audio_receiver = '''
{
    "id": "00000000-0304-4000-ab00-4d5458005058",
    "version": "1730490691:18280852",
    "label": "Net Stream 1 Audio 0",
    "description": "This is the Net Stream 1 Audio 0",
    "tags": {
        "urn:x-nmos:tag:grouphint/v1.0": [
            "RTP 1:AUDIO 0"
        ],
        "urn:x-nmos:tag:wallhint/v1.0": [
            "WALL 21"
        ]
    },
    "transport": "urn:x-nmos:transport:rtp.mcast",
    "device_id": "00000000-0100-4000-ab00-4d5458005058",
    "interface_bindings": [
        "lo"
    ],
    "subscription": {
        "sender_id": null,
        "active": false
    },
    "format": "urn:x-nmos:format:audio",
    "caps": {
        "media_types": [
            "audio/mpeg4-generic",
            "audio/MP4A-LATM"
        ],
        "version": "1730490691:18253908",
        "constraint_sets": [
            {
                "urn:x-nmos:cap:meta:label": "Native Audio constraints",
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 100,
                "urn:x-nmos:cap:format:channel_count": {
                    "enum": [
                        2
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "AAC"
                    ]
                },
                "urn:x-matrox:cap:transport:parameter_sets_transport_mode": {
                    "enum": [
                        "out_of_band"
                    ]
                },
                "urn:x-matrox:cap:transport:parameter_sets_flow_mode": {
                    "enum": [
                        "strict"
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "audio/mpeg4-generic"
                    ]
                },
                "urn:x-nmos:cap:format:sample_rate": {
                    "enum": [
                        {
                            "numerator": 48000,
                            "denominator": 1
                        }
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "2"
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "enum": [
                        128
                    ]
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        true
                    ]
                },
                "urn:x-nmos:cap:transport:packet_transmission_mode": {
                    "enum": [
                        "non_interleaved_access_units"
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "AAC multi-channels constraints",
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 1,
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "HighQuality",
                        "AAC",
                        "HighEfficiencyAAC",
                        "HighEfficiencyAACv2"
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "maximum": 1728
                },
                "urn:x-matrox:cap:transport:parameter_sets_transport_mode": {
                    "enum": [
                        "out_of_band"
                    ]
                },
                "urn:x-matrox:cap:transport:parameter_sets_flow_mode": {
                    "enum": [
                        "strict"
                    ]
                },
                "urn:x-nmos:cap:format:sample_rate": {
                    "enum": [
                        {
                            "numerator": 48000,
                            "denominator": 1
                        }
                    ]
                },
                "urn:x-nmos:cap:format:channel_count": {
                    "enum": [
                        2,
                        6
                    ]
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false,
                        true
                    ]
                },
                "urn:x-nmos:cap:transport:packet_transmission_mode": {
                    "enum": [
                        "non_interleaved_access_units"
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "audio/mpeg4-generic"
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "4"
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "AAC stereo constraints",
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 0,
                "urn:x-nmos:cap:format:channel_count": {
                    "enum": [
                        2
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "maximum": 576
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false,
                        true
                    ]
                },
                "urn:x-nmos:cap:transport:packet_transmission_mode": {
                    "enum": [
                        "non_interleaved_access_units"
                    ]
                },
                "urn:x-matrox:cap:transport:parameter_sets_flow_mode": {
                    "enum": [
                        "strict"
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "audio/mpeg4-generic"
                    ]
                },
                "urn:x-nmos:cap:format:sample_rate": {
                    "enum": [
                        {
                            "numerator": 48000,
                            "denominator": 1
                        }
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "Main",
                        "Natural",
                        "LowDelayAAC",
                        "LowDelayAACv2"
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "1"
                    ]
                },
                "urn:x-matrox:cap:transport:parameter_sets_transport_mode": {
                    "enum": [
                        "out_of_band"
                    ]
                }
            }
        ]
    }
}
'''

mp2t_receiver = '''
{
    "id": "00000000-0300-4000-ab00-4d5458005057",
    "version": "1730479011:563096971",
    "label": "Net Stream MPEG2-TS 0",
    "description": "This is the Net Stream MPEG2-TS 0",
    "tags": {
        "urn:x-nmos:tag:grouphint/v1.0": [
            "RTP 0:MUX 0"
        ],
        "urn:x-nmos:tag:wallhint/v1.0": [
            "WALL 80"
        ]
    },
    "transport": "urn:x-nmos:transport:rtp.mcast",
    "device_id": "00000000-0100-4000-ab00-4d5458005057",
    "interface_bindings": [
        "lo"
    ],
    "subscription": {
        "sender_id": null,
        "active": false
    },
    "format": "urn:x-nmos:format:mux",
    "caps": {
        "media_types": [
            "application/MP2T"
        ],
        "version": "1730479011:563096357",
        "constraint_sets": [
            {
                "urn:x-nmos:cap:meta:label": "Native Audio sub-constraints",
                "urn:x-matrox:cap:meta:format": "urn:x-nmos:format:audio",
                "urn:x-matrox:cap:meta:layer": 1,
                "urn:x-matrox:cap:meta:layer_compatibility_groups": [
                    0
                ],
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 100,
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "audio/MP4A-ADTS"
                    ]
                },
                "urn:x-nmos:cap:format:sample_rate": {
                    "enum": [
                        {
                            "numerator": 48000,
                            "denominator": 1
                        }
                    ]
                },
                "urn:x-nmos:cap:format:channel_count": {
                    "enum": [
                        2
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "AAC"
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "2"
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "enum": [
                        128
                    ]
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        true
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "Native Mux constraints",
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 100,
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "application/MP2T"
                    ]
                },
                "urn:x-matrox:cap:format:video_layers": {
                    "minimum": 1,
                    "maximum": 1
                },
                "urn:x-matrox:cap:format:audio_layers": {
                    "minimum": 2,
                    "maximum": 2
                },
                "urn:x-matrox:cap:format:data_layers": {
                    "minimum": 0,
                    "maximum": 0
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "Native Video sub-constraints",
                "urn:x-matrox:cap:meta:format": "urn:x-nmos:format:video",
                "urn:x-matrox:cap:meta:layer": 0,
                "urn:x-matrox:cap:meta:layer_compatibility_groups": [
                    0
                ],
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 100,
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "High-422"
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "4"
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "enum": [
                        40000
                    ]
                },
                "urn:x-nmos:cap:format:frame_height": {
                    "enum": [
                        1080
                    ]
                },
                "urn:x-nmos:cap:format:colorspace": {
                    "enum": [
                        "BT709"
                    ]
                },
                "urn:x-nmos:cap:format:color_sampling": {
                    "enum": [
                        "YCbCr-4:2:2"
                    ]
                },
                "urn:x-nmos:cap:format:frame_width": {
                    "enum": [
                        1920
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "video/H264"
                    ]
                },
                "urn:x-nmos:cap:format:component_depth": {
                    "enum": [
                        10
                    ]
                },
                "urn:x-nmos:cap:format:transfer_characteristic": {
                    "enum": [
                        "SDR"
                    ]
                },
                "urn:x-nmos:cap:format:interlace_mode": {
                    "enum": [
                        "progressive"
                    ]
                },
                "urn:x-nmos:cap:format:grain_rate": {
                    "enum": [
                        {
                            "numerator": 60,
                            "denominator": 1
                        }
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "Native Audio sub-constraints",
                "urn:x-matrox:cap:meta:format": "urn:x-nmos:format:audio",
                "urn:x-matrox:cap:meta:layer": 0,
                "urn:x-matrox:cap:meta:layer_compatibility_groups": [
                    0
                ],
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 100,
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "2"
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "enum": [
                        128
                    ]
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        true
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "audio/MP4A-ADTS"
                    ]
                },
                "urn:x-nmos:cap:format:sample_rate": {
                    "enum": [
                        {
                            "numerator": 48000,
                            "denominator": 1
                        }
                    ]
                },
                "urn:x-nmos:cap:format:channel_count": {
                    "enum": [
                        2
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "AAC"
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "AAC multi-channels sub-constraints",
                "urn:x-matrox:cap:meta:format": "urn:x-nmos:format:audio",
                "urn:x-matrox:cap:meta:layer": 0,
                "urn:x-matrox:cap:meta:layer_compatibility_groups": [
                    0
                ],
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 1,
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "audio/MP4A-ADTS"
                    ]
                },
                "urn:x-nmos:cap:format:sample_rate": {
                    "enum": [
                        {
                            "numerator": 48000,
                            "denominator": 1
                        }
                    ]
                },
                "urn:x-nmos:cap:format:channel_count": {
                    "enum": [
                        2,
                        6
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "HighQuality",
                        "AAC",
                        "HighEfficiencyAAC",
                        "HighEfficiencyAACv2"
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "4"
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "maximum": 1728
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false,
                        true
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "H.264 sub-constraints",
                "urn:x-matrox:cap:meta:format": "urn:x-nmos:format:video",
                "urn:x-matrox:cap:meta:layer": 0,
                "urn:x-matrox:cap:meta:layer_compatibility_groups": [
                    0
                ],
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 1,
                "urn:x-nmos:cap:format:grain_rate": {
                    "enum": [
                        {
                            "numerator": 24,
                            "denominator": 1
                        },
                        {
                            "numerator": 60,
                            "denominator": 1
                        },
                        {
                            "numerator": 6000,
                            "denominator": 1001
                        },
                        {
                            "numerator": 30,
                            "denominator": 1
                        },
                        {
                            "numerator": 3000,
                            "denominator": 1001
                        }
                    ]
                },
                "urn:x-nmos:cap:format:frame_width": {
                    "enum": [
                        720,
                        1280,
                        1920,
                        3840
                    ]
                },
                "urn:x-nmos:cap:format:transfer_characteristic": {
                    "enum": [
                        "SDR"
                    ]
                },
                "urn:x-nmos:cap:format:component_depth": {
                    "enum": [
                        8,
                        10
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "High-422",
                        "HighIntra-422"
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "minimum": 40000,
                    "maximum": 3200000
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "video/H264"
                    ]
                },
                "urn:x-nmos:cap:format:interlace_mode": {
                    "enum": [
                        "progressive"
                    ]
                },
                "urn:x-nmos:cap:format:colorspace": {
                    "enum": [
                        "BT601",
                        "BT709",
                        "BT2020"
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "3",
                        "3.1",
                        "3.2",
                        "4",
                        "4.1",
                        "4.2",
                        "5",
                        "5.1",
                        "5.2",
                        "6",
                        "6.1",
                        "6.2"
                    ]
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false,
                        true
                    ]
                },
                "urn:x-nmos:cap:format:frame_height": {
                    "enum": [
                        480,
                        720,
                        1080,
                        2160
                    ]
                },
                "urn:x-nmos:cap:format:color_sampling": {
                    "enum": [
                        "YCbCr-4:2:0",
                        "YCbCr-4:2:2"
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "Mux constraints",
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 1,
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "application/MP2T"
                    ]
                },
                "urn:x-matrox:cap:format:video_layers": {
                    "minimum": 1,
                    "maximum": 1
                },
                "urn:x-matrox:cap:format:audio_layers": {
                    "minimum": 0,
                    "maximum": 2
                },
                "urn:x-matrox:cap:format:data_layers": {
                    "minimum": 0,
                    "maximum": 0
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "AAC multi-channels sub-constraints",
                "urn:x-matrox:cap:meta:format": "urn:x-nmos:format:audio",
                "urn:x-matrox:cap:meta:layer": 1,
                "urn:x-matrox:cap:meta:layer_compatibility_groups": [
                    0
                ],
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 1,
                "urn:x-nmos:cap:format:sample_rate": {
                    "enum": [
                        {
                            "numerator": 48000,
                            "denominator": 1
                        }
                    ]
                },
                "urn:x-nmos:cap:format:channel_count": {
                    "enum": [
                        2,
                        6
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "HighQuality",
                        "AAC",
                        "HighEfficiencyAAC",
                        "HighEfficiencyAACv2"
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "4"
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "maximum": 1728
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false,
                        true
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "audio/MP4A-ADTS"
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "H.265 sub-constraints",
                "urn:x-matrox:cap:meta:format": "urn:x-nmos:format:video",
                "urn:x-matrox:cap:meta:layer": 0,
                "urn:x-matrox:cap:meta:layer_compatibility_groups": [
                    0
                ],
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 0,
                "urn:x-nmos:cap:format:frame_height": {
                    "enum": [
                        480,
                        720,
                        1080,
                        2160
                    ]
                },
                "urn:x-nmos:cap:format:component_depth": {
                    "enum": [
                        8,
                        10
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "Main10-422",
                        "Main10-444",
                        "Main10Intra-422",
                        "Main10Intra-444"
                    ]
                },
                "urn:x-nmos:cap:format:color_sampling": {
                    "enum": [
                        "YCbCr-4:2:0",
                        "YCbCr-4:2:2",
                        "YCbCr-4:4:4"
                    ]
                },
                "urn:x-nmos:cap:format:transfer_characteristic": {
                    "enum": [
                        "SDR"
                    ]
                },
                "urn:x-nmos:cap:format:colorspace": {
                    "enum": [
                        "BT601",
                        "BT709",
                        "BT2020"
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "Main-3",
                        "Main-3.1",
                        "Main-4",
                        "High-4",
                        "Main-4.1",
                        "High-4.1",
                        "Main-5",
                        "High-5",
                        "Main-5.1",
                        "High-5.1",
                        "Main-5.2",
                        "High-5.2",
                        "Main-6",
                        "High-6",
                        "Main-6.1",
                        "High-6.1",
                        "Main-6.2",
                        "High-6.2"
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "video/H265"
                    ]
                },
                "urn:x-nmos:cap:format:interlace_mode": {
                    "enum": [
                        "progressive"
                    ]
                },
                "urn:x-nmos:cap:format:grain_rate": {
                    "enum": [
                        {
                            "numerator": 24,
                            "denominator": 1
                        },
                        {
                            "numerator": 60,
                            "denominator": 1
                        },
                        {
                            "numerator": 6000,
                            "denominator": 1001
                        },
                        {
                            "numerator": 30,
                            "denominator": 1
                        },
                        {
                            "numerator": 3000,
                            "denominator": 1001
                        }
                    ]
                },
                "urn:x-nmos:cap:format:frame_width": {
                    "enum": [
                        720,
                        1280,
                        1920,
                        3840
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "minimum": 10002,
                    "maximum": 4000000
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false,
                        true
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "JPEG-XS sub-constraints",
                "urn:x-matrox:cap:meta:format": "urn:x-nmos:format:video",
                "urn:x-matrox:cap:meta:layer": 0,
                "urn:x-matrox:cap:meta:layer_compatibility_groups": [
                    0
                ],
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 0,
                "urn:x-nmos:cap:format:component_depth": {
                    "enum": [
                        8,
                        10
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "4k-1",
                        "4k-2",
                        "4k-3"
                    ]
                },
                "urn:x-nmos:cap:format:grain_rate": {
                    "enum": [
                        {
                            "numerator": 24,
                            "denominator": 1
                        },
                        {
                            "numerator": 30,
                            "denominator": 1
                        },
                        {
                            "numerator": 3000,
                            "denominator": 1001
                        },
                        {
                            "numerator": 60,
                            "denominator": 1
                        },
                        {
                            "numerator": 6000,
                            "denominator": 1001
                        }
                    ]
                },
                "urn:x-nmos:cap:format:frame_width": {
                    "enum": [
                        720,
                        1280,
                        1920,
                        3840
                    ]
                },
                "urn:x-nmos:cap:format:colorspace": {
                    "enum": [
                        "BT601",
                        "BT709",
                        "BT2020"
                    ]
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false,
                        true
                    ]
                },
                "urn:x-nmos:cap:format:color_sampling": {
                    "enum": [
                        "YCbCr-4:2:0",
                        "YCbCr-4:2:2",
                        "YCbCr-4:4:4"
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "Main420.12",
                        "High420.12",
                        "Main444.12",
                        "High444.12"
                    ]
                },
                "urn:x-nmos:cap:format:sublevel": {
                    "enum": [
                        "Sublev3bpp",
                        "Sublev4bpp"
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "video/jxsv"
                    ]
                },
                "urn:x-nmos:cap:format:interlace_mode": {
                    "enum": [
                        "progressive"
                    ]
                },
                "urn:x-nmos:cap:format:frame_height": {
                    "enum": [
                        480,
                        720,
                        1080,
                        2160
                    ]
                },
                "urn:x-nmos:cap:format:transfer_characteristic": {
                    "enum": [
                        "SDR"
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "minimum": 802161,
                    "maximum": 4278190
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "AAC stereo sub-constraints",
                "urn:x-matrox:cap:meta:format": "urn:x-nmos:format:audio",
                "urn:x-matrox:cap:meta:layer": 0,
                "urn:x-matrox:cap:meta:layer_compatibility_groups": [
                    0
                ],
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 0,
                "urn:x-nmos:cap:format:bit_rate": {
                    "maximum": 576
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false,
                        true
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "audio/MP4A-ADTS"
                    ]
                },
                "urn:x-nmos:cap:format:sample_rate": {
                    "enum": [
                        {
                            "numerator": 48000,
                            "denominator": 1
                        }
                    ]
                },
                "urn:x-nmos:cap:format:channel_count": {
                    "enum": [
                        2
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "Main",
                        "Natural",
                        "LowDelayAAC",
                        "LowDelayAACv2"
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "1"
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "AM824 sub-constraints",
                "urn:x-matrox:cap:meta:format": "urn:x-nmos:format:audio",
                "urn:x-matrox:cap:meta:layer": 0,
                "urn:x-matrox:cap:meta:layer_compatibility_groups": [
                    0
                ],
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 0,
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "audio/AM824"
                    ]
                },
                "urn:x-nmos:cap:format:channel_count": {
                    "enum": [
                        2,
                        4,
                        8,
                        10
                    ]
                },
                "urn:x-nmos:cap:format:sample_rate": {
                    "enum": [
                        {
                            "numerator": 48000,
                            "denominator": 1
                        }
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "PCM sub-constraints",
                "urn:x-matrox:cap:meta:format": "urn:x-nmos:format:audio",
                "urn:x-matrox:cap:meta:layer": 0,
                "urn:x-matrox:cap:meta:layer_compatibility_groups": [
                    0
                ],
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 0,
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "audio/L16",
                        "audio/L20",
                        "audio/L24"
                    ]
                },
                "urn:x-nmos:cap:format:channel_count": {
                    "enum": [
                        2,
                        6,
                        8
                    ]
                },
                "urn:x-nmos:cap:format:sample_depth": {
                    "enum": [
                        16,
                        20,
                        24
                    ]
                },
                "urn:x-nmos:cap:format:sample_rate": {
                    "enum": [
                        {
                            "numerator": 48000,
                            "denominator": 1
                        }
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "AAC stereo sub-constraints",
                "urn:x-matrox:cap:meta:format": "urn:x-nmos:format:audio",
                "urn:x-matrox:cap:meta:layer": 1,
                "urn:x-matrox:cap:meta:layer_compatibility_groups": [
                    0
                ],
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 0,
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "1"
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "maximum": 576
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false,
                        true
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "audio/MP4A-ADTS"
                    ]
                },
                "urn:x-nmos:cap:format:sample_rate": {
                    "enum": [
                        {
                            "numerator": 48000,
                            "denominator": 1
                        }
                    ]
                },
                "urn:x-nmos:cap:format:channel_count": {
                    "enum": [
                        2
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "Main",
                        "Natural",
                        "LowDelayAAC",
                        "LowDelayAACv2"
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "AM824 sub-constraints",
                "urn:x-matrox:cap:meta:format": "urn:x-nmos:format:audio",
                "urn:x-matrox:cap:meta:layer": 1,
                "urn:x-matrox:cap:meta:layer_compatibility_groups": [
                    0
                ],
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 0,
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "audio/AM824"
                    ]
                },
                "urn:x-nmos:cap:format:channel_count": {
                    "enum": [
                        2,
                        4,
                        8,
                        10
                    ]
                },
                "urn:x-nmos:cap:format:sample_rate": {
                    "enum": [
                        {
                            "numerator": 48000,
                            "denominator": 1
                        }
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "PCM sub-constraints",
                "urn:x-matrox:cap:meta:format": "urn:x-nmos:format:audio",
                "urn:x-matrox:cap:meta:layer": 1,
                "urn:x-matrox:cap:meta:layer_compatibility_groups": [
                    0
                ],
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 0,
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "audio/L16",
                        "audio/L20",
                        "audio/L24"
                    ]
                },
                "urn:x-nmos:cap:format:channel_count": {
                    "enum": [
                        2,
                        6,
                        8
                    ]
                },
                "urn:x-nmos:cap:format:sample_depth": {
                    "enum": [
                        16,
                        20,
                        24
                    ]
                },
                "urn:x-nmos:cap:format:sample_rate": {
                    "enum": [
                        {
                            "numerator": 48000,
                            "denominator": 1
                        }
                    ]
                }
            }
        ]
    }
}
'''

ndi_receiver = '''
{
    "id": "00000000-0300-4000-ab00-4d5458005056",
    "version": "1730485958:299768986",
    "label": "Net Stream NDI 0",
    "description": "This is the Net Stream NDI 0",
    "tags": {
        "urn:x-nmos:tag:grouphint/v1.0": [
            "NDI 0:MUX 0"
        ],
        "urn:x-nmos:tag:wallhint/v1.0": [
            "WALL 0"
        ]
    },
    "transport": "urn:x-matrox:transport:ndi",
    "device_id": "00000000-0100-4000-ab00-4d5458005056",
    "interface_bindings": [
        "lo"
    ],
    "subscription": {
        "sender_id": null,
        "active": false
    },
    "format": "urn:x-nmos:format:mux",
    "caps": {
        "media_types": [
            "application/ndi"
        ],
        "version": "1730485958:299670843",
        "constraint_sets": [
            {
                "urn:x-nmos:cap:meta:label": "Native Mux constraints",
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 100,
                "urn:x-matrox:cap:format:data_layers": {
                    "minimum": 0,
                    "maximum": 0
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "application/ndi"
                    ]
                },
                "urn:x-matrox:cap:format:video_layers": {
                    "minimum": 1,
                    "maximum": 1
                },
                "urn:x-matrox:cap:format:audio_layers": {
                    "minimum": 1,
                    "maximum": 1
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "Mux constraints",
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 1,
                "urn:x-matrox:cap:format:audio_layers": {
                    "minimum": 0,
                    "maximum": 1
                },
                "urn:x-matrox:cap:format:data_layers": {
                    "minimum": 0,
                    "maximum": 0
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "application/ndi"
                    ]
                },
                "urn:x-matrox:cap:format:video_layers": {
                    "minimum": 1,
                    "maximum": 1
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "Native Video sub-constraints",
                "urn:x-matrox:cap:meta:format": "urn:x-nmos:format:video",
                "urn:x-matrox:cap:meta:layer": 0,
                "urn:x-matrox:cap:meta:layer_compatibility_groups": [
                    1
                ],
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 100,
                "urn:x-nmos:cap:format:color_sampling": {
                    "enum": [
                        "YCbCr-4:2:0"
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "4"
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "enum": [
                        40000
                    ]
                },
                "urn:x-nmos:cap:format:grain_rate": {
                    "enum": [
                        {
                            "numerator": 60,
                            "denominator": 1
                        }
                    ]
                },
                "urn:x-nmos:cap:format:frame_width": {
                    "enum": [
                        1920
                    ]
                },
                "urn:x-nmos:cap:format:frame_height": {
                    "enum": [
                        1080
                    ]
                },
                "urn:x-nmos:cap:format:transfer_characteristic": {
                    "enum": [
                        "SDR"
                    ]
                },
                "urn:x-nmos:cap:format:colorspace": {
                    "enum": [
                        "BT709"
                    ]
                },
                "urn:x-nmos:cap:format:component_depth": {
                    "enum": [
                        8
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "High"
                    ]
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "video/H264"
                    ]
                },
                "urn:x-nmos:cap:format:interlace_mode": {
                    "enum": [
                        "progressive"
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "Native Audio sub-constraints",
                "urn:x-matrox:cap:meta:format": "urn:x-nmos:format:audio",
                "urn:x-matrox:cap:meta:layer": 0,
                "urn:x-matrox:cap:meta:layer_compatibility_groups": [
                    1
                ],
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 100,
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "audio/mpeg4-generic"
                    ]
                },
                "urn:x-nmos:cap:format:sample_rate": {
                    "enum": [
                        {
                            "numerator": 48000,
                            "denominator": 1
                        }
                    ]
                },
                "urn:x-nmos:cap:format:channel_count": {
                    "enum": [
                        2
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "AAC"
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "2"
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "enum": [
                        128
                    ]
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        true
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "H.264 sub-constraints",
                "urn:x-matrox:cap:meta:format": "urn:x-nmos:format:video",
                "urn:x-matrox:cap:meta:layer": 0,
                "urn:x-matrox:cap:meta:layer_compatibility_groups": [
                    1
                ],
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 1,
                "urn:x-nmos:cap:format:transfer_characteristic": {
                    "enum": [
                        "SDR"
                    ]
                },
                "urn:x-nmos:cap:format:interlace_mode": {
                    "enum": [
                        "progressive"
                    ]
                },
                "urn:x-nmos:cap:format:grain_rate": {
                    "enum": [
                        {
                            "numerator": 24,
                            "denominator": 1
                        },
                        {
                            "numerator": 60,
                            "denominator": 1
                        },
                        {
                            "numerator": 6000,
                            "denominator": 1001
                        },
                        {
                            "numerator": 30,
                            "denominator": 1
                        },
                        {
                            "numerator": 3000,
                            "denominator": 1001
                        }
                    ]
                },
                "urn:x-nmos:cap:format:color_sampling": {
                    "enum": [
                        "YCbCr-4:2:0"
                    ]
                },
                "urn:x-nmos:cap:format:colorspace": {
                    "enum": [
                        "BT709",
                        "BT2020"
                    ]
                },
                "urn:x-nmos:cap:format:component_depth": {
                    "enum": [
                        8
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "High10",
                        "High10Intra"
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "3",
                        "3.1",
                        "3.2",
                        "4",
                        "4.1",
                        "4.2",
                        "5",
                        "5.1",
                        "5.2",
                        "6",
                        "6.1",
                        "6.2"
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "minimum": 30000,
                    "maximum": 2400000
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "video/H264"
                    ]
                },
                "urn:x-nmos:cap:format:frame_width": {
                    "enum": [
                        640,
                        1280,
                        1920
                    ]
                },
                "urn:x-nmos:cap:format:frame_height": {
                    "enum": [
                        360,
                        720,
                        1080
                    ]
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false,
                        true
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "H.265 sub-constraints",
                "urn:x-matrox:cap:meta:format": "urn:x-nmos:format:video",
                "urn:x-matrox:cap:meta:layer": 0,
                "urn:x-matrox:cap:meta:layer_compatibility_groups": [
                    1
                ],
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 0,
                "urn:x-nmos:cap:format:color_sampling": {
                    "enum": [
                        "YCbCr-4:2:0",
                        "YCbCr-4:4:4"
                    ]
                },
                "urn:x-nmos:cap:format:transfer_characteristic": {
                    "enum": [
                        "SDR"
                    ]
                },
                "urn:x-nmos:cap:format:colorspace": {
                    "enum": [
                        "BT709",
                        "BT2020"
                    ]
                },
                "urn:x-nmos:cap:format:component_depth": {
                    "enum": [
                        8,
                        10
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "Main10",
                        "Main10-444",
                        "Main10Intra",
                        "Main10Intra-444"
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "video/H265"
                    ]
                },
                "urn:x-nmos:cap:format:interlace_mode": {
                    "enum": [
                        "progressive"
                    ]
                },
                "urn:x-nmos:cap:format:frame_width": {
                    "enum": [
                        640,
                        1280,
                        1920
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "Main-3",
                        "Main-3.1",
                        "Main-4",
                        "High-4",
                        "Main-4.1",
                        "High-4.1",
                        "Main-5",
                        "High-5",
                        "Main-5.1",
                        "High-5.1",
                        "Main-5.2",
                        "High-5.2",
                        "Main-6",
                        "High-6",
                        "Main-6.1",
                        "High-6.1",
                        "Main-6.2",
                        "High-6.2"
                    ]
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false,
                        true
                    ]
                },
                "urn:x-nmos:cap:format:grain_rate": {
                    "enum": [
                        {
                            "numerator": 24,
                            "denominator": 1
                        },
                        {
                            "numerator": 60,
                            "denominator": 1
                        },
                        {
                            "numerator": 6000,
                            "denominator": 1001
                        },
                        {
                            "numerator": 30,
                            "denominator": 1
                        },
                        {
                            "numerator": 3000,
                            "denominator": 1001
                        }
                    ]
                },
                "urn:x-nmos:cap:format:frame_height": {
                    "enum": [
                        360,
                        720,
                        1080
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "minimum": 6000,
                    "maximum": 4000000
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "RAW sub-constraints",
                "urn:x-matrox:cap:meta:format": "urn:x-nmos:format:video",
                "urn:x-matrox:cap:meta:layer": 0,
                "urn:x-matrox:cap:meta:layer_compatibility_groups": [
                    0
                ],
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 0,
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "video/raw"
                    ]
                },
                "urn:x-nmos:cap:format:frame_height": {
                    "enum": [
                        480,
                        720,
                        1080,
                        2160
                    ]
                },
                "urn:x-nmos:cap:format:colorspace": {
                    "enum": [
                        "BT601",
                        "BT709",
                        "BT2020"
                    ]
                },
                "urn:x-nmos:cap:format:color_sampling": {
                    "enum": [
                        "YCbCr-4:2:2"
                    ]
                },
                "urn:x-nmos:cap:format:interlace_mode": {
                    "enum": [
                        "progressive"
                    ]
                },
                "urn:x-nmos:cap:format:grain_rate": {
                    "enum": [
                        {
                            "numerator": 24,
                            "denominator": 1
                        },
                        {
                            "numerator": 30,
                            "denominator": 1
                        },
                        {
                            "numerator": 3000,
                            "denominator": 1001
                        },
                        {
                            "numerator": 60,
                            "denominator": 1
                        },
                        {
                            "numerator": 6000,
                            "denominator": 1001
                        }
                    ]
                },
                "urn:x-nmos:cap:format:frame_width": {
                    "enum": [
                        720,
                        1280,
                        1920,
                        3840
                    ]
                },
                "urn:x-nmos:cap:format:transfer_characteristic": {
                    "enum": [
                        "SDR"
                    ]
                },
                "urn:x-nmos:cap:format:component_depth": {
                    "enum": [
                        8
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "AAC stereo sub-constraints",
                "urn:x-matrox:cap:meta:format": "urn:x-nmos:format:audio",
                "urn:x-matrox:cap:meta:layer": 0,
                "urn:x-matrox:cap:meta:layer_compatibility_groups": [
                    1
                ],
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 1,
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false,
                        true
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "audio/mpeg4-generic"
                    ]
                },
                "urn:x-nmos:cap:format:sample_rate": {
                    "enum": [
                        {
                            "numerator": 48000,
                            "denominator": 1
                        }
                    ]
                },
                "urn:x-nmos:cap:format:channel_count": {
                    "enum": [
                        2
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "Main",
                        "Natural",
                        "LowDelayAAC",
                        "LowDelayAACv2"
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "1"
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "maximum": 576
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "AAC multi-channels sub-constraints",
                "urn:x-matrox:cap:meta:format": "urn:x-nmos:format:audio",
                "urn:x-matrox:cap:meta:layer": 0,
                "urn:x-matrox:cap:meta:layer_compatibility_groups": [
                    1
                ],
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 0,
                "urn:x-nmos:cap:format:channel_count": {
                    "enum": [
                        2,
                        6
                    ]
                },
                "urn:x-nmos:cap:format:profile": {
                    "enum": [
                        "HighQuality",
                        "AAC",
                        "HighEfficiencyAAC",
                        "HighEfficiencyAACv2"
                    ]
                },
                "urn:x-nmos:cap:format:level": {
                    "enum": [
                        "4"
                    ]
                },
                "urn:x-nmos:cap:format:bit_rate": {
                    "maximum": 1728
                },
                "urn:x-matrox:cap:format:constant_bit_rate": {
                    "enum": [
                        false,
                        true
                    ]
                },
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "audio/mpeg4-generic"
                    ]
                },
                "urn:x-nmos:cap:format:sample_rate": {
                    "enum": [
                        {
                            "numerator": 48000,
                            "denominator": 1
                        }
                    ]
                }
            },
            {
                "urn:x-nmos:cap:meta:label": "PCM sub-constraints",
                "urn:x-matrox:cap:meta:format": "urn:x-nmos:format:audio",
                "urn:x-matrox:cap:meta:layer": 0,
                "urn:x-matrox:cap:meta:layer_compatibility_groups": [
                    0
                ],
                "urn:x-nmos:cap:meta:enabled": true,
                "urn:x-nmos:cap:meta:preference": 0,
                "urn:x-nmos:cap:format:media_type": {
                    "enum": [
                        "audio/L16",
                        "audio/L24"
                    ]
                },
                "urn:x-nmos:cap:format:channel_count": {
                    "enum": [
                        2,
                        6,
                        8
                    ]
                },
                "urn:x-nmos:cap:format:sample_depth": {
                    "enum": [
                        16,
                        24
                    ]
                },
                "urn:x-nmos:cap:format:sample_rate": {
                    "enum": [
                        {
                            "numerator": 48000,
                            "denominator": 1
                        }
                    ]
                }
            }
        ]
    }
}
'''


currentAudio = CapSet(
    label="Current Audio",
    preference=100,
    caps=make_capset(
        Capability(CapFormatMediaType, RangeValue(("audio/mpeg4-generic",))),
        Capability(CapFormatProfile, RangeValue(("AAC",))),
        Capability(CapFormatLevel, RangeValue(("2",))),
        Capability(CapFormatChannelCount, RangeValue((2,))),
        Capability(CapFormatConstantBitRate, RangeValue((True,))),
        Capability(CapFormatSampleRate, RangeValue((Fraction(48000, 1),))),
        Capability(CapFormatBitRate, RangeValue((128,))),
        Capability(CapTransportParameterSetsFlowMode, RangeValue(("strict",))),
        Capability(CapTransportPacketTransmissionMode, RangeValue(("non_interleaved_access_units",))),
        Capability(CapTransportParameterSetsTransportMode, RangeValue(("out_of_band",))),
    )
)

currentVideo = CapSet(
    label="Current Video",
    preference=100,
    caps=make_capset(
        Capability(CapFormatMediaType, RangeValue(("video/H264",))),
        Capability(CapFormatProfile, RangeValue(("High-422",))),
        Capability(CapFormatLevel, RangeValue(("4",))),
        Capability(CapFormatFrameWidth, RangeValue((1920,))),
        Capability(CapFormatFrameHeight, RangeValue((1080,))),
        Capability(CapFormatComponentDepth, RangeValue((10,))),
        Capability(CapFormatColorSampling, RangeValue(("YCbCr-4:2:2",))),
        Capability(CapFormatInterlaceMode, RangeValue(("progressive",))),
        Capability(CapFormatGrainRate, RangeValue((Fraction(60, 1),))),
        Capability(CapFormatColorspace, RangeValue(("BT709",))),
        Capability(CapFormatConstantBitRate, RangeValue((False,))),
        Capability(CapFormatBitRate, RangeValue((40000,))),
        Capability(CapFormatTransferCharacteristic, RangeValue(("SDR",))),
        Capability(CapTransportParameterSetsTransportMode, RangeValue(("in_and_out_of_band",))),
        Capability(CapTransportParameterSetsFlowMode, RangeValue(("strict",))),
        Capability(CapTransportPacketTransmissionMode, RangeValue(("non_interleaved_nal_units",))),
    )
)

nextVideo = CapSet(
    label="Next Video",
    preference=100,
    caps=make_capset(
        Capability(CapFormatMediaType, RangeValue(("video/H264",))),
        Capability(CapFormatProfile, RangeValue(("High-422",))),
        Capability(CapFormatLevel, RangeValue(("4",))),
        Capability(CapFormatFrameWidth, RangeValue((1920 * 2,))),
        Capability(CapFormatFrameHeight, RangeValue((1080 * 2,))),
        Capability(CapFormatComponentDepth, RangeValue((10,))),
        Capability(CapFormatColorSampling, RangeValue(("YCbCr-4:2:2",))),
        Capability(CapFormatInterlaceMode, RangeValue(("progressive",))),
        Capability(CapFormatGrainRate, RangeValue((Fraction(60, 1),))),
        Capability(CapFormatColorspace, RangeValue(("BT709",))),
        Capability(CapFormatConstantBitRate, RangeValue((False,))),
        Capability(CapFormatBitRate, RangeValue((40000,))),
        Capability(CapFormatTransferCharacteristic, RangeValue(("SDR",))),
        Capability(CapTransportParameterSetsTransportMode, RangeValue(("in_and_out_of_band",))),
        Capability(CapTransportParameterSetsFlowMode, RangeValue(("strict",))),
        Capability(CapTransportPacketTransmissionMode, RangeValue(("non_interleaved_nal_units",))),
    )
)

caps_ndi_sender = convert_caps_json_to_caps(json.loads(ndi_sender))
caps_mp2t_sender = convert_caps_json_to_caps(json.loads(mp2t_sender))
caps_video_sender = convert_caps_json_to_caps(json.loads(video_sender))
caps_audio_sender = convert_caps_json_to_caps(json.loads(audio_sender))
caps_compressed_video_sender = convert_caps_json_to_caps(json.loads(compressed_video_sender))
caps_compressed_audio_sender = convert_caps_json_to_caps(json.loads(compressed_audio_sender))
caps_ndi_receiver = convert_caps_json_to_caps(json.loads(ndi_receiver))
caps_mp2t_receiver = convert_caps_json_to_caps(json.loads(mp2t_receiver))
caps_video_receiver = convert_caps_json_to_caps(json.loads(video_receiver))
caps_audio_receiver = convert_caps_json_to_caps(json.loads(audio_receiver))
caps_compressed_video_receiver = convert_caps_json_to_caps(json.loads(compressed_video_receiver))
caps_compressed_audio_receiver = convert_caps_json_to_caps(json.loads(compressed_audio_receiver))

def show_data():
    print("available data")
    print({k for k, v in globals().items() if re.compile(r"^.+_sender$").match(k)}) 
    print({k for k, v in globals().items() if re.compile(r"^.+_receiver$").match(k)}) 

pcmAudio = ConSet(
    label="PCM Audio",
    preference=100,
    cons=make_conset(
        Constraint(CapFormatMediaType, RangeValue(("audio/L24",))),
        Constraint(CapFormatChannelCount, RangeValue((2,))),
        Constraint(CapFormatSampleRate, RangeValue((Fraction(48000, 1),))),
    )
)

am824Audio = ConSet(
    label="AM824 Audio",
    preference=100,
    cons=make_conset(
        Constraint(CapFormatMediaType, RangeValue(("audio/AM824",))),
        Constraint(CapFormatChannelCount, RangeValue((2,))),
        Constraint(CapFormatSampleRate, RangeValue((Fraction(48000, 1),))),
    )
)

