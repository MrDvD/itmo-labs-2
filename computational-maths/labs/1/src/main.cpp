#include <fstream>
#include <cmath>

#include <lib/lagrange.h>
#include <lib/test.h>

int main() {
  std::ofstream interpolation_file("pgf/interpolation_results.csv");
  std::ofstream plots_file("pgf/function_plots.csv");

  interpolation_file << "f_id,x,y,residual,n\n";
  plots_file << "f_id,x,y\n";

  std::vector<test_case> cases = generate_tests(0.3);
  int current_func_num = 0;
  for (std::size_t i = 0; i < cases.size(); i++) {
    test_case c = cases[i];
    if (c.function_number != current_func_num) {
      current_func_num = c.function_number;
    }
    std::function<double(double)> func = get_function(c.function_number);
    
    plots_file << c.function_number << "," 
               << c.x << "," 
               << func(c.x) << "\n";
    if (c.calc) {
      debug_result debug = interpolate_by_lagrange(c.function_number, c.a, c.b, c.x);
      double y_actual = func(c.x);
      double error = y_actual - debug.result;
      interpolation_file << c.function_number << ","
                         << c.x << ","
                         << debug.result << "," 
                         << error << ","
                         << debug.end_iteration << "\n";
    }
  }

  interpolation_file.close();
  plots_file.close();

  return 0;
}