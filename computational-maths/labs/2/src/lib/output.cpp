#include "output.h"

void outputTrace(const vector<vector<double>>& t_matrix, const vector<double>& answer) {
  int n = t_matrix.size();

  double det = 1.0;
  for (int i = 0; i < n; ++i) {
    det *= t_matrix[i][i];
  }
  cout << "Determinant: " << det << endl;
  cout << "Triangular matrix:" << endl;
  output2DVector(t_matrix);
  cout << "Root:" << endl;
  outputVector(answer.begin(), next(answer.begin(), n));
  cout << "Residuals:" << endl;
  outputVector(next(answer.begin(), n), answer.end());
}

void output2DVector(const vector<vector<double>>& arr) {
  for (int i = 0; i < arr.size(); ++i) {
    for (int j = 0; j < arr[i].size(); ++j) {
      cout << setw(10) << fixed << setprecision(4) << arr[i][j] << " ";
    }
    cout << endl;
  }
}

template <typename Iterator>
void outputVector(Iterator begin, Iterator end) {
  for (Iterator it = begin; it != end; ++it) {
    cout << *it << (next(it) == end ? "" : " ");
  }
  cout << endl;
}