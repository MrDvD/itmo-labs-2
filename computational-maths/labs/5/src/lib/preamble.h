#include <bits/stdc++.h>
#include <math.h>

#include <iostream>

using namespace std;

string ltrim(const string&);
string rtrim(const string&);

using fn_t = double(double);

string error_message = "";
bool has_discontinuity = false;

double first_function(double x) {
  return 1 / x;
}

double second_function(double x) {
  return sin(x) / x;
}

double third_function(double x) {
  return x * x + 2;
}

double fourth_function(double x) {
  return 2 * x + 2;
}

double five_function(double x) {
  return log(x);
}

double sineIntegral(double x) {
  if (x == 0)
    return 0;

  double sum = 0;
  double term = x;
  double x2 = x * x;

  for (int n = 0; n < 50; ++n) {
    sum += term / (2 * n + 1);
    term *= -x2 / ((2 * n + 2) * (2 * n + 3));

    if (std::abs(term) < 1e-15)
      break;
  }
  return sum;
}

fn_t& get_function(int n) {
  switch (n) {
    case 1:
      return first_function;
    case 2:
      return second_function;
    case 3:
      return third_function;
    case 4:
      return fourth_function;
    case 5:
      return five_function;
  }
  return five_function;
}