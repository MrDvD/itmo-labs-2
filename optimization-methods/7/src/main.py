import lib.config as config 
from lib.plot import Visualizer
from lib.optimize import GradientDescentOptimizer, OurAdamOptimizer, PyTorchAdamOptimizer
from lib.report import ReportFiller
from numpy.typing import NDArray
import os
import numpy as np

if __name__ == "__main__":
  cfg = config.load()
  
  pics_dir = os.path.join(cfg['report_dir'], "pics")
  x_range = (-20, 20)
  y_range = (-50, 50)
  plot = Visualizer(
    x_range=x_range,
    y_range=y_range,
    output_dir=pics_dir
  )

  def function(x: NDArray[np.float64], y: NDArray[np.float64]) -> NDArray[np.float64]:
    return 10 ** (-2) * (8 * x ** 2 + 2 * x * y + 43 * x + 10 * y + 15)
  
  saddle_points = (np.array([-5.0]), np.array([18.5]))
  min_points = (np.array([57/16]), np.array([-50]))
  plot.plot_contour_lines(function, saddle_points, min_points, "contour_lines.pdf")

  start_param = (12.0, 20.6)

  gd_optimizer = GradientDescentOptimizer(cfg['gd_learning_rate'], cfg['max_iter'], cfg['gd_eps'])
  gd_iterations = gd_optimizer.optimize(start_param)
  plot.plot_optimization_trajectory(function, gd_iterations, saddle_points, min_points, 20, "gd_iterations.pdf")

  plot2 = Visualizer(
    x_range=(-30, 30),
    y_range=(-100, 60),
    output_dir=pics_dir
  )

  adam_optimizer = OurAdamOptimizer(cfg['adam_learning_rate'], len(gd_iterations) - 1, cfg['adam_eps'])
  adam_iterations = adam_optimizer.optimize(np.array([*start_param, cfg['adam_beta_1'], cfg['adam_beta_2']]))
  plot2.plot_optimization_trajectory(function, adam_iterations, saddle_points, (np.array([]), np.array([])), 20, 'adam_iterations.pdf')

  zig_optimizer = OurAdamOptimizer(cfg['zig_learning_rate'], len(gd_iterations) - 1, cfg['zig_eps'])
  zig_iterations = zig_optimizer.optimize(np.array([*start_param, cfg['zig_beta_1'], cfg['zig_beta_2']]))
  plot2.plot_optimization_trajectory(function, zig_iterations, saddle_points, (np.array([]), np.array([])), 20, 'adam_iterations_zig.pdf')

  torch_optimizer = PyTorchAdamOptimizer(cfg['torch_learning_rate'], len(gd_iterations) - 1, cfg['torch_eps'])
  torch_iterations = torch_optimizer.optimize(np.array([*start_param, cfg['torch_beta_1'], cfg['torch_beta_2']]))
  plot2.plot_optimization_trajectory(function, torch_iterations, saddle_points, (np.array([]), np.array([])), 20, 'adam_iterations_torch.pdf')

  report = ReportFiller({
    'gd_init': f"({start_param[0]}, {start_param[1]})^T",
    'gd_learning_rate': cfg['gd_learning_rate'],
    'max_iter': cfg['max_iter'],
    'gd_eps': f"{cfg['gd_eps']:.5f}",
    'gd_iterations_num': str(len(gd_iterations) - 1),
    'adam_init': f"({start_param[0]}, {start_param[1]})^T",
    'adam_learning_rate': cfg['adam_learning_rate'],
    'adam_iterations': str(len(gd_iterations) - 1),
    'adam_beta_1': cfg['adam_beta_1'],
    'adam_beta_2': cfg['adam_beta_2'],
    'adam_eps': f"{cfg['adam_eps']:.5f}",
    'adam_iterations_num': str(len(adam_iterations) - 1),
    'adam_init_zig': f"({start_param[0]}, {start_param[1]})^T",
    'adam_learning_rate_zig': cfg['zig_learning_rate'],
    'adam_iterations_zig': str(len(gd_iterations) - 1),
    'adam_beta_1_zig': cfg['zig_beta_1'],
    'adam_beta_2_zig': cfg['zig_beta_2'],
    'adam_eps_zig': f"{cfg['zig_eps']:.5f}",
    'zig_iterations_num': str(len(zig_iterations) - 1),
  }, cfg['report_dir'])
  
  report.compile_patterns()