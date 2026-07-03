#ifndef INTERPOLATE_H
#define INTERPOLATE_H

#include <vector>
#include <tuple>
#include <functional>
#include <algorithm>
#include <cmath>

struct InterpolationResult {
  std::vector<std::tuple<double, double>> points;
  std::size_t chebyshev_k;
};

std::vector<double> GetChebyshevRoots(double a, double b, std::size_t n_size) {
  std::vector<double> roots(n_size);
  const double pi = std::acos(-1.0);

  for (std::size_t i = 0; i < n_size; i++) {
    double x_standard = std::cos((2.0 * i + 1.0) / (2.0 * n_size) * pi);
    roots[i] = 0.5 * (a + b) + 0.5 * (b - a) * x_standard;
  }

  return roots;
}

InterpolationResult InterpolateLagrange(double a, double b, std::function<double(double)> func, double eps, std::size_t n_lagrange_max, std::size_t dots_num) {
  std::vector<std::tuple<double, double>> lagrange_values(dots_num + 1);
  std::vector<double> prev_values(dots_num + 1, 0.0);
  std::vector<double> curr_values(dots_num + 1, 0.0);

  auto eval_lagrange = [](double x, const std::vector<double>& nodes, const std::vector<double>& values) {
    double total_sum = 0.0;
    std::size_t n = nodes.size();
    for (std::size_t i = 0; i < n; ++i) {
      double term = values[i];
      for (std::size_t j = 0; j < n; ++j) {
        if (j != i) {
          term *= (x - nodes[j]) / (nodes[i] - nodes[j]);
        }
      }
      total_sum += term;
    }
    return total_sum;
  };

  std::size_t final_k = 0;
  for (std::size_t k = 5; k <= n_lagrange_max; ++k) {
    final_k = k;
    auto nodes = GetChebyshevRoots(a, b, k);
    std::vector<double> values(k);
    for (std::size_t j = 0; j < k; ++j) {
      values[j] = func(nodes[j]);
    }

    for (std::size_t i = 0; i <= dots_num; ++i) {
      double x = (i == 0) ? a : ((i == dots_num) ? b : a + i * (b - a) / dots_num);
      curr_values[i] = eval_lagrange(x, nodes, values);
    }

    if (k > 1) {
      double max_diff = 0.0;
      for (std::size_t i = 0; i <= dots_num; ++i) {
        max_diff = std::max(max_diff, std::abs(curr_values[i] - prev_values[i]));
      }
      if (max_diff <= eps) {
        break;
      }
    }
    prev_values = curr_values;
  }

  for (std::size_t i = 0; i <= dots_num; ++i) {
    double x = (i == 0) ? a : ((i == dots_num) ? b : a + i * (b - a) / dots_num);
    lagrange_values[i] = std::make_tuple(x, curr_values[i]);
  }

  return {lagrange_values, final_k};
}

#endif