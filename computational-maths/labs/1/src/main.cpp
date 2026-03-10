#include <bits/stdc++.h>

using namespace std;
using fn_t = double (double);

string ltrim(const string &);
string rtrim(const string &);
vector<string> split(const string &);


double weierstrass_function(double x){
    double f_x = 0;
    int n = 5;
    double b = 0.5;
    int a = 13;
    for(int i = 0; i < n; i++){
        f_x += pow(b, i) * cos(pow(a, n) * M_PI * x);
    }
    return f_x;
}

double gamma_function(double x){
    double tmp = (x - 0.5) * log(x + 4.5) - (x + 4.5);
    double ser = 1.0 +
            76.18009173   / (x + 0.0) -  86.50532033   / (x + 1.0) +
            24.01409822   / (x + 2.0) -  1.231739516   / (x + 3.0) +
            0.00120858003 / (x + 4.0) -  0.00000536382 / (x + 5.0);
    return exp(tmp + log(ser * sqrt(2 * M_PI)));
}

/*
* How to use this function:
*    fn_t& f = get_function(4);
*    f(0.0001);
*/
fn_t& get_function (int n)
{
  switch (n)
    {
    case 1:  return weierstrass_function;
    case 2:  return gamma_function;
    default: return gamma_function;
    }
}

void fill_chebyshev_polynomial_roots(const int n, const double a, const double b, double roots[]) {
  for (int k = 1; k <= n; k++) {
    roots[k - 1] = 0.5 * (a + b + (b - a) * cos(M_PI * (2 * k - 1) / (2.0 * n)));
  }
}

function<double(double)> generate_lagrange_polynomial(const int n, const function<double(double)> func, const double grid[]) {
  return [n, func, grid](double x) {
    double result = 0;
    for (int i = 0; i < n; i++) {
      double current_term = func(grid[i]);
      for (int j = 0; j < n; j++) {
        if (j != i) {
          current_term *= x - grid[j];
          current_term /= grid[i] - grid[j];
        }
      }
      result += current_term;
    }
    return result;
  };
}

double interpolate_by_lagrange(int f, double a, double b, double x) {
  function<double(double)> func = get_function(f);
  int n = 1;
  std::vector<double> roots(n);
  fill_chebyshev_polynomial_roots(n, a, b, roots.data());
  double lagrange_old, lagrange_current = generate_lagrange_polynomial(n, func, roots.data())(x);
  do {
    n++;
    lagrange_old = lagrange_current;
    roots.reserve(n);
    fill_chebyshev_polynomial_roots(n, a, b, roots.data());
    lagrange_current = generate_lagrange_polynomial(n, func, roots.data())(x);
  } while (abs(lagrange_current - lagrange_old) > 1e-4 && n < 100);
  return lagrange_current;
}