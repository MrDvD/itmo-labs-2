#ifndef ITERATIONS_H
#define ITERATIONS_H

#include "preamble.h"

#include <unordered_map>
#include <string>

struct ResultInfo {
  std::vector<double> solution;
  std::size_t iterations_count;
};

class SimpleIterationsSystem {
  using SystemHandler = std::function<std::vector<double>(const std::vector<double>& x)>;

public:
  SimpleIterationsSystem(const double eps, const std::size_t max_iterations)
      : _eps(eps), _max_iterations(max_iterations), _handlers({}) {
  }

  const SystemHandler& GetHandler(std::size_t system_num) {
    if (this->_handlers.count(system_num) != 0U) {
      return this->_handlers.at(system_num);
    }
    throw std::invalid_argument("no handlers for specified system: " + std::to_string(system_num));
  }

  void SetHandler(std::size_t system_num, const SystemHandler& handler) {
    this->_handlers[system_num] = handler;
  }

  const ResultInfo SolveSystem(std::size_t system_num, const std::vector<double>& init_x) {
    std::vector<double> prev_x(init_x);

    std::size_t iterations_count = 0;
    for (std::size_t i = 0; i < this->_max_iterations; i++) {
      const SystemHandler& handler = GetHandler(system_num);
      const std::vector<double> new_x = handler(prev_x);

      double residual = 0.0;
      for (std::size_t j = 0; j < new_x.size(); j++) {
        residual += std::pow(new_x[j] - prev_x[j], 2);
      }
      residual = std::sqrt(residual);

      prev_x = new_x;
      iterations_count++;
      if (residual < this->_eps) {
        break;
      }
    }
    return { prev_x, iterations_count };
  }

private:
  const double _eps;
  const std::size_t _max_iterations;
  std::unordered_map<std::size_t, SystemHandler> _handlers;
};

const SimpleIterationsSystem InitSystem() {
  SimpleIterationsSystem obj = SimpleIterationsSystem(1e-7, 1e5);
  obj.SetHandler(0, [](const std::vector<double>& x) {
    return x;
  });
  obj.SetHandler(1, [](const std::vector<double>& x) {
    std::vector<double> new_x(x.size());

    new_x[0] = x[0] - sin(x[0]);
    new_x[1] = x[1] - (x[0] * x[1] / 2.0);

    return new_x;
  });
  obj.SetHandler(2, [](const std::vector<double>& x) {
    std::vector<double> new_x(x.size());

    new_x[0] = -pow(9.0 * x[1] - 2.0, 0.25);
    new_x[1] = cbrt((x[0] * x[0] * x[1] * x[1] - 3.0 * pow(x[0], 3.0) + 8.0) / 6.0);

    return new_x;
  });
  obj.SetHandler(3, [](const std::vector<double>& x) {
    std::vector<double> new_x(x.size());

    new_x[0] = 0.1 - pow(x[0], 2.0) + 2.0 * x[1] * x[2];
    new_x[1] = -0.2 - pow(x[1], 2.0) - 3.0 * x[0] * x[2];
    new_x[2] = 0.3 - pow(x[2], 2.0) - 2.0 * x[0] * x[1];

    return new_x;
  });
  obj.SetHandler(4, [](const std::vector<double>& x) {
    std::vector<double> new_x(x.size());

    new_x[0] = cbrt(x[1]);
    new_x[1] = sqrt(1.0 - x[0] * x[0]);

    return new_x;
  });
  obj.SetHandler(5, [](const std::vector<double>& x) {
    std::vector<double> new_x(x.size());

    new_x[0] = log(2.0 - x[0]);
    new_x[1] = x[0] - sin(x[1]);

    return new_x;
  });
  return obj;
}

namespace {
vector<double> solve_by_fixed_point_iterations(
    int system_id, int number_of_unknowns, vector<double> x
) {
  SimpleIterationsSystem obj = InitSystem();
  return obj.SolveSystem(system_id, x).solution;
}

std::vector<double> CaluclateResidues(const std::size_t system_num, const std::vector<double>& result) {
  funcvec_t funcs = get_functions(system_num);
  std::vector<double> residues(funcs.size());
  for (std::size_t i = 0; i < funcs.size(); i++) {
    residues[i] = -funcs[i](result);
  }
  return residues;
}
}  // namespace

#endif