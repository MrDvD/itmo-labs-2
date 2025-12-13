import matplotlib.pyplot as plt
import numpy as np

def generate_hilbert_string(level):
  """
  Generate Hilbert curve string using L-system rules
  """
  def apply_rules(char):
    if char == 'A':
      return '-BF+AFA+FB-'
    elif char == 'B':
      return '+AF-BFB-FA+'
    else:
      return char
  
  current_string = 'A' # axiom
  
  for _ in range(level):
    new_string = ''
    for char in current_string:
      new_string += apply_rules(char)
    current_string = new_string
  
  return current_string

def draw_hilbert_from_string(hilbert_string, level, step=10, angle=90, filename="hilbert_curve.png"):
  """
  Draw Hilbert curve by interpreting the generated string using matplotlib
  """
  x, y, direction = 0, 0, 0
  points = [(x, y)]
  
  for char in hilbert_string:
    if char == 'F':
      rad = np.radians(direction)
      x += step * np.cos(rad)
      y += step * np.sin(rad)
      points.append((x, y))
    elif char == '+':
      direction -= angle
    elif char == '-':
      direction += angle
  
  plt.figure(figsize=(10, 10))
  plt.plot(
      [p[0] for p in points],
      [p[1] for p in points],
      'b-',
      linewidth=1)
  plt.axis('off')

  total_segments = hilbert_string.count('F')
  print(f'Hilbert Curve - Level {level}')
  print(f'Total segments: {total_segments:,}')
  print(f'Saving plot to: {filename}')
  plt.tight_layout()
  plt.savefig(filename, dpi=150, bbox_inches='tight', facecolor='white')
  plt.close()

def main():
  try:
    level = int(input("Enter the level for Hilbert curve: "))
    if level < 1:
      print("Level must be at least 1. Using level 1.")
      level = 1
    elif level > 7:
      print("Warning: High levels may take long to compute and render.")
    
    output_file = f"hilbert_curve_level{level}.png"
    draw_hilbert_from_string(generate_hilbert_string(level), level=level, step=8, filename=output_file)
  
  except ValueError:
    print("Invalid input. Please enter a valid integer.")
    return

if __name__ == "__main__":
  main()