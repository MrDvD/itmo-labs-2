from typing import List, Tuple
from dataclasses import dataclass

@dataclass
class GeneticIteration:
  start_population: List[str]
  pairs: List[Tuple[str, str]]
  children: List[Tuple[str, str]]
  mutations: List[Tuple[str, str]]
  goals_tuple: List[Tuple[int, int]]
  candidates: List[str]
  goals_linear: List[int]
  probabilities: List[float]
  end_population: List[str]
  end_goals: List[int]