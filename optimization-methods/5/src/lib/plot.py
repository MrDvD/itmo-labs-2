import os
import matplotlib.pyplot as plt
from lib.optimize import OptimizerProtocol
import numpy as np
from typing import Tuple, Callable, Any

class Visualizer:
  def __init__(self, x_range: Tuple[float, float], y_range: Tuple[float, float], resolution: int = 50, output_dir: str = "plots") -> None:
    self.x_grid = np.linspace(x_range[0], x_range[1], resolution)
    self.y_grid = np.linspace(y_range[0], y_range[1], resolution)
    self.X_grid, self.Y_grid = np.meshgrid(self.x_grid, self.y_grid)
    self.output_dir = output_dir
    if not os.path.exists(self.output_dir):
      os.makedirs(self.output_dir)

  def plot_learning_curve(self, optimizer: OptimizerProtocol, filename: str = "learning_curve.png") -> None:
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
    filename: str = "model_visualization.png"
  ) -> None:
    Z_pred_grid = predict_func(self.X_grid, self.Y_grid)
    
    plt.figure(figsize=(8, 6))
    
    contour = plt.contourf(self.X_grid, self.Y_grid, Z_pred_grid, levels=25, cmap='viridis', alpha=0.9)
    plt.scatter(X_orig, Y_orig, c=Z_orig, s=120, edgecolors='black', cmap='viridis')
    plt.contour(self.X_grid, self.Y_grid, Z_pred_grid, levels=10, colors='white', alpha=0.3, linewidths=0.5)
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
    filename: str = "model_visualization.png"
  ) -> None:
    Z_pred_grid = predict_func(self.X_grid, self.Y_grid)
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    ax.plot_surface(self.X_grid, self.Y_grid, Z_pred_grid, cmap='viridis', alpha=0.7)
    ax.scatter(X_orig, Y_orig, Z_orig, c='red', s=50)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.tight_layout()
    plt.savefig(os.path.join(self.output_dir, filename))
    plt.close()