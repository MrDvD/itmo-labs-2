import os
import re
import math
from typing import Dict, List
from jinja2 import Environment, FileSystemLoader, meta
from lib.primitives import TableEntry, KmeansIteration

class ReportFiller:
  def __init__(self, context: Dict[str, str], report_dir: str):
    self.context: Dict[str, str] = context
    self.report_dir = report_dir
    self.section_regex = re.compile(r"## (.+)\n([\s\S]*?)(?=\n## |$)")

  def parse_artifact(self, artifact_path: str):
    if not os.path.exists(artifact_path):
      raise FileNotFoundError(f"Artifact not found: {artifact_path}")
    
    try:
      with open(artifact_path, "r") as f:
        content = f.read()
      
      sections = self.section_regex.findall(content)
      
      if not sections:
        return
      
      for name, body in sections:
        self.context[name.strip()] = body.strip()
    except IOError as e:
      raise RuntimeError(f"Error reading artifact: {e}")
  
  @staticmethod
  def print_vector(vector: List[float], prec: int = 5) -> str:
    vec_str: List[str] = list()
    for c in vector:
      vec_str.append(f"{c:.{prec}f}")
    return f"({','.join(vec_str)})^T"
  
  def fill_rbf_handmade(self, c1: List[float], c2: List[float], objects: List[TableEntry], kmeans_log: List[KmeansIteration], kmeans_epsilon: float, first_params: List[float]) -> None:
    distance_lines: List[str] = list()
    new_lines: List[str] = list()
    c1_vertices: List[TableEntry] = list()
    c2_vertices: List[TableEntry] = list()
    c1_vertices_str: List[str] = list()
    c2_vertices_str: List[str] = list()
    for i in range(len(objects)):
      line: List[str] = [f"$x_{i + 1}$"]
      obj = objects[i]
      d1: float = math.hypot(obj.x - c1[0], obj.y - c1[1])
      line.append(f"{d1:.5f}")
      d2: float = math.hypot(obj.x - c2[0], obj.y - c2[1])
      line.append(f"${d2:.5f}$")
      if d1 <= d2:
        line.append("$C_1$")
        c1_vertices_str.append(f"$x_{i + 1}$")
        c1_vertices.append(obj)
      else:
        line.append("$C_2$")
        c2_vertices_str.append(f"$x_{i + 1}$")
        c2_vertices.append(obj)
      raw_line = " & ".join(line)
      raw_line += "\\\\ \\hline"
      distance_lines.append(raw_line)
    self.context['distance_centers_rbf'] = '\n'.join(distance_lines)
    
    line_new  = "1 & "
    line_new += f"\\{{ {','.join(c1_vertices_str)} \\}} & "
    
    def find_avg_vector(arr: List[TableEntry]) -> str:
      avg_vector: List[float] = [0.0, 0.0]
      for v in arr:
        avg_vector[0] += v.x
        avg_vector[1] += v.y
      avg_vector[0] /= len(arr)
      avg_vector[1] /= len(arr)
      return ReportFiller.print_vector(avg_vector)

    line_new += f"${find_avg_vector(c1_vertices)}$"
    line_new += "\\\\ \\hline"
    new_lines.append(line_new)

    line_new  = "2 & "
    line_new += f"\\{{ {','.join(c2_vertices_str)} \\}} & "
    line_new += f"${find_avg_vector(c2_vertices)}$"
    line_new += "\\\\ \\hline"
    new_lines.append(line_new)

    self.context['new_centers_rbf'] = '\n'.join(new_lines)

    kmeans_lines: List[str] = list()
    for i, iteration in enumerate(kmeans_log[1:]):
      row: List[str] = list()
      row.append(f"{i + 2}")
      
      cluster1_str: str = "{"
      cluster1: List[str] = list()
      for c in iteration.cluster1:
        cluster1.append(f"${ReportFiller.print_vector(list(c), 2)}$")
      a = '\\\\'.join(cluster1)
      cluster1_str += f"{ a }}}"
      row.append(cluster1_str)

      cluster2_str: str = "{"
      cluster2: List[str] = list()
      for c in iteration.cluster2:
        cluster2.append(f"${ReportFiller.print_vector(list(c), 2)}$")
      b = '\\\\'.join(cluster2)
      cluster2_str += f"{ b }}}"
      row.append(cluster2_str)

      c = '\\\\'.join(map(lambda x: f"{x:.4f}", list(iteration.center1)))
      row.append(f"$\\begin{{pmatrix}} {c} \\end{{pmatrix}}$")
      d = '\\\\'.join(map(lambda x: f"{x:.4f}", list(iteration.center2)))
      row.append(f"$\\begin{{pmatrix}} {d} \\end{{pmatrix}}$")
      row.append(f"{iteration.delta1:.3f}")
      row.append(f"{iteration.delta2:.3f}")
      kmeans_lines.append(' & '.join(row) + "\\\\")

    self.context['kmeans_all_iterations_rbf'] = '\n'.join(kmeans_lines)

    self.context['d1_rbf'] = f"{kmeans_log[0].delta1:.3f}" + ('>\\varepsilon' if kmeans_log[0].delta1 > kmeans_epsilon else '\\leq\\varepsilon')
    self.context['d2_rbf'] = f"{kmeans_log[0].delta2:.3f}" + ('>\\varepsilon' if kmeans_log[0].delta2 > kmeans_epsilon else '\\leq\\varepsilon')

    params_lines: List[str] = list()
    for p in first_params:
      params_lines.append(f"{p:.6f}")
    self.context['omega_params_rbf'] = "\\begin{pmatrix}" + "\\\\".join(params_lines) + "\\end{pmatrix}"

  def compile_patterns(self):
    if not os.path.isdir(self.report_dir):
      raise NotADirectoryError(f"Invalid report directory: {self.report_dir}")

    env = Environment(loader=FileSystemLoader(self.report_dir))

    for root, _, files in os.walk(self.report_dir):
      for filename in files:
        if filename.endswith(".jinja"):
          rel_path = os.path.relpath(os.path.join(root, filename), self.report_dir)
          base, ext, _ = os.path.join(self.report_dir, rel_path).rsplit('.', 2)
          output_path = base + '.compiled.' + ext
          
          rendered_content = self._render_template(env, rel_path)
          
          os.makedirs(os.path.dirname(output_path), exist_ok=True)
          with open(output_path, "w") as f:
            f.write(rendered_content)

  def _render_template(self, env: Environment, template_name: str) -> str:
    if env.loader is None:
      raise RuntimeError("Jinja loader not initialized. Provide self.report_dir.")
    template_source, _, _ = env.loader.get_source(env, template_name)
    ast = env.parse(template_source)
    required_vars = meta.find_undeclared_variables(ast)

    render_kwargs = {v: self.context.get(v, "") for v in required_vars}
    
    template = env.get_template(template_name)
    return template.render(**render_kwargs)