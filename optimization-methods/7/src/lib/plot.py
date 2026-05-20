import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from typing import Tuple, Callable, List
from numpy.typing import NDArray

class Visualizer:
  def __init__(self, x_range: Tuple[float, float], y_range: Tuple[float, float], resolution: int = 50, output_dir: str = "plots") -> None:
    self.x_range = x_range
    self.y_range = y_range
    self.resolution = resolution
    self.output_dir = output_dir
    if not os.path.exists(self.output_dir):
      os.makedirs(self.output_dir)
  
  def plot_contour_lines(
    self,
    predict_func: Callable[[np.ndarray, np.ndarray], np.ndarray],
    saddle_points: Tuple[NDArray[np.floating], NDArray[np.floating]],
    min_points: Tuple[NDArray[np.floating], NDArray[np.floating]],
    filename: str
  ) -> None:
    padding_x = (self.x_range[1] - self.x_range[0]) * 0.05 if self.x_range[0] != self.x_range[1] else 1.0
    padding_y = (self.y_range[1] - self.y_range[0]) * 0.05 if self.y_range[0] != self.y_range[1] else 1.0
    x_limits = (self.x_range[0] - padding_x, self.x_range[1] + padding_x)
    y_limits = (self.y_range[0] - padding_y, self.y_range[1] + padding_y)
    plot_x = np.linspace(x_limits[0], x_limits[1], 200)
    plot_y = np.linspace(y_limits[0], y_limits[1], 200)
    X_plot_grid, Y_plot_grid = np.meshgrid(plot_x, plot_y)

    Z_pred_grid = predict_func(X_plot_grid, Y_plot_grid)
    
    plt.figure(figsize=(8, 6))
    
    contour = plt.contourf(X_plot_grid, Y_plot_grid, Z_pred_grid, levels=25, cmap='viridis', alpha=0.9)
    plt.xlabel('X', fontsize=10)
    plt.ylabel('Y', fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.scatter(saddle_points[0], saddle_points[1], c='white', s=120, edgecolors='black', label='Saddle point')
    plt.scatter(min_points[0], min_points[1], c='red', s=120, edgecolors='black', label='Global Min')
    cbar = plt.colorbar(contour, label='F(X, Y)')
    cbar.ax.tick_params(labelsize=9)
    plt.legend(loc='upper right')
    
    plt.tight_layout()
    plt.savefig(os.path.join(self.output_dir, filename))
    plt.close()
  
  def plot_optimization_trajectory(
    self,
    predict_func: Callable[[np.ndarray, np.ndarray], np.ndarray],
    history: List[Tuple[float, float]],
    saddle_points: Tuple[NDArray[np.floating], NDArray[np.floating]],
    min_points: Tuple[NDArray[np.floating], NDArray[np.floating]],
    line_count: int,
    filename: str
  ) -> None:
    history_x = np.array([p[0] for p in history])
    history_y = np.array([p[1] for p in history])

    x_min = min(self.x_range[0], history_x.min())
    x_max = max(self.x_range[1], history_x.max())
    y_min = min(self.y_range[0], history_y.min())
    y_max = max(self.y_range[1], history_y.max())
    
    padding_x = (x_max - x_min) * 0.05 if x_max != x_min else 1.0
    padding_y = (y_max - y_min) * 0.05 if y_max != y_min else 1.0
    
    x_limits = (x_min - padding_x, x_max + padding_x)
    y_limits = (y_min - padding_y, y_max + padding_y)

    plot_x = np.linspace(x_limits[0], x_limits[1], 200)
    plot_y = np.linspace(y_limits[0], y_limits[1], 200)
    X_plot_grid, Y_plot_grid = np.meshgrid(plot_x, plot_y)
    
    Z_pred_grid = predict_func(X_plot_grid, Y_plot_grid)
    history_z = predict_func(history_x, history_y)
    
    exact_levels = np.unique(np.sort(history_z[:line_count]))
    
    if len(exact_levels) < 2:
      exact_levels = np.linspace(Z_pred_grid.min(), Z_pred_grid.max(), 25)

    plt.figure(figsize=(10, 8))
    
    contour_f = plt.contourf(X_plot_grid, Y_plot_grid, Z_pred_grid, levels=25, cmap='viridis', alpha=0.5)
    plt.contour(
      X_plot_grid, Y_plot_grid, Z_pred_grid, 
      levels=exact_levels, 
      colors='black', 
      linewidths=0.7, 
      linestyles='dashed',
      alpha=0.8
    )
    
    box = patches.Rectangle(
      (self.x_range[0], self.y_range[0]),
      self.x_range[1] - self.x_range[0],
      self.y_range[1] - self.y_range[0],
      linewidth=2,
      edgecolor='red',
      facecolor='none',
      linestyle='--',
      label='Boundary Domain',
      zorder=5
    )
    plt.gca().add_patch(box)            
    
    plt.plot(history_x, history_y, color='gray', linewidth=2, zorder=3)
    plt.scatter(history_x, history_y, c='gold', s=30, edgecolors='black', label='Iteration', zorder=4)
    
    plt.scatter(history_x[0], history_y[0], c='lime', s=150, marker='*', edgecolors='black', label='Start', zorder=5)
    plt.scatter(history_x[-1], history_y[-1], c='cyan', s=100, marker='X', edgecolors='black', label='End', zorder=5)

    plt.scatter(saddle_points[0], saddle_points[1], c='white', s=120, edgecolors='black', label='Saddle point', zorder=6)
    plt.scatter(min_points[0], min_points[1], c='red', s=120, edgecolors='black', label='Global Min', zorder=6)
    
    plt.xlabel('X', fontsize=10)
    plt.ylabel('Y', fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.legend(loc='upper right')
    
    cbar = plt.colorbar(contour_f, label='F(X, Y)')
    cbar.ax.tick_params(labelsize=9)
    
    plt.tight_layout()
    plt.savefig(os.path.join(self.output_dir, filename), dpi=300)
    plt.close()