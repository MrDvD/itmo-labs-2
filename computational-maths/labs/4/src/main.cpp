#include "lib/integration.hpp"

#include <iostream>
#include <unordered_map>

int main() {
  IntegrateFunctions obj = InitMain(1e-6);

  std::unordered_map<std::size_t, std::vector<double>> bounds = {
    {1, { 0.0, 0.0 }},
    {2, { -1.9, 2.1 }},
    {3, { 0.0, 2.0 }},
    {4, { 0.8, 0.6 }},
    {5, { 0.4, 0.2 }},
  };
  for (std::size_t i = 1; i <= 5; i++) {
    std::cout << "--- Solution for function #" << i << ":\n";
    IntegrationResult res = obj.Integrate(i, bounds[i][0], bounds[i][1]);
    if (!res.has_result) {
      std::cout << "[Error] " << res.message << '\n';
      continue;
    }
    if (res.has_discontinuity) {
      std::cout << "[Warning] The function has discontinuity. The interval was split down." << '\n';
    }
    std::cout << "Result: " << res.result << '\n';
    // std::cout << "MSE: " << mse << "\n";
    // std::cout << "Total iterations: " << rawInfo.iterations_count << "\n";
  }
}