import os
import lib.config as config
from lib.artifacts import ArtifactsFiller
from lib.report import ReportFiller
from lib.genetic import GeneticAlgorithm
from lib.ant import AntColonyAlgorithm
from lib.utils import Utils
from typing import List, Any, Dict, Callable

if __name__ == "__main__":
  cfg = config.load('config.yml')

  matrix_1: List[List[int]] = list()
  with open(cfg['task_1_file'], 'r') as f:
    for line in f.readlines():
      matrix_1.append(list(map(int, line.split())))
  
  matrix_2: List[List[int]] = list()
  with open(cfg['task_2_file'], 'r') as f:
    for line in f.readlines():
      result_line: List[int] = list()
      for c in line.split():
        result_line.append(cfg['infinity'] if c == '∞' else int(c))
      matrix_2.append(result_line)
  
  compute_goal_1: Callable[[str], int] = lambda x: sum(
    matrix_1[int(x[i]) - 1][int(x[(i + 1) % 5]) - 1] for i in range(5)
  )

  genetic = GeneticAlgorithm(compute_goal_1, cfg['limit_gene'], cfg['prob_mutate_gene'], cfg['c_constant_gene'])
  init_population = genetic.init_population(cfg['population_size'])
  res_gene, log_gene = genetic.simulate(init_population)
  ans_gene = genetic.brute_force()

  graph = Utils.transform_matrix_to_graph(matrix_2, ['A', 'B', 'C', 'D', 'E', 'F', 'G'], cfg['infinity'])

  ant = AntColonyAlgorithm(graph,
                           'A',
                           'G',
                           cfg['infinity'],
                           cfg['colony_size'],
                           cfg['limit_ant'],
                           cfg['alpha_ant'],
                           cfg['beta_ant'],
                           cfg['rho_ant'],
                           cfg['q0_ant'],
                           cfg['q_ant'])
  res_ant, log_ant = ant.simulate()
  ans_ant = ant.brute_force()
  
  context: Dict[str, Any] = {
    'variant_number': cfg['variant_num'],
    'population_size': cfg['population_size'],
    'prob_mutate_gene': cfg['prob_mutate_gene'],
    'h_res_gene': f"( {','.join(res_gene[1])} )^T",
    'f_res_gene': str(res_gene[0]),
    'h_opt_gene': f"( {','.join(ans_gene[1])} )^T",
    'f_opt_gene': str(ans_gene[0]),
    'genetic_result': ans_gene[0] == res_gene[0],
    'c_constant_gene': cfg['c_constant_gene'],
    'colony_size': cfg['colony_size'],
    'q0_ant': cfg['q0_ant'],
    'q_ant': cfg['q_ant'],
    'limit_gene': cfg['limit_gene'],
    'limit_ant': cfg['limit_ant'],
    'rho_ant': cfg['rho_ant'],
    'alpha_ant': cfg['alpha_ant'],
    'beta_ant': cfg['beta_ant'],
    'h_res_ant': f"( {','.join(res_ant[1])} )^T",
    'f_res_ant': str(res_ant[0]),
    'h_opt_ant': f"( {','.join(ans_ant[1])} )^T",
    'f_opt_ant': str(ans_ant[0]),
    'ant_result': ans_ant[0] == res_ant[0],
  }

  pattern_path = os.path.join(cfg['report_dir'], 'sections', 'algorithms', 'genetic_iteration.j2')
  pics_path = os.path.join(cfg['report_dir'], 'pics')
  os.makedirs(pics_path, exist_ok=True)
  population_diagram_path = os.path.join(pics_path, 'population.pdf')
  colony_diagram_path = os.path.join(pics_path, 'colony.pdf')

  report = ReportFiller(context, cfg['infinity'])
  report.fill_task(1, matrix_1)
  report.fill_task(2, matrix_2)
  report.fill_initial_population(init_population, compute_goal_1)
  report.fill_genetic_descriptive(log_gene[:3], pattern_path)
  report.draw_population_diagram(log_gene, population_diagram_path)
  report.draw_colony_diagram(log_ant, colony_diagram_path)

  artifacts = ArtifactsFiller(context, cfg['report_dir'])
  artifacts.compile_patterns()