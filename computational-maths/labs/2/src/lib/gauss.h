#ifndef GAUSS_H
#define GAUSS_H

#include "preamble.h"

bool triangulateMatrix(const int n, vector<vector<double>>& matrix);
vector<double> solveByGauss(int n, vector<vector<double>> matrix);

#endif