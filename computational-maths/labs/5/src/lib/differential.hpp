#ifndef DIFFERENTIAL_H
#define DIFFERENTIAL_H

#include "preamble.h"
#include <cstdlib>

std::size_t ITERATIONS_MAX = 1e6;

struct EulerSolution {
  double answer;
  std::size_t n_grid;
};

double calcForGrid(int f, double y_a, double a, double b, std::size_t n_grid) {
  double h = (b - a) / n_grid;
  std::function<double(double,double)> func = get_function(f);
  double y_b = y_a;
  double x = a;
  for (std::size_t i = 1; i <= n_grid; i++) {
    y_b += h * func(x, y_b);
    x += h;
  }
  return y_b;
}

EulerSolution solveByEuler(int f, double epsilon, double a, double y_a, double b) {
  std::size_t n_grid = 2;
  double y_b_h = calcForGrid(f, y_a, a, b, n_grid);
  while (n_grid < ITERATIONS_MAX) {
    n_grid *= 2;
    double y_b_h_2 = calcForGrid(f, y_a, a, b, n_grid);
    if (std::abs(y_b_h - y_b_h_2) <= epsilon) {
      return { y_b_h_2, n_grid };
    }
    y_b_h = y_b_h_2;
  }
  return { y_b_h, n_grid };
}

#endif