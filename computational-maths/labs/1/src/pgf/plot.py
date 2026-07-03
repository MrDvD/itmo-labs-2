import csv, os

header = r"""
\begin{tikzpicture}
\begin{axis}[
    width=10cm, height=10cm,
    axis lines=middle,
    axis line style={thick, black, dashed},
    xlabel=$x$,
    ylabel=$y$,
    xlabel style={right},
    ylabel style={above},
    grid=major,
    grid style={dashed, gray!30},
    axis background/.style={fill=white},
    tick label style={font=\small},
    label style={font=\small}
]
"""
footer = r"""
\end{axis}
\end{tikzpicture}
"""

def generate_plots():
  base_dir = "src/pgf"
  out_dir = "report/tikz"
  if not os.path.exists(out_dir):
    os.makedirs(out_dir)

  with open(f'{base_dir}/interpolation_results.csv', 'r') as f:
    interp_data = list(csv.DictReader(f))

  with open(f'{base_dir}/function_plots.csv', 'r') as f:
    func_data = list(csv.DictReader(f))

  for plot_num in range(1, 6):
      file_path = os.path.join(out_dir, f"{plot_num}.tex")
      with open(file_path, "w") as out:
        out.write(header)
        
        out.write(r"%% Continuous Function Data" + "\n")
        out.write(r"\addplot[no marks, dashed, thick] coordinates {" + "\n")
        for row in func_data:
          if int(row['f_id']) == plot_num:
            out.write(f"({row['x']}, {row['y']}) ")
        out.write("\n};\n")

        out.write(r"%% Interpolation Points" + "\n")
        out.write(r"\addplot[only marks, mark=*, mark size=1.5pt] coordinates {" + "\n")
        for row in interp_data:
          if int(row['f_id']) == plot_num:
            out.write(f"({row['x']}, {row['y']}) ")
        out.write("\n};\n")
        
        out.write(footer)

if __name__ == "__main__":
  generate_plots()