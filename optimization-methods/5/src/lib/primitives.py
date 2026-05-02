from dataclasses import dataclass
from typing import Tuple, List

@dataclass
class TableEntry:
  x: float
  y: float
  z: float

@dataclass
class KmeansIteration:
  center1_prev: Tuple[float, float]
  center2_prev: Tuple[float, float]
  cluster1: List[Tuple[float, float]]
  cluster2: List[Tuple[float, float]]
  center1: Tuple[float, float]
  center2: Tuple[float, float]
  delta1: float
  delta2: float