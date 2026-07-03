#include <bits/stdc++.h>
#include <math.h>

#include <iostream>

using namespace std;

string ltrim(const string&);
string rtrim(const string&);

using fn_t = double(double);

string error_message = "";
bool has_discontinuity = false;

double first_function (double x, double y)
{
  return sin(x);
}

double second_function (double x, double y)
{
  return (x * y)/2;
}

double third_function (double x, double y)
{
  return y - (2 * x)/y;
}

double fourth_function (double x, double y)
{
  return x + y;
}

double default_function(double x, double y)
{
    return 0.0;
}

std::function<double(double,double)> get_function(int n) {
  switch (n) {
    case 1:  return first_function;
    case 2:  return second_function;
    case 3:  return third_function;
    case 4:  return fourth_function;
    case 5:  return [](double x, double y) { return y * y; };
    default: return default_function;
  }
}