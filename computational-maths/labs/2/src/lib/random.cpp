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

vector<double> calculateRHS(const vector<vector<double>>& A, const vector<double>& x) {
  int n = A.size();
  vector<double> b(n, 0.0);

  for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j++) {
      b[i] += A[i][j] * x[j];
    }
  }

  return b;
}

void compareSolutions(
    const vector<double>& original, const vector<double>& calculated, double epsilon
) {
  cout << "\n=== COMPARISON OF SOLUTIONS ===\n";
  cout << setw(10) << "Variable" << setw(15) << "Original" << setw(15) << "Calculated" << setw(15)
       << "Difference" << setw(15) << "Status" << endl;
  cout << string(70, '-') << endl;

  bool allMatch = true;
  double maxDiff = 0.0;

  for (int i = 0; i < original.size(); i++) {
    double diff = abs(original[i] - calculated[i]);
    maxDiff = max(maxDiff, diff);
    bool match = (diff < epsilon);
    if (!match)
      allMatch = false;

    cout << setw(10) << "x" + to_string(i + 1) << setw(15) << fixed << setprecision(6)
         << original[i] << setw(15) << fixed << setprecision(6) << calculated[i] << setw(15)
         << scientific << setprecision(6) << diff << setw(15) << (match ? "MATCH" : "MISMATCH")
         << endl;
  }

  cout << string(70, '-') << endl;
  cout << "Maximum difference: " << scientific << maxDiff << endl;
  cout << "Overall result: "
       << (allMatch ? "✓ SUCCESS - Solutions match!" : "✗ FAILURE - Solutions differ!") << endl;
}