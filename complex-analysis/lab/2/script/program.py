import matplotlib.pyplot as plt
import numpy as np

epsilon = 0.02

def complex_positive(density):
  angles_far = np.linspace(np.pi - np.pi / 4, np.pi - epsilon, density // 9)
  radius_far = np.exp(np.linspace(np.log(0.005), np.log(3), density // 2))
  r_grid, theta_grid = np.meshgrid(radius_far, angles_far)
  z = r_grid * np.exp(1j * theta_grid)
  points = z.flatten()
  distances = np.abs(points)
  colors = distances / np.max(distances)
  return points, colors

def complex_negative(density):
  angles_center = np.linspace(-np.pi + epsilon, -np.pi + np.pi / 4, density // 9)
  radius_center = np.exp(np.linspace(np.log(0.005), np.log(3), density // 2))
  r_grid, theta_grid = np.meshgrid(radius_center, angles_center)
  z = r_grid * np.exp(1j * theta_grid)
  points = z.flatten()
  distances = np.abs(points)
  colors = distances / np.max(distances)
  return points, colors

def complex_far_positive(density):
  angles_center = np.linspace(epsilon, np.pi - np.pi/4, density // 4)
  radius_center = np.exp(np.linspace(np.log(0.005), np.log(3), density // 2))
  r_grid, theta_grid = np.meshgrid(radius_center, angles_center)
  z = r_grid * np.exp(1j * theta_grid)
  points = z.flatten()
  distances = np.abs(points)
  colors = distances / np.max(distances)
  return points, colors

def complex_far_negative(density):
  angles_center = np.linspace(-np.pi + np.pi/4, -epsilon, density // 4)
  radius_center = np.exp(np.linspace(np.log(0.005), np.log(3), density // 2))
  r_grid, theta_grid = np.meshgrid(radius_center, angles_center)
  z = r_grid * np.exp(1j * theta_grid)
  points = z.flatten()
  distances = np.abs(points)
  colors = distances / np.max(distances)
  return points, colors

def get_P(plane):
  mask = np.logical_or(plane.real >= 0, plane.imag != 0)
  return plane[mask]

def omega_1(z):
  return -z

def omega_2(z):
  r = np.abs(z)
  theta = np.angle(z)
  sqrt_r = np.sqrt(r)
  theta_pos = np.mod(theta, 2*np.pi)
  new_theta = theta_pos / 2
  return sqrt_r * (np.cos(new_theta) + 1j * np.sin(new_theta))

def omega_3(z):
  return (z-1j)/(z+1j)

def omega_4(z):
  return 1/z

def omega_5(z):
  return z * np.e

def get_all_Ps(complex_region):
  P = get_P(complex_region)
  P1 = omega_1(P)
  P2 = omega_2(P1)
  P3 = omega_3(P2)
  P4 = omega_4(P3)
  P5 = omega_5(P4)
  return [P, P1, P2, P3, P4, P5]

def scatter_regions(regions, axes, colors, cmap):
  if len(regions) < 6:
    print("Error: lack of regions")
    pass
  for y in range(3):
    for x in range(2):
      axes[y, x].scatter(regions[y * 2 + x].real, regions[y * 2 + x].imag, s=1, alpha=0.6, c=colors, cmap=cmap)
      axes[y, x].set_aspect('equal')
      axes[y, x].set_xlim(-5, 5)
      axes[y, x].set_ylim(-5, 5)

fig, ax = plt.subplots(3, 2)

density = 50

reg1, col1 = complex_far_positive(density)
scatter_regions(get_all_Ps(reg1), ax, col1, 'winter')
reg2, col2 = complex_far_negative(density)
scatter_regions(get_all_Ps(reg2), ax, col2, 'copper')
reg3, col3 = complex_positive(density)
scatter_regions(get_all_Ps(reg3), ax, col3, 'cool')
reg4, col4 = complex_negative(density)
scatter_regions(get_all_Ps(reg4), ax, col4, 'autumn')

ax[1, 0].plot([-5, 5], [0, 0], color='r', linestyle='--', alpha=0.5)
ax[1, 1].add_patch(plt.Circle((0, 0), 1, fill=False, color='r', alpha=0.5, linestyle='--'))
ax[2, 0].add_patch(plt.Circle((0, 0), 1, fill=False, color='r', alpha=0.5, linestyle='--'))
ax[2, 1].add_patch(plt.Circle((0, 0), np.e, fill=False, color='r', alpha=0.5, linestyle='--'))

for i in range(6):
    row = i // 2
    col = i % 2
    
    with open(f'step_{i+1}_data.txt', 'w') as f:
        for collection_idx, collection in enumerate(ax[row, col].collections):
            data = collection.get_offsets()
            colors = collection.get_array()
            cmap_name = collection.get_cmap().name
            
            for j in range(len(data)):
                x, y = data[j]
                color_val = colors[j] if j < len(colors) else 0.0
                f.write(f'{x:.6f} {y:.6f} {color_val:.6f} {cmap_name}\n')
    
    print(f"Step {i+1}: data saved with colormap names")
