from lib.config import Config
from lib.function import QuadraticFunction
from lib.math_utils import Vector
from lib.optimizers import CyclicCoordinateDescent, GradientDescent, SteepestDescent
from lib.renderer import ReportRenderer

def main():
  config = Config()
  
  func = QuadraticFunction(
    a=config.func_a, 
    b=config.func_b, 
    c=config.func_c, 
    d=config.func_d, 
    e=config.func_e,
    f=config.func_f
  )
  
  x0 = Vector(*config.initial_x)
  
  cyclic = CyclicCoordinateDescent(func, config.epsilon, config.max_iterations)
  cyclic_res = cyclic.optimize(x0)
  
  gd = GradientDescent(func, config.epsilon, config.max_iterations, config.gd_learning_rate)
  gd_res = gd.optimize(x0)
  
  steepest = SteepestDescent(func, config.epsilon, config.max_iterations)
  steepest_res = steepest.optimize(x0)
  
  renderer = ReportRenderer(config, func)
  
  renderer.render({
    "variant": config.variant,
    "epsilon": config.epsilon,
    "x0": x0,
    # "target_point": config.target_point,
    "cyclic_data": cyclic_res,
    "gd_data": gd_res,
    "gd_eta": config.gd_learning_rate,
    "steepest_data": steepest_res
  })

if __name__ == "__main__":
  main()