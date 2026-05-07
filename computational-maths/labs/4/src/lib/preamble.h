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