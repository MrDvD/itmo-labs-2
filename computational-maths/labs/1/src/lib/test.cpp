#include <test.h>

#include <algorithm>
#include <random>
#include <vector>

std::vector<test_case> generate_tests(const double threshold) {
  std::vector<test_case> all_cases;
  std::random_device rd;
  std::mt19937 gen(rd());

  std::uniform_real_distribution<double> calc_chance(0.0, 1.0);

  struct {
    int id;
    double a, b;
  } configs[] = {
      {1, -std::numbers::pi, std::numbers::pi},
      {2,              -5.0,              5.0},
      {3,              -2.0,              2.0},
      {4,               0.5,              5.0},
      {5,              -3.0,              3.0}
  };

  for (auto config : configs) {
    int points = 100;
    for (int i = 0; i <= points; ++i) {
      double x = config.a + (config.b - config.a) * (static_cast<double>(i) / points);

      bool should_calc = (calc_chance(gen) < threshold);

      all_cases.push_back({config.id, x, config.a, config.b, should_calc});
    }
  }
  return all_cases;
}