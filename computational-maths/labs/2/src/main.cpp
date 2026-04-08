#include "lib/gauss.h"
#include "lib/input.h"
#include "lib/output.h"
#include "lib/preamble.h"
#include "lib/random.h"

int main() {
  cout << "=== LINEAR SYSTEM SOLVER TEST ===\n" << endl;

  int source = InputModule::getInputSource();
  vector<vector<double>> augmented;
  int n = 0;

  if (source == 1) {
    n = InputModule::getDimension("console");
    augmented = InputModule::readMatrixFromConsole(n);
  } else if (source == 2) {
    string filename = InputModule::getFilename();
    augmented = InputModule::readMatrixFromFile(filename);
    if (augmented.empty()) {
      return 1;
    }
    n = augmented.size();
  } else if (source == 3) {
    cout << "Enter system dimension (n): ";
    n = InputModule::getDimension("console");

    cout << "\nGenerating random system..." << endl;
    vector<vector<double>> A = generateMatrixA(n);
    vector<double> x_original = generateUnknowns(n);
    vector<double> b = calculateRHS(A, x_original);

    augmented = A;
    for (int i = 0; i < n; i++) {
      augmented[i].push_back(b[i]);
    }

    cout << "\nOriginal solution:" << endl;
    outputVector(x_original.begin(), x_original.end());
  }

  cout << "\n### SOLVING SYSTEM" << endl;
  cout << "Given matrix:" << endl;
  output2DVector(augmented);
  vector<double> x_solved = solveByGauss(n, augmented);

  if (errorMessage != "") {
    cout << errorMessage << endl;
    cout << "Do solutions exist? " << (isSolutionExists ? "Yes" : "No") << endl;
    return 1;
  }
  return 0;
}