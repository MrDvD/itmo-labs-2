import lib.config as config
from lib.hermite import HermiteOptimizer, PlotApprox
from lib.report import ReportFiller
from typing import Dict
import os

def hermite_f(x: float) -> float: 
  return x ** 4 / 4 + x ** 2 - 8 * x + 12

def hermite_df(x: float) -> float: 
  return x ** 3 + 2 * x - 8

if __name__ == "__main__":
  cfg = config.load()

  optimizer = HermiteOptimizer(f=hermite_f, df=hermite_df, eps=cfg['hermite_eps'], max_iter=cfg['hermite_max_iters'])
  optimizer.optimize(x0_start=cfg['hermite_a'], x1_start=cfg['hermite_b'])

  plots_dir = os.path.join(cfg['report_dir'], 'plots')
  plot_approx = PlotApprox(hermite_f, plots_dir)
  plot_approx.generate(optimizer.raw_history)

  render_data: Dict[str, object] = {
    'hermite_eps': cfg['hermite_eps'],
    'iterations': optimizer.iterations,
    'history': optimizer.history,
  }

  report = ReportFiller(render_data, cfg['report_dir'])
  report.compile_patterns()