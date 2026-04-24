#include "iterations.h"

class SimpleIterationsSystem {
  using SystemHandler = std::function<std::vector<double>(const std::vector<double>& x)>;

public:
  std::unordered_map<std::size_t, SystemHandler> handlers;

  SimpleIterationsSystem(const double eps, const std::size_t max_iterations) : _eps(eps), _max_iterations(max_iterations) {
  }

  const SystemHandler& GetHandler(std::size_t system_num) {
    if (this->handlers.contains(system_num)) {
      return this->handlers.at(system_num);
    }
    throw std::invalid_argument("no handlers for specified system");
  }

  void SetHandler(std::size_t system_num, const SystemHandler& handler) {
    this->handlers.at(system_num) = handler;
  }

  const std::vector<double> SolveSystem(std::size_t system_num, const std::vector<double>& init_x) {
    std::vector<double> prev_x(init_x);

    for (std::size_t i = 0; i < this->_max_iterations; i++) {
      const SystemHandler& handler = GetHandler(system_num);
      const std::vector<double> new_x = handler(prev_x);
      
      double residual = 0.0;
      for (std::size_t i = 0; i < new_x.size(); i++) {
        residual += std::pow(new_x[i] - prev_x[i], 2);
      }
      residual = std::sqrt(residual);

      if (residual)
    }
  }

private:
  const double _eps;
  const std::size_t _max_iterations;
};

vector<double> solve_by_fixed_point_iterations(
    int system_id,
    int number_of_unknowns,
    vector<double> x)
{
    const double eps = 1e-7;
    const int max_iters = 100000;
    vector<double> nx(number_of_unknowns);

    for (int it = 0; it < max_iters; ++it)
    {
if (system_id == 1)
{
    nx[0] = x[0] - sin(x[0]);
    nx[1] = x[1] - (x[0] * x[1] / 2.0);
}
else if (system_id == 2)
{
    double val = (x[0] * x[0] * x[1] * x[1] - 6.0 * pow(x[1], 3.0) + 8.0) / 3.0;
    nx[0] = cbrt(val);
    nx[1] = (pow(x[0], 4.0) + 2.0) / 9.0;
}
else if (system_id == 3)
{
    // Здесь важно, чтобы начальные x, y, z были близки к 0, 
    // иначе x^2 и y^2 приведут к расходимости.
    nx[0] = 0.1 - pow(x[0], 2.0) + 2.0 * x[1] * x[2];
    nx[1] = -0.2 - pow(x[1], 2.0) - 3.0 * x[0] * x[2];
    nx[2] = 0.3 - pow(x[2], 2.0) - 2.0 * x[0] * x[1];
}

        double sum_sq = 0.0;
        for (int i = 0; i < number_of_unknowns; ++i) {
          double delta = nx[i] - x[i];
          sum_sq += delta * delta;
        }
        
        // Евклидова норма (L2)
        double diff = sqrt(sum_sq);

        x = nx;

        if (diff < eps)
            break;
    }

    return x;
}

vector<double> solve_by_fixed_point_iterations(
    int system_id,
    int number_of_unknowns,
    vector<double> x)
{
    const double eps = 1e-7;
    const int max_iters = 100000;
    vector<double> nx(number_of_unknowns);

    for (int it = 0; it < max_iters; ++it)
    {
if (system_id == 1)
{
    nx[0] = x[0] - sin(x[0]);
    nx[1] = x[1] - (x[0] * x[1] / 2.0);
}
else if (system_id == 2)
{
    double val = (x[0] * x[0] * x[1] * x[1] - 6.0 * pow(x[1], 3.0) + 8.0) / 3.0;
    nx[0] = cbrt(val);
    nx[1] = (pow(x[0], 4.0) + 2.0) / 9.0;
}
else if (system_id == 3)
{
    // Здесь важно, чтобы начальные x, y, z были близки к 0, 
    // иначе x^2 и y^2 приведут к расходимости.
    nx[0] = 0.1 - pow(x[0], 2.0) + 2.0 * x[1] * x[2];
    nx[1] = -0.2 - pow(x[1], 2.0) - 3.0 * x[0] * x[2];
    nx[2] = 0.3 - pow(x[2], 2.0) - 2.0 * x[0] * x[1];
}

double sum_sq = 0.0;
        for (int i = 0; i < number_of_unknowns; ++i) {
            double delta = nx[i] - x[i];
            sum_sq += delta * delta;
        }
        
        // Евклидова норма (L2)
        double diff = sqrt(sum_sq);

        x = nx;

        if (diff < eps)
            break;
    }

    return x;
}