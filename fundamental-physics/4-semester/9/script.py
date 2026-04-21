import sys
import math
from matplotlib.textpath import TextPath
from matplotlib.font_manager import FontProperties

def extract_letter_outline(ttf_path, letter, output_file, min_dist):
  prop = FontProperties(fname=ttf_path)
  path = TextPath((0, 0), letter, prop=prop, size=1000.0)
  polygons = path.to_polygons()
  
  with open(output_file, 'w') as f:
    f.write(f"{len(polygons)}\n") 
    for poly in polygons:
      if len(poly) == 0: continue
      
      filtered_poly = [poly[0]]
      for i in range(1, len(poly)):
        prev = filtered_poly[-1]
        curr = poly[i]
        if math.hypot(curr[0]-prev[0], curr[1]-prev[1]) >= min_dist:
          filtered_poly.append(curr)
      
      if len(filtered_poly) < 3: 
        filtered_poly = poly

      f.write(f"{len(filtered_poly)}\n")
      for x, y in filtered_poly:
        f.write(f"{x:.6f} {y:.6f}\n")

if __name__ == "__main__":
  if len(sys.argv) < 4:
    print("Usage: script.py <font> <letter> <min_dist>")
    sys.exit(1)
    
  font_arg = sys.argv[1]
  letter_arg = sys.argv[2]
  dist_arg = float(sys.argv[3])
  
  extract_letter_outline(font_arg, letter_arg, "glyph_data.txt", dist_arg)