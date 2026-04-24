#include "lib/iterations.hpp"

#include <iostream>
#include <unordered_map>

int main() {
  SimpleIterationsSystem obj = InitSystem();

  std::unordered_map<std::size_t, std::vector<double>> initial_x = {
    {1, { 0.0, 0.0 }},
    {2, { -1.9, 2.1 }},
    {3, { 0.0, 0.0, 0.0 }},
    {4, { 0.8, 0.6 }},
    {5, { 0.4, 0.2 }},
  };
  for (std::size_t i = 1; i <= 5; i++) {
    std::cout << "--- Solution for system #" << i << ":\n";
    ResultInfo rawInfo = obj.SolveSystem(i, initial_x[i]);
    std::vector<double> result = rawInfo.solution;
    std::vector<double> residues = CaluclateResidues(i, result);
    for (std::size_t j = 0; j < result.size(); j++) {
      std::cout << "x[" << j << "]: " << result[j] << "\t\t" << "res[" << j << "]: " << residues[j] << "\n";
    }
    double mse = 0.0;
    for (const auto& res : residues) {
      mse += res * res;
    }
    mse /= residues.size();
    std::cout << "MSE: " << mse << "\n";
    std::cout << "Total iterations: " << rawInfo.iterations_count << "\n";
  }
}