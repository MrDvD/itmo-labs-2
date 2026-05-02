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
  res_gauss = np.array(gauss_opt.optimize(params_start=start_params_gauss))
  plot.plot_learning_curve(gauss_opt, filename="learning_curve_gauss.pdf")
  plot.plot_model(gauss_opt.get_model(res_gauss), pts[:, 0], pts[:, 1], targets, filename="model_plot_gauss.pdf")
  plot.plot_contour_lines(gauss_opt.get_model(res_gauss), pts[:, 0], pts[:, 1], targets, filename="contour_lines_gauss.pdf")
  plot.plot_residuals(gauss_opt.get_model(res_gauss), pts[:, 0], pts[:, 1], targets, filename="residuals_gauss.pdf")
  A_GAUSS, X0_GAUSS, Y0_GAUSS, SIGMAX_GAUSS, SIGMAY_GAUSS, THETA_GAUSS, Z0_GAUSS = map(lambda x: f"{x:.3f}", res_gauss)

  # Elliptic
  elliptic_opt = EllipticOptimizer(
    X_data=pts, 
    targets=targets,
    bounds=[
      (0.0, 6.0), (0.0, 6.0), (-1.0, 6.0), (-2.0, 2.0), (-2.0, 2.0), (-1.0, 1.0)
    ]
  )
  start_params_elliptic = np.array([pts[max_idx, 0], pts[max_idx, 1], targets[max_idx], 0.3, 0.3, 0.0])
  res_elliptic = np.array(elliptic_opt.optimize(params_start=start_params_elliptic))
  plot.plot_learning_curve(elliptic_opt, filename="learning_curve_elliptic.pdf")
  plot.plot_model(elliptic_opt.get_model(res_elliptic), pts[:, 0], pts[:, 1], targets, filename="model_plot_elliptic.pdf")
  plot.plot_contour_lines(elliptic_opt.get_model(res_elliptic), pts[:, 0], pts[:, 1], targets, filename="contour_lines_elliptic.pdf")
  plot.plot_residuals(elliptic_opt.get_model(res_elliptic), pts[:, 0], pts[:, 1], targets, filename="residuals_elliptic.pdf")
  X0_ELLIPTIC, Y0_ELLIPTIC, Z0_ELLIPTIC, A_ELLIPTIC, B_ELLIPTIC, C_ELLIPTIC = map(lambda x: f"{x:.3f}", res_elliptic)

  # Constant
  constant_opt_mse = ConstantOptimizer(
    targets=targets,
    metric="MSE",
  )
  constant_opt_mae = ConstantOptimizer(
    targets=targets,
    metric="MAE",
  )
  res_constant_mse = np.array(constant_opt_mse.optimize(params_start=np.array([np.mean(targets)])))
  MSE_CONSTANT = f"{res_constant_mse[0]:.6f}"
  plot.plot_residuals(constant_opt_mse.get_model(res_constant_mse), pts[:, 0], pts[:, 1], targets, filename="residuals_mse.pdf")
  res_constant_mae = np.array(constant_opt_mae.optimize(params_start=np.array([np.median(targets)])))
  MAE_CONSTANT = f"{res_constant_mae[0]:.6f}"
  plot.plot_residuals(constant_opt_mae.get_model(res_constant_mae), pts[:, 0], pts[:, 1], targets, filename="residuals_mae.pdf")

  # RBF
  rbf_opt = RBFOptimizer(
    X_data=pts,
    targets=targets
  )
  start_params_rbf = rbf_opt.get_initial_params()
  res_rbf = np.array(rbf_opt.optimize(params_start=start_params_rbf))
  plot.plot_learning_curve(rbf_opt, filename="learning_curve_rbf.pdf")
  plot.plot_model(rbf_opt.get_model(res_rbf), pts[:, 0], pts[:, 1], targets, filename="model_plot_rbf.pdf")
  plot.plot_contour_lines(rbf_opt.get_model(res_rbf), pts[:, 0], pts[:, 1], targets, filename="contour_lines_rbf.pdf")
  plot.plot_residuals(rbf_opt.get_model(res_rbf), pts[:, 0], pts[:, 1], targets, filename="residuals_rbf.pdf")
  W0_RBF, W1_RBF, W2_RBF, C1X_RBF, C1Y_RBF, C2X_RBF, C2Y_RBF, SIGMA1_RBF, SIGMA2_RBF = map(lambda x: f"{x:.3f}", res_rbf)

  centers = rbf_opt.get_initial_centers()

  report = ReportFiller({
    'variant_number': cfg['variant_number'],
    'input_table_data': input_table_data,
    'A_ELLIPTIC': A_ELLIPTIC,
    'B_ELLIPTIC': B_ELLIPTIC,
    'C_ELLIPTIC': C_ELLIPTIC,
    'X0_ELLIPTIC': X0_ELLIPTIC,
    'Y0_ELLIPTIC': Y0_ELLIPTIC,
    'Z0_ELLIPTIC': Z0_ELLIPTIC,
    'A_GAUSS': A_GAUSS,
    'X0_GAUSS': X0_GAUSS,
    'Y0_GAUSS': Y0_GAUSS,
    'SIGMAX_GAUSS': SIGMAX_GAUSS,
    'SIGMAY_GAUSS': SIGMAY_GAUSS,
    'THETA_GAUSS': THETA_GAUSS,
    'Z0_GAUSS': Z0_GAUSS,
    'MSE_CONSTANT': MSE_CONSTANT,
    'MAE_CONSTANT': MAE_CONSTANT,
    'W0_RBF': W0_RBF,
    'W1_RBF': W1_RBF,
    'W2_RBF': W2_RBF,
    'C1X_RBF': C1X_RBF,
    'C2X_RBF': C2X_RBF,
    'C1Y_RBF': C1Y_RBF,
    'C2Y_RBF': C2Y_RBF,
    'SIGMA1_RBF': SIGMA1_RBF,
    'SIGMA2_RBF': SIGMA2_RBF,
    'c1_vector_init': ReportFiller.print_vector(centers[0]), 
    'c2_vector_init': ReportFiller.print_vector(centers[1]),
    'weights_init_rbf': ReportFiller.print_vector(start_params_rbf[0:3]),
    'c1_init_rbf': ReportFiller.print_vector(start_params_rbf[3:5]),
    'c2_init_rbf': ReportFiller.print_vector(start_params_rbf[5:7]),
    'sigma_init_rbf': f"{start_params_rbf[7]:.5f}",
  }, cfg['report_dir'])

  report.fill_rbf_handmade(centers[0], centers[1], values)

  report.compile_patterns()