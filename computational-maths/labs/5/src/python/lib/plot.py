import os
import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray
from matplotlib.backends.backend_pdf import PdfPages

class Visualizer:
  def __init__(self, output_dir: str = "plots") -> None:
    self.output_dir = output_dir
    if not os.path.exists(self.output_dir):
      os.makedirs(self.output_dir)
      
  def _ensure_pdf_extension(self, filename: str) -> str:
    base, _ = os.path.splitext(filename)
    return f"{base}.pdf"

  def plot_ode_trajectory(self, euler_data: NDArray[np.float64], exact_data: NDArray[np.float64], filename: str) -> None:
    fig = plt.figure(figsize=(8, 6))
    
    if exact_data.size > 0:
      plt.plot(exact_data[:, 0], exact_data[:, 1], label="Analytical Solution", color="navy", linewidth=2.5, zorder=2)
      
    if euler_data.size > 0:
      plt.plot(euler_data[:, 0], euler_data[:, 1], label="Euler's Method", color="crimson", linestyle="--", linewidth=2, zorder=3)
    
    plt.xlabel("x", fontsize=10)
    plt.ylabel("y(x)", fontsize=10)
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend(loc="best")
    plt.tight_layout()

    pdf_path = os.path.join(self.output_dir, self._ensure_pdf_extension(filename))
    with PdfPages(pdf_path) as pdf:
      pdf.savefig(fig, bbox_inches='tight')
    plt.close(fig)