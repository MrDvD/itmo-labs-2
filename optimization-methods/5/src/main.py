import numpy as np
import lib.config as config
from lib.report import ReportFiller
from lib.primitives import TableEntry
from lib.plot import Visualizer
from lib.optimize import EllipticOptimizer, GaussOptimizer, ConstantOptimizer, RBFOptimizer
from typing import List
import os, subprocess

if __name__ == "__main__":
  cfg = config.load()

  values: List[TableEntry] = list()
  with open(cfg['table_file'], 'r') as f:
    for line in f.readlines():
      params = line.split(', ')
      values.append(TableEntry(*map(float, params)))

  input_table_data = ''
  for entry in values:
    input_table_data += ' & '.join(map(lambda x: f"${x}$", [entry.x, entry.y, entry.z]))
    input_table_data += '\\\\\n'

  pts = np.array([[v.x, v.y] for v in values])
  targets = np.array([v.z for v in values])
  
  pics_dir = os.path.join(cfg['report_dir'], 'pics')
  result = subprocess.run(['rm', '-rf', pics_dir])
  if result.returncode != 0:
    raise RuntimeError(f"Failed to remove {pics_dir}")
  
  plot = Visualizer(
    x_range=(0, 6),
    y_range=(0, 6),
    output_dir=pics_dir
  )

  # Gauss
  gauss_opt = GaussOptimizer(
    X_data=pts, 
    targets=targets,
    bounds=[
      (0.1, 10.0), (0.0, 6.0), (0.0, 6.0),
      (0.1, 5.0), (0.1, 5.0), (-np.pi/4, np.pi/4), (-1.0, 1.0)
    ]
  )
  max_idx = np.argmax(targets)
  start_params_gauss = np.array([targets[max_idx] + 0.1, pts[max_idx, 0], pts[max_idx, 1], np.std(pts[:, 0]) * 0.5, np.std(pts[:, 1]) * 0.5, 0.0, 0.0])
  res_gauss = gauss_opt.optimize(params_start=start_params_gauss)
  plot.plot_learning_curve(gauss_opt, filename="learning_curve_gauss.pdf")
  plot.plot_model(gauss_opt.get_model(res_gauss.x), pts[:, 0], pts[:, 1], targets, filename="model_plot_gauss.pdf")
  plot.plot_contour_lines(gauss_opt.get_model(res_gauss.x), pts[:, 0], pts[:, 1], targets, filename="contour_lines_gauss.pdf")

  # Elliptic
  elliptic_opt = EllipticOptimizer(
    X_data=pts, 
    targets=targets,
    bounds=[
      (0.0, 6.0), (0.0, 6.0), (-1.0, 6.0), (-2.0, 2.0), (-2.0, 2.0), (-1.0, 1.0)
    ]
  )
  start_params_elliptic = np.array([pts[max_idx, 0], pts[max_idx, 1], targets[max_idx], 0.3, 0.3, 0.0])
  res_elliptic = elliptic_opt.optimize(params_start=start_params_elliptic)
  plot.plot_learning_curve(elliptic_opt, filename="learning_curve_elliptic.pdf")
  plot.plot_model(elliptic_opt.get_model(res_elliptic.x), pts[:, 0], pts[:, 1], targets, filename="model_plot_elliptic.pdf")
  plot.plot_contour_lines(elliptic_opt.get_model(res_elliptic.x), pts[:, 0], pts[:, 1], targets, filename="contour_lines_elliptic.pdf")

  # Constant
  constant_opt_mse = ConstantOptimizer(
    targets=targets,
    metric="MSE",
  )
  constant_opt_mae = ConstantOptimizer(
    targets=targets,
    metric="MAE",
  )
  res_constant_mse = constant_opt_mse.optimize(params_start=np.array([np.mean(targets)]))
  res_constant_mae = constant_opt_mae.optimize(params_start=np.array([np.median(targets)]))

  # RBF
  rbf_opt = RBFOptimizer(
    X_data=pts,
    targets=targets
  )
  start_params_rbf = rbf_opt.get_initial_params()
  res_rbf = rbf_opt.optimize(params_start=start_params_rbf)
  plot.plot_learning_curve(rbf_opt, filename="learning_curve_rbf.pdf")
  plot.plot_model(rbf_opt.get_model(res_rbf.x), pts[:, 0], pts[:, 1], targets, filename="model_plot_rbf.pdf")
  plot.plot_contour_lines(rbf_opt.get_model(res_rbf.x), pts[:, 0], pts[:, 1], targets, filename="contour_lines_rbf.pdf")

  report = ReportFiller({
    'variant_number': cfg['variant_number'],
    'input_table_data': input_table_data,
    'gauss_loss': f"{gauss_opt.loss_history[-1]:.6f}",
    'elliptic_loss': f"{elliptic_opt.loss_history[-1]:.6f}",
    'rbf_loss': f"{rbf_opt.loss_history[-1]:.6f}",
  }, cfg['report_dir'])
  
  report.compile_patterns()