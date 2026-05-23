import os
from typing import Dict
from jinja2 import Environment, FileSystemLoader, meta, Template

class ReportFiller:
  def __init__(self, context: Dict[str, str], report_dir: str):
    self.context: Dict[str, str] = context
    self.report_dir = report_dir
    self.env = Environment(loader=FileSystemLoader(report_dir))

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
  
  def add_plot(self, report_dir: str, num: str, filename: str, a: str, b: str, ya: str, eps: str, cheb_calc: str, cheb_an: str, iters: str):
    template_path = os.path.join(report_dir, 'body', 'plot.tex.j2')
  
    if not os.path.exists(template_path):
      raise FileNotFoundError(f"Template not found: {template_path}")
      
    with open(template_path, 'r', encoding='utf-8') as f:
      template = Template(f.read())
      
      rendered_snippet = template.render(
        odu_equation_num=num,
        odu_a=a,
        odu_b=b,
        odu_ya=ya,
        odu_eps=eps,
        odu_chebyshev_calc=cheb_calc,
        odu_chebyshev_an=cheb_an,
        odu_iters=iters,
        filename=f"pics/{filename}",
      )
      self.context['odu_plots'] = self.context.get('odu_plots', '') + rendered_snippet + '\n'

  def _render_template(self, env: Environment, template_name: str) -> str:
    if env.loader is None:
      raise RuntimeError("Jinja loader not initialized. Provide self.report_dir.")
    template_source, _, _ = env.loader.get_source(env, template_name)
    ast = env.parse(template_source)
    required_vars = meta.find_undeclared_variables(ast)

    render_kwargs = {v: self.context.get(v, "") for v in required_vars}
    
    template = env.get_template(template_name)
    return template.render(**render_kwargs)