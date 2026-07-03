#include <algorithm>
#include <random>
#include <vector>

struct test_case {
  int function_number;
  double x, a, b;
  bool calc;
};

std::vector<test_case> generate_tests(const double threshold);