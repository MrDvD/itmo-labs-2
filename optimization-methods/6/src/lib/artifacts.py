import os
import re
from typing import Dict
from jinja2 import Environment, FileSystemLoader, meta

class ArtifactsFiller:
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