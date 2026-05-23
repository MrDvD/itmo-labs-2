#include <iostream>
#include <vector>
#include <cmath>
#include <iomanip>
#include <fstream>
#include <string>
#include <filesystem>

#include "lib/differential.hpp"
#include "lib/interpolate.hpp"

struct TestCase {
  int func_number;
  int case_index;
  double a;
  double y_a;
  double b;
  double epsilon;
};

double getExactResult(int f, double a, double y_a, double b) {
  switch (f) {
    case 1:
      return y_a + std::cos(a) - std::cos(b);
    case 2:
      return y_a * std::exp((b * b - a * a) / 4.0);
    case 3: {
      double C = (y_a * y_a - 2.0 * a - 1.0) * std::exp(-2.0 * a);
      double expr = 2.0 * b + 1.0 + C * std::exp(2.0 * b);
      return (expr >= 0.0) ? std::sqrt(expr) : std::nan("");
    }
    case 4:
      return (y_a + a + 1.0) * std::exp(b - a) - b - 1.0;
    case 5: {
      double denom = (1.0 / y_a) - (b - a);
      return (std::abs(denom) > 1e-9) ? (1.0 / denom) : std::nan("");
    }
    default:
      return 0.0;
  }
}

void GenerateTrajectoryData(const TestCase& t) {
  namespace fs = std::filesystem;

  fs::path dir_path = "output";
  fs::create_directories(dir_path);

  std::string prefix = "f" + std::to_string(t.func_number) + "_case" + std::to_string(t.case_index);
  fs::path euler_path = dir_path / (prefix + "_euler.txt");
  fs::path exact_path = dir_path / (prefix + "_exact.txt");

  std::ofstream euler_file(euler_path);
  std::ofstream exact_file(exact_path);

  if (!euler_file.is_open() || !exact_file.is_open()) return;

  std::size_t samples = 100;
  std::size_t euler_iterations = 0;

  auto eval_euler = [t, &euler_iterations](double x) {
    EulerSolution solution = solveByEuler(t.func_number, t.epsilon, t.a, t.y_a, x);
    euler_iterations = std::max(euler_iterations, solution.n_grid);
    return solution.answer;
  };
  auto eval_exact = [t](double x) {
    return getExactResult(t.func_number, t.a, t.y_a, x);
  };

  InterpolationResult euler_result = InterpolateLagrange(t.a, t.b, eval_euler, t.epsilon, samples, samples);
  InterpolationResult exact_result = InterpolateLagrange(t.a, t.b, eval_exact, t.epsilon, samples, samples);
  euler_file << euler_result.chebyshev_k << " " << t.a << " " << t.b << " " << t.epsilon << " " << t.y_a << " " << euler_iterations << '\n';
  exact_file << exact_result.chebyshev_k << '\n';
  for (std::tuple<double, double> point : euler_result.points) {
    euler_file << std::get<0>(point) << " " << std::get<1>(point) << "\n";
  }
  for (std::tuple<double, double> point : exact_result.points) {
    exact_file << std::get<0>(point) << " " << std::get<1>(point) << "\n";
  }
}

int main() {
  std::cout << std::fixed << std::setprecision(6);

  std::vector<TestCase> tests = {
    {1, 1, 0.0, 0.0, 3.141592, 1e-4}, 
    {1, 2, 0.0, 1.0, 6.283185, 1e-4}, 
    {2, 1, 0.0, 1.0, 2.0, 1e-4}, 
    {2, 2, 0.0, 0.2, 7.2, 1e-4}, 
    {3, 1, 0.0, 2.0, 1.5, 1e-4}, 
    {3, 2, 0.0, 1.0, 0.8, 1e-4}, 
    {4, 1, 0.0, 0.0, 1.0, 1e-4}, 
    {4, 2, 0.0, -1.0, 2.0, 1e-4}, 
    {5, 1, 0.0, 0.5, 1.5, 1e-4}, 
    {5, 2, 0.0, 0.8, 1.1, 1e-4},
  };

  for (const TestCase& t : tests) {
    GenerateTrajectoryData(t);
    std::cout << "Trajectory data written to disk.\n";
  }

  return 0;
}