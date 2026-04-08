#ifndef RANDOM_H
#define RANDOM_H

#include "gauss.h"
#include "preamble.h"

// Function to generate a random invertible matrix A (satisfying method applicability)
vector<vector<double>> generateMatrixA(int n);

// Generate a column of unknowns (the "secret" solution)
vector<double> generateUnknowns(int n);

// Calculate right-hand side b = A * x
vector<double> calculateRHS(const vector<vector<double>>& A, const vector<double>& x);

// Compare calculated and original unknowns
void compareSolutions(
    const vector<double>& original, const vector<double>& calculated, double epsilon = 1e-9
);

#endif