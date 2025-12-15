import matplotlib.pyplot as plt
import numpy as np

# Parameters for point generation
epsilon = 0.02  # Small number to exclude boundary values
density = 50    # Parameter affecting point density

def complex_positive(density):
  """
  Generates points in the sector (3pi/4, pi) of the complex plane.
  Points are distributed in logarithmic scale by radius.
  """
  angles_far = np.linspace(np.pi - np.pi / 4 + epsilon, np.pi - epsilon, density // 9)
  radius_far = np.exp(np.linspace(np.log(0.005), np.log(3), density // 2))
  r_grid, theta_grid = np.meshgrid(radius_far, angles_far)
  z = r_grid * np.exp(1j * theta_grid)
  points = z.flatten()
  distances = np.abs(points)
  colors = distances / np.max(distances)  # Normalized distances for coloring
  return points, colors

def complex_negative(density):
  """
  Generates points in the sector (-pi, -3pi/4) of the complex plane.
  """
  angles_center = np.linspace(-np.pi + epsilon, -np.pi + np.pi / 4 - epsilon, density // 9)
  radius_center = np.exp(np.linspace(np.log(0.005), np.log(3), density // 2))
  r_grid, theta_grid = np.meshgrid(radius_center, angles_center)
  z = r_grid * np.exp(1j * theta_grid)
  points = z.flatten()
  distances = np.abs(points)
  colors = distances / np.max(distances)
  return points, colors

def complex_far_positive(density):
  """
  Generates points in the sector [0, 3pi/4] of the complex plane.
  """
  angles_center = np.linspace(0, np.pi - np.pi/4, density // 4)
  radius_center = np.exp(np.linspace(np.log(0.005), np.log(3), density // 2))
  r_grid, theta_grid = np.meshgrid(radius_center, angles_center)
  z = r_grid * np.exp(1j * theta_grid)
  points = z.flatten()
  distances = np.abs(points)
  colors = distances / np.max(distances)
  return points, colors

def complex_far_negative(density):
  """
  Generates points in the sector [-3pi/4, 0) of the complex plane.
  """
  angles_center = np.linspace(-np.pi + np.pi/4, -epsilon, density // 4)
  radius_center = np.exp(np.linspace(np.log(0.005), np.log(3), density // 2))
  r_grid, theta_grid = np.meshgrid(radius_center, angles_center)
  z = r_grid * np.exp(1j * theta_grid)
  points = z.flatten()
  distances = np.abs(points)
  colors = distances / np.max(distances)
  return points, colors

def get_P(plane):
  """
  Filters points: keeps only those with Re(z) > 0 
  or Im(z) != 0 (excludes non-positive real axis).
  """
  mask = np.logical_or(plane.real > 0, plane.imag != 0)
  return plane[mask]

# Definition of mapping functions omega_1, ..., omega_5
def omega_1(z):
  """omega_1(z) = -z (central symmetry about origin)"""
  return -z

def omega_2(z):
  """omega_2(z) = sqrt(z) (square root extraction)"""
  r = np.abs(z)
  theta = np.angle(z)
  sqrt_r = np.sqrt(r)
  theta_pos = np.mod(theta, 2*np.pi)  # Bring angle to [0, 2*pi)
  new_theta = theta_pos / 2
  return sqrt_r * (np.cos(new_theta) + 1j * np.sin(new_theta))

def omega_3(z):
  """omega_3(z) = (z - i)/(z + i) (fractional-linear transformation)"""
  return (z-1j)/(z+1j)

def omega_4(z):
  """omega_4(z) = 1/z (inversion)"""
  return 1/z

def omega_5(z):
  """omega_5(z) = z * e (multiplication by Euler's number e)"""
  return z * np.e

def get_all_Ps(complex_region):
  """
  Applies all five mappings sequentially to input set.
  """
  P = get_P(complex_region)
  P1 = omega_1(P)
  P2 = omega_2(P1)
  P3 = omega_3(P2)
  P4 = omega_4(P3)
  P5 = omega_5(P4)
  return [P, P1, P2, P3, P4, P5]

def scatter_regions(regions, axes, colors, cmap):
  """
  Displays 6 sets on 3x2 grid of plots.

  Parameters:
  regions: list of 6 arrays of complex numbers
  axes: 3x2 matrix of axes
  colors: array of values for colormap
  cmap: name of colormap
  """
  if len(regions) < 6:
    print("Error: lack of regions")
    pass
  for y in range(3):
    for x in range(2):
      axes[y, x].scatter(regions[y * 2 + x].real, regions[y * 2 + x].imag, 
                        s=1, alpha=0.6, c=colors, cmap=cmap)

if __name__ == "__main__":
  fig, ax = plt.subplots(3, 2)
  
  # Generate and display points from four sectors with different colormaps
  reg1, col1 = complex_far_positive(density)
  scatter_regions(get_all_Ps(reg1), ax, col1, 'winter')
  
  reg2, col2 = complex_far_negative(density)
  scatter_regions(get_all_Ps(reg2), ax, col2, 'copper')
  
  reg3, col3 = complex_positive(density)
  scatter_regions(get_all_Ps(reg3), ax, col3, 'cool')
  
  reg4, col4 = complex_negative(density)
  scatter_regions(get_all_Ps(reg4), ax, col4, 'autumn')
  
  # Save data from each plot to separate file
  for i in range(6):
    row = i // 2
    col = i % 2
    
    with open(f'step_{i+1}_data.txt', 'w') as f:
      # Get all point collections from the plot
      for collection_idx, collection in enumerate(ax[row, col].collections):
        data = collection.get_offsets()  # Coordinates (x, y)
        colors = collection.get_array()   # Values for colormap
        cmap_name = collection.get_cmap().name  # Name of colormap
        
        # Write data to file: x, y, color value, colormap name
        for j in range(len(data)):
          x, y = data[j]
          color_val = colors[j] if j < len(colors) else 0.0
          f.write(f'{x:.6f} {y:.6f} {color_val:.6f} {cmap_name}\n')
    
    print(f"Step {i+1}: data saved")