from lib.models import State
from lib.math_utils import calc_parabola_coeffs, Point

def generate_plot(state: State, func_tikz: str) -> str:
  a, b, c = calc_parabola_coeffs(
    Point(state.x1, state.f1),
    Point(state.x2, state.f2),
    Point(state.x3, state.f3)
  )
  
  lines = [
    "\\begin{center}",
    "\\begin{tikzpicture}",
    "\\begin{axis}[",
    "  width=12cm, height=8cm,",
    "  grid=major,",
    "  grid style={dashed, black!30},",
    "  legend pos=outer north east,",
    "  enlargelimits=true,",
    "  xlabel={\\(x\\)},",
    "  ylabel={\\(f(x)\\)}",
    "]",
    f"\\addplot [domain={state.x1}:{state.x2}, samples=100, dashed, thick] {{{func_tikz}}};",
    "\\addlegendentry{Исходная функция}",
  ]
  
  if abs(a) > 1e-12 or abs(b) > 1e-12:
    min_x, max_x = min(state.x1, state.x3), max(state.x1, state.x3)
    span = max_x - min_x
    lines.extend([
      f"\\addplot [domain={min_x - span*0.2}:{max_x + span*0.2}, samples=100, solid, thick] {{{a}*x^2 + {b}*x + {c}}};",
      "\\addlegendentry{Аппроксимация}"
    ])
    
  lines.extend([
    f"\\addplot[only marks, mark=*, text=black] coordinates {{({state.x1}, {state.f1}) ({state.x2}, {state.f2}) ({state.x3}, {state.f3})}};",
    "\\addlegendentry{Узлы}",
  ])
  
  if state.x_star is not None and state.f_star is not None:
    lines.extend([
      f"\\addplot[only marks, mark=square*, text=black] coordinates {{({state.x_star}, {state.f_star})}};",
      "\\addlegendentry{\\(\\tilde{x}_{*}" + f"^{{({state.k})}}" + "\\)}"
    ])
    
  lines.extend([
    "\\end{axis}",
    "\\end{tikzpicture}",
    "\\end{center}"
  ])
  return "\n".join(lines)