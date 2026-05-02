import random
from typing import List, Tuple, Callable
from lib.primitives import GeneticIteration
from itertools import permutations

class GeneticAlgorithm:
  def __init__(self, compute_goal: Callable[[str], int], max_iterations: int, prob_mutation: float, C_constant: float):
    self.max_iterations = max_iterations
    self.prob_mutation = prob_mutation
    self.compute_goal = compute_goal
    self.C_constant = C_constant

  def crossover(self, chromosomes: Tuple[str, str]) -> Tuple[str, str]:
    parent1, parent2 = chromosomes
    n = len(parent1)
    i, j = sorted(random.sample(range(n + 1), 2))
    
    child1: list[str] = [''] * n
    child2: list[str] = [''] * n
    
    child1[i:j] = list(parent2[i:j])
    child2[i:j] = list(parent1[i:j])
    
    def fill(child: list[str], parent: str) -> None:
      used: set[str] = set(child)
      pos: int = 0
      for x in parent:
        if x not in used:
          while pos < n and child[pos] != '':
            pos += 1
          child[pos] = x
          used.add(x)
    
    fill(child1, parent1)
    fill(child2, parent2)
    
    return (''.join(child1), ''.join(child2))

  def mutate(self, chromosome: str) -> str:
    indices = list(range(5))
    i, j = random.sample(indices, 2)
    
    chr_list = list(chromosome)
    chr_list[i], chr_list[j] = chr_list[j], chr_list[i]
    
    return ''.join(chr_list)

  def make_pairs(self, population: List[str]) -> List[Tuple[str, str]]:
    shuffled = population.copy()
    random.shuffle(shuffled)
    
    pairs: List[Tuple[str, str]] = list()
    for k in range(0, len(shuffled), 2):
      if k + 1 < len(shuffled):
        pairs.append((shuffled[k], shuffled[k + 1]))
    
    return pairs
  
  def init_population(self, count: int) -> List[str]:
    population: List[str] = list()
    for _ in range(count):
      chromosome = list(range(1, 6))
      random.shuffle(chromosome)
      population.append(''.join(map(str, chromosome)))
    return population
  
  def calculate_optimum(self, population: List[str]) -> Tuple[int, str]:
    optimum = min(population, key=lambda x: self.compute_goal(x))
    return (self.compute_goal(optimum), optimum)
  
  def brute_force(self) -> Tuple[int, str]:
    cities: list[str] = list(map(str, range(1, 6)))
    
    min_distance: int = 10**9
    best_route: str = ''
    
    for perm in permutations(cities):
      route: str = ''.join(perm)
      distance: int = self.compute_goal(route)
      if distance < min_distance:
        min_distance = distance
        best_route = route
    
    return (min_distance, best_route)
  
  def simulate(self, population: List[str]) -> Tuple[Tuple[int, str], List[GeneticIteration]]:
    answer = self.calculate_optimum(population)
    algorithm_log: List[GeneticIteration] = list()
    prev_population = population.copy()
    n = len(population)
    for _ in range(self.max_iterations):
      pairs = self.make_pairs(prev_population)
      children: List[Tuple[str, str]] = list()
      for p in pairs:
        children.append(self.crossover(p))
      mutations: List[Tuple[str, str]] = list()
      for c in children:
        mutated: List[str] = list()
        for i in range(2):
          if random.random() < self.prob_mutation:
            mutated.append(self.mutate(c[i]))
          else:
            mutated.append("")
        mutations.append((mutated[0], mutated[1]))
      goals_tuple: List[Tuple[int, int]] = list()
      candidates: List[str] = prev_population.copy()
      goals_linear: List[int] = list(map(self.compute_goal, candidates))
      for i in range(n // 2):
        goal_tuple: List[int] = list()
        for j in range(2):
          if mutations[i][j] == "":
            candidates.append(children[i][j])
            goals_linear.append(self.compute_goal(children[i][j]))
            goal_tuple.append(self.compute_goal(children[i][j]))
          else:
            candidates.append(mutations[i][j])
            goals_linear.append(self.compute_goal(mutations[i][j]))
            goal_tuple.append(self.compute_goal(mutations[i][j]))
        goals_tuple.append((goal_tuple[0], goal_tuple[1]))
      
      denominator = 2 * n * self.C_constant - sum(goals_linear)
      probabilities = [(self.C_constant - g) / denominator for g in goals_linear]

      end_population: List[str] = list()
      for _ in range(n):
        r = random.random()
        cumulative_prob = 0
        for i, prob in enumerate(probabilities):
          cumulative_prob += prob
          if r <= cumulative_prob:
            end_population.append(candidates[i])
            break

      end_goals = list(map(lambda x: self.compute_goal(x), end_population))

      iteration = GeneticIteration(
        start_population=prev_population.copy(),
        pairs=pairs,
        children=children,
        mutations=mutations,
        goals_tuple=goals_tuple,
        candidates=candidates,
        goals_linear=goals_linear,
        probabilities=probabilities,
        end_population=end_population,
        end_goals=end_goals,
      )

      curr_optimum = self.calculate_optimum(end_population)
      if curr_optimum[0] < answer[0]:
        answer = curr_optimum

      algorithm_log.append(iteration)
      prev_population = end_population.copy()

    return (answer, algorithm_log)