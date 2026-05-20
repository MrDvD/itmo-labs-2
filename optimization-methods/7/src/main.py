import lib.config as config 
from lib.plot import Visualizer
from lib.optimize import GradientDescentOptimizer
from lib.report import ReportFiller
import os
import numpy as np

if __name__ == "__main__":
  cfg = config.load()
  
  pics_dir = os.path.join(cfg['report_dir'], "pics")
  plot = Visualizer(
    x_range=(-20, 20),
    y_range=(-50, 50),
    output_dir=pics_dir
  )

  def function(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    return 10 ** (-2) * (8 * x ** 2 + 2 * x * y + 43 * x + 10 * y + 15)
  
  saddle_points = (np.array([-5.0]), np.array([18.5]))
  min_points = (np.array([57/16]), np.array([-50]))
  plot.plot_contour_lines(function, saddle_points, min_points, "contour_lines.pdf")

  start_param = (12.0, 20.6)

  gd_optimizer = GradientDescentOptimizer(cfg['gd_learning_rate'], cfg['max_iter'], cfg['gd_eps'])
  gd_iterations = gd_optimizer.optimize(start_param)
  plot.plot_optimization_trajectory(function, gd_iterations, saddle_points, min_points, 20, "gd_iterations.pdf")

  report = ReportFiller({
    'gd_init': f"({start_param[0]}, {start_param[1]})^T",
    'gd_learning_rate': cfg['gd_learning_rate'],
    'max_iter': cfg['max_iter'],
    'gd_eps': f"{cfg['gd_eps']:.5f}",
    'gd_iterations_num': str(len(gd_iterations) - 1),
  }, cfg['report_dir'])
  
  report.compile_patterns()