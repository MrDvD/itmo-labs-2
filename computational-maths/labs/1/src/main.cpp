#include <bits/stdc++.h>

using namespace std;
using fn_t = double (double);

string ltrim(const string &);
string rtrim(const string &);
vector<string> split(const string &);


double weierstrass_function(double x){
    double f_x = 0;
    int n = 5;
    double b = 0.5;
    int a = 13;
    for(int i = 0; i < n; i++){
        f_x += pow(b, i) * cos(pow(a, n) * M_PI * x);
    }
    return f_x;
}

double gamma_function(double x){
    double tmp = (x - 0.5) * log(x + 4.5) - (x + 4.5);
    double ser = 1.0 +
            76.18009173   / (x + 0.0) -  86.50532033   / (x + 1.0) +
            24.01409822   / (x + 2.0) -  1.231739516   / (x + 3.0) +
            0.00120858003 / (x + 4.0) -  0.00000536382 / (x + 5.0);
    return exp(tmp + log(ser * sqrt(2 * M_PI)));
}

/*
* How to use this function:
*    fn_t& f = get_function(4);
*    f(0.0001);
*/
fn_t& get_function (int n)
{
  switch (n)
    {
    case 1:  return weierstrass_function;
    case 2:  return gamma_function;
    default: return gamma_function;
    }
}

/*
 * Complete the 'interpolate_by_lagrange' function below.
 *
 * The function is expected to return a DOUBLE.
 * The function accepts following parameters:
    *  1. INTEGER f
    *  2. DOUBLE a     
    *  3. DOUBLE b     
    *  4. DOUBLE x
 */

double interpolate_by_lagrange(int f, double a, double b, double x) {
  fn_t& func = get_function(f);
  
}