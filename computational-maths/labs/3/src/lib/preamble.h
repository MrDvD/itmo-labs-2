#include <bits/stdc++.h>
#include <vector>
#include <cmath>

using namespace std;

string ltrim(const string &);
string rtrim(const string &);


typedef double fn_t(vector<double>);
typedef vector<fn_t*> funcvec_t;


double first_function(vector<double> args)
{
  return sin(args[0]);
}

double second_function(vector<double> args)
{
  return (args[0] * args[1])/2;
}

double third_function(vector<double> args)
{
  return pow(args[0], 2) * pow(args[1], 2) - 3 * pow(args[0], 3) - 6 * pow(args[1], 3) + 8;
}


double fourth_function(vector<double> args)
{
  return pow(args[0], 4) - 9 * args[1] + 2;
}

double fifth_function(vector<double> args)
{
  return args[0] + pow(args[0], 2) - 2 * args[1] * args[2] - 0.1;
}

double six_function(vector<double> args)
{
  return args[1] + pow(args[1], 2) + 3 * args[0] * args[2] + 0.2;
}


double seven_function(vector<double> args)
{
  return args[2] + pow(args[2], 2) + 2 * args[0] * args[1] - 0.3;
}

double default_function(vector<double> args)
{
    return 0.0;
}


/*
* How to use this function:
*    funcvec_t funs = get_functions(4);
*    f[0](0.0001);
*/
funcvec_t get_functions(int n)
{
  switch (n)
    {
        case 1:  return {first_function, second_function};
        case 2:  return {third_function, fourth_function};
        case 3:  return {fifth_function, six_function, seven_function};
        default: return {default_function};
    }
}

/*
 * Complete the 'solve_by_fixed_point_iterations' function below.
 *
 * The function is expected to return a DOUBLE_ARRAY.
 * The function accepts following parameters:
 *  1. INTEGER system_id
 *  2. INTEGER number_of_unknowns
 *  3. DOUBLE_ARRAY initial_approximations
 */