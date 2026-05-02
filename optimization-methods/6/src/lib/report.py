from typing import Dict, List, Optional, Callable, Tuple
from lib.primitives import GeneticIteration
from jinja2 import Template
import matplotlib.pyplot as plt

class ReportFiller:
  def __init__(self, context: Dict[str, str], infty: int):
    self.context: Dict[str, str] = context
    self.infty = infty
  
  def fill_task(self, task_num: int, matrix: List[List[int]]) -> None:
    match task_num:
      case 1:
        lines: List[str] = list()
        for i in range(5):
          lines.append(f"\\textbf{{Город {i + 1}}} & {' & '.join(map(str, matrix[i]))} \\\\ \\hline")
        self.context[f'task_{task_num}_input_latex'] = '\n'.join(lines)
      case 2:
        lines: List[str] = list()
        infty_str = r'$\infty$'
        for i in range(7):
          lines.append(f"\\textbf{{{chr(ord('A') + i)}}} & {' & '.join(map(lambda x: str(x) if x != self.infty else infty_str, matrix[i]))} \\\\ \\hline")
        self.context[f'task_{task_num}_input_latex'] = '\n'.join(lines)
      case _:
        raise RuntimeError("Invalid task number.")
  
  def _fill_population_review(self, population: List[str], goals: List[int]) -> List[str]:
    total_table: List[str] = list()
    for i in range(len(population)):
      row: List[str] = list()
      row.append(f"{i + 1}")
      row.append(f"$( {','.join(population[i])} )^T$")
      row.append(f"{goals[i]}")
      total_table.append(' & '.join(row) + "\\\\ \\hline")
    return total_table
  
  def _fill_next_generation(self, pairs: List[Tuple[str, str]], child: List[Tuple[str, str]], mutate: List[Tuple[str, str]], goals: List[Tuple[int, int]]) -> List[str]:
    total_table: List[str] = list()
    for i in range(len(pairs)):
      for j in range(2):
        row: List[str] = list()
        mutation = f"$( {','.join(mutate[i][j]) } )^T$" if mutate[i][j] != '' else '---'
        row.append(f"$( {','.join(pairs[i][j])} )^T$")
        row.append(f"$( {','.join(child[i][j])} )^T$")
        row.append(mutation)
        row.append(f"{goals[i][j]}")
        total_table.append(' & '.join(row) + "\\\\ \\hline")
      if i + 1 != len(pairs):
        total_table[-1] += "\\hline"
    return total_table
  
  def _fill_probabilities(self, population: List[str], goals: List[int], probabilities: List[float]) -> List[str]:
    total_table: List[str] = list()
    for i in range(len(population)):
      row: List[str] = list()
      row.append(f"{i + 1}")
      row.append(f"$( {','.join(population[i])} )^T$")
      row.append(f"{goals[i]}")
      row.append(f"{probabilities[i]:.5f}")
      total_table.append(' & '.join(row) + "\\\\ \\hline")
    return total_table
  
  def draw_population_diagram(self, iterations_meta: List[GeneticIteration], diagram_path: str) -> None:
    plt.figure(figsize=(12, 6))
  
    iterations = range(len(iterations_meta))
    sample_means = []
    optimums = []
    
    for meta in iterations_meta:
      goals = meta.end_goals
      sample_means.append(sum(goals) / len(goals))
      optimums.append(min(goals + optimums))
    
    plt.plot(iterations, sample_means, 'o-', label='Sample mean', color='blue', linewidth=2)
    plt.plot(iterations, optimums, 's-', label='Optimum (min)', color='red', linewidth=2)
    
    plt.xlabel('Iteration')
    plt.ylabel('Goal value')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(diagram_path, dpi=150)
    plt.close()
  
  def fill_initial_population(self, population: List[str], compute_goal: Callable[[str], int]) -> None:
    goals: List[int] = list(map(lambda x: compute_goal(x), population))
    total_table = self._fill_population_review(population, goals)
    self.context['initial_population_gene'] = '\n'.join(total_table)
  
  def fill_genetic_descriptive(self, iterations_meta: List[GeneticIteration], pattern_path: str) -> None:
    template: Optional[Template] = None
    with open(pattern_path, 'r') as f:
      template = Template(f.read())
    
    if template is None:
      raise ValueError(f"Failed to load template from {pattern_path}")
    
    iterations_data: List[str] = list()
    for i, iteration in enumerate(iterations_meta):
      avg_goal = sum(iteration.end_goals) / len(iteration.end_goals)
      iter_dict: Dict[str, str] = {
        'iteration_num': str(i + 1),
        'iteration_num_prev': str(i),
        'final_population': '\n'.join(self._fill_population_review(iteration.end_population, iteration.end_goals)),
        'probabilities_num': '\n'.join(self._fill_probabilities(iteration.candidates, iteration.goals_linear, iteration.probabilities)),
        'next_generation': '\n'.join(self._fill_next_generation(iteration.pairs, iteration.children, iteration.mutations, iteration.goals_tuple)),
        'f_avg': f'{avg_goal:.2f}',
      }
      iterations_data.append(template.render(iter_dict))
    
    self.context['genetic_iterations'] = '\n'.join(iterations_data)