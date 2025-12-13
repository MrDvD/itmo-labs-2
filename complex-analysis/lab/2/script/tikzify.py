import numpy as np
import matplotlib as plt

def get_tikz_color_with_alpha(color_val, colormap, alpha=1.0):
  cmap = plt.colormaps[colormap]
  rgba = cmap(color_val)
  
  r = int(rgba[0] * 255)
  g = int(rgba[1] * 255)
  b = int(rgba[2] * 255)
  a = rgba[3] * alpha
  
  return f"{{rgb,255:red,{r}; green,{g}; blue,{b}}}, opacity={a:.2f}"

def convert_to_tikz(input_file, output_file):
  data = np.loadtxt(input_file, dtype=object, skiprows=1)
  
  if data.shape[1] != 4:
      raise ValueError("Нужны x, y, color, cmap")
  
  # Конвертируем числовые колонки
  points = data[:, :2].astype(float)
  colors = data[:, 2].astype(float)
  cmaps = data[:, 3]
  
  # Нормализуем цвета
  colors_min = colors.min()
  colors_max = colors.max()
  colors_norm = (colors - colors_min) / (colors_max - colors_min)
  
  tikz_code = r"""\begin{tikzpicture}[scale=0.8]

\draw[->, thick] (-3.5,0) -- (3.5,0) node[right] {$\Re z$};
\draw[->, thick] (0,-3.5) -- (0,3.5) node[above] {$\Im z$};

\fill (0,0) circle (2.5pt) node[below right] {$0$};

"""
  count = 0
  for (x, y), color_val, cmap in zip(points, colors_norm, cmaps):
      if abs(x) > 3.5 or abs(y) > 3.5:
          continue
      count += 1
      tikz_color = get_tikz_color_with_alpha(color_val, cmap, alpha=0.6)
      
      tikz_code += f"\\fill[color={tikz_color}] ({x:.4f},{y:.4f}) circle (1.5pt);\n"
  
  tikz_code += "\n\\end{tikzpicture}"
  
  with open(output_file, 'w') as f:
      f.write(tikz_code)
  
  print(f"Сохранено: {output_file} ({count} точек)")

import os

data_files = [f for f in os.listdir() if f.startswith('step_') and f.endswith('_data.txt')]

for data_file in data_files:
  step_num = data_file.split('_')[1]
  output_file = f'step_{step_num}_tikz.tex'
  
  convert_to_tikz(data_file, output_file)