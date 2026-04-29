import os
import matplotlib.pyplot as plt
from lib.optimize import OptimizerProtocol
from lib.primitives import TableEntry
import numpy as np
from typing import Tuple, Callable, List

class Visualizer:
  def __init__(self, x_range: Tuple[float, float], y_range: Tuple[float, float], resolution: int = 50, output_dir: str = "plots") -> None:
    self.x_grid = np.linspace(x_range[0], x_range[1], resolution)
    self.y_grid = np.linspace(y_range[0], y_range[1], resolution)
    self.X_grid, self.Y_grid = np.meshgrid(self.x_grid, self.y_grid)
    self.output_dir = output_dir
    if not os.path.exists(self.output_dir):
      os.makedirs(self.output_dir)

  def plot_learning_curve(self, optimizer: OptimizerProtocol, filename: str) -> None:
    plt.figure(figsize=(10, 4))
    plt.plot(optimizer.loss_history, 'b-o', markersize=4)
    plt.title('Learning Curve')
    plt.xlabel('Iteration')
    plt.ylabel('Loss')
    plt.yscale('log')
    plt.grid(True, which="both", alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join(self.output_dir, filename))
    plt.close()
  
  def plot_contour_lines(
    self,
    predict_func: Callable[[np.ndarray, np.ndarray], np.ndarray],
    X_orig: np.ndarray,
    Y_orig: np.ndarray,
    Z_orig: np.ndarray,
    filename: str
  ) -> None:
    Z_pred_grid = predict_func(self.X_grid, self.Y_grid)

    vmin = min(Z_pred_grid.min(), Z_orig.min())
    vmax = max(Z_pred_grid.max(), Z_orig.max())
    
    plt.figure(figsize=(8, 6))
    
    contour = plt.contourf(self.X_grid, self.Y_grid, Z_pred_grid, levels=25, cmap='viridis', alpha=0.9, vmin=vmin, vmax=vmax)
    plt.scatter(X_orig, Y_orig, c=Z_orig, s=120, edgecolors='black', cmap='viridis', vmin=vmin, vmax=vmax)
    plt.xlabel('X', fontsize=10)
    plt.ylabel('Y', fontsize=10)
    plt.grid(True, alpha=0.3)
    cbar = plt.colorbar(contour, label='Z')
    cbar.ax.tick_params(labelsize=9)
    
    plt.tight_layout()
    plt.savefig(os.path.join(self.output_dir, filename))
    plt.close()

  def plot_model(
    self,
    predict_func: Callable[[np.ndarray, np.ndarray], np.ndarray],
    X_orig: np.ndarray,
    Y_orig: np.ndarray,
    Z_orig: np.ndarray,
    filename: str
  ) -> None:
    Z_pred_grid = predict_func(self.X_grid, self.Y_grid)

    vmin = min(Z_pred_grid.min(), Z_orig.min())
    vmax = max(Z_pred_grid.max(), Z_orig.max())
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    ax.plot_surface(self.X_grid, self.Y_grid, Z_pred_grid, cmap='viridis', alpha=0.7, vmin=vmin, vmax=vmax)
    ax.scatter(X_orig, Y_orig, Z_orig, c='red', s=50)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.tight_layout()
    plt.savefig(os.path.join(self.output_dir, filename))
    plt.close()
  
  def plot_residuals(self,
                     predict_func: Callable[[np.ndarray, np.ndarray], np.ndarray],
                     X_orig: np.ndarray,
                     Y_orig: np.ndarray,
                     Z_orig: np.ndarray,
                     filename: str) -> None:
    z_pred = predict_func(X_orig, Y_orig)
    residuals = Z_orig - z_pred
    indices = np.arange(len(X_orig))
    
    plt.figure(figsize=(10, 5))
    bars = plt.bar(indices, residuals, color='skyblue', edgecolor='navy')
    
    plt.axhline(0, color='black', linewidth=0.8)
    
    for bar in bars:
      yval = bar.get_height()
      plt.text(bar.get_x() + bar.get_width()/2, yval, f'{yval:.4g}', 
               va='bottom' if yval > 0 else 'top', ha='center', fontsize=8)

    plt.xlabel('Data Object Index')
    plt.ylabel('Residual Value')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig(os.path.join(self.output_dir, filename))
    plt.close()