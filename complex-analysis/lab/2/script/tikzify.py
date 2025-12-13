import numpy as np
import matplotlib as plt
import os

def get_tikz_color_with_alpha(color_val, colormap, alpha=1.0):
  """
  Convert matplotlib colormap value to TikZ color with alpha transparency.
  
  Parameters:
  color_val: normalized color value [0, 1]
  colormap: name of matplotlib colormap
  alpha: opacity value [0, 1]
  """
  cmap = plt.colormaps[colormap]
  rgba = cmap(color_val)
  
  # Convert rgba values (0-1) to rgb (0-255) for TikZ
  r = int(rgba[0] * 255)
  g = int(rgba[1] * 255)
  b = int(rgba[2] * 255)
  a = rgba[3] * alpha  # Use alpha from colormap if available
  
  return f"{{rgb,255:red,{r}; green,{g}; blue,{b}}}, opacity={a:.2f}"

def convert_to_tikz(input_file, output_file, step_num):
  """
  Convert data file with point coordinates to TikZ code.
  
  Parameters:
  input_file: text file with columns: x, y, color_value, colormap_name
  output_file: output .tex file with TikZ code
  step_num: ordinal numeral of current step
  """
  data = np.loadtxt(input_file, dtype=object)
  
  # Validate data format
  if data.shape[1] != 4:
      raise ValueError("File must have 4 columns: x, y, color, colormap")
  
  # Extract and convert data columns
  points = data[:, :2].astype(float)
  colors = data[:, 2].astype(float)
  cmaps = data[:, 3]
  
  # Normalize color values to [0, 1] range
  colors_min = colors.min()
  colors_max = colors.max()
  colors_norm = (colors - colors_min) / (colors_max - colors_min)
  
  # Initialize TikZ code with axes and origin point
  tikz_code = r"""\begin{tikzpicture}[scale=0.8]

\draw[->, thick] (-3.5,0) -- (3.5,0) node[right] {$\Re z$};
\draw[->, thick] (0,-3.5) -- (0,3.5) node[above] {$\Im z$};

\fill (0,0) circle (2.5pt) node[below right] {$0$};
"""
  match step_num:
    case '4' | '5':
      tikz_code += "\\fill (1,0) circle (2.5pt) node[below left] {$1$};\n"
    case '6':
      tikz_code += f"\\fill ({np.e},0) circle (2.5pt) node[below left] {{$e$}};\n"
    case _:
      tikz_code += "\n"
     
  count = 0
  for (x, y), color_val, cmap in zip(points, colors_norm, cmaps):
      # Skip points outside the plotting area
      if abs(x) > 3.5 or abs(y) > 3.5:
          continue
      
      count += 1
      tikz_color = get_tikz_color_with_alpha(color_val, cmap, alpha=0.6)
      tikz_code += f"\\fill[color={tikz_color}] ({x:.4f},{y:.4f}) circle (1.5pt);\n"
  
  tikz_code += "\n\\end{tikzpicture}"
  
  with open(output_file, 'w') as f:
      f.write(tikz_code)
  
  print(f"Saved: {output_file} ({count} points)")

if __name__ == "__main__":
  # Find all data files starting with 'step_' and ending with '_data.txt'
  data_files = [f for f in os.listdir() if f.startswith('step_') and f.endswith('_data.txt')]
  
  for data_file in data_files:
    # Extract step number from filename (e.g., 'step_1_data.txt' -> '1')
    step_num = data_file.split('_')[1]
    output_file = f'step_{step_num}_tikz.tex'
    
    convert_to_tikz(data_file, output_file, step_num)