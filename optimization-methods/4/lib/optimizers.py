from lib.math_utils import Vector

class Optimizer:
  def __init__(self, func, epsilon, max_iter):
    self.func = func
    self.epsilon = epsilon
    self.max_iter = max_iter
    
  def optimize(self, x0: Vector):
    raise NotImplementedError

class CyclicCoordinateDescent(Optimizer):
  def optimize(self, x0: Vector):
    history = []
    current_x = x0
    
    for k in range(1, self.max_iter + 1):
      prev_x = current_x
      
      step_x_dir = Vector(1.0, 0.0)
      alpha_1 = self.func.minimize_1d(current_x, step_x_dir)
      mid_x = current_x + step_x_dir * alpha_1
      
      step_y_dir = Vector(0.0, 1.0)
      alpha_2 = self.func.minimize_1d(mid_x, step_y_dir)
      current_x = mid_x + step_y_dir * alpha_2
      
      diff = (current_x - prev_x).norm()
      
      history.append({
        "k": k,
        "prev_x": prev_x,
        "alpha": Vector(alpha_1, alpha_2),
        "mid_x": mid_x,
        "new_x": current_x,
        "diff": diff
      })
      
      if diff < self.epsilon:
        break
    else:
      raise ValueError
        
    return history

class GradientDescent(Optimizer):
  def __init__(self, func, epsilon, max_iter, eta):
    super().__init__(func, epsilon, max_iter)
    self.eta = eta

  def optimize(self, x0: Vector):
    history = []
    current_x = x0
    
    for k in range(1, self.max_iter + 1):
      grad = self.func.gradient(current_x)
      grad_norm = grad.norm()
      
      prev_x = current_x
      current_x = current_x - grad * self.eta
      
      history.append({
        "k": k,
        "prev_x": prev_x,
        "grad": grad,
        "new_x": current_x,
        "grad_norm": grad_norm
      })
      
      if grad_norm < self.epsilon:
        break
    else:
      raise ValueError
        
    return history

class SteepestDescent(Optimizer):
  def optimize(self, x0: Vector):
    history = []
    current_x = x0
    
    for k in range(1, self.max_iter + 1):
      grad = self.func.gradient(current_x)
      grad_norm = grad.norm()
        
      u = grad.normalize() * (-1.0)
      beta = self.func.minimize_1d(current_x, u)
      
      prev_x = current_x
      current_x = current_x + u * beta
      
      history.append({
        "k": k,
        "prev_x": prev_x,
        "grad": grad,
        "u": u,
        "beta": beta,
        "new_x": current_x,
        "grad_norm": grad_norm
      })

      if grad_norm < self.epsilon:
        break
    else:
      raise ValueError
      
    return history