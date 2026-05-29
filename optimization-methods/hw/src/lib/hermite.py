import math
import os
from typing import Callable, List, Dict, Any, Union
import matplotlib.pyplot as plt

class PlotApprox:
  def __init__(self, f: Callable[[float], float], save_dir: str = ".") -> None:
    self.f: Callable[[float], float] = f
    self.save_dir: str = save_dir

  def generate(self, seq_data: List[Dict[str, Any]]) -> None:
    if self.save_dir and self.save_dir != ".":
      os.makedirs(self.save_dir, exist_ok=True)
      
    for data in seq_data:
      x0: float = data['x0']
      x1: float = data['x1']
      h: float = data['h']
      f0: float = data['f0']
      f1: float = data['f1']
      df0: float = data['df0']
      df1: float = data['df1']
      idx: int = data['i']

      x_opt: float = data.get('x_opt', x0 + h * data.get('t_opt', 0.0))
      f_opt: float = self.f(x_opt)
      
      margin: float = max(0.2 * abs(h), 0.1)
      start_x: float = min(x0, x1, x_opt) - margin
      end_x: float = max(x0, x1, x_opt) + margin
      
      steps: int = 500
      step_size: float = (end_x - start_x) / steps
      x_vals: List[float] = [start_x + i * step_size for i in range(steps + 1)]
      
      y_true: List[float] = [self.f(x) for x in x_vals]
      y_approx: List[float] = []
      
      for x in x_vals:
        t: float = (x - x0) / h
        h00: float = 1.0 - 3.0 * t**2 + 2.0 * t**3
        h10: float = t - 2.0 * t**2 + t**3
        h01: float = 3.0 * t**2 - 2.0 * t**3
        h11: float = -t**2 + t**3
        val: float = h00 * f0 + h10 * h * df0 + h01 * f1 + h11 * h * df1
        y_approx.append(val)
        
      plt.figure(figsize=(8, 6))
      plt.plot(x_vals, y_true, label="f(x)", color="blue", linewidth=2)
      plt.plot(x_vals, y_approx, label="$H_3(x)$", color="red", linestyle="--", linewidth=2)
      
      plt.scatter([x0, x1], [f0, f1], color="black", s=40, zorder=5, label="($x_0, x_1$)")
      
      plt.scatter([x_opt], [f_opt], color="green", marker="*", s=150, zorder=6, label="$x^*$")

      plt.xlabel("x")
      plt.ylabel("y")
      plt.grid(True, linestyle=":", alpha=0.6)
      plt.legend()
      
      out_path: str = os.path.join(self.save_dir, f"hermite_iteration_{idx}.pdf")
      plt.savefig(out_path, format="pdf", bbox_inches="tight")
      plt.close()

class HermiteOptimizer:
  def __init__(self, f: Callable[[float], float], df: Callable[[float], float], eps: float = 1e-3, max_iter: int = 10) -> None:
    self.f: Callable[[float], float] = f
    self.df: Callable[[float], float] = df
    self.eps: float = eps
    self.max_iter: int = max_iter
    self.iterations: List[Dict[str, Any]] = []
    self.history: List[Dict[str, Any]] = []
    self.raw_history: List[Dict[str, Any]] = []

  def _fmt(self, val: Union[int, float, str]) -> str:
    if isinstance(val, (int, float)):
      if abs(val - round(val)) < 1e-9:
        return str(int(round(val)))
      return f"{val:.5f}"
    return str(val)

  def optimize(self, x0_start: Union[int, float], x1_start: Union[int, float]) -> float:
    self.iterations = []
    self.history = []
    self.raw_history = []
    x0: float = float(x0_start)
    x1: float = float(x1_start)

    x_opt = 0.0
    
    for idx in range(1, self.max_iter + 1):
      h: float = x1 - x0
      f0: float = self.f(x0)
      f1: float = self.f(x1)
      df0: float = self.df(x0)
      df1: float = self.df(x1)
      
      a: float = 6 * (f0 - f1) + 3 * h * (df0 + df1)
      b: float = 6 * (f1 - f0) - h * (4 * df0 + 2 * df1)
      c: float = h * df0
      
      t1: float = 0.0
      t2: float = 0.0
      
      if abs(a) < 1e-9:
        t1 = -c / b if abs(b) > 1e-9 else 0.0
        t2 = t1
      else:
        descr: float = b**2 - 4 * a * c
        if descr < 0:
          descr = 0.0
        t1 = (-b - math.sqrt(descr)) / (2 * a)
        t2 = (-b + math.sqrt(descr)) / (2 * a)
      
      d2H_t1: float = 2 * a * t1 + b
      d2H_t2: float = 2 * a * t2 + b
      
      sign1: str = ">" if d2H_t1 > 0 else "<" if d2H_t1 < 0 else "="
      type1: str = "локальный минимум" if d2H_t1 > 0 else "локальный максимум"
      
      sign2: str = ">" if d2H_t2 > 0 else "<" if d2H_t2 < 0 else "="
      type2: str = "локальный минимум" if d2H_t2 > 0 else "локальный максимум"
      
      t_opt: float = t1
      if d2H_t2 > 0 and (0 <= t2 <= 1 or not (0 <= t1 <= 1)):
        t_opt = t2
        
      x_opt: float = x0 + h * t_opt
      f_x_opt: float = self.f(x_opt)
      df_x_opt: float = self.df(x_opt)
      abs_df: float = abs(df_x_opt)

      self.raw_history.append({
        'i': idx, 'x0': x0, 'x1': x1, 'h': h, 'f0': f0, 'f1': f1, 'df0': df0, 'df1': df1, 'x_opt': x_opt
      })
      
      sign_df: str = ">" if df_x_opt > 0 else "<" if df_x_opt < 0 else "="
      
      new_x0: float = x0
      new_x1: float = x1
      if df_x_opt < 0:
        new_x0 = x_opt
        new_x1 = x1
      else:
        new_x0 = x0
        new_x1 = x_opt
        
      self.iterations.append({
        'i': idx,
        'x0': self._fmt(x0), 'x1': self._fmt(x1), 'h': self._fmt(h),
        'f0': self._fmt(f0), 'f1': self._fmt(f1),
        'df0': self._fmt(df0), 'df1': self._fmt(df1),
        't1': self._fmt(t1), 't2': self._fmt(t2),
        'val1': self._fmt(d2H_t1), 'sign1': sign1, 'type1': type1,
        'val2': self._fmt(d2H_t2), 'sign2': sign2, 'type2': type2,
        't_opt': self._fmt(t_opt), 'x_opt': self._fmt(x_opt),
        'df_x_opt': self._fmt(df_x_opt), 'abs_df_x_opt': self._fmt(abs_df),
        'sign_df': sign_df,
        'new_x0': self._fmt(new_x0), 'new_x1': self._fmt(new_x1)
      })
      
      self.history.append({
        'i': idx,
        'x0': self._fmt(x0),
        'x1': self._fmt(x1),
        'h': self._fmt(h),
        't_opt': self._fmt(t_opt),
        'x_opt': self._fmt(x_opt),
        'f_x_opt': self._fmt(f_x_opt),
        'df_x_opt': self._fmt(df_x_opt)
      })
      
      if abs_df <= self.eps:
        break
        
      x0 = new_x0
      x1 = new_x1
      
    return x_opt