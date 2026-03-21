from lib.models import State
from lib.latex_generator import ReportGenerator
from lib.math_utils import calc_x_star, get_true_min, calc_x2_initial
import math

def f(x: float) -> float:
  return x ** 2 - 3 * x + x * math.log(x)

def compile_latex(doc_content: str) -> None:
  with open("report.tex", "w", encoding="utf-8") as f_out:
    f_out.write(doc_content)
  print("Saved to report.tex. Please run `xelatex report.tex`.")

def main() -> None:
  func_tex = r"x^2-3x+x\ln x"
  func_tikz = r"x^2 - 3*x + x*ln(x)"
  a, b = 0.9, 2.0
  eps = 0.0001
  
  real_min_x, real_min_f = get_true_min(a, b, f)
  
  with open("lib/preamble.tex", "r", encoding="utf-8") as file:
    preamble = file.read()
  
  doc = [preamble]
  
  rg = ReportGenerator(f, func_tex, func_tikz, real_min_x, real_min_f, a, b, eps)
  doc.append(rg.generate_intro())
  
  x1, x3 = a, b
  x2, _ = calc_x2_initial(x1, x3, f)
  doc.append(rg.generate_initialization(x1, x2, x3))
  
  current_state = State(1, x1, x2, x3, f(x1), f(x2), f(x3))
  states: list[State] = []
  
  while True:
    states.append(current_state)
    
    current_state.x_star = calc_x_star(current_state.x1, current_state.x2, current_state.x3, 
                                       current_state.f1, current_state.f2, current_state.f3)
    current_state.f_star = f(current_state.x_star)
    
    interval_len = current_state.x3 - current_state.x1
    
    if current_state.k <= 3:
      doc.append(rg.generate_iteration(current_state, detailed=True))
    
    x_star, f_star = current_state.x_star, current_state.f_star
    if (x_star >= current_state.x2) and (x_star <= current_state.x3):
      current_state.condition = 'а' if f_star <= current_state.f2 else 'б'
    else:
      current_state.condition = 'в' if f_star <= current_state.f2 else 'г'

    if interval_len < eps:
      break
      
    current_state = rg.get_next_state(current_state)
    
  if len(states) > 3:
    doc.append(rg.generate_table(states[3:]))
    
  doc.append("\\end{document}")
  compile_latex("\n".join(doc))

if __name__ == "__main__":
  main()