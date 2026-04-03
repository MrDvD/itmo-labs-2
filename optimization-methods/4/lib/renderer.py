import os, math

class ReportRenderer:
  def __init__(self, config, func):
    self.config = config
    self.func = func
    self.templates_path = config.templates_dir

  def read_template(self, filename):
    path = os.path.join(self.templates_path, filename)
    with open(path, "r", encoding="utf-8") as f:
      return f.read()

  def replace_tags(self, text, data):
    for key, value in data.items():
      text = text.replace(f"[[{key}]]", str(value))
    return text

  def format_val(self, val):
    return f"{val:.{self.config.precision}f}"

  def build_cyclic_iterations(self, data):
    steps = ""
    z_levels = [self.format_val(self.func.evaluate(data[0]['prev_x']))]
    min_x, min_y, max_x, max_y = data[0]['prev_x'][0], data[0]['prev_x'][1], data[0]['prev_x'][0], data[0]['prev_x'][1]
    for i, row in enumerate(data[:3]):
      cyclic_template = self.read_template("cyclic_iterations.tex")
      z_levels.append(self.format_val(self.func.evaluate(data[i]['mid_x'])))
      z_levels.append(self.format_val(self.func.evaluate(data[i]['new_x'])))
      min_x = min(min_x, data[i]['mid_x'][0], data[i]['new_x'][0])
      min_y = min(min_y, data[i]['mid_x'][1], data[i]['new_x'][1])
      max_x = max(max_x, data[i]['mid_x'][0], data[i]['new_x'][0])
      max_y = max(max_y, data[i]['mid_x'][1], data[i]['new_x'][1])
      tags = {
        "K": row["k"],
        "K_PREV": row["k"] - 1,
        "A": self.func.a,
        "B": self.func.b,
        "C": self.func.c,
        "D": self.func.d,
        "E": self.func.e,
        "F": self.func.f,
        "X_MIN": self.format_val(min_x - 1),
        "X_MAX": self.format_val(max_x + 1),
        "Y_MIN": self.format_val(min_y - 1),
        "Y_MAX": self.format_val(max_y + 1),
        "X0": self.format_val(row["prev_x"][0]),
        "Y0": self.format_val(row["prev_x"][1]),
        "X1": self.format_val(row["mid_x"][0]),
        "Y1": self.format_val(row["mid_x"][1]),
        "X2": self.format_val(row["new_x"][0]),
        "Y2": self.format_val(row["new_x"][1]),
        "ALPHA_1": self.format_val(row["alpha"][0]),
        "ALPHA_2": self.format_val(row["alpha"][1]),
        "Z_LEVELS": ", ".join(z_levels),
        "CYCLIC_PATH_ITER": self.build_pgf_path(data[:i+1], True),
      }
      break_info = (row["new_x"] - row["prev_x"]).norm() 
      if break_info < self.config.epsilon:
        tags["BREAKPOINT_CHECK"] = f"|x^{{({tags['K']})}}-x^{{({tags['K_PREV']})}}|={self.format_val(break_info)}<{self.config.epsilon}\\implies\\tilde{{x}}^\\ast={row['new_x'].to_latex(self.config.precision)}"
      else:
        tags["BREAKPOINT_CHECK"] = f"|x^{{({tags['K']})}}-x^{{({tags['K_PREV']})}}|={self.format_val(break_info)}<{self.config.epsilon}\\implies\\text{{продолжаем алгоритм.}}"
      steps += self.replace_tags(cyclic_template, tags)
    return steps

  def build_gd_iterations(self, data):
    steps = ""
    z_levels = [self.format_val(self.func.evaluate(data[0]['prev_x']))]
    min_x, min_y, max_x, max_y = data[0]['prev_x'][0], data[0]['prev_x'][1], data[0]['prev_x'][0], data[0]['prev_x'][1]
    for i, row in enumerate(data[:3]):
      gd_template = self.read_template("gd_iterations.tex")
      z_levels.append(self.format_val(self.func.evaluate(data[i]['new_x'])))
      min_x = min(min_x, data[i]['new_x'][0])
      min_y = min(min_y, data[i]['new_x'][1])
      max_x = max(max_x, data[i]['new_x'][0])
      max_y = max(max_y, data[i]['new_x'][1])
      tags = {
        "K": row["k"],
        "K_PREV": row["k"] - 1,
        "A": self.func.a,
        "B": self.func.b,
        "C": self.func.c,
        "D": self.func.d,
        "E": self.func.e,
        "F": self.func.f,
        "X_MIN": self.format_val(min_x - 1),
        "X_MAX": self.format_val(max_x + 1),
        "Y_MIN": self.format_val(min_y - 1),
        "Y_MAX": self.format_val(max_y + 1),
        "X_PREV": self.format_val(row["prev_x"][0]),
        "Y_PREV": self.format_val(row["prev_x"][1]),
        "X_NEW": self.format_val(row["new_x"][0]),
        "Y_NEW": self.format_val(row["new_x"][1]),
        "OMEGA": row["grad"].to_latex(self.config.precision),
        "Z_LEVELS": ", ".join(z_levels),
        "GD_PATH_ITER": self.build_pgf_path(data[:i+1], False),
      }
      break_info = row['grad_norm']
      if break_info < self.config.epsilon:
        tags["BREAKPOINT_CHECK"] = f"|\omega^{{({row['k']})}}|={self.format_val(break_info)}<{self.config.epsilon}\\implies\\tilde{{x}}^\\ast={row['new_x'].to_latex(self.config.precision)}"
      else:
        tags["BREAKPOINT_CHECK"] = f"|\omega^{{({row['k']})}}|={self.format_val(break_info)}<{self.config.epsilon}\\implies\\text{{продолжаем алгоритм.}}"
      steps += self.replace_tags(gd_template, tags)
    return steps

  def build_steepest_iterations(self, data):
    steps = ""
    z_levels = [self.format_val(self.func.evaluate(data[0]['prev_x']))]
    min_x, min_y, max_x, max_y = data[0]['prev_x'][0], data[0]['prev_x'][1], data[0]['prev_x'][0], data[0]['prev_x'][1]
    for i, row in enumerate(data[:3]):
      gd_template = self.read_template("steepest_iterations.tex")
      z_levels.append(self.format_val(self.func.evaluate(data[i]['new_x'])))
      min_x = min(min_x, data[i]['new_x'][0])
      min_y = min(min_y, data[i]['new_x'][1])
      max_x = max(max_x, data[i]['new_x'][0])
      max_y = max(max_y, data[i]['new_x'][1])
      tags = {
        "K": row["k"],
        "K_PREV": row["k"] - 1,
        "A": self.func.a,
        "B": self.func.b,
        "C": self.func.c,
        "D": self.func.d,
        "E": self.func.e,
        "F": self.func.f,
        "X_MIN": self.format_val(min_x - 1),
        "X_MAX": self.format_val(max_x + 1),
        "Y_MIN": self.format_val(min_y - 1),
        "Y_MAX": self.format_val(max_y + 1),
        "U_X": self.format_val(row["u"][0]),
        "U_Y": self.format_val(row["u"][1]),
        "X_PREV": self.format_val(row["prev_x"][0]),
        "Y_PREV": self.format_val(row["prev_x"][1]),
        "X_NEW": self.format_val(row["new_x"][0]),
        "Y_NEW": self.format_val(row["new_x"][1]),
        "OMEGA": row["grad"].to_latex(self.config.precision),
        "OMEGA_NORM": self.format_val(row["grad_norm"]),
        "BETA": self.format_val(row["beta"]),
        "Z_LEVELS": ", ".join(z_levels),
        "STEEPEST_PATH_ITER": self.build_pgf_path(data[:i+1], False),
      }
      break_info = row['grad_norm']
      if break_info < self.config.epsilon:
        tags["BREAKPOINT_CHECK"] = f"|\omega^{{({row['k']})}}|={self.format_val(break_info)}<{self.config.epsilon}\\implies\\tilde{{x}}^\\ast={row['new_x'].to_latex(self.config.precision)}"
      else:
        tags["BREAKPOINT_CHECK"] = f"|\omega^{{({row['k']})}}|={self.format_val(break_info)}<{self.config.epsilon}\\implies\\text{{продолжаем алгоритм.}}"
      steps += self.replace_tags(gd_template, tags)
    return steps

  def build_cyclic_table(self, data):
    rows = ""
    for row in data:
      rows += f"{row['k']} & ${row['prev_x'].to_latex(self.config.precision)}$ & ${row['alpha'].to_latex(self.config.precision)}$ & ${row['new_x'].to_latex(self.config.precision)}$ & ${self.format_val(row['diff'])}$ \\\\\n\\hline\n"
    return rows

  def build_gd_table(self, data):
    rows = ""
    for row in data:
      rows += f"{row['k']} & ${row['prev_x'].to_latex(self.config.precision)}$ & ${row['grad'].to_latex(self.config.precision)}$ & ${row['new_x'].to_latex(self.config.precision)}$ & ${self.format_val(row['grad_norm'])}$ \\\\\n\\hline\n"
    return rows

  def build_steepest_table(self, data):
    rows = ""
    for row in data:
      rows += f"{row['k']} & ${row['prev_x'].to_latex(self.config.precision)}$ & ${row['u'].to_latex(self.config.precision)}$ & ${self.format_val(row['beta'])}$ & ${row['new_x'].to_latex(self.config.precision)}$ & ${self.format_val(row['grad_norm'])}$ \\\\\n\\hline\n"
    return rows
  
  def build_pgf_path(self, data, is_cyclic=False):
    lines = []
    for i, row in enumerate(data):
      is_last = (i == len(data) - 1)
      base_style = "" if is_last else "thin, gray!80, dashed"
      dots_style = "fill=black, mark=*, mark size=1pt" if is_last else "mark=*, mark size=1pt, draw=gray, fill=gray"
      
      px, py = row['prev_x'][0], row['prev_x'][1]
      nx, ny = row['new_x'][0], row['new_x'][1]
      
      if is_cyclic:
        mx, my = row['mid_x'][0], row['mid_x'][1]
        c1 = f"({px:.3f}, {py:.3f}) ({mx:.3f}, {my:.3f})"
        lines.append(f"\\addplot[{base_style}, -{{Stealth[scale=0.8]}}] coordinates {{{c1}}};")
        c2 = f"({mx:.3f}, {my:.3f}) ({nx:.3f}, {ny:.3f})"
        lines.append(f"\\addplot[{base_style}, -{{Stealth[scale=0.8]}}] coordinates {{{c2}}};")

        
        lines.append(f"\\addplot[{dots_style}] coordinates {{({px:.3f}, {py:.3f})}};")
        lines.append(f"\\addplot[{dots_style}] coordinates {{({mx:.3f}, {my:.3f})}};")
      else:
        coord_str = f"({px:.3f}, {py:.3f}) ({nx:.3f}, {ny:.3f})"
        lines.append(f"\\addplot[{base_style}, -Stealth] coordinates {{{coord_str}}};")
      if is_last:
        lines.append(f"\\addplot[{dots_style}] coordinates {{({nx:.3f}, {ny:.3f})}};")
    return "\n".join(lines)

  def render(self, context):
    main_tpl = self.read_template("main.tex")

    all_x_cyclic = [row["prev_x"][0] for row in context["cyclic_data"]] + \
                   [row["mid_x"][0] for row in context["cyclic_data"]] + \
                   [row["new_x"][0] for row in context["cyclic_data"]]
    all_y_cyclic = [row["prev_x"][1] for row in context["cyclic_data"]] + \
                   [row["mid_x"][1] for row in context["cyclic_data"]] + \
                   [row["new_x"][1] for row in context["cyclic_data"]]
    all_x_gd = [row["prev_x"][0] for row in context["gd_data"]] + \
               [row["new_x"][0] for row in context["gd_data"]]
    all_y_gd = [row["prev_x"][1] for row in context["gd_data"]] + \
               [row["new_x"][1] for row in context["gd_data"]]
    all_x_steepest = [row["prev_x"][0] for row in context["steepest_data"]] + \
                     [row["new_x"][0] for row in context["steepest_data"]]
    all_y_steepest = [row["prev_x"][1] for row in context["steepest_data"]] + \
                     [row["new_x"][1] for row in context["steepest_data"]]
    
    replacements = {
      "VARIANT": context["variant"],
      "EPSILON": context["epsilon"],
      "X0": context["x0"].to_latex(self.config.precision),
      # "TARGET_POINT": f"({context['target_point'][0]}, {context['target_point'][1]})",
      "A": self.func.a,
      "B": self.func.b,
      "C": self.func.c,
      "D": self.func.d,
      "E": self.func.e,
      "F": self.func.f,
      
      "CYCLIC_ITERATIONS": self.build_cyclic_iterations(context["cyclic_data"]),
      "CYCLIC_TABLE": self.build_cyclic_table(context["cyclic_data"]),
      "CYCLIC_PATH": self.build_pgf_path(context["cyclic_data"], True),
      "X_MIN_CYCLIC": min(all_x_cyclic) - 1,
      "X_MAX_CYCLIC": max(all_x_cyclic) + 1,
      "Y_MIN_CYCLIC": min(all_y_cyclic) - 1,
      "Y_MAX_CYCLIC": max(all_y_cyclic) + 1,
      
      "GD_ETA": context["gd_eta"],
      "GD_ITERATIONS": self.build_gd_iterations(context["gd_data"]),
      "GD_TABLE": self.build_gd_table(context["gd_data"]),
      "GD_PATH": self.build_pgf_path(context["gd_data"], False),
      "X_MIN_GD": min(all_x_gd) - 1,
      "X_MAX_GD": max(all_x_gd) + 1,
      "Y_MIN_GD": min(all_y_gd) - 1,
      "Y_MAX_GD": max(all_y_gd) + 1,
      
      "STEEPEST_ITERATIONS": self.build_steepest_iterations(context["steepest_data"]),
      "STEEPEST_TABLE": self.build_steepest_table(context["steepest_data"]),
      "STEEPEST_PATH": self.build_pgf_path(context["steepest_data"], False),
      "X_MIN_STEEPEST": min(all_x_steepest) - 1,
      "X_MAX_STEEPEST": max(all_x_steepest) + 1,
      "Y_MIN_STEEPEST": min(all_y_steepest) - 1,
      "Y_MAX_STEEPEST": max(all_y_steepest) + 1,
      
      "FINAL_CYCLIC": context["cyclic_data"][-1]['new_x'].to_latex(self.config.precision),
      "FINAL_GD": context["gd_data"][-1]['new_x'].to_latex(self.config.precision),
      "FINAL_STEEPEST": context["steepest_data"][-1]['new_x'].to_latex(self.config.precision),
    }
    
    output = self.replace_tags(main_tpl, replacements)
    
    with open(self.config.output_file, "w", encoding="utf-8") as f:
      f.write(output)