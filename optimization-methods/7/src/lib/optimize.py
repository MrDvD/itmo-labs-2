import numpy as np
import torch
from typing import List, Tuple, Protocol, runtime_checkable
from numpy.typing import NDArray
from abc import ABC

@runtime_checkable
class OptimizerProtocol(Protocol):
  iter_history: List[Tuple[float, float]]
  def optimize(self, params_start: Tuple[float, float]) -> List[float]: ...

class BaseOptimizer(ABC):
  def __init__(self) -> None:
    self.iter_history: List[Tuple[float, float]] = list()

  def _callback(self, x: Tuple[float, float]) -> None:
    self.iter_history.append(x)

class GradientDescentOptimizer(BaseOptimizer):
  def __init__(self, learning_rate: float, max_iter: int, eps: float) -> None:
    super().__init__()
    self.learning_rate = learning_rate
    self.max_iter = max_iter
    self.eps = eps
  
  def _get_gradient(self, params: NDArray[np.float32]) -> np.ndarray:
    x, y = params[0], params[1]
    df_dx = 10**-2 * (16 * x + 2 * y + 43)
    df_dy = 10**-2 * (2 * x + 10)
    return np.array([df_dx, df_dy], dtype=float)

  def optimize(self, params_start: Tuple[float, float]) -> List[Tuple[float, float]]:
    params = np.array(params_start, dtype=float)
    self.iter_history = [tuple(params)]
    for _ in range(self.max_iter):
      grad = self._get_gradient(params)
      if np.linalg.norm(grad) < self.eps:
        break
      next_params = params - self.learning_rate * grad
      self._callback(tuple(next_params))
      if np.linalg.norm(next_params - params) < self.eps:
        params = next_params
        break
      params = next_params
    return self.iter_history

class OurAdamOptimizer(BaseOptimizer):
  def __init__(self, learning_rate: float, max_iter: int, eps: float) -> None:
    super().__init__()
    self.learning_rate = learning_rate
    self.max_iter = max_iter
    self.eps = eps
  
  def _get_gradient(self, x: float, y: float) -> NDArray[np.float32]:
    df_dx = 10**-2 * (16 * x + 2 * y + 43)
    df_dy = 10**-2 * (2 * x + 10)
    return np.array([df_dx, df_dy], dtype=float)

  def optimize(self, params_start: NDArray[np.float32]) -> List[Tuple[float, float]]:
    x0, y0, beta1, beta2 = params_start
    params = np.array([x0, y0])
    self.iter_history = [(x0, y0)]
    velocity = 0.0
    mass = 0.0
    for t in range(1, self.max_iter + 1):
      grad = self._get_gradient(*self.iter_history[-1])
      if np.linalg.norm(grad) < self.eps:
        break
      mass = beta1 * mass + (1 - beta1) * grad
      velocity: float = beta2 * velocity + (1 - beta2) * grad ** 2
      next_params = params - self.learning_rate / np.sqrt(velocity / (1.0 - beta1 ** t)) * mass / (1 - beta1 ** t)
      self._callback(tuple(next_params))
      if np.linalg.norm(next_params - params) < self.eps:
        params = next_params
        break
      params = next_params
    return self.iter_history

class PyTorchAdamOptimizer(BaseOptimizer):
  def __init__(self, learning_rate: float, max_iter: int, eps: float) -> None:
    super().__init__()
    self.learning_rate = learning_rate
    self.max_iter = max_iter
    self.eps = eps

  def optimize(self, params_start: NDArray[np.float32]) -> List[Tuple[float, float]]:
    x0, y0, beta1, beta2 = params_start
    params_tensor = torch.tensor([x0, y0], dtype=torch.float64, requires_grad=True)
    optimizer = torch.optim.Adam(
      [params_tensor], 
      lr=self.learning_rate, 
      betas=(beta1, beta2), 
      eps=1e-8
    )
    self.iter_history = [(float(params_tensor[0]), float(params_tensor[1]))]
    for t in range(1, self.max_iter + 1):
      optimizer.zero_grad()
      x = params_tensor[0]
      y = params_tensor[1]
      loss = 10 ** (-2) * (8 * x ** 2 + 2 * x * y + 43 * x + 10 * y + 15)
      loss.backward()
      grad_norm = torch.linalg.norm(params_tensor.grad).item()
      if grad_norm < self.eps:
        break
      old_params = params_tensor.clone().detach()
      optimizer.step()
      current_position = (float(params_tensor[0]), float(params_tensor[1]))
      self._callback(current_position)
      if torch.linalg.norm(params_tensor - old_params).item() < self.eps:
        break
    return self.iter_history