from typing import Callable
from lib.models import State
from lib.math_utils import calc_x_star
from lib.tikz_generator import generate_plot

class ReportGenerator:
  def __init__(self, func: Callable[[float], float], func_tex: str, func_tikz: str, 
               real_min_x: float, real_min_f: float, a: float, b: float, eps: float) -> None:
    self.func = func
    self.func_tex = func_tex
    self.func_tikz = func_tikz
    self.real_min_x = real_min_x
    self.real_min_f = real_min_f
    self.a = a
    self.b = b
    self.eps = eps
    self.states: list[State] = []
    
  def format_float(self, val: float, precision: int = 7) -> str:
    return f"{val:.{precision}f}".rstrip('0').rstrip('.') if '.' in f"{val:.{precision}f}" else f"{val:.{precision}f}"

  def generate_intro(self) -> str:
    lines = [
      "\\section{Метод квадратичной аппроксимации}",
      "\\subsection{Применимость метода}",
      f"Дана функция одной переменной \\( f(x) = {self.func_tex} \\), определённая на отрезке \\( [{self.a}, {self.b}] \\).",
      "Метод применим, так как функция предполагается унимодальной и непрерывной на заданном отрезке, что гарантирует существование единственного минимума, сходимость алгоритма и возможность аппроксимации многочленом.",
      "\\subsection{График исходной функции и реальный минимум}",
      f"Точка минимума из графика: \\( x_* \\approx {self.format_float(self.real_min_x)} \\), \\( f(x_*) \\approx {self.format_float(self.real_min_f)} \\).",
    ]
    
    init_state = State(0, self.a, (self.a + self.b) / 2, self.b, 
                       self.func(self.a), self.func((self.a + self.b) / 2), self.func(self.b))
    lines.append(generate_plot(init_state, self.func_tikz))
    return "\n".join(lines)

  def generate_initialization(self, x1: float, x2: float, x3: float) -> str:
    f1, f2, f3 = self.func(x1), self.func(x2), self.func(x3)
    return "\n".join([
      "\\subsection{Начальные значения}",
      "Выберем начальные точки так, чтобы выполнялось условие \\( f_2 \\le f_1 \\) и \\( f_2 \\le f_3 \\):",
      "\\begin{itemize}",
      f"  \\item \\( x_1^{{(1)}} = {self.format_float(x1)}, \\; f_1^{{(1)}} = {self.format_float(f1)} \\)",
      f"  \\item \\( x_2^{{(1)}} = {self.format_float(x2)}, \\; f_2^{{(1)}} = {self.format_float(f2)} \\)",
      f"  \\item \\( x_3^{{(1)}} = {self.format_float(x3)}, \\; f_3^{{(1)}} = {self.format_float(f3)} \\)",
      "\\end{itemize}"
    ])

  def generate_iteration(self, state: State, detailed: bool = True) -> str:
    lines = [f"\\subsection{{Итерация {state.k}}}"]
    interval_len = state.x3 - state.x1
    
    lines.append(f"Проверка критерия останова: интервал неопределенности равен \\( {self.format_float(state.x3)} - {self.format_float(state.x1)} = {self.format_float(interval_len)} \\).")
    if interval_len < self.eps:
      lines.append(f"Так как \\( {self.format_float(interval_len)} < {self.eps} \\), критерий останова выполнен.")
      return "\n".join(lines)
    else:
      lines.append(f"Так как \\( {self.format_float(interval_len)} \\ge {self.eps} \\), продолжаем вычисления.")
      lines.append("\n")

    state.x_star = calc_x_star(state.x1, state.x2, state.x3, state.f1, state.f2, state.f3)
    state.f_star = self.func(state.x_star)
    
    if detailed:
      r23 = state.x2**2 - state.x3**2
      r31 = state.x3**2 - state.x1**2
      r12 = state.x1**2 - state.x2**2
      s23 = state.x2 - state.x3
      s31 = state.x3 - state.x1
      s12 = state.x1 - state.x2
      
      lines.append("Вычисляем \\( \\tilde{x}_{*}^{(%d)} \\):" % state.k)
      if state.k == 1:
        lines.append("\\begin{multline*}")
        lines.append("\\tilde{x}_{*}^{(1)} = \\frac{1}{2}\\cdot\\frac{f_1(x_2^2 - x_3^2) + f_2(x_3^2 - x_1^2) + f_3(x_1^2 - x_2^2)}{f_1(x_2 - x_3) + f_2(x_3 - x_1) + f_3(x_1 - x_2)} = \\\\")
        lines.append(f"= \\frac{{1}}{{2}}\\cdot\\frac{{{self.format_float(state.f1)}({self.format_float(r23)}) + {self.format_float(state.f2)}({self.format_float(r31)}) + {self.format_float(state.f3)}({self.format_float(r12)})}}{{{self.format_float(state.f1)}({self.format_float(s23)}) + {self.format_float(state.f2)}({self.format_float(s31)}) + {self.format_float(state.f3)}({self.format_float(s12)})}} = {self.format_float(state.x_star)}")
        lines.append("\\end{multline*}")
      else:
        lines.append("$$ \\tilde{x}_{*}^{(%d)} = \\frac{1}{2}\\cdot\\frac{%s(%s) + %s(%s) + %s(%s)}{%s(%s) + %s(%s) + %s(%s)} = %s $$" % (
          state.k, 
          self.format_float(state.f1), self.format_float(r23),
          self.format_float(state.f2), self.format_float(r31),
          self.format_float(state.f3), self.format_float(r12),
          self.format_float(state.f1), self.format_float(s23),
          self.format_float(state.f2), self.format_float(s31),
          self.format_float(state.f3), self.format_float(s12),
          self.format_float(state.x_star)
        ))
      
      lines.append(r"Вычисляем значение функции: \( \tilde{f}_{*}^{(" + str(state.k) + r")} = f(" + self.format_float(state.x_star) + r") = " + self.format_float(state.f_star) + r"\).")
      
      cond_a_1 = (state.x_star >= state.x2) and (state.x_star <= state.x3)
      cond_a_2 = state.f_star <= state.f2
      cond_a = cond_a_1 and cond_a_2
      
      cond_b_1 = (state.x_star >= state.x2) and (state.x_star <= state.x3)
      cond_b_2 = state.f_star > state.f2
      cond_b = cond_b_1 and cond_b_2
      
      cond_c_1 = (state.x_star >= state.x1) and (state.x_star <= state.x2)
      cond_c_2 = state.f_star <= state.f2
      cond_c = cond_c_1 and cond_c_2
      
      cond_d_1 = (state.x_star >= state.x1) and (state.x_star <= state.x2)
      cond_d_2 = state.f_star > state.f2
      cond_d = cond_d_1 and cond_d_2

      lines.append(f"Проверяем условия выбора новой тройки точек при $f_2^{{({state.k})}} = {state.f2}$:")
      lines.append("\\begin{itemize}")
      lines.append(f"  \\item а) \\( \\tilde{{x}}_{{*}}^{{({state.k})}} \\in [x_2, x_3] \\) и \\( \\tilde{{f}}_{{*}}^{{({state.k})}} \\le f_2^{{({state.k})}} \\) --- {'Истинно' if cond_a else 'Ложно'}.")
      lines.append(f"  \\item б) \\( \\tilde{{x}}_{{*}}^{{({state.k})}} \\in [x_2, x_3] \\) и \\( \\tilde{{f}}_{{*}}^{{({state.k})}} > f_2^{{({state.k})}} \\) --- {'Истинно' if cond_b else 'Ложно'}.")
      lines.append(f"  \\item в) \\( \\tilde{{x}}_{{*}}^{{({state.k})}} \\in [x_1, x_2] \\) и \\( \\tilde{{f}}_{{*}}^{{({state.k})}} \\le f_2^{{({state.k})}} \\) --- {'Истинно' if cond_c else 'Ложно'}.")
      lines.append(f"  \\item г) \\( \\tilde{{x}}_{{*}}^{{({state.k})}} \\in [x_1, x_2] \\) и \\( \\tilde{{f}}_{{*}}^{{({state.k})}} > f_2^{{({state.k})}} \\) --- {'Истинно' if cond_d else 'Ложно'}.")
      lines.append("\\end{itemize}")
      
      if cond_a: state.condition = 'а'
      elif cond_b: state.condition = 'б'
      elif cond_c: state.condition = 'в'
      elif cond_d: state.condition = 'г'
      
      lines.append(f"Выполнено условие {state.condition}).")
      lines.append(generate_plot(state, self.func_tikz))
      
    return "\n".join(lines)

  def get_next_state(self, state: State) -> State:
    x_star, f_star = state.x_star, state.f_star
    k_next = state.k + 1
    
    cond_a_1 = (x_star >= state.x2) and (x_star <= state.x3)
    cond_a_2 = f_star <= state.f2
    cond_b_1 = (x_star >= state.x2) and (x_star <= state.x3)
    cond_b_2 = f_star > state.f2
    cond_c_1 = (x_star >= state.x1) and (x_star <= state.x2)
    cond_c_2 = f_star <= state.f2
    
    if cond_a_1 and cond_a_2:
      return State(k_next, state.x2, x_star, state.x3, state.f2, f_star, state.f3)
    elif cond_b_1 and cond_b_2:
      return State(k_next, state.x1, state.x2, x_star, state.f1, state.f2, f_star)
    elif cond_c_1 and cond_c_2:
      return State(k_next, state.x1, x_star, state.x2, state.f1, f_star, state.f2)
    else:
      return State(k_next, x_star, state.x2, state.x3, f_star, state.f2, state.f3)

  def generate_table(self, remaining_states: list[State]) -> str:
    lines = [
      "\\newpage",
      "\\begin{landscape}",
      "\\section{Таблица результатов}",
      "\\subsection{Остальные итерации}",
      "\\begin{longtable}{|c|c|c|c|c|c|c|c|}",
      "\\hline",
      "\\( k \\) & \\( x_1^{(k)} \\) & \\( x_2^{(k)} \\) & \\( x_3^{(k)} \\) & "
      "\\( \\tilde{x}_{*}^{(k)} \\) & \\( f(\\tilde{x}_{*}^{(k)}) \\) & "
      "\\( f_2^{(k)} \\) & Условие \\\\",
      "\\hline",
      "\\endhead"
    ]
    
    for s in remaining_states:
      cond = s.condition if s.condition else "-"
      lines.append(
        f"{s.k} & {self.format_float(s.x1, 12)} & {self.format_float(s.x2, 12)} & "
        f"{self.format_float(s.x3, 12)} & {self.format_float(s.x_star, 12)} & "
        f"{self.format_float(s.f_star, 12)} & {self.format_float(s.f2, 12)} & {cond} \\\\"
      )
      lines.append("\\hline")
      
    lines.extend([
      "\\end{longtable}",
      "\\end{landscape}"
    ])
    return "\n".join(lines)