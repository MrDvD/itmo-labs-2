import lib.config as config
from lib.artifacts import ArtifactsFiller
from lib.report import ReportFiller
from typing import List, Any, Dict

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
  
  context: Dict[str, Any] = {
    'variant_number': cfg['variant_num'],
  }

  report = ReportFiller(context, cfg['infinity'])
  report.fill_task(1, matrix_1)
  report.fill_task(2, matrix_2)

  artifacts = ArtifactsFiller(context, cfg['report_dir'])
  artifacts.compile_patterns()