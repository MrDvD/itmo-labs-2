#ifndef OUTPUT_H
#define OUTPUT_H

#include "preamble.h"

void outputTrace(const vector<vector<double>>& t_matrix, const vector<double>& answer);
void output2DVector(const vector<vector<double>>& arr);
template <typename Iterator>
void outputVector(Iterator begin, Iterator end);

#endif