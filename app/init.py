from __future__ import annotations
import hashlib
import random
from dataclasses import dataclass
from enum import IntEnum
from typing import Sequence, Tuple

class Trit(IntEnum):
    NEG = -1
    ZERO = 0
    POS = 1

TEN_D_AXES = ("G","D","R","A","I","N","U","C","V","T")

@dataclass(frozen=True)
class Physics10D:
    G:int; D:int; R:int; A:int; I:int; N:int; U:int; C:int; V:int; T:int
    def as_tuple(self)->Tuple[int,...]:
        return tuple(getattr(self,k) for k in TEN_D_AXES)
    def key(self)->str:
        return hashlib.blake2b(",".join(map(str,self.as_tuple())).encode(),digest_size=16).hexdigest()

def flatten_frame(frame_data):
    result = []
    for layer in frame_data:
        if isinstance(layer, list):
            for row in layer:
                if isinstance(row, list):
                    result.extend(int(v) for v in row)
                else:
                    result.append(int(row))
        else:
            result.append(int(layer))
    return result

def frame_to_ascii(frame_data, width=32, height=12):
    flat = flatten_frame(frame_data)
    if not flat:
        return "." * (width * height)
    max_val = max(flat) if flat else 1
    min_val = min(flat) if flat else 0
    rng = max_val - min_val or 1
    chars = " .:-=+*#%@"
    result = []
    for y in range(height):
        row = []
        for x in range(width):
            idx = (y * len(flat) // height + x * len(flat) // width) % len(flat)
            v = flat[idx]
            ci = int((v - min_val) / rng * (len(chars) - 1))
            row.append(chars[ci])
        result.append("".join(row))
    return "\n".join(result)

def extract_physics(frame_data) -> Physics10D:
    flat = flatten_frame(frame_data)
    n = len(flat)
    if n == 0:
        return Physics10D(0,0,0,0,0,0,0,0,0,0)
    chunk = max(n // 10, 1)
    features = []
    for i in range(10):
        s = i * chunk
        e = min(s + chunk, n)
        features.append(sum(flat[s:e]) // max(e - s, 1))
    return Physics10D(*features[:10])

def ternarize(state:Physics10D, dead_zones:Sequence[int])->Tuple[Trit,...]:
    out=[]
    for x,d in zip(state.as_tuple(),dead_zones,strict=True):
        out.append(Trit.POS if x>d else Trit.NEG if x<-d else Trit.ZERO)
    return tuple(out)

print("Core utils defined")
