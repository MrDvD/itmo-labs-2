#include <functional>

std::function<double(double)> get_function(int n, bool add_noise);
std::function<double(double)> get_function(int n);

struct debug_result {
  double result;
  int end_iteration;
};

void fill_chebyshev_polynomial_roots(const int n, const double a, const double b, double roots[]);
std::function<double(double)> generate_lagrange_polynomial(const int n, const std::function<double(double)> func, const double grid[]);
debug_result interpolate_by_lagrange(int f, double a, double b, double x);