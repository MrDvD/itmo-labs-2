import math
import os
import numpy as np
from typing import Callable, List, Dict, Any, Union
from numpy.typing import NDArray
import matplotlib.pyplot as plt

class NewtonPlot:
  def __init__(self, f: Callable[[float, float], float], save_dir: str = ".") -> None:
    self.f = f
    self.save_dir = save_dir

  def generate(self, seq_data: List[Dict[str, Any]]) -> None:
    if self.save_dir and self.save_dir != ".":
      os.makedirs(self.save_dir, exist_ok=True)
      
    for s_idx, data in enumerate(seq_data):
      idx: int = data['i']
      x: float = data['x']
      y: float = data['y']
      next_x: float = data['next_x']
      next_y: float = data['next_y']
      
      history = seq_data[:s_idx]
      all_x = [d['x'] for d in history] + [x, next_x]
      all_y = [d['y'] for d in history] + [y, next_y]
      
      x_min, x_max = min(all_x), max(all_x)
      y_min, y_max = min(all_y), max(all_y)
      
      margin_x = abs(x_max - x_min) * 0.3 if x_max != x_min else 0.6
      margin_y = abs(y_max - y_min) * 0.3 if y_max != y_min else 0.6
      if margin_x == 0: margin_x = 0.6
      if margin_y == 0: margin_y = 0.6
      
      x_min -= margin_x
      x_max += margin_x
      y_min -= margin_y
      y_max += margin_y
      
      x_vals: NDArray[np.floating[Any]] = np.linspace(x_min, x_max, 100)
      y_vals: NDArray[np.floating[Any]] = np.linspace(y_min, y_max, 100)
      X, Y = np.meshgrid(x_vals, y_vals)
      
      Z: NDArray[np.floating[Any]] = np.zeros_like(X)
      for r in range(X.shape[0]):
        for c in range(X.shape[1]):
          Z[r, c] = self.f(X[r, c], Y[r, c])
          
      plt.figure(figsize=(8, 6))
      
      current_levels = sorted(list(set([self.f(d['x'], d['y']) for d in history] + [self.f(x, y), self.f(next_x, next_y)])))
      
      if len(current_levels) > 1:
        contour_colors = [str(g) for g in np.linspace(0.3, 0.6, len(current_levels))]
      else:
        contour_colors = ["0.4"]
        
      contours = plt.contour(X, Y, Z, levels=current_levels, colors=contour_colors, alpha=0.8)
      plt.clabel(contours, inline=True, fontsize=8, fmt="%.2f")
      
      for h_data in history:
        plt.quiver(h_data['x'], h_data['y'], h_data['next_x'] - h_data['x'], h_data['next_y'] - h_data['y'],
                   angles='xy', scale_units='xy', scale=1, color='lightgray', width=0.004, headwidth=4, alpha=0.5)
        plt.scatter([h_data['x']], [h_data['y']], color='lightgray', s=50, zorder=4, alpha=0.5)
      
      plt.quiver(x, y, next_x - x, next_y - y, angles='xy', scale_units='xy', scale=1, 
                 color='red', width=0.004, headwidth=4, label=f'$\Delta \mathbf{{x}}^{{({idx})}}$')
      
      plt.scatter([x], [y], color='black', s=50, zorder=5, label=f'$\mathbf{{x}}^{{({idx-1})}}$')
      plt.scatter([next_x], [next_y], color='green', marker='*', s=150, zorder=6, label=f'$\mathbf{{x}}^{{({idx})}}$')
      
      plt.xlabel("x")
      plt.ylabel("y")
      plt.grid(True, linestyle=":", alpha=0.5)
      plt.legend(loc='upper right')
      
      out_path: str = os.path.join(self.save_dir, f"newton_iteration_{idx}.pdf")
      plt.savefig(out_path, format="pdf", bbox_inches="tight")
      plt.close()

class NewtonOptimizer:
  def __init__(self, 
               f: Callable[[float, float], float], 
               grad: Callable[[float, float], List[float]], 
               hess: Callable[[float, float], List[List[float]]], 
               eps: float = 1e-4, 
               max_iter: int = 20) -> None:
    self.f = f
    self.grad = grad
    self.hess = hess
    self.eps = eps
    self.max_iter = max_iter
    self.iterations: List[Dict[str, Any]] = []
    self.raw_history: List[Dict[str, Any]] = []

  def _fmt(self, val: Union[int, float, str]) -> str:
    if isinstance(val, (int, float)):
      if abs(val - round(val)) < 1e-9:
        return str(int(round(val)))
      return f"{val:.5f}"
    return str(val)

  def optimize(self, x_start: float, y_start: float) -> List[float]:
    self.iterations = []
    x, y = float(x_start), float(y_start)
    
    for idx in range(1, self.max_iter + 1):
      g = self.grad(x, y)
      grad_x, grad_y = g[0], g[1]
      grad_norm = math.sqrt(grad_x**2 + grad_y**2)
      
      H = self.hess(x, y)
      h11, h12 = H[0][0], H[0][1]
      h21, h22 = H[1][0], H[1][1]
      
      det = h11 * h22 - h12 * h21
      if abs(det) < 1e-12:
        h11 += 1e-6
        h22 += 1e-6
        det = h11 * h22 - h12 * h21
        
      dx = (-grad_x * h22 - (-grad_y) * h12) / det
      dy = (h11 * (-grad_y) - h21 * (-grad_x)) / det
      
      next_x = x + dx
      next_y = y + dy
      z_val = self.f(next_x, next_y)

      self.raw_history.append({
        'i': idx, 'x': x, 'y': y, 'next_x': next_x, 'next_y': next_y
      })
      
      self.iterations.append({
        'i': idx,
        'x': self._fmt(x),
        'y': self._fmt(y),
        'grad_x': self._fmt(grad_x),
        'grad_y': self._fmt(grad_y),
        'grad_norm': self._fmt(grad_norm),
        'h11': self._fmt(h11),
        'h12': self._fmt(h12),
        'h21': self._fmt(h21),
        'h22': self._fmt(h22),
        'dx': self._fmt(dx),
        'dy': self._fmt(dy),
        'next_x': self._fmt(next_x),
        'next_y': self._fmt(next_y),
        'z_val': self._fmt(z_val)
      })
      
      if grad_norm <= self.eps:
        break
        
      x, y = next_x, next_y
      
    return [x, y]