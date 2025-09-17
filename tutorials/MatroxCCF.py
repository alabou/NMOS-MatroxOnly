#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2025, Matrox Graphics Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions, and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions, and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
  
""" Constraint-Capability Framework (CCF)

Implements all the major concepts and operators from the underlying constraint/capability formalism:

 - RangeValue (finite, infinite, empty, typed)
 - Capability, Constraint
 - CapSet (map of capabilities), ConSet (map of constraints)
 - Caps (array of CapSet), Cons (array of ConSet)
 - Operators:
   1) x <- y     (inheritance)
   2) x << y     (constriction)
   3) x <& y     (constriction with adjustment)
   4) x & y      (intersection)
   5) x <= y     (inclusion)
   6) NS(x) = {} <- x  (namespace extraction)
   7) {x}, {y}, {} (empty or partial namespace)
   8) typed NUL ([1.0 ... 0.0]), typed INF, etc.

In the __main__ we include tests that illustrate how each operation works.

"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Set, List, Union, Dict, Tuple, Any
from fractions import Fraction
import enum

FormatAudio = "urn:x-nmos:format:audio"
FormatVideo = "urn:x-nmos:format:video"
FormatData = "urn:x-nmos:format:data"
FormatMux = "urn:x-nmos:format:mux"

CapFormatMediaType = "urn:x-nmos:cap:format:media_type"
CapFormatEventType = "urn:x-nmos:cap:format:event_type"
CapFormatGrainRate = "urn:x-nmos:cap:format:grain_rate"
CapFormatFrameWidth = "urn:x-nmos:cap:format:frame_width"
CapFormatFrameHeight = "urn:x-nmos:cap:format:frame_height"
CapFormatInterlaceMode = "urn:x-nmos:cap:format:interlace_mode"
CapFormatColorspace = "urn:x-nmos:cap:format:colorspace"
CapFormatTransferCharacteristic = "urn:x-nmos:cap:format:transfer_characteristic"
CapFormatColorSampling = "urn:x-nmos:cap:format:color_sampling"
CapFormatComponentDepth = "urn:x-nmos:cap:format:component_depth"
CapFormatChannelCount = "urn:x-nmos:cap:format:channel_count"
CapFormatSampleRate = "urn:x-nmos:cap:format:sample_rate"
CapFormatSampleDepth = "urn:x-nmos:cap:format:sample_depth"
CapFormatBitRate = "urn:x-nmos:cap:format:bit_rate"
CapFormatProfile = "urn:x-nmos:cap:format:profile"
CapFormatLevel = "urn:x-nmos:cap:format:level"
CapFormatSublevel = "urn:x-nmos:cap:format:sublevel"
CapFormatConstantBitRate = "urn:x-matrox:cap:format:constant_bit_rate"
CapFormatVideoLayers = "urn:x-matrox:cap:format:video_layers"
CapFormatAudioLayers = "urn:x-matrox:cap:format:audio_layers"
CapFormatDataLayers = "urn:x-matrox:cap:format:data_layers"
CapTransportBitRate = "urn:x-nmos:cap:transport:bit_rate"
CapTransportPacketTime = "urn:x-nmos:cap:transport:packet_time"
CapTransportMaxPacketTime = "urn:x-nmos:cap:transport:max_packet_time"
CapTransport_ST2110_21_SenderType = "urn:x-nmos:cap:transport:st2110_21_sender_type"
CapTransportPacketTransmissionMode = "urn:x-nmos:cap:transport:packet_transmission_mode"
CapTransportParameterSetsFlowMode = "urn:x-matrox:cap:transport:parameter_sets_flow_mode"
CapTransportParameterSetsTransportMode = "urn:x-matrox:cap:transport:parameter_sets_transport_mode"
CapTransportChannelOrder = "urn:x-matrox:cap:transport:channel_order"
CapTransportHkep = "urn:x-matrox:cap:transport:hkep"
CapTransportPrivacy = "urn:x-matrox:cap:transport:privacy"
CapTransportClockRefType = "urn:x-matrox:cap:transport:clock_ref_type"
CapTransportInfoBlock = "urn:x-matrox:cap:transport:info_block"
CapTransportSynchronousMedia = "urn:x-matrox:cap:transport:synchronous_media"

CapMetaLabel = "urn:x-nmos:cap:meta:label"
CapMetaPreference = "urn:x-nmos:cap:meta:preference"
CapMetaFormat = "urn:x-matrox:cap:meta:format"
CapMetaLayer = "urn:x-matrox:cap:meta:layer"
CapMetaLayerCompatibilityGroups = "urn:x-matrox:cap:meta:layer_compatibility_groups"

def Namespace(*names: str) -> Set[str]:
    return set(names)

def _pretty_format(obj, indent=2, level=0, skip_key=False): # type: ignore
    """
    Pretty formats a nested dictionary, list, or custom objects like CapSet and ConSet
    with specified indentation.
    """
    spacing = ' ' * (indent * level)

    # Handle CapSet and ConSet explicitly
    if isinstance(obj, (CapSet, ConSet)):
        return str(obj).replace("\n", f"\n{' ' * (indent * level)}")

    # Handle dictionary
    if isinstance(obj, dict):
        if not skip_key:
            items = [f"{spacing}{' ' * indent}{repr(k)}: {_pretty_format(v, indent, level + 1, skip_key)}" for k, v in obj.items()] # type: ignore
        else:
            items = [f"{spacing}{' ' * indent}{_pretty_format(v, indent, level + 1, skip_key)}" for v in obj.values()] # type: ignore
        return "{\n" + ",\n".join(items) + f"\n{spacing}}}"

    # Handle list
    elif isinstance(obj, list):
        items = [f"{spacing}{' ' * indent}{_pretty_format(v, indent, level + 1, skip_key)}" for v in obj] # type: ignore
        return "[\n" + ",\n".join(items) + f"\n{spacing}]"

    # Default for other types
    else:
        return str(obj) # type: ignore

# -----------------------------------------------------------------------------
# 1) RangeType
# -----------------------------------------------------------------------------

class RangeType(enum.Enum):
    UNTYPED  = 0
    BOOL     = 1
    STRING   = 2
    INT      = 3
    FLOAT    = 4
    RATIONAL = 5

    def __str__(self) -> str:
        return self.name

def _coerce_value_to_type(v: Union[bool, int, float, Fraction, str], type:RangeType ) ->  Union[bool, int, float, Fraction, str]:

    if type == RangeType.BOOL:
        return bool(v)
    elif type == RangeType.INT:
        return int(v)
    elif type == RangeType.FLOAT:
        return float(v)
    elif type == RangeType.RATIONAL:
        return Fraction(v)
    elif type == RangeType.STRING:
        return str(v)
    
    return v

# -----------------------------------------------------------------------------
# 2) RangeValue
# -----------------------------------------------------------------------------

@dataclass
class RangeValue:
    """
    Represents a range which can be:
      - empty (NUL) (typed or unknown)
      - infinite (INF) (typed or unknown)
      - typed [min ... max], [.. max], [min ..]
      - typed enumeration

    Also:
      - no [min ... max], [.. max], [min ..] for STRING and BOOL
      - automatic typed NUL => min>max
      - automatic unknown INF if min, max and values are None
      - values being None or empty does not generate NUL
      - values if not None must not be empty. It is invalid according to formalism.

    Note: Inclusion and intersections are implemented as if both sides are capabilities.

    Note: When [min ... max], [.. max] or [min ..] is provided along with enumerated values,
          the inclusion test of a value in that range must be satisfied by both the range and
          the enumerated values. This may be counter intuitive that v = 5 is not included in 
          a range [1 .. 10, 1, 2, 8]. Either a range or an enumeration should be used.
    """
    infinite: bool = False
    empty: bool = False
    type: RangeType = RangeType.UNTYPED
    min: Optional[Union[int, float, Fraction]] = None
    max: Optional[Union[int, float, Fraction]] = None
    values: Optional[Tuple[Union[bool, int, float, Fraction, str], ...]] = None
    enumerated: Set[Union[bool, int, float, Fraction, str]] = field(default_factory=set, init=False)

    def __init__(
        self,
        values: Optional[Tuple[Union[bool, int, float, Fraction, str], ...]] = None,
        infinite: bool = False,
        empty: bool = False,
        type: RangeType = RangeType.UNTYPED,
        min: Optional[Union[int, float, Fraction]] = None,
        max: Optional[Union[int, float, Fraction]] = None,
    ):
        if infinite and empty:
            raise ValueError(
                f"Cannot have infinite and empty range at the same time."
            )

        # special case: automatic INF
        if not empty and values is None and min is None and max is None:
            infinite = True

        self.infinite = infinite
        self.empty = empty
        self.type = type
        self.min = min
        self.max = max
        self.enumerated = set(values) if values is not None else set()
        self.values = values # keep to know about None

        # Infer type if not specified
        if self.type == RangeType.UNTYPED:
            self._infer_type_from_data()

        # Convert min, max, enumerated to declared type if typed
        self._coerce_to_type()

        # No sub-range for STRING or BOOL
        if (self.type in [RangeType.STRING, RangeType.BOOL]) and (self.min is not None or self.max is not None):
            raise ValueError(
                f"No sub-range allowed for type={self.type.name}. "
                f"Got min={self.min}, max={self.max}."
            )

        # An untyped range cannot have enumerated values
        if self.type == RangeType.UNTYPED and self.enumerated:
            raise ValueError(
                f"Cannot have enumerated values {self.enumerated} for an untyped range."
            )

        # Post init final checks
        self.__post_init__()

    def __str__(self) -> str:

        suffix = ""

        if self.type == RangeType.UNTYPED:
            suffix = ""
        elif self.type == RangeType.BOOL:
            suffix = "b"
        elif self.type == RangeType.STRING:
            suffix = "s"
        elif self.type == RangeType.INT:
            suffix = "i"
        elif self.type == RangeType.FLOAT:
            suffix = "f"
        elif self.type == RangeType.RATIONAL:
            suffix = "r"
        else:
            raise ValueError("invalid type")

        if self.infinite:
            return f"INF{suffix}"
        elif self.empty:
            return f"NUL{suffix}"

        if self.min is not None and self.max is not None:
            return f"[ {self.min} .. {self.max} {', '.join(str(v) for v in self.enumerated)}]{suffix}"
        elif self.min is None and self.max is not None:
            return f"[ .. {self.max} {', '.join(str(v) for v in self.enumerated)}]{suffix}"
        elif self.min is not None and self.max is None:
            return f"[ {self.min} .. {', '.join(str(v) for v in self.enumerated)}]{suffix}"

        return f"[{', '.join(str(v) for v in self.enumerated)}]{suffix}"

    def _infer_type_from_data(self):

        # if a type is specified keeps it
        if self.type != RangeType.UNTYPED:
            return

        # favor min/max over enumerated values
        if (self.min is not None or self.max is not None):
            # pick min or max
            probe = self.min if self.min is not None else self.max
        elif self.enumerated:
            # pick first value
            probe = next(iter(self.enumerated))
        else:
            # pick nothing
            probe = None

        if isinstance(probe, bool):
            self.type = RangeType.BOOL
        elif isinstance(probe, int):
            self.type = RangeType.INT
        elif isinstance(probe, float):
            self.type = RangeType.FLOAT
        elif isinstance(probe, Fraction):
            self.type = RangeType.RATIONAL
        elif isinstance(probe, str):
            self.type = RangeType.STRING
        else:
            self.type = RangeType.UNTYPED

    def _coerce_to_type(self):

        if self.type == RangeType.INT:

            # If min/max are floats or rationals that are not integral,
            # raising ValueError ensures we don't break cardinality.
            if self.min is not None and not float(self.min).is_integer():
                raise ValueError(
                    f"Cannot coerce min={self.min} (float/rational) into an integer sub-range."
                )
            if self.max is not None and not float(self.max).is_integer():
                raise ValueError(
                    f"Cannot coerce max={self.max} (float/rational) into an integer sub-range."
                )

            if self.min is not None:
                self.min = int(self.min)
            if self.max is not None:
                self.max = int(self.max)
            self.enumerated = {int(v) for v in self.enumerated}

        elif self.type == RangeType.FLOAT:
            if self.min is not None:
                self.min = float(self.min)
            if self.max is not None:
                self.max = float(self.max)
            self.enumerated = {float(v) for v in self.enumerated}

        elif self.type == RangeType.RATIONAL:
            if self.min is not None:
                self.min = Fraction(self.min)
            if self.max is not None:
                self.max = Fraction(self.max)
            self.enumerated = {Fraction(v) for v in self.enumerated}

        elif self.type == RangeType.BOOL:
            if self.min is not None or self.max is not None:
                raise ValueError("range cannot be of types STRING or BOOL")
            self.enumerated = {bool(v) for v in self.enumerated}

        elif self.type == RangeType.STRING:
            if self.min is not None or self.max is not None:
                raise ValueError("range cannot be of types STRING or BOOL")
            self.enumerated = {str(v) for v in self.enumerated}

    def __post_init__(self):
        # If infinite => ignore everything else
        if self.infinite:
            self.empty = False
            self.min = None
            self.max = None
            self.values = None
            self.enumerated.clear()

        # If empty => ignore everything else
        elif self.empty:
            self.infinite = False
            self.min = None
            self.max = None
            self.values = None
            self.enumerated.clear()

        # automatic NUL => if min>max => empty
        elif self.min is not None and self.max is not None and self.min > self.max:
            self.empty = True
            self.infinite = False
            self.min = None
            self.max = None
            self.values = None
            self.enumerated.clear()

        # Verify that enumerated values are in [min..max] or [min..] or [..max].
        if not self.infinite and not self.empty and self.enumerated:
            if self.min is not None and self.max is not None:
                invalid_vals = {v for v in self.enumerated if not isinstance(v, bool) and not isinstance(v, str) and not (self.min <= v <= self.max)}
            elif self.min is not None and self.max is None:
                invalid_vals = {v for v in self.enumerated if not isinstance(v, bool) and not isinstance(v, str) and not (self.min <= v)}
            elif self.min is None and self.max is not None:
                invalid_vals = {v for v in self.enumerated if not isinstance(v, bool) and not isinstance(v, str) and  not (v <= self.max)}
            else:
                invalid_vals = None

            if invalid_vals:
                raise ValueError(f"Enumerated values {invalid_vals} are out of [min, max] or [min..] or [..max]")

    def is_infinite(self) -> bool:
        return self.infinite

    def is_empty(self) -> bool:
        return self.empty

    def has_enum_exception(self) -> bool:
        return self.values is not None and len(self.values) == 0
    
    def includes_value(self, val: Union[bool, int, float, Fraction, str]) -> bool:
        """Used to test membership."""

        _verify_value_type(self, val)

        if self.empty:
            return False
        if self.infinite:
            return True

        if not isinstance(val, bool) and not isinstance(val, str):
            if self.min is not None and val < self.min:
                return False
            if self.max is not None and val > self.max:
                return False

        if val not in self.enumerated and self.values is not None:
            return False

        return True

    def includes_range(self, other: RangeValue) -> bool:
        """
        x <= y for RangeValue (other <= self).
        Means: every value in x is included in y.
        """
        _verify_same_type(self, other)

        if other.empty:
            return True
        if self.empty:
            return False # self not empty
        if self.is_infinite():
            return True
        if other.is_infinite() and not self.is_infinite():
            return False

        if other.min is not None:
            if self.min is not None and other.min < self.min:
                return False
            if self.max is not None and other.min > self.max:
                return False
            if other.type == RangeType.INT:
                if self.values is not None and other.max is None:
                    return False
            else:
                if self.values is not None:
                    return False

        if other.max is not None:
            if self.min is not None and other.max < self.min:
                return False
            if self.max is not None and other.max > self.max:
                return False
            if other.type == RangeType.INT:
                if self.values is not None and other.min is None:
                    return False
            else:
                if self.values is not None:
                    return False

        if other.type == RangeType.INT:
            if other.min is not None and other.max is not None and self.values is not None:
                for v in range(int(other.min), int(other.max+1)):
                    if v not in self.enumerated:
                        return False

        if other.values is not None:
            for v in other.enumerated:
                if not isinstance(v, bool) and not isinstance(v, str):
                    if self.min is not None and v < self.min:
                        return False
                    if self.max is not None and v > self.max:
                        return False
                if v not in self.enumerated and self.values is not None:
                    return False

        return True

    def intersection(self, other: RangeValue) -> RangeValue:
        """x & y for RangeValue => intersection"""
        _verify_same_type(self, other)

        new_type = self.type if self.type != RangeType.UNTYPED else other.type

        if self.is_empty() or other.is_empty():
            # Intersection with empty => empty
            return RangeValue(empty=True, type=new_type)

        if self.is_infinite() and other.is_infinite():
            return RangeValue(infinite=True, type=new_type)

        if self.is_infinite():
            # intersection => other's finite side
            return RangeValue(
                infinite=other.infinite,
                empty=other.empty,
                type=new_type,
                min=other.min,
                max=other.max,
                values=other.values
            )
        
        if other.is_infinite():
            return RangeValue(
                infinite=self.infinite,
                empty=self.empty,
                type=new_type,
                min=self.min,
                max=self.max,
                values=self.values
            )

        min = None
        max = None

        # 1) check min
        if self.min is not None:
            if other.min is not None:
                if self.min < other.min:
                    min = other.min
                else:
                    min = self.min
            else:
                min = self.min
        else:
            if other.min is not None:
                min = other.min

        # 2) check max
        if self.max is not None:
            if other.max is not None:
                if self.max > other.max:
                    max = other.max
                else:
                    max = self.max
            else:
                max = self.max
        else:
            if other.max is not None:
                max = other.max

    	# Intersecting the range first may be enough to call it EMPTY
        if min is not None and max is not None and min > max:
            return RangeValue(empty=True, type=new_type)

        # 3) check enum
        if self.values is None and other.values is None:
            return RangeValue(type=new_type, min=min, max=max,values=None)
        
        if self.values is None and other.values is not None:

            common : Set[bool | int | float | Fraction | str] = set()

            for v in other.enumerated:
                if isinstance(v, bool) or isinstance(v, str): # for static check only, bool and str do not have ranges
                    common.add(v)
                elif (min is None or v >= min) and (max is None or v <= max):
                    common.add(v)

            if not common:
                return RangeValue(empty=True, type=new_type)

            # discrete intersection with range result in discrete
            return RangeValue(type=new_type, min=None, max=None,values=tuple(common))

        if self.values is not None and other.values is None:

            common : Set[bool | int | float | Fraction | str] = set()

            for v in self.enumerated:
                if isinstance(v, bool) or isinstance(v, str): # for static check only, bool and str do not have ranges
                    common.add(v)
                elif (min is None or v >= min) and (max is None or v <= max):
                    common.add(v)

            if not common:
                return RangeValue(empty=True, type=new_type)

            # discrete intersection with range result in discrete
            return RangeValue(type=new_type, min=None, max=None,values=tuple(common))

        common : Set[bool | int | float | Fraction | str] = set()

        for v in self.enumerated.intersection(other.enumerated):
            if isinstance(v, bool) or isinstance(v, str): # for static check only, bool and str do not have ranges
                common.add(v)
            elif (min is None or v >= min) and (max is None or v <= max):
                common.add(v)

        if not common:
            return RangeValue(empty=True, type=new_type)

        # discrete intersection with range result in discrete
        return RangeValue(type=new_type, min=None, max=None,values=tuple(common))

# -----------------------------------------------------------------------------
# 3) Helper: verify_same_type
# -----------------------------------------------------------------------------

def _verify_same_type(r1: RangeValue, r2: RangeValue):
    """
    Raises ValueError if r1,r2 have incompatible types.
    The theory says:
     - If one or both is infinite/empty => it's okay
     - If either is UNTYPED => it's okay
     - Otherwise, they must have the same type
    """
    # if typed INF, the type must match
    if (r1.is_infinite() and r1.type == RangeType.UNTYPED) or (r2.is_infinite() and r2.type == RangeType.UNTYPED):
        return
    # if typed NUL, the type must match
    if (r1.is_empty() and r1.type == RangeType.UNTYPED) or (r2.is_empty() and r2.type == RangeType.UNTYPED):
        return
    if r1.type == RangeType.UNTYPED or r2.type == RangeType.UNTYPED:
        return
    if r1.type != r2.type:
        raise ValueError(
            f"Type mismatch: {r1.type.name} vs {r2.type.name}"
        )

def _verify_value_type(r1: RangeValue, v: Union[bool, int, float, Fraction, str]):
    # if typed INF, the type must match
    if (r1.is_infinite() and r1.type == RangeType.UNTYPED):
        return
    # if typed NUL, the type must match
    if (r1.is_empty() and r1.type == RangeType.UNTYPED):
        return
    
    if r1.type == RangeType.UNTYPED:
        return
    
    if r1.type == RangeType.BOOL and not isinstance(v, bool):
        raise ValueError(
            f"Type mismatch: {r1.type.name} vs {v}"
        )
    elif r1.type == RangeType.INT and not isinstance(v, int):
        raise ValueError(
            f"Type mismatch: {r1.type.name} vs {v}"
        )
    elif r1.type == RangeType.FLOAT and not isinstance(v, float):
        raise ValueError(
            f"Type mismatch: {r1.type.name} vs {v}"
        )
    elif r1.type == RangeType.RATIONAL and not isinstance(v, Fraction):
        raise ValueError(
            f"Type mismatch: {r1.type.name} vs {v}"
        )
    elif r1.type == RangeType.STRING and not isinstance(v, str):
        raise ValueError(
            f"Type mismatch: {r1.type.name} vs {v}"
        )

def _remove_prefix(s: str, prefixes: list[str]) -> str:
    for prefix in prefixes:
        if s.startswith(prefix):
            return s.removeprefix(prefix)
    return s

# -----------------------------------------------------------------------------
# 4) Capability, Constraint
# -----------------------------------------------------------------------------

@dataclass
class Capability:
    name: str
    value: RangeValue
    original: bool = False

    def __str__(self) -> str:
        prefixes = ["urn:x-nmos:cap:", "urn:x-matrox:cap:"]
        return f"Cap(name='{_remove_prefix(self.name, prefixes)}', value={self.value}{', original=True' if self.original else ''})"

Cap = Capability # type alias

@dataclass
class Constraint:
    name: str
    value: RangeValue
    original: bool = False

    def __str__(self) -> str:
        prefixes = ["urn:x-nmos:cap:", "urn:x-matrox:cap:"]
        return f"Con(name='{_remove_prefix(self.name, prefixes)}', value={self.value}{', original=True' if self.original else ''})"

Con = Constraint # type alias

# -----------------------------------------------------------------------------
# 5) CapSet, ConSet
# -----------------------------------------------------------------------------

@dataclass
class CapSet:
    caps: Dict[str, Capability] = field(default_factory=dict)

    preference: int = 0
    label: str = ""
    format: Optional[str] = None
    layer: Optional[int] = None
    layer_compatibility_groups: Optional[Set[int]] = None

    def __str__(self) -> str:
        return (
            f"CapSet(\n"
            f"  label={repr(self.label)},\n"
            f"  preference={self.preference},\n"
            f"  format={repr(self.format)},\n"
            f"  layer={repr(self.layer)},\n"
            f"  layer_compatibility_groups={repr(self.layer_compatibility_groups)},\n"
            f"  caps={_pretty_format(self.caps, indent=2, level=2, skip_key=True)}\n"
            f")"
        )
    
    def __getitem__(self, pname: str) -> Capability:
        if pname not in self.caps:
            return Capability(pname, RangeValue(infinite=True))
        return self.caps[pname]

    def __setitem__(self, pname: str, val: Union[Capability, RangeValue]):
        if isinstance(val, Capability):
            self.caps[pname] = val
        else:
            self.caps[pname] = Capability(pname, val)

    def namespace(self) -> Set[str]:
        return set(self.caps.keys())

    def check_part_valid(self):
        if (self.format is None) ^ (self.layer is None):
            ValueError(f"Invalid capset: CapSet with format={self.format}, layer={self.layer}")

    def is_same_part(self, other: Union[CapSet, ConSet]) -> bool:

        self.check_part_valid()
        other.check_part_valid()

        if (self.format != other.format) or (self.layer != other.layer):
            return False
        
        return True

    def to_conset(self) -> ConSet:
        # Create a new ConSet with the same meta-attributes
        conset = ConSet(
            preference=self.preference,
            label=self.label,
            format=self.format,
            layer=self.layer,
            layer_compatibility_groups=self.layer_compatibility_groups
        )
        # Copy each capability -> constraint
        for param_name, cap_obj in self.caps.items():
            # Rebuild a RangeValue. (Reusing the same reference is typically fine,
            # but often we copy to avoid any accidental side effects.)
            rv = RangeValue(
                infinite=cap_obj.value.infinite,
                empty=cap_obj.value.empty,
                type=cap_obj.value.type,
                min=cap_obj.value.min,
                max=cap_obj.value.max,
                values=cap_obj.value.values
            )
            # Add as a Constraint in this ConSet
            conset.cons[param_name] = Constraint(
                name=cap_obj.name,
                value=rv,
                original=cap_obj.original
            )

        return conset

def make_capset(*capabilities: Capability) -> Dict[str, Capability]:
    """Helper to build a caps dictionary from Capability objects."""
    return {cap.name: cap for cap in capabilities}

def make_conset(*constraints: Constraint) -> Dict[str, Constraint]:
    """Helper to build a caps dictionary from Capability objects."""
    return {con.name: con for con in constraints}

@dataclass
class ConSet:
    cons: Dict[str, Constraint] = field(default_factory=dict)

    preference: int = 0
    label: str = ""
    format: Optional[str] = None
    layer: Optional[int] = None
    layer_compatibility_groups: Optional[Set[int]] = None

    def __str__(self) -> str:
        return (
            f"ConSet(\n"
            f"  label={repr(self.label)},\n"
            f"  preference={self.preference},\n"
            f"  format={repr(self.format)},\n"
            f"  layer={repr(self.layer)},\n"
            f"  layer_compatibility_groups={repr(self.layer_compatibility_groups)},\n"
            f"  cons={_pretty_format(self.cons, indent=2, level=2, skip_key=True)}\n"
            f")"
        )
    
    def __getitem__(self, pname: str) -> Constraint:
        if pname not in self.cons:
            return Constraint(pname, RangeValue(infinite=True))
        return self.cons[pname]

    def __setitem__(self, pname: str, val: Union[Constraint, RangeValue]):
        if isinstance(val, Constraint):
            self.cons[pname] = val
        else:
            self.cons[pname] = Constraint(pname, val)

    def namespace(self) -> Set[str]:
        return set(self.cons.keys())

    def check_part_valid(self):
        if (self.format is None) ^ (self.layer is None):
            ValueError(f"Invalid capset: CapSet with format={self.format}, layer={self.layer}")

    def is_same_part(self, other: Union[CapSet, ConSet]) -> bool:

        self.check_part_valid()
        other.check_part_valid()

        if (self.format != other.format) or (self.layer != other.layer):
            return False
        
        return True

    def to_capset(self) -> CapSet:
        # Create a new ConSet with the same meta-attributes
        capset = CapSet(
            preference=self.preference,
            label=self.label,
            format=self.format,
            layer=self.layer,
            layer_compatibility_groups=self.layer_compatibility_groups
        )
        # Copy each capability -> constraint
        for param_name, con_obj in self.cons.items():
            # Rebuild a RangeValue. (Reusing the same reference is typically fine,
            # but often we copy to avoid any accidental side effects.)
            rv = RangeValue(
                infinite=con_obj.value.infinite,
                empty=con_obj.value.empty,
                type=con_obj.value.type,
                min=con_obj.value.min,
                max=con_obj.value.max,
                values=con_obj.value.values
            )
            # Add as a Constraint in this ConSet
            capset.caps[param_name] = Capability(
                name=con_obj.name,
                value=rv,
                original=con_obj.original
            )

        return capset

# -----------------------------------------------------------------------------
# 6) Caps, Cons
# -----------------------------------------------------------------------------

@dataclass
class Caps:
    capsets: List[CapSet] = field(default_factory=list)
    filtered: bool = False

    def __str__(self) -> str:
        capsets_str = _pretty_format(self.capsets, indent=2, level=1, skip_key=True)
        return (
            f"Caps(\n"
            f"  filtered={self.filtered},\n"
            f"  capsets={capsets_str}\n"
            f")"
        )

    def get_compatibility_groups(self) -> Set[int]:

        out : Set[int] = set() 

        for cs in self.capsets:

            cs.check_part_valid()

            # explicit ones
            if cs.layer_compatibility_groups is not None:
                out = out.union(cs.layer_compatibility_groups)

        # if none explicit then default to 63 to prevent users from thinking it is really a group 0 and not an ANY group.
        if not out:
            out = set([63])

        return out
    
    # Filtering by compatibility_group is independent of the other filters
    def _filter(self, format: Optional[str] = None, layer: Optional[int] = None, compatibility_group: Optional[int] = None, media_types: Optional[List[str]] = None, no_filter : bool = False) -> List[CapSet]:

        if format is not None and not isinstance(format, str): # type: ignore
            raise ValueError(f"Invalid format parameter, expected Optional[str]")
        if layer is not None and not isinstance(layer, int): # type: ignore
            raise ValueError(f"Invalid layer parameter, expected Optional[int]")
        if compatibility_group is not None and not isinstance(compatibility_group, int): # type: ignore
            raise ValueError(f"Invalid compatibility_group parameter, expected Optional[int]")
        if media_types is not None:
            if not isinstance(media_types, list) or not all(isinstance(item, str) for item in media_types): # type: ignore
                raise ValueError(f"Invalid media_types parameter, expected Optional[List[str]]")

        if format is not None and format not in (FormatVideo, FormatAudio, FormatData):
            raise ValueError(f"Invalid format parameter {format}, mus tbe one of {(FormatAudio, FormatVideo, FormatData)}")
        if layer is not None and layer < 0:
            raise ValueError(f"Invalid layer parameter {layer}, must be >= 0")

        if compatibility_group is not None and (format is not None or layer is not None or media_types is not None):
            raise ValueError(f"Filtering by compatibility group is exclusive to the use of other filter parameters")
        if compatibility_group is not None and (compatibility_group < 0 or compatibility_group > 63):
            raise ValueError(f"Invalid compatibility_group parameter {compatibility_group}, expected 0 <= compatibility_group <= 63")

        out : List[CapSet] = [] 

        for cs in self.capsets:

            cs.check_part_valid()

            if no_filter:
                out.append(cs)
            else:
                if compatibility_group is not None:

                    if cs.layer_compatibility_groups is None or compatibility_group in cs.layer_compatibility_groups:
                        out.append(cs)
                else:
                    
                    if (format is None and layer is None):
                        # trunk only
                        if cs.format is None and cs.layer is None:
                            if media_types is not None and CapFormatMediaType in cs.caps:
                                if any(t for t in media_types if cs.caps[CapFormatMediaType].value.includes_value(t)):
                                    out.append(cs)
                            else:
                                out.append(cs)
                    elif (format is not None and layer is None):
                        # leaves only
                        if cs.format == format:
                            out.append(cs)
                    elif (format is None and layer is not None):
                        # leaves only
                        if cs.layer == layer:
                            out.append(cs)
                    elif (format is not None and layer is not None):
                        # leaves only
                        if cs.format == format and cs.layer == layer:
                            out.append(cs)
                    else:
                        raise ValueError(f"Invalid filter: format={format}, layer={layer}")

        return out

    # Filtering by compatibility_group is independent of the other filters
    def get(self, format: Optional[str] = None, layer: Optional[int] = None, compatibility_group: Optional[int] = None, media_types: Optional[List[str]] = None, no_filter : bool = False) -> Caps:
        subset = self._filter(format, layer, compatibility_group, media_types, no_filter)
        subset.sort(key=lambda c: c.preference, reverse=True)
        return Caps(capsets=subset, filtered=True)

    # Filtering by compatibility_group is independent of the other filters
    def get_capset(self, format: Optional[str] = None, layer: Optional[int] = None, compatibility_group: Optional[int] = None, media_types: Optional[List[str]] = None, no_filter : bool = False, index: int = 0) -> CapSet:
        subset = self._filter(format, layer, compatibility_group, media_types, no_filter)
        subset.sort(key=lambda c: c.preference, reverse=True)
        if index<0 or index>=len(subset):
            raise IndexError(f"No matching CapSet for format={format}, layer={layer}, index={index}")
        return subset[index]

    def to_cons(self) -> Cons:
        """
        Cast each CapSet in this Caps into a ConSet, effectively
        interpreting the RangeValue 'INF' as 'unconstrained' 
        instead of 'supports all values'.

        Returns a new Cons object.
        """
        new_consets: List[ConSet] = []
        for capset in self.capsets:
            # Create a new ConSet with the same meta-attributes
            conset = ConSet(
                preference=capset.preference,
                label=capset.label,
                format=capset.format,
                layer=capset.layer,
                layer_compatibility_groups=capset.layer_compatibility_groups
            )
            # Copy each capability -> constraint
            for param_name, cap_obj in capset.caps.items():
                # Rebuild a RangeValue. (Reusing the same reference is typically fine,
                # but often we copy to avoid any accidental side effects.)
                rv = RangeValue(
                    infinite=cap_obj.value.infinite,
                    empty=cap_obj.value.empty,
                    type=cap_obj.value.type,
                    min=cap_obj.value.min,
                    max=cap_obj.value.max,
                    values=cap_obj.value.values
                )
                # Add as a Constraint in this ConSet
                conset.cons[param_name] = Constraint(
                    name=cap_obj.name,
                    value=rv,
                    original=cap_obj.original
                )
            new_consets.append(conset)

        return Cons(consets=new_consets, filtered=self.filtered)

    # trunk_namespace must be filled by the caller based on the expected format associated with the capabilities
    def normalize(
        self,
        audio_layers: Optional[int] = None,
        video_layers: Optional[int] = None,
        data_layers: Optional[int] = None,
        trunk_namespace: Optional[Set[str]] = None,
        audio_namespace: Optional[Set[str]] = None,
        video_namespace: Optional[Set[str]] = None,
        data_namespace: Optional[Set[str]] = None,
    ) -> "Caps":
        """
        Normalize this Caps according to the theory:
          - If audio_layers, video_layers, data_layers are all None => non-hierarchical.
            * No capset can have format/layer set, or raise an error.
          - Otherwise => hierarchical:
            * Must ensure trunk (format=None, layer=None).
            * For each format in {audio, video, data}, define layers in [0..N-1] if N>0.
              If N=0 => remove or disallow that format.
            * Disallow any layer >= N.
        
        Returns a NEW Caps instance with normalized definition.
        """
        if self.filtered:
            raise ValueError(f"This operation requires non-filtered Caps")

        # 1) Copy 'self' so we do not mutate the original
        new_caps = Caps(capsets=[
            CapSet(
                caps=dict(cs.caps),
                preference=cs.preference,
                label=cs.label,
                format=cs.format,
                layer=cs.layer,
                layer_compatibility_groups=cs.layer_compatibility_groups
            )
            for cs in self.capsets
        ])

        # 2) Check if hierarchical or non-hierarchical
        hierarchical = (audio_layers is not None or video_layers is not None or data_layers is not None)

        if not hierarchical:
            # Non-hierarchical => must not have format/layer
            for cs in new_caps.capsets:

                cs.check_part_valid()

                if cs.format is not None or cs.layer is not None:
                    raise ValueError(
                        f"Non-hierarchical: CapSet '{cs.label}' "
                        f"cannot have format={cs.format} or layer={cs.layer}."
                    )
                
            for cs in new_caps.capsets:

                cs.check_part_valid()

                for k in cs.caps.keys():
                    if trunk_namespace is not None and k not in trunk_namespace:
                        cs.caps.pop(k)
                        
            return new_caps

        # hierarchical => must ensure trunk
        trunk_list = [
            cs for cs in new_caps.capsets
            if cs.format is None and cs.layer is None
        ]

        if not trunk_list:
            trunk_capset = CapSet(
                preference=100,
                label="Trunk",
                format=None,
                layer=None
            )
            new_caps.capsets.append(trunk_capset)

        # Helper
        def ensure_format_layers(fmt: str, count: int):
            if count <= 0:
                # Remove all capsets that have this format
                new_capsets : List[CapSet] = []
                for cset in new_caps.capsets:
                    if cset.format == fmt:
                        # skip
                        continue
                    new_capsets.append(cset)
                new_caps.capsets = new_capsets
            else:
                # Ensure each layer in [0..count-1] is present
                for layer_id in range(count):
                    existing = [
                        cset for cset in new_caps.capsets
                        if cset.format == fmt and cset.layer == layer_id
                    ]
                    if not existing:
                        # create it
                        new_caps.capsets.append(
                            CapSet(
                                preference=100,
                                label=f"{fmt}{layer_id}",
                                format=fmt,
                                layer=layer_id
                            )
                        )
                # disallow any layer >= count
                keep : List[CapSet] = []
                for cset in new_caps.capsets:
                    if cset.format == fmt and cset.layer is not None:
                        if cset.layer >= count:
                            raise ValueError(
                                f"CapSet '{cset.label}' has layer={cset.layer} for format='{fmt}', "
                                f"but allowed layers are [0..{count-1}]."
                            )
                        else:
                            keep.append(cset)
                    else:
                        keep.append(cset)
                new_caps.capsets = keep

        # 3) Apply to each format
        ensure_format_layers(FormatAudio, audio_layers if audio_layers is not None else 0)
        ensure_format_layers(FormatVideo, video_layers if video_layers is not None else 0)
        ensure_format_layers(FormatData,  data_layers  if data_layers  is not None else 0)

        for cs in new_caps.capsets:

            cs.check_part_valid()

            for k in cs.caps.keys():
                if cs.format == FormatAudio:
                    if audio_namespace is not None and k not in audio_namespace:
                        cs.caps.pop(k)
                elif cs.format == FormatVideo:
                    if video_namespace is not None and k not in video_namespace:
                        cs.caps.pop(k)
                elif cs.format == FormatData:
                    if data_namespace is not None and k not in data_namespace:
                        cs.caps.pop(k)

        return new_caps        

@dataclass
class Cons:
    consets: List[ConSet] = field(default_factory=list)
    filtered: bool = False

    def __str__(self) -> str:
        consets_str = _pretty_format(self.consets, indent=2, level=1, skip_key=True)
        return (
            f"Cons(\n"
            f"  filtered={self.filtered},\n"
            f"  consets={consets_str}\n"
            f")"
        )
    
    def get_compatibility_groups(self) -> Set[int]:

        out : Set[int] = set() 

        for cs in self.consets:

            cs.check_part_valid()

            # explicit ones
            if cs.layer_compatibility_groups is not None:
                out = out.union(cs.layer_compatibility_groups)

        # if none explicit then default to 63 to prevent users from thinking it is really a group 0 and not an ANY group.
        if not out:
            out = set([63])

        return out
            
    # Filtering by compatibility_group is independent of the other filters
    def _filter(self, format: Optional[str] = None, layer: Optional[int] = None, compatibility_group: Optional[int] = None, media_types: Optional[str] = None, no_filter : bool = False) -> List[ConSet]:

        if format is not None and not isinstance(format, str): # type: ignore
            raise ValueError(f"Invalid format parameter, expected Optional[str]")
        if layer is not None and not isinstance(layer, int): # type: ignore
            raise ValueError(f"Invalid layer parameter, expected Optional[int]")
        if compatibility_group is not None and not isinstance(compatibility_group, int): # type: ignore
            raise ValueError(f"Invalid compatibility_group parameter, expected Optional[int]")
        if media_types is not None:
            if not isinstance(media_types, list) or not all(isinstance(item, str) for item in media_types): # type: ignore
                raise ValueError(f"Invalid media_types parameter, expected Optional[List[str]]")

        if format is not None and format not in (FormatVideo, FormatAudio, FormatData):
            raise ValueError(f"Invalid format parameter {format}, mus tbe one of {(FormatAudio, FormatVideo, FormatData)}")
        if layer is not None and layer < 0:
            raise ValueError(f"Invalid layer parameter {layer}, must be >= 0")

        if compatibility_group is not None and (format is not None or layer is not None or media_types is not None):
            raise ValueError(f"Filtering by compatibility group is exclusive to the use of other filter parameters")
        if compatibility_group is not None and (compatibility_group < 0 or compatibility_group > 63):
            raise ValueError(f"Invalid compatibility_group parameter {compatibility_group}, expected 0 <= compatibility_group <= 63")

        out : List[ConSet] = []
        for cs in self.consets:

            cs.check_part_valid()

            if no_filter:
                    out.append(cs)
            else:
                if compatibility_group is not None:

                    if cs.layer_compatibility_groups is None or compatibility_group in cs.layer_compatibility_groups:
                        out.append(cs)
                else:

                    if (format is None and layer is None):
                        # trunk only
                        if cs.format is None and cs.layer is None:
                            if media_types is not None and CapFormatMediaType in cs.cons:
                                if any(t for t in media_types if cs.cons[CapFormatMediaType].value.includes_value(t)):
                                    out.append(cs)
                            else:
                                out.append(cs)
                    elif (format is not None and layer is None):
                        if cs.format == format:
                            out.append(cs)
                    elif (format is not None and layer is not None):
                        # both format, layer
                        if cs.format == format and cs.layer == layer:
                            out.append(cs)
                    else:
                        raise ValueError(f"Invalid filter: format={format}, layer={layer}")

        return out

    # Filtering by compatibility_group is independent of the other filters
    def get(self, format: Optional[str] = None, layer: Optional[int] = None, compatibility_group: Optional[int] = None, media_types: Optional[str] = None, no_filter : bool = False) -> Cons:
        subset = self._filter(format, layer, compatibility_group, media_types, no_filter)
        subset.sort(key=lambda c: c.preference, reverse=True)
        return Cons(consets=subset, filtered=True)

    # Filtering by compatibility_group is independent of the other filters
    def get_conset(self, format: Optional[str] = None, layer: Optional[int] = None, compatibility_group: Optional[int] = None, media_types: Optional[str] = None, no_filter : bool = False, index: int = 0) -> ConSet:
        subset = self._filter(format, layer, compatibility_group, media_types, no_filter)
        subset.sort(key=lambda c: c.preference, reverse=True)
        if index<0 or index>=len(subset):
            raise IndexError(f"No matching ConSet for format={format}, layer={layer}, index={index}")
        return subset[index]

    def normalize(
        self,
        audio_layers: Optional[int] = None,
        video_layers: Optional[int] = None,
        data_layers: Optional[int] = None,
        trunk_namespace: Optional[Set[str]] = None,
        audio_namespace: Optional[Set[str]] = None,
        video_namespace: Optional[Set[str]] = None,
        data_namespace: Optional[Set[str]] = None,

    ) -> "Cons":
        """
        Normalize this Cons according to the same hierarchical vs. non-hierarchical
        theory as Caps.normalize(...).
        
        1) If audio_layers, video_layers, data_layers are all None => non-hierarchical:
        * No ConSet can have format/layer set, or we raise an error.
        2) Otherwise => hierarchical:
        * Must ensure we have a trunk ConSet (format=None, layer=None).
        * For each format in {audio, video, data}, define layers in [0..N-1] if N>0.
            If N=0 => remove or disallow that format/layer.
        * Disallow any layer >= N.
        
        Returns a NEW Cons instance with normalized definition.
        """
        if self.filtered:
            raise ValueError(f"This operation requires non-filtered Cons")

        # 1) Make a copy, so we don't mutate the original self.
        new_cons = Cons(consets=[
            ConSet(
                cons=dict(cs.cons),  # copy the dict of constraints
                preference=cs.preference,
                label=cs.label,
                format=cs.format,
                layer=cs.layer,
                layer_compatibility_groups=cs.layer_compatibility_groups
            )
            for cs in self.consets
        ])

        # 2) Decide if hierarchical or not
        hierarchical = (
            audio_layers is not None
            or video_layers is not None
            or data_layers is not None
        )

        if not hierarchical:
            # Non-hierarchical => must not have format/layer
            for cs in new_cons.consets:

                cs.check_part_valid()

                if cs.format is not None or cs.layer is not None:
                    raise ValueError(
                        f"Non-hierarchical: ConSet '{cs.label}' "
                        f"cannot have format={cs.format} or layer={cs.layer}."
                    )
                
            for cs in new_cons.consets:

                cs.check_part_valid()

                for k in cs.cons.keys():
                    if trunk_namespace is not None and k not in trunk_namespace:
                        cs.cons.pop(k)

            return new_cons

        # hierarchical => must ensure trunk
        trunk_list = [
            cs for cs in new_cons.consets
            if cs.format is None and cs.layer is None
        ]

        if not trunk_list:
            trunk_conset = ConSet(
                preference=100,
                label="Trunk",
                format=None,
                layer=None
            )
            new_cons.consets.append(trunk_conset)

        # Helper function to ensure or remove format-layers
        def ensure_format_layers(fmt: str, count: int):
            if count <= 0:
                # Remove all ConSet objects for this format
                filtered  : List[ConSet] = []
                for cset in new_cons.consets:
                    if cset.format == fmt:
                        # skip => removing
                        continue
                    filtered.append(cset)
                new_cons.consets = filtered
            else:
                # Ensure each layer in [0..count-1] is present
                for layer_id in range(count):
                    existing = [
                        cset for cset in new_cons.consets
                        if cset.format == fmt and cset.layer == layer_id
                    ]
                    if not existing:
                        new_cons.consets.append(
                            ConSet(
                                preference=100,
                                label=f"{fmt}{layer_id}",
                                format=fmt,
                                layer=layer_id
                            )
                        )
                
                # Disallow any layer >= count
                keep : List[ConSet] = []
                for cset in new_cons.consets:
                    if cset.format == fmt and cset.layer is not None:
                        if cset.layer >= count:
                            raise ValueError(
                                f"ConSet '{cset.label}' has layer={cset.layer} for format='{fmt}', "
                                f"but allowed layers are [0..{count-1}]."
                            )
                        else:
                            keep.append(cset)
                    else:
                        keep.append(cset)
                new_cons.consets = keep

        # 3) Apply to each format
        ensure_format_layers(FormatAudio, audio_layers if audio_layers is not None else 0)
        ensure_format_layers(FormatVideo, video_layers if video_layers is not None else 0)
        ensure_format_layers(FormatData,  data_layers  if data_layers  is not None else 0)

        for cs in new_cons.consets:

            cs.check_part_valid()

            for k in cs.cons.keys():
                if cs.format == FormatAudio:
                    if audio_namespace is not None and k not in audio_namespace:
                        cs.cons.pop(k)
                elif cs.format == FormatVideo:
                    if video_namespace is not None and k not in video_namespace:
                        cs.cons.pop(k)
                elif cs.format == FormatData:
                    if data_namespace is not None and k not in data_namespace:
                        cs.cons.pop(k)

        return new_cons

def caps_union(caps1: Caps, caps2: Caps) -> Caps:
    """
    Implements caps1 | caps2 (Union of Caps).
    Ensures that no two CapSets of the same layer:format pair collide.
    """
    capset_dict: Dict[Tuple[Optional[str], Optional[int]], CapSet] = {}
    
    for capset in caps1.capsets + caps2.capsets:

        capset.check_part_valid()

        key = (capset.format, capset.layer)

        if key in capset_dict:
            raise ValueError(f"Collision detected: CapSet with format={capset.format}, layer={capset.layer}")
        
        capset_dict[key] = capset
    
    return Caps(capsets=list(capset_dict.values()))

def cons_union(cons1: Cons, cons2: Cons) -> Cons:
    """
    Implements cons1 | cons2 (Union of Cons).
    Ensures that no two ConSets of the same layer:format pair collide.
    """
    conset_dict: Dict[Tuple[Optional[str], Optional[int]], ConSet] = {}    

    for conset in cons1.consets + cons2.consets:

        conset.check_part_valid()

        key = (conset.format, conset.layer)

        if key in conset_dict:
            raise ValueError(f"Collision detected: ConSet with format={conset.format}, layer={conset.layer}")
        
        conset_dict[key] = conset
    
    return Cons(consets=list(conset_dict.values()))

# -----------------------------------------------------------------------------
# 7) Operators
# -----------------------------------------------------------------------------

# (A) Inheritance: x <- y

def namespace_inherit_from_caps(x: Set[str], y_caps: Caps) -> Set[str]:
    """
    Implements {x} <- y_caps.

    BEGIN
    {r} = {x}
    for all capset in y_caps: {r} = {r} <- capset
    return {r}
    END
    """
    # Start with a copy of x
    r = x.copy()

    for capset in y_caps.capsets:

        capset.check_part_valid()

        r = namespace_inherit_from_capset(r, capset)

    return r

def namespace_inherit_from_capset(x: Set[str], y_capset: CapSet) -> Set[str]:
    """
    Implements {x} <- y_capset.

    BEGIN
    {r} = {x}
    for all cap in y_capset: {r} = {r} <- cap
    return {r}
    END
    """
    y_capset.check_part_valid()

    # Start with a copy of x
    r = x.copy()

    for cap in y_capset.caps.values():
        r = namespace_inherit_from_cap(r, cap)

    return r

def namespace_inherit_from_cap(x: Set[str], y_cap: Capability) -> Set[str]:
    """
    Implements {x} <- y_cap.

    BEGIN
    {r} = {x}
    {r} = {r} <- cap.name
    return {r}
    END
    """
    if y_cap.value.has_enum_exception():
        raise ValueError("capability enum cannot be empty if not None")

    # Start with a copy of x
    r = x.copy()
    r = namespace_inherit_from_name(r, y_cap.name)
    return r

def namespace_inherit_from_name(x: Set[str], name: str) -> Set[str]:
    """
    Implements {x} <- name.

    BEGIN
    {r} = {x}
    if name not in {r}:  add name to {r}
    return {r}
    END
    """
    # Start with a copy of x
    r = x.copy()
    if name not in r:
        r.add(name)
    return r

def namespace_inherit_from_cons(x: Set[str], y_cons: Cons) -> Set[str]:
    """
    Implements {x} <- y_cons.

    BEGIN
    {r} = {x}
    for all conset in y_cons: {r} = {r} <- conset
    return {r}
    END
    """
    # Start with a copy of x
    r = x.copy()

    for conset in y_cons.consets:

        conset.check_part_valid()

        r = namespace_inherit_from_conset(r, conset)

    return r

def namespace_inherit_from_conset(x: Set[str], y_conset: ConSet) -> Set[str]:
    """
    Implements {x} <- y_conset.

    BEGIN
    {r} = {x}
    for all con in y_conset: {r} = {r} <- con
    return {r}
    END
    """
    y_conset.check_part_valid()

    # Start with a copy of x
    r = x.copy()

    for con in y_conset.cons.values():
        r = namespace_inherit_from_con(r, con)

    return r

def namespace_inherit_from_con(x: Set[str], y_con: Constraint) -> Set[str]:
    """
    Implements {x} <- y_con.

    BEGIN
    {r} = {x}
    {r} = {r} <- con.name
    return {r}
    END
    """
    if y_con.value.has_enum_exception():
        raise ValueError("constraint enum cannot be empty if not None")
    
    # Start with a copy of x
    r = x.copy()
    r = namespace_inherit_from_name(r, y_con.name)
    return r

def capset_inherit_from_namespace(x_capset: CapSet, names: Set[str]) -> CapSet:
    """
    Implements x_capset <- {y}

    BEGIN
    r_capset = x_capset
    for all name in {y}: r_capset = r_capset <- name
    return r_capset
    END
    """
    x_capset.check_part_valid()

    result = CapSet(
        caps=dict(x_capset.caps),
        preference=x_capset.preference,
        label=x_capset.label,
        format=x_capset.format,
        layer=x_capset.layer,
        layer_compatibility_groups=x_capset.layer_compatibility_groups
    )
    for n in names:
        result = capset_inherit_from_name(result, n)

    return result

def capset_inherit_from_name(x_capset: CapSet, name: str) -> CapSet:
    """
    Implements x_capset <- name

    BEGIN
    r_capset = x_capset
    if name not in NS(x_capset): r_capset[name] = INF
    return r_capset
    END
    """
    x_capset.check_part_valid()

    result = CapSet(
        caps=dict(x_capset.caps),
        preference=x_capset.preference,
        label=x_capset.label,
        format=x_capset.format,
        layer=x_capset.layer,
        layer_compatibility_groups=x_capset.layer_compatibility_groups
    )
    if name not in result.caps:
        result.caps[name] = Capability(name, RangeValue(infinite=True))

    return result

def capset_inherit_from_capset(x_capset: CapSet, y_capset: CapSet) -> CapSet:
    """
    Implements x_capset <- y_capset

    BEGIN
    r_capset = x_capset
    for all cap in y_capset: r_capset = r_capset <- cap
    return r_capset
    END
    """
    result = CapSet(
        caps=dict(x_capset.caps),
        preference=x_capset.preference,
        label=x_capset.label,
        format=x_capset.format,
        layer=x_capset.layer,
        layer_compatibility_groups=x_capset.layer_compatibility_groups
    )

    if not x_capset.is_same_part(y_capset):
        return result

    for cap in y_capset.caps.values():
        result = capset_inherit_from_cap(result, cap)

    return result

def capset_inherit_from_cap(x_capset: CapSet, y_cap: Capability) -> CapSet:
    """
    Implements x_capset <- y_cap

    BEGIN
    r_capset = x_capset
    if y_cap.name not in NS(x_capset): r_capset[y_cap.name] = y_cap.value
    return r_capset
    END
    """
    x_capset.check_part_valid()

    if y_cap.value.has_enum_exception():
        raise ValueError("capability enum cannot be empty if not None")

    result = CapSet(
        caps=dict(x_capset.caps),
        preference=x_capset.preference,
        label=x_capset.label,
        format=x_capset.format,
        layer=x_capset.layer,
        layer_compatibility_groups=x_capset.layer_compatibility_groups
    )

    if y_cap.name not in result.namespace():
        result.caps[y_cap.name] = y_cap

    return result

def conset_inherit_from_namespace(x_conset: ConSet, names: Set[str]) -> ConSet:
    """
    Implements x_conset <- {y}

    BEGIN
    r_conset = x_conset
    for all name in {y}: r_conset = r_conset <- name
    return r_conset
    END
    """
    x_conset.check_part_valid()

    result = ConSet(
        cons=dict(x_conset.cons),
        preference=x_conset.preference,
        label=x_conset.label,
        format=x_conset.format,
        layer=x_conset.layer,
        layer_compatibility_groups=x_conset.layer_compatibility_groups
    )

    for n in names:
        result = conset_inherit_from_name(result, n)

    return result

def conset_inherit_from_name(x_conset: ConSet, name: str) -> ConSet:
    """
    Implements x_conset <- name

    BEGIN
    r_conset = x_conset
    if name not in NS(x_conset): r_conset[name] = INF
    return r_conset
    END
    """
    x_conset.check_part_valid()

    result = ConSet(
        cons=dict(x_conset.cons),
        preference=x_conset.preference,
        label=x_conset.label,
        format=x_conset.format,
        layer=x_conset.layer,
        layer_compatibility_groups=x_conset.layer_compatibility_groups
    )
    
    if name not in result.cons:
        result.cons[name] = Constraint(name, RangeValue(infinite=True))

    return result

def conset_inherit_from_conset(x_conset: ConSet, y_conset: ConSet) -> ConSet:
    """
    Implements x_conset <- y_conset

    BEGIN
    r_conset = x_conset
    for all con in y_conset: r_conset = r_conset <- con
    return r_conset
    END
    """
    result = ConSet(
        cons=dict(x_conset.cons),
        preference=x_conset.preference,
        label=x_conset.label,
        format=x_conset.format,
        layer=x_conset.layer,
        layer_compatibility_groups=x_conset.layer_compatibility_groups
    )

    if not x_conset.is_same_part(y_conset):
        return result

    for con in y_conset.cons.values():
        result = conset_inherit_from_con(result, con)
    return result

def conset_inherit_from_con(x_conset: ConSet, y_con: Constraint) -> ConSet:
    """
    Implements x_conset <- y_con

    BEGIN
    r_conset = x_conset
    if y_con.name not in NS(x_conset): r_conset[y_con.name] = y_con.value
    return r_conset
    END
    """
    x_conset.check_part_valid()

    if y_con.value.has_enum_exception():
        raise ValueError("constraint enum cannot be empty if not None")

    result = ConSet(
        cons=dict(x_conset.cons),
        preference=x_conset.preference,
        label=x_conset.label,
        format=x_conset.format,
        layer=x_conset.layer,
        layer_compatibility_groups=x_conset.layer_compatibility_groups
    )

    if y_con.name not in result.namespace():
        result.cons[y_con.name] = Constraint(name=y_con.name, value=y_con.value)

    return result

# (B) Constriction: x << y

def caps_constrict_by_cons(x_caps: Caps, y_cons: Cons) -> Caps:
    """
    Implements x_caps << y_cons
    BEGIN
    r_caps = []
    forall conset in y_cons: r_caps.append(x_caps << conset)
    if r_caps is empty ? error : return r_caps
    END
    """
    r_caps : List[CapSet] = []
    for conset in y_cons.consets:
        
        conset.check_part_valid()

        try:
            r_caps.append(caps_constrict_by_conset(x_caps, conset))
        except ValueError:
            # If none matched, skip
            pass

    if not r_caps:
        raise ValueError("No valid results from x_caps << y_cons")

    return Caps(capsets=r_caps)

def caps_constrict_by_conset(x_caps: Caps, y_conset: ConSet) -> CapSet:
    """
    Implements x_caps << y_conset
    BEGIN
    r_capset = null
    forany capset in x_caps:
        if y_conset <= capset: r_capset = (capset << y_conset)
    if r_capset is null ? error : return r_capset
    END
    """
    y_conset.check_part_valid()

    r_capset = None
    for capset in x_caps.capsets:

        if not y_conset.is_same_part(capset):
            continue

        if conset_included_in_capset(y_conset, capset):
            # Then we do (capset << y_conset)
            r_capset = capset_constrict_by_conset(capset, y_conset)
            break

    if r_capset is None:
        raise ValueError("x_caps << y_conset => no suitable capset found")

    return r_capset

def capset_constrict_by_conset(x_capset: CapSet, y_conset: ConSet) -> CapSet:
    """
    Implements x_capset << y_conset
    BEGIN
    r_capset = x_capset
    for all con in y_conset: r_capset = (r_capset << con)
    r_capset.preference = y_conset.preference
    return r_capset
    END
    """
    x_capset.check_part_valid()
    y_conset.check_part_valid()

    # Make a copy to avoid mutating x_capset directly
    r_capset = CapSet(
        caps=dict(x_capset.caps),
        preference=x_capset.preference,
        label=x_capset.label,
        format=x_capset.format,
        layer=x_capset.layer,
        layer_compatibility_groups=x_capset.layer_compatibility_groups
    )

    if not x_capset.is_same_part(y_conset):
        return r_capset

    # For each Constraint in y_conset, do "r_capset << constraint"
    for con in y_conset.cons.values():
        r_capset = capset_constrict_by_con(r_capset, con)

    # Finally, set preference from y_conset
    r_capset.preference = y_conset.preference

    return r_capset

def capset_constrict_by_con(x_capset: CapSet, y_con: Constraint) -> CapSet:
    """
    Implements: x_capset << y_con
    BEGIN
    r_capset = x_capset
    r_capset[y_con.name] = (r_capset[y_con.name] << y_con)
    return r_capset
    END
    """
    x_capset.check_part_valid()

    if y_con.value.has_enum_exception():
        raise ValueError("constraint enum cannot be empty if not None")

    # Copy to avoid mutating original
    r_capset = CapSet(
        caps=dict(x_capset.caps),
        preference=x_capset.preference,
        label=x_capset.label,
        format=x_capset.format,
        layer=x_capset.layer,
        layer_compatibility_groups=x_capset.layer_compatibility_groups
    )

    r_capset.caps[y_con.name] = cap_constrict_by_con(r_capset[y_con.name], y_con)

    return r_capset

def cap_constrict_by_con(x_cap: Capability, y_con: Constraint) -> Capability:
    """
    Implements x_cap << y_con
    BEGIN
    if x_cap.name != y_con.name : error
    r_cap = x_cap
    if y_con.value != INF:
        if y_con <= r_cap ? r_cap = y_con : error
    return r_cap
    END
    """
    if x_cap.value.has_enum_exception():
        raise ValueError("capability enum cannot be empty if not None")

    if y_con.value.has_enum_exception():
        raise ValueError("constraint enum cannot be empty if not None")

    if x_cap.name != y_con.name:
        raise ValueError(f"Name mismatch: x_cap.name={x_cap.name}, y_con.name={y_con.name}")

    r_cap = Capability(
        name=x_cap.name,
        value=RangeValue(
                    infinite=x_cap.value.infinite,
                    empty=x_cap.value.empty,
                    type=x_cap.value.type,
                    min=x_cap.value.min,
                    max=x_cap.value.max,
                    values=x_cap.value.values
                ),
        original=x_cap.original
    )

    # if constraint is infinite => no change
    if not y_con.value.is_infinite():
        # Check "y_con <= r_cap"
        # i.e. y_con.value <= x_cap.value
        if r_cap.value.includes_range(y_con.value):
            r_cap.value = y_con.value
        else:
            raise ValueError(
                f"Constraint {y_con.name} cannot expand capability: "
                f"{y_con.value} !<= {r_cap.value}"
            )

    return r_cap

# (C) Constriction with adjustment: x <& y

def caps_constrict_adjust_by_cons(x_caps: Caps, y_cons: Cons) -> Caps:
    """
    Implements x_caps <& y_cons
    BEGIN
    r_caps = []
    forall conset in y_cons: r_caps.append(x_caps <& conset)
    if r_caps is empty ? error : return r_caps
    END
    """
    r_caps : List[CapSet] = []
    for conset in y_cons.consets:

        conset.check_part_valid()

        try:
            r_caps.append(caps_constrict_adjust_by_conset(x_caps, conset))
        except ValueError:
            # If none matched, skip
            pass

    if not r_caps:
        raise ValueError("No valid results from x_caps <& y_cons")

    return Caps(capsets=r_caps)

def caps_constrict_adjust_by_conset(x_caps: Caps, y_conset: ConSet) -> CapSet:
    """
    Implements x_caps <& y_conset
    BEGIN
    r_capset = null
    forany capset in x_caps: 
        r_capset = capset <& y_conset
        if r_capset != null:
            break
    if r_capset is null ? error : return r_capset
    END
    """
    y_conset.check_part_valid()

    r_capset = None
    for capset in x_caps.capsets:

        if not capset.is_same_part(y_conset):
            continue

        try:
            # We special case preference of 100 as it indicates a native set. We intersect an X native
            # set only with a Y native set. We allow a Y native set to intersect with any set because
			# it remains a set of the Y preference. Others intersect without considering the preference.
            if y_conset.preference != 100 and capset.preference == 100:
                continue

            r_capset = capset_constrict_adjust_by_conset(capset, y_conset)
            break
        except ValueError:
            pass

    if r_capset is None:
        raise ValueError("x_caps <& y_conset => no suitable capset found")

    return r_capset

def capset_constrict_adjust_by_conset(x_capset: CapSet, y_conset: ConSet) -> CapSet:
    """
    Implements x_capset << y_conset
    BEGIN
    r_capset = x_capset
    for all con in y_conset: r_capset = (r_capset <& con)
    r_capset.preference = y_conset.preference
    return r_capset
    END
    """
    x_capset.check_part_valid()
    y_conset.check_part_valid()

    # Make a copy to avoid mutating x_capset directly
    r_capset = CapSet(
        caps=dict(x_capset.caps),
        preference=x_capset.preference,
        label=x_capset.label,
        format=x_capset.format,
        layer=x_capset.layer,
        layer_compatibility_groups=x_capset.layer_compatibility_groups
    )

    if not x_capset.is_same_part(y_conset):
        return r_capset

    # For each Constraint in y_conset, do "r_capset << constraint"
    for con in y_conset.cons.values():
        r_capset = capset_constrict_adjust_by_con(r_capset, con)

    # Finally, set preference from y_conset
    r_capset.preference = y_conset.preference

    return r_capset

def capset_constrict_adjust_by_con(x_capset: CapSet, y_con: Constraint) -> CapSet:
    """
    Implements: x_capset << y_con
    BEGIN
    r_capset = x_capset
    r_capset[y_con.name] = r_capset[y_con.name] <& y_con
    return r_capset
    END
    """
    x_capset.check_part_valid()

    if y_con.value.has_enum_exception():
        raise ValueError("constraint enum cannot be empty if not None")

    # Copy to avoid mutating original
    r_capset = CapSet(
        caps=dict(x_capset.caps),
        preference=x_capset.preference,
        label=x_capset.label,
        format=x_capset.format,
        layer=x_capset.layer,
        layer_compatibility_groups=x_capset.layer_compatibility_groups
    )

    r_capset.caps[y_con.name] = cap_constrict_adjust_by_con(r_capset[y_con.name], y_con)

    return r_capset

def cap_constrict_adjust_by_con(x_cap: Capability, y_con: Constraint) -> Capability:
    """
    Implements x_cap << y_con
    BEGIN
    if x_cap.name != y_con.name : error
    r_cap = x_cap
    if y_con.value != INF: 
        r_cap.value = r_cap.value & y_con.value
        if r_cap.value == NUL ? error 
            
    return r_cap

    Note: an error is returned if the capability have different names or the intersection is NUL
    END
    """
    if x_cap.value.has_enum_exception():
        raise ValueError("capability enum cannot be empty if not None")

    if y_con.value.has_enum_exception():
        raise ValueError("constraint enum cannot be empty if not None")

    if x_cap.name != y_con.name:
        raise ValueError(f"Name mismatch: x_cap.name={x_cap.name}, y_con.name={y_con.name}")

    r_cap = Capability(
        name=x_cap.name,
        value=RangeValue(
            infinite=x_cap.value.infinite,
            empty=x_cap.value.empty,
            type=x_cap.value.type,
            min=x_cap.value.min,
            max=x_cap.value.max,
            values=x_cap.value.values
        ),
        original=x_cap.original
    )

    # if constraint is infinite => no change
    if not y_con.value.is_infinite():
        # intersection => can return NUL range if empty
        r_cap.value = r_cap.value.intersection(y_con.value)

        if r_cap.value.is_empty():
            raise ValueError(
                f"Constraint {y_con.name} not intersecting capability: "
                f"{y_con.value} !& {r_cap.value}"
            )       
    
    return r_cap

# (D) Intersection: x & y

def range_intersection(r1: RangeValue, r2: RangeValue) -> RangeValue:
    """Just calls r1.intersection(r2). For convenience."""
    return r1.intersection(r2)

# (E) Inclusion: x <= y

from typing import Set

def caps_included_in_caps(x_caps: Caps, y_caps: Caps) -> bool:
    """
    Implements x_caps <= y_caps

    BEGIN
      forall capset in x_caps: capset <= y_caps
    END
    """
    for capset in x_caps.capsets:

        capset.check_part_valid()

        if not capset_included_in_caps(capset, y_caps):
            # print(f"BECAUSE of CapSet {capset}")
            return False

    return True

def capset_included_in_caps(x_capset: CapSet, y_caps: Caps) -> bool:
    """
    Implements x_capset <= y_caps

    BEGIN
      forany capset in y_caps: x_capset <= capset
    END
    """
    x_capset.check_part_valid()

    for capset in y_caps.capsets:

        if not capset.is_same_part(x_capset):
            continue

        if capset_included_in_capset(x_capset, capset):
            return True

    return False

def capset_included_in_capset(x_capset: CapSet, y_capset: CapSet) -> bool:
    """
    Implements x_capset <= y_capset

    BEGIN
      forall name in (NS(x_capset) <- NS(y_capset)): x_capset[name] <= y_capset[name]
    END
    """
    if not x_capset.is_same_part(y_capset):
        return False

    # gather the union or intersection of names
    all_names = namespace_inherit_from_capset(x_capset.namespace(), y_capset)
    for name in all_names:
        if not cap_included_in_cap(x_capset[name], y_capset[name]):
            return False
        
    return True

def cap_included_in_cap(x_cap: Capability, y_cap: Capability) -> bool:
    """
    Implements x_cap <= y_cap
    BEGIN
      x_cap.name == y_cap.name AND x_cap.value <= y_cap.value
    END
    """
    if x_cap.value.has_enum_exception():
        raise ValueError("capability enum cannot be empty if not None")

    if y_cap.value.has_enum_exception():
        raise ValueError("capability enum cannot be empty if not None")

    if x_cap.name != y_cap.name:
        return False

    return (y_cap.value.includes_range(x_cap.value))

def cons_included_in_cons(x_cons: Cons, y_cons: Cons) -> bool:
    """
    Implements x_cons <= y_cons

    BEGIN
      forall conset in x_cons: conset <= y_cons
    END
    """
    for conset in x_cons.consets:
        
        conset.check_part_valid()

        if not conset_included_in_cons(conset, y_cons):
            return False
        
    return True

def conset_included_in_cons(x_conset: ConSet, y_cons: Cons) -> bool:
    """
    Implements x_conset <= y_cons

    BEGIN
      forany conset in y_cons: x_conset <= conset
    END
    """
    x_conset.check_part_valid()

    for conset in y_cons.consets:

        if not conset.is_same_part(x_conset):
            continue

        if conset_included_in_conset(x_conset, conset):
            return True
    
    return False

def conset_included_in_conset(x_conset: ConSet, y_conset: ConSet) -> bool:
    """
    Implements x_conset <= y_conset

    BEGIN
      forall name in (NS(x_conset) <- NS(y_conset)): x_conset[name] <= y_conset[name]
    END
    """
    if not y_conset.is_same_part(x_conset):
        return False

    # gather the union or intersection of names
    all_names = namespace_inherit_from_conset(x_conset.namespace(), y_conset)
    for name in all_names:
        if not con_included_in_con(x_conset[name], y_conset[name]):
            return False
        
    return True

def con_included_in_con(x_con: Constraint, y_con: Constraint) -> bool:
    """
    Implements x_con <= y_con
    BEGIN
      x_con.name == y_con.name AND x_con.value <= y_con.value
    END
    """
    if x_con.value.has_enum_exception():
        raise ValueError("constraint enum cannot be empty if not None")

    if y_con.value.has_enum_exception():
        raise ValueError("capability enum cannot be empty if not None")

    if x_con.name != y_con.name:
        return False

    return y_con.value.includes_range(x_con.value)


def cons_included_in_caps(x_cons: Cons, y_caps: Caps) -> bool:
    """
    Implements x_cons <= y_caps

    BEGIN
      forall conset in x_cons: conset <= y_caps
    END
    """
    for conset in x_cons.consets:

        conset.check_part_valid()

        if not conset_included_in_caps(conset, y_caps):
            return False
        
    return True

def conset_included_in_caps(x_conset: ConSet, y_caps: Caps) -> bool:
    """
    Implements x_conset <= y_caps

    BEGIN
      forany capset in y_caps: x_conset <= capset
    END
    """
    x_conset.check_part_valid()

    for capset in y_caps.capsets:

        if not capset.is_same_part(x_conset):
            continue

        if conset_included_in_capset(x_conset, capset):
            return True

    return False

def conset_included_in_capset(x_conset: ConSet, y_capset: CapSet) -> bool:
    """
    Implements x_conset <= y_capset

    BEGIN
    forall con in x_conset: if con.value = INF { true } else { con <= y_capset[con.name] }    
    END
    """
    if not x_conset.is_same_part(y_capset):
        return False
    
    for con in x_conset.cons.values():
        if not con.value.is_infinite():
            if not con_included_in_cap(con, y_capset[con.name]):
                return False

    return True

def con_included_in_cap(x_con: Constraint, y_cap: Capability) -> bool:
    """
    Implements x_con <= y_cap
    BEGIN
      x_con.name == y_cap.name AND (x_con.value = INF OR x_con.value <= y_cap.value)
    END
    """
    if x_con.value.has_enum_exception():
        raise ValueError("constraint enum cannot be empty if not None")

    if y_cap.value.has_enum_exception():
        raise ValueError("capability enum cannot be empty if not None")

    if x_con.name == y_cap.name and (x_con.value.is_infinite() or (y_cap.value.includes_range(x_con.value))):
        return True

    return False

def range_included_in_range(x: RangeValue, y: RangeValue) -> bool:
    return y.includes_range(x)

def value_included_in_range(x: Union[bool, int, float, Fraction, str], y: RangeValue) -> bool:
    return y.includes_value(x)

def namespace_included_in_namespace(x_ns: Set[str], y_ns: Set[str]) -> bool:
    """
    {x} <= {y}
    BEGIN
      forall v in {x}: v is in namespace {y}
    END

    Means x_ns is a subset of y_ns.
    """
    return x_ns.issubset(y_ns)

# (F) NS(x) = {} <- x

def namespace_of_capset(x_capset: CapSet) -> Set[str]:
    """
    NS(x_capset) = {} <- x_capset
    In the theory => means just the set of param names in x_capset.
    """
    x_capset.check_part_valid()

    return x_capset.namespace()

def namespace_of_conset(x_conset: ConSet) -> Set[str]:
    """
    NS(x_conset) = {} <- x_conset
    In the theory => means just the set of param names in x_conset.
    """
    x_conset.check_part_valid()

    return x_conset.namespace()

def convert_caps_json_to_caps(caps_json: Dict[str, Any]) -> Caps:
    """
    Converts a JSON "caps" dictionary of a Sender or Receiver into a Caps dataclass instance.

    Args:
        caps_json (dict): The JSON dictionary representing "caps".

    Returns:
        Caps: An instance of the Caps dataclass containing all CapSet instances.
    """
    from fractions import Fraction

    # Mapping of capability URNs to RangeType enums
    capability_type_map = {
	    CapFormatMediaType: RangeType.STRING,
	    CapFormatEventType: RangeType.STRING,
	    CapFormatGrainRate: RangeType.RATIONAL,
	    CapFormatFrameWidth: RangeType.INT,
	    CapFormatFrameHeight: RangeType.INT,
	    CapFormatInterlaceMode: RangeType.STRING,
	    CapFormatColorspace: RangeType.STRING,
	    CapFormatTransferCharacteristic: RangeType.STRING,
	    CapFormatColorSampling: RangeType.STRING,
	    CapFormatComponentDepth: RangeType.INT,
	    CapFormatChannelCount: RangeType.INT,
	    CapFormatSampleRate: RangeType.RATIONAL,
	    CapFormatSampleDepth: RangeType.INT,
	    CapFormatBitRate: RangeType.INT,
	    CapFormatProfile: RangeType.STRING,
	    CapFormatLevel: RangeType.STRING,
	    CapFormatSublevel: RangeType.STRING,
	    CapFormatConstantBitRate: RangeType.BOOL,
	    CapFormatVideoLayers: RangeType.INT,
	    CapFormatAudioLayers: RangeType.INT,
	    CapFormatDataLayers: RangeType.INT,
	    CapTransportBitRate: RangeType.INT,
	    CapTransportPacketTime: RangeType.FLOAT,
	    CapTransportMaxPacketTime: RangeType.FLOAT,
	    CapTransport_ST2110_21_SenderType: RangeType.STRING,
	    CapTransportPacketTransmissionMode: RangeType.STRING,
	    CapTransportParameterSetsFlowMode: RangeType.STRING,
	    CapTransportParameterSetsTransportMode: RangeType.STRING,
	    CapTransportChannelOrder: RangeType.STRING,
	    CapTransportHkep: RangeType.BOOL,
	    CapTransportPrivacy: RangeType.BOOL,
	    CapTransportClockRefType: RangeType.STRING,
	    CapTransportInfoBlock: RangeType.INT,
	    CapTransportSynchronousMedia: RangeType.BOOL,
    }

    def parse_range_value(cap_constraints : Dict[str, Any], range_type: RangeType) -> RangeValue:

        infinite = False  # Default value
        min = cap_constraints.get("minimum")
        max = cap_constraints.get("maximum")
        enumerated : List[Union[bool, int, float, Fraction, str]] = []

        if "enum" in cap_constraints:
            enum_list = cap_constraints["enum"]
            for item in enum_list:
                if isinstance(item, dict):
                    numerator : Optional[int] = item.get("numerator") # type: ignore
                    denominator : Optional[int] = item.get("denominator", 1) # type: ignore
                    if numerator is not None and isinstance(numerator, int) and isinstance(denominator, Optional[int]):
                        try:
                            fraction = Fraction(numerator, denominator)
                            enumerated.append(fraction)
                        except ZeroDivisionError:
                            raise ValueError(f"Invalid fraction with denominator 0 in capability constraints: {item}")
                    else:
                        raise ValueError(f"Invalid enumerated dict without 'numerator': {item}")
                else:
                    enumerated.append(item)

        if min is None and max is None and not "enum" in cap_constraints:
            infinite = True

        return RangeValue(
            infinite=infinite,
            empty=False, # cannot make explicitly empty by JSON parsing
            type=range_type,
            min=min,
            max=max,
            values= tuple(enumerated) if len(enumerated) != 0 else None
        )

    capsets : List[CapSet] = []
    constraint_sets = caps_json.get("caps", {}).get("constraint_sets", [])

    for cs_index, cs in enumerate(constraint_sets, start=1):

        label = cs.get(CapMetaLabel, f"Unnamed CapSet {cs_index}")
        preference = cs.get(CapMetaPreference, 0)
        format = cs.get(CapMetaFormat, None)
        layer = cs.get(CapMetaLayer, None)
        layer_compatibility_groups = cs.get(CapMetaLayerCompatibilityGroups, None)

        # Extract capability entries by excluding meta keys
        capability_entries = {
            k: v for k, v in cs.items()
            if not k.startswith("urn:x-nmos:cap:meta:") and not k.startswith("urn:x-matrox:cap:meta:")
        }

        capabilities : Dict[str, Capability] = {}

        for cap_name, cap_constraints in capability_entries.items():
            # Determine the RangeType; default to UNTYPED if not found
            range_type = capability_type_map.get(cap_name, RangeType.UNTYPED)

            if isinstance(cap_constraints, dict):

                caps : Dict[str, Any] = cap_constraints

                try:
                    range_value = parse_range_value(caps, range_type)
                except ValueError as ve:
                    raise ValueError(f"Error parsing capability '{cap_name}' in CapSet '{label}': {ve}")
            elif isinstance(cap_constraints, list):

                elements : List[Union[int, float, Fraction, str, bool]] = cap_constraints

                range_value = RangeValue(
                    empty=False,
                    infinite=False,
                    type=range_type,
                    values=tuple(v for v in elements),
                )
            else:
                range_value = RangeValue(
                    empty=False,
                    infinite=False,
                    type=range_type,
                    values=(cap_constraints,),
                )
            
            capability = Capability(name=cap_name, value=range_value)
            capabilities[cap_name] = capability

        # Create a CapSet instance
        capset = CapSet(
            caps=capabilities,
            preference=preference,
            label=label,
            format=format,
            layer=layer,
            layer_compatibility_groups=layer_compatibility_groups
        )

        capsets.append(capset)

    # Create the Caps instance with all CapSet instances
    caps_instance = Caps(
        capsets=capsets,
        filtered=False
    )

    return caps_instance
