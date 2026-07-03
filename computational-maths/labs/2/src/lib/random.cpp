#include "random.h"

vector<vector<double>> generateMatrixA(int n) {
  vector<vector<double>> A(n, vector<double>(n));
  random_device rd;
  mt19937 gen(rd());
  uniform_real_distribution<double> dist(-10.0, 10.0);

  for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j++) {
      A[i][j] = dist(gen);
    }
  }

  for (int i = 0; i < n; i++) {
    double rowSum = 0;
    for (int j = 0; j < n; j++) {
      if (i != j)
        rowSum += abs(A[i][j]);
    }
    if (abs(A[i][i]) <= rowSum) {
      A[i][i] = rowSum + abs(A[i][i]) + 1.0;
    }
  }

  return A;
}

vector<double> generateUnknowns(int n) {
  vector<double> x(n);
  random_device rd;
  mt19937 gen(rd());
  uniform_real_distribution<double> dist(-10.0, 10.0);

  for (int i = 0; i < n; i++) {
    x[i] = dist(gen);
  }

  return x;
}

vector<double> calculateF(const vector<vector<double>>& A, const vector<double>& x) {
  int n = A.size();
  vector<double> b(n, 0.0);

  for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j++) {
      b[i] += A[i][j] * x[j];
    }
  }

  return b;
}