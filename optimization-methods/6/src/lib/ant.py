import random
from typing import List, Tuple, Dict, Set
from lib.primitives import AntIteration

class AntColonyAlgorithm:
  def __init__(self,
               graph: Dict[str, Dict[str, int]],
               start_node: str,
               end_node: str,
               infty: int,
               num_ants: int = 10,
               max_iterations: int = 100,
               alpha: float = 1.0,
               beta: float = 1.0,
               rho: float = 0.2,
               q0: float = 0.75,
               Q: float = 10):
    self.graph = graph
    self.start_node = start_node
    self.end_node = end_node
    self.num_ants = num_ants
    self.max_iterations = max_iterations
    self.alpha = alpha
    self.beta = beta
    self.rho = rho
    self.q0 = q0
    self.Q = Q
    self.pheromones: Dict[Tuple[str, str], float] = dict()
    self.infty = infty
    for u in self.graph:
      for v in self.graph[u]:
        self.pheromones[(u, v)] = 1.0
  
  def brute_force(self) -> Tuple[float, List[str]]:
    min_dist = self.infty
    best_path: List[str] = list()

    def solve(curr: str, path: List[str], dist: int):
      nonlocal min_dist, best_path
      if len(path) > 7:
        return
      if curr == self.end_node:
        if dist < min_dist:
          min_dist = dist
          best_path = path.copy()
        return
      if curr in self.graph:
        for neighbor, weight in self.graph[curr].items():
          if neighbor not in path:
            solve(neighbor, path + [neighbor], dist + weight)

    solve(self.start_node, [self.start_node], 0)
    return (min_dist, best_path)

  def compute_goal(self, route: List[str]) -> int:
    if not route or route[-1] != self.end_node:
      return self.infty

    total_weight = 0
    for i in range(len(route) - 1):
      total_weight += self.graph[route[i]][route[i+1]]
    return total_weight

  def choose_next_node(self, current_node: str, visited: Set[str]) -> str:
    neighbors = self.graph[current_node]
    unvisited: List[str] = list()
    for n in neighbors:
      if n not in visited:
        unvisited.append(n)
    
    if not unvisited:
      return ""
    
    q = random.random()
    
    if q <= self.q0:
      best_node = ""
      max_val = -1.0
      for node in unvisited:
        tau = self.pheromones[(current_node, node)]
        eta = 1.0 / self.graph[current_node][node]
        val = (tau ** self.alpha) * (eta ** self.beta)
        if val > max_val:
          max_val = val
          best_node = node
      return best_node
    else:
      probabilities: List[Tuple[str, float]] = list()
      sum_val = 0.0
      for node in unvisited:
        tau = self.pheromones[(current_node, node)]
        eta = 1.0 / self.graph[current_node][node]
        val = (tau ** self.alpha) * (eta ** self.beta)
        probabilities.append((node, val))
        sum_val += val
      
      r = random.random()
      cumulative_prob = 0.0
      for node, prob in probabilities:
        cumulative_prob += prob / sum_val
        if r <= cumulative_prob:
          return node
      return probabilities[-1][0]

  def build_tour(self) -> List[str]:
    route: List[str] = [self.start_node]
    visited: Set[str] = set(route)
    current_node = self.start_node
    
    while current_node != self.end_node:
      next_node = self.choose_next_node(current_node, visited)
      if not next_node:
        break
      route.append(next_node)
      visited.add(next_node)
      current_node = next_node
      
    return route

  def update_pheromones(self, tours: List[List[str]]) -> None:
    for edge in self.pheromones:
      self.pheromones[edge] *= (1.0 - self.rho)
      
    for tour in tours:
      if tour[-1] == self.end_node:
        L = self.compute_goal(tour)
        delta = self.Q / L
        for i in range(len(tour) - 1):
          u, v = tour[i], tour[i+1]
          if (u, v) in self.pheromones:
            self.pheromones[(u, v)] += delta
          if (v, u) in self.pheromones:
            self.pheromones[(v, u)] += delta
    return

  def simulate(self) -> Tuple[Tuple[float, List[str]], List[AntIteration]]:
    best_route: List[str] = list()
    min_distance: float = float('inf')
    algorithm_log: List[AntIteration] = list()
    
    for _ in range(self.max_iterations):
      tours: List[List[str]] = list()
      current_goals: List[int] = list()
      for _ in range(self.num_ants):
        tour = self.build_tour()
        tours.append(tour)
        distance = self.compute_goal(tour)
        current_goals.append(distance)
        
        if tour[-1] == self.end_node and distance < min_distance:
          min_distance = distance
          best_route = tour.copy()
      
      self.update_pheromones(tours)
      algorithm_log.append(AntIteration(end_goals=current_goals))
      
    return ((min_distance, best_route), algorithm_log)