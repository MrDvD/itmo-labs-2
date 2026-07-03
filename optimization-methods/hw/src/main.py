import lib.config as config
from lib.hermite import HermiteOptimizer, HermitePlot
from lib.newton import NewtonOptimizer, NewtonPlot
from lib.report import ReportFiller
from typing import Dict, List
import os

def hermite_f(x: float) -> float: 
  return x ** 4 / 4 + x ** 2 - 8 * x + 12

def hermite_df(x: float) -> float: 
  return x ** 3 + 2 * x - 8

def newton_f(x: float, y: float) -> float:
  return x ** 3 - 9 * x ** 2 + 24 * x + y ** 3 - 14 * y ** 2 + 64 * y - 116

def newton_grad(x: float, y: float) -> List[float]:
  df_dx = 3 * x ** 2 - 18 * x + 24
  df_dy = 3 * y ** 2 - 28 * y + 64
  return [df_dx, df_dy]

def newton_hess(x: float, y: float) -> List[List[float]]:
  d2f_dx2 = 6 * x - 18
  d2f_dy2 = 6 * y - 28
  d2f_dxdy = 0.0
  
  return [
    [d2f_dx2, d2f_dxdy],
    [d2f_dxdy, d2f_dy2]
  ]

if __name__ == "__main__":
  cfg = config.load()

  optimizer = HermiteOptimizer(f=hermite_f, df=hermite_df, eps=cfg['hermite_eps'], max_iter=cfg['hermite_max_iters'])
  optimizer.optimize(x0_start=cfg['hermite_a'], x1_start=cfg['hermite_b'])

  plots_dir = os.path.join(cfg['report_dir'], 'plots')
  plot_approx = HermitePlot(hermite_f, plots_dir)
  plot_approx.generate(optimizer.raw_history)

  newton_opt = NewtonOptimizer(
    f=newton_f, grad=newton_grad, hess=newton_hess, 
    eps=cfg['newton_eps'], max_iter=cfg['newton_max_iters']
  )
  newton_opt.optimize(x_start=cfg['newton_x0'], y_start=cfg['newton_y0'])

  newton_plot = NewtonPlot(newton_f, plots_dir)
  newton_plot.generate(newton_opt.raw_history[:3])

  render_data: Dict[str, object] = {
    'hermite_eps': cfg['hermite_eps'],
    'hermite_iterations': optimizer.iterations,
    'hermite_history': optimizer.history,
    'newton_eps': cfg['newton_eps'],
    'newton_iterations': newton_opt.iterations,
  }

  report = ReportFiller(render_data, cfg['report_dir'])
  report.compile_patterns()