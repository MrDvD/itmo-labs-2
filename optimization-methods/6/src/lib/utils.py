from typing import List, Dict

class Utils:
  @staticmethod
  def transform_matrix_to_graph(matrix: List[List[int]], labels: List[str], infty: int) -> Dict[str, Dict[str, int]]:
    graph: Dict[str, Dict[str, int]] = dict()
    n = len(labels)
    
    for i in range(n):
      node_edges = {}
      for j in range(n):
        weight = matrix[i][j]
        if 0 < weight < infty:
          node_edges[labels[j]] = weight
      graph[labels[i]] = node_edges
      
    return graph