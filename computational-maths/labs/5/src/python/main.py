from lib.plot import Visualizer
from lib.report import ReportFiller
import lib.config as config
import numpy as np
import os

if __name__ == "__main__":  
  cfg = config.load()
  out_dir = os.path.join(cfg['report_dir'], 'pics')
  viz = Visualizer(output_dir=out_dir)

  report = ReportFiller({}, cfg['report_dir'])

  for func_id in range(1, 6):
    for case_num in range(1, 3):
      output_name = f"ode_f{func_id}_case{case_num}"
      euler_path = os.path.join(cfg['output_dir'], f"f{func_id}_case{case_num}_euler.txt")
      exact_path = os.path.join(cfg['output_dir'], f"f{func_id}_case{case_num}_exact.txt")

      euler_chebyshev = ""
      a = ""
      b = ""
      ya = ""
      epsilon = ""
      iters = ""
      case = ""
      euler_data = None
      if os.path.exists(euler_path):
        with open(euler_path, 'r') as f:
          first_line = f.readline().strip()
          if first_line:
            euler_chebyshev, a, b, epsilon, ya, iters, case = first_line.split()
          euler_data = np.loadtxt(f)
      exact_chebyshev = ""
      exact_data = None
      if os.path.exists(exact_path):
        with open(exact_path, 'r') as f:
          first_line = f.readline().strip()
          if first_line:
            exact_chebyshev = first_line
          exact_data = np.loadtxt(f)
      if euler_data is None or exact_data is None:
        raise Exception('Can not read data files')
      print(f"Generating isolated vector PDF plot for ODE #{func_id}...")
      viz.plot_ode_trajectory(
        euler_data=euler_data,
        exact_data=exact_data,
        filename=output_name
      )
      report.add_plot(cfg['report_dir'], str(func_id), output_name + ".pdf", a, b, ya, epsilon, euler_chebyshev, exact_chebyshev, iters, case)

  print("All individual plots successfully exported.")

  report.compile_patterns()