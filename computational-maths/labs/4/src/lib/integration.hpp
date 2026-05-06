#ifndef INTEGRATION_H
#define INTEGRATION_H

#include "preamble.h"

#include "unordered_map"
#include "vector"
#include <limits>

struct DiscontinuityDot {
  double x;
  bool is_second_order;
};

struct DiscontinuityPlace {
  bool is_interval;
  DiscontinuityDot left;
  DiscontinuityDot right;
};

struct FunctionMeta {
  std::function<double(double)> f;
  std::vector<DiscontinuityPlace> discontinuity_places;
};

struct IntegrationResult {
  double result;
  bool has_result;
  bool has_discontinuity;
  std::string message;
};

class IntegrateFunctions {
public:
  IntegrateFunctions(double epsilon) : IntegrateFunctions(epsilon, 1e6, std::unordered_map<std::size_t, FunctionMeta>{}) {
  }

  IntegrateFunctions(double epsilon, std::size_t max_iterations, std::unordered_map<std::size_t, FunctionMeta> funcs) : _funcs(funcs), _epsilon(epsilon), _max_iterations(max_iterations) {
  }

  void AddFunction(const std::size_t number, const FunctionMeta& func) {
    this->_funcs[number] = func;
  }
  
  IntegrationResult Integrate(std::size_t number, double a, double b) {
    double result_sign = 1.0;
    if (b < a) {
      std::swap(a, b);
      result_sign = -1.0;
    }
    if (this->_funcs.count(number) == 0U) {
      throw std::invalid_argument("no integration functions registered under specified number");
    }
    double result = 0.0;
    FunctionMeta meta = this->_funcs[number];
    std::vector<double> split_points = {a};

    for (const auto& place : meta.discontinuity_places) {
      if (place.is_interval) {
        if (place.left.x < b && place.right.x > a) {
          return {0.0, false, true, "Integrated function has discontinuity or does not defined in current interval"};
        }
      } else {
        double dx = place.left.x;
        if (dx >= a && dx <= b) {
          if (place.left.is_second_order) {
            return {0.0, false, true, "Integrated function has discontinuity or does not defined in current interval"};
          }
          if (dx != a && dx != b) {
            split_points.push_back(dx);
          }
        }
      }
    }
    split_points.push_back(b);

    double total_result = 0.0;
    for (std::size_t i = 0; i < split_points.size() - 1; ++i) {
      double sub_a = split_points[i];
      double sub_b = split_points[i + 1];
      total_result += _IntegrateSubInterval(meta.f, sub_a, sub_b);
    }

    return {
      total_result * result_sign,
      true,
      false,
    };
  }

private:
  double _IntegrateSubInterval(const std::function<double(double)>& f, double a, double b) {
    auto safe_eval = [&](double x, double h_step) -> double {
      double val = f(x);
      if (std::isnan(val) || std::isinf(val)) {
        double eps = std::max(1e-12, h_step * 0.01);
        double v_l = f(x - eps);
        double v_r = f(x + eps);
        bool bad_l = std::isnan(v_l) || std::isinf(v_l);
        bool bad_r = std::isnan(v_r) || std::isinf(v_r);
        
        if (!bad_l && !bad_r) {
          return (v_l + v_r) * 0.5;
        }
        if (!bad_l) {
          return v_l;
        }
        if (!bad_r) {
          return v_r;
        }
        return 0.0;
      }
      return val;
    };
    double prev_res = 0.0;
    std::size_t n = 1;

    while (n <= this->_max_iterations) {
      double h = (b - a) / n;
      double current_res = 0.5 * (safe_eval(a, h) + safe_eval(b, h));
      for (std::size_t i = 1; i < n; i++) {
        current_res += f(a + i * h);
      }
      current_res *= h;

      if (n > 1 && std::abs(current_res - prev_res) < this->_epsilon) {
        return current_res;
      }
      prev_res = current_res;
      n *= 2;
    }
    return prev_res;
  }

  std::unordered_map<std::size_t, FunctionMeta> _funcs;
  const std::size_t _max_iterations;
  const double _epsilon;
};

IntegrateFunctions InitMain(double epsilon) {
  IntegrateFunctions integrate = IntegrateFunctions(epsilon);
  integrate.AddFunction(1, FunctionMeta{
    get_function(1),
    {
      DiscontinuityPlace{
        false,
        {
          0.0,
          true,
        },
      },
    },
  });
  integrate.AddFunction(2, FunctionMeta{
    get_function(2),
    {
      DiscontinuityPlace{
        false,
        {
          0.0,
          false,
        },
      },
    },
  });
  integrate.AddFunction(3, FunctionMeta{
    get_function(3),
    {},
  });
  integrate.AddFunction(4, FunctionMeta{
    get_function(4),
    {},
  });
  integrate.AddFunction(5, FunctionMeta{
    get_function(5),
    {
      DiscontinuityPlace{
        true,
        {
          -std::numeric_limits<double>::infinity(),
          false,
        },
        {
          0.0,
          true,
        },
      },
    },
  });
  return integrate;
}

double calculate_integral(double a, double b, int f, double epsilon) {
  IntegrateFunctions integrate = InitMain(epsilon);
  IntegrationResult result = integrate.Integrate(static_cast<std::size_t>(f), a, b);
  has_discontinuity = result.has_discontinuity;
  if (!result.has_result) {
    error_message = result.message;
  }
  return result.result;
}

#endif