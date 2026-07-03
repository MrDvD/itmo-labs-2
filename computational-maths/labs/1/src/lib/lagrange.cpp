#include <lagrange.h>

#include <cmath>
#include <numbers>
#include <random>
#include <stdexcept>

std::function<double(double)> get_function(int n, bool add_noise) {
  std::random_device rd;
  std::mt19937 gen(rd());
  std::normal_distribution<double> noise_dist(0.0, 0.05);

  switch (n) {
    case 1:
      return [](double x) { return std::sin(x) - std::cos(2 * x); };
    case 2:
      return [add_noise, noise_dist, gen](double x) mutable {
        double noise = add_noise ? noise_dist(gen) : 0.0;
        return 0.5 * x - 1 + noise;
      };
    case 3:
      return [](double x) {
        if (x > 0) {
          return 1;
        } else if (x < 0) {
          return -1;
        } else {
          return 0;
        }
      };
    case 4:
      return [](double x) { return 2 / x; };
    case 5:
      return [](double x) { return std::pow(x, 2); };
    default:
      throw std::runtime_error("function not found");
  }
}

std::function<double(double)> get_function(int n) {
  return get_function(n, true);
}

void fill_chebyshev_polynomial_roots(const int n, const double a, const double b, double roots[]) {
  for (int k = 1; k <= n; k++) {
    roots[k - 1] = 0.5 * (a + b + (b - a) * std::cos(std::numbers::pi * (2 * k - 1) / (2.0 * n)));
  }
}

void fill_function_values(
    const std::function<double(double)> func, std::size_t n, double values[], const double roots[]
) {
  for (int i = 0; i < n; i++) {
    values[i] = func(roots[i]);
  }
}

std::function<double(double)> generate_lagrange_polynomial(
    const int n, const double values[], const double grid[]
) {
  return [n, values, grid](double x) {
    double result = 0;
    for (int i = 0; i < n; i++) {
      double current_term = values[i];
      for (int j = 0; j < n; j++) {
        if (j != i) {
          current_term *= x - grid[j];
          current_term /= grid[i] - grid[j];
        }
      }
      result += current_term;
    }
    return result;
  };
}

debug_result interpolate_by_lagrange(int f, double a, double b, double x) {
  std::function<double(double)> func = get_function(f);
  int n = 4;
  std::vector<double> roots(n), values(n);
  fill_chebyshev_polynomial_roots(n, a, b, roots.data());
  fill_function_values(func, n, values.data(), roots.data());
  double lagrange_old,
      lagrange_current = generate_lagrange_polynomial(n, values.data(), roots.data())(x);
  do {
    n++;
    lagrange_old = lagrange_current;
    roots.reserve(n);
    values.reserve(n);
    fill_chebyshev_polynomial_roots(n, a, b, roots.data());
    fill_function_values(func, n, values.data(), roots.data());
    lagrange_current = generate_lagrange_polynomial(n, values.data(), roots.data())(x);
  } while (abs(lagrange_current - lagrange_old) > 1e-4 && n < 100);
  return {lagrange_current, n};
}