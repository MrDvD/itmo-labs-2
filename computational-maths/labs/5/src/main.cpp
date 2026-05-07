#include <iostream>
#include <unordered_map>

#include "lib/integration.hpp"

struct TestCase {
  std::size_t func_number;
  double a;
  double b;
};

int main() {
  IntegrateFunctions obj = InitMain(1e-6);

  std::vector<TestCase> tests = {
      {1,  0.1,             2.0},
      {1, -1.0,             1.0},
      {2, -1.0,             1.0},
      {2,  0.0,             1.0},
      {3,  0.0,             3.0},
      {4,  0.0,             5.0},
      {5,  1.0, std::numbers::e},
      {5, -1.0,             1.0},
  };
  for (const TestCase& t : tests) {
    std::cout << "--- Solution for function #" << t.func_number << ":\n";
    IntegrationResult res = obj.Integrate(t.func_number, t.a, t.b);
    if (!res.has_result) {
      std::cout << "[Error] " << res.message << '\n';
      continue;
    }
    if (res.has_discontinuity) {
      std::cout << "[Warning] The function has discontinuity. The interval was split down." << '\n';
    }
    std::cout << "Bounds: [" << t.a << ", " << t.b << "]\n";
    std::cout << "Result: " << res.result << '\n';
    std::cout << "Exact: " << res.exact_result << '\n';
    std::cout << "Difference: " << std::abs(res.exact_result - res.result) << '\n';
    std::cout << "Intervals: " << res.num_iterations << '\n';
  }
}