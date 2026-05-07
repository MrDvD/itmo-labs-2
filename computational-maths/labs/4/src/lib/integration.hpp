#ifndef INTEGRATION_H
#define INTEGRATION_H

#include <limits>

#include "preamble.h"
#include "unordered_map"
#include "vector"

struct DiscontinuityDot {
  double x;
  // 0 - continuous
  // 1 - first order
  // 2 - second order
  std::size_t order;
};

struct DiscontinuityPlace {
  bool is_interval;
  DiscontinuityDot left;
  DiscontinuityDot right;
};

struct FunctionMeta {
  std::function<double(double)> f;
  std::function<double(double, double)> integrate;
  std::vector<DiscontinuityPlace> discontinuity_places;
};

struct IntegrationResult {
  double result;
  double exact_result;
  bool has_result;
  bool has_discontinuity;
  std::string message;
  std::size_t num_iterations;
};

class IntegrateFunctions {
public:
  IntegrateFunctions(double epsilon)
      : IntegrateFunctions(epsilon, 1e6, std::unordered_map<std::size_t, FunctionMeta>{}) {
  }

  IntegrateFunctions(
      double epsilon,
      std::size_t max_iterations,
      std::unordered_map<std::size_t, FunctionMeta> funcs
  )
      : _funcs(funcs), _epsilon(epsilon), _max_iterations(max_iterations) {
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

    auto get_point_order = [&](double x) -> std::size_t {
      for (const auto& place : meta.discontinuity_places) {
        if (place.is_interval) {
          if (x > place.left.x && x < place.right.x) {
            return 2; 
          }
        } else {
          if (std::abs(place.left.x - x) < 1e-12) {
            return place.left.order;
          }
        }
      }
      return 0;
    };

    std::size_t order_a = get_point_order(a);
    std::size_t order_b = get_point_order(b);

    std::vector<DiscontinuityDot> split_points = {
        {a, order_a}
    };

    bool is_discontinued = order_a != 0 || order_b != 0;

    for (const auto& place : meta.discontinuity_places) {
      if (place.is_interval) {
        if (place.left.x < b && a < place.right.x) {
          return {
              0.0,
              0.0,
              false,
              true,
              "Integrated function has discontinuity or does not defined in current interval",
              0,
          };
        }
      } else {
        double dx = place.left.x;
        if (dx >= a && dx <= b) {
          if (place.left.order == 2) {
            return {
                0.0,
                0.0,
                false,
                true,
                "Integrated function has discontinuity or does not defined in current interval",
                0,
            };
          }
          if (dx != a && dx != b) {
            is_discontinued = true;
            split_points.push_back({dx, place.left.order});
          }
        }
      }
    }
    split_points.push_back({b, order_b});

    double total_result = 0.0;
    std::size_t intervals = 0;
    for (std::size_t i = 0; i < split_points.size() - 1; ++i) {
      DiscontinuityDot sub_a = split_points[i];
      DiscontinuityDot sub_b = split_points[i + 1];
      SubintervalResult sub_res = _IntegrateSubInterval(meta.f, sub_a, sub_b);
      total_result += sub_res.integral;
      intervals += sub_res.num_iterations;
    }

    return {
        total_result * result_sign,
        meta.integrate(a, b),
        true,
        is_discontinued,
        "",
        intervals,
    };
  }

private:
  struct SubintervalResult {
    double integral;
    std::size_t num_iterations;
  };

  SubintervalResult _IntegrateSubInterval(
      const std::function<double(double)>& f, const DiscontinuityDot& a, const DiscontinuityDot& b
  ) {
    auto safe_eval = [&](double x, double h_step, bool is_left, bool is_continuous) -> double {
      if (!is_continuous) {
        double eps = std::max(1e-12, h_step * 0.01);
        if (is_left) {
          double v_r = f(x + eps);
          bool bad_r = std::isnan(v_r) || std::isinf(v_r);
          if (!bad_r) {
            return v_r;
          }
        }

        double v_l = f(x - eps);
        bool bad_l = std::isnan(v_l) || std::isinf(v_l);
        if (!bad_l) {
          return v_l;
        }
        return 0.0;
      }
      return f(x);
    };
    double prev_res = 0.0;
    std::size_t n = 1;

    std::size_t prev_n = 1;
    while (n <= this->_max_iterations) {
      double h = (b.x - a.x) / n;
      double current_res =
          0.5 * (safe_eval(a.x, h, true, a.order == 0) + safe_eval(b.x, h, false, b.order == 0));
      for (std::size_t i = 1; i < n; i++) {
        current_res += f(a.x + i * h);
      }
      current_res *= h;

      if (n > 1 && std::abs(current_res - prev_res) < this->_epsilon) {
        return {current_res, n};
      }
      prev_res = current_res;
      prev_n = n;
      n *= 2;
    }
    return {prev_res, prev_n};
  }

  std::unordered_map<std::size_t, FunctionMeta> _funcs;
  const std::size_t _max_iterations;
  const double _epsilon;
};

IntegrateFunctions InitMain(double epsilon) {
  IntegrateFunctions integrate = IntegrateFunctions(epsilon);
  integrate.AddFunction(
      1,
      FunctionMeta{
          get_function(1),
          [](double a, double b) { return log(std::abs(b / a)); },
          {
                                  DiscontinuityPlace{
                  false,
                  {
                      0.0,
                      2,
                  },
              }, },
  }
  );
  integrate.AddFunction(
      2,
      FunctionMeta{
          get_function(2),
          [](double a, double b) {
            double result = 0.0;
            if (b < a) {
              std::swap(a, b);
            }
            if (a < 0) {
              result += sineIntegral(-a);
              if (b < 0) {
                result -= sineIntegral(-b);
              } else {
                result += sineIntegral(b);
              }
            } else {
              result = sineIntegral(b) - sineIntegral(a);
            }
            return result;
                                  },
          {
                                  DiscontinuityPlace{
                  false,
                  {
                      0.0,
                      1,
                  },
              }, },
  }
  );
  integrate.AddFunction(
      3,
      FunctionMeta{
          get_function(3),
          [](double a, double b) { return (pow(b, 3) - pow(a, 3)) / 3 + 2 * (b - a); },
          {},
      }
  );
  integrate.AddFunction(
      4,
      FunctionMeta{
          get_function(4),
          [](double a, double b) { return pow(b, 2) - pow(a, 2) + 2 * (b - a); },
          {},
      }
  );
  integrate.AddFunction(
      5,
      FunctionMeta{
          get_function(5),
          [](double a, double b) { return b * log(b) - a * log(a) + a - b; },
          {
                                  DiscontinuityPlace{
                  true,
                  {
                      -std::numeric_limits<double>::infinity(),
                      0,
                  },
                  {
                      0.0,
                      2,
                  },
              }, },
  }
  );
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