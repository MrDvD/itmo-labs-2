from typing import Dict, List

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