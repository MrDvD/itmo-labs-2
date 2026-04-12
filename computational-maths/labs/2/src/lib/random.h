#ifndef RANDOM_H
#define RANDOM_H

#include "gauss.h"
#include "preamble.h"

vector<vector<double>> generateMatrixA(int n);
vector<double> generateUnknowns(int n);
vector<double> calculateF(const vector<vector<double>>& A, const vector<double>& x);

#endif