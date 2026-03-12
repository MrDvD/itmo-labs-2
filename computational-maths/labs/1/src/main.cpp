#include <fstream>
#include <cmath>

#include <lib/lagrange.h>
#include <lib/test.h>

int main() {
  std::ofstream csv_file("interpolation_results.csv");

  csv_file << "f_id,a,b,x,y_interp,y_actual,y_noise,residual,n\n";

  std::vector<test_case> cases = generate_tests(0.3);
  for (int i = 0; i < 1; i++) {
    test_case c = cases[i];
    std::function<double(double)> func = get_function(c.function_number);
    if (!c.calc) {
      csv_file << c.function_number << "," 
              << std::nan << "," 
              << std::nan << "," 
              << c.x << "," 
              << std::nan << "," 
              << func(c.x) << "," 
              << std::nan << ","
              << std::nan << "\n";
      continue;
    }
    debug_result debug = interpolate_by_lagrange(c.function_number, c.a, c.b, c.x);
    double y_actual = func(c.x);
    double error = y_actual - debug.result;
    csv_file << c.function_number << "," 
             << c.a << "," 
             << c.b << "," 
             << c.x << "," 
             << debug.result << "," 
             << y_actual << "," 
             << error << ","
             << debug.end_iteration << "\n";
  }

  csv_file.close();

  return 0;
}