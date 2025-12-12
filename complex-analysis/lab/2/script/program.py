import matplotlib.pyplot as plt
import numpy as np

def create_complex_plane(density=101):
  real_points = np.linspace(-10,10,num=density)
  imag_points = np.linspace(-10,10,num=density)

  real_grid, imag_grid = np.meshgrid(real_points, imag_points)
  return real_grid + imag_grid * 1j

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

fig, ax = plt.subplots()

complex_plane = create_complex_plane()
P = get_P(complex_plane)
result_region = omega_1(P)
result_region = omega_2(result_region)
result_region = omega_3(result_region)
result_region = omega_4(result_region)
result_region = omega_5(result_region)

ax.scatter(result_region.real, result_region.imag, s=1, alpha=0.6)
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.add_patch(plt.Circle((0, 0), np.e, fill=False, color='r', alpha=0.5, linestyle='--'))
plt.show()