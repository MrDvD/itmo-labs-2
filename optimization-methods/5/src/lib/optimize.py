import numpy as np
from scipy.optimize import minimize, OptimizeResult
from typing import List, Tuple, Optional, Protocol, runtime_checkable, Callable
from abc import ABC, abstractmethod

@runtime_checkable
class OptimizerProtocol(Protocol):
  loss_history: List[float]
  def loss_function(self, params: np.ndarray) -> float: ...
  def optimize(self, params_start: np.ndarray) -> List[float]: ...
  def get_model(self, params: np.ndarray) -> Callable[[np.ndarray, np.ndarray], np.ndarray]: ...

class BaseOptimizer(ABC):
  def __init__(self) -> None:
    self.loss_history: List[float] = []

  @abstractmethod
  def loss_function(self, params: np.ndarray) -> float:
    pass

  def _callback(self, x: np.ndarray) -> None:
    self.loss_history.append(self.loss_function(x))

  def get_residuals(self, x: np.ndarray) -> np.ndarray:
    targets = getattr(self, 'targets', getattr(self, 'y_targets', None))
    return targets.flatten() - self.predict(x).flatten()

  @abstractmethod
  def predict(self, params: np.ndarray, X: np.ndarray) -> np.ndarray:
    pass

  def get_model(self, params: np.ndarray) -> Callable[[np.ndarray, np.ndarray], np.ndarray]:
    def model(x_grid: np.ndarray, y_grid: np.ndarray) -> np.ndarray:
      original_shape = x_grid.shape
      points = np.column_stack([x_grid.ravel(), y_grid.ravel()])
      return self.predict(params, points).reshape(original_shape)
    return model

class GaussOptimizer(BaseOptimizer):
  def __init__(self, X_data: np.ndarray, targets: np.ndarray, bounds: Optional[List[Tuple[float, float]]]) -> None:
    super().__init__()
    self.X_data = X_data
    self.targets = targets
    self.bounds = bounds

  def predict(self, params: np.ndarray, X: np.ndarray) -> np.ndarray:
    A, cx, cy, sx, sy, theta, offset = params
    c, s = np.cos(theta), np.sin(theta)
    
    # Center the coordinates
    dx = X[:, 0] - cx
    dy = X[:, 1] - cy
    
    # Rotate and scale
    tx = (dx * c - dy * s) / sx
    ty = (dx * s + dy * c) / sy
    
    exponent = -0.5 * (tx**2 + ty**2)
    return A * np.exp(exponent) + offset

  def loss_function(self, params: np.ndarray) -> float:
    return float(np.mean((self.predict(params, self.X_data) - self.targets)**2))

  def optimize(self, params_start: np.ndarray, bounds: Optional[List[Tuple[float, float]]] = None) -> List[float]:
    self.loss_history = [self.loss_function(params_start)]
    return minimize(
      self.loss_function,
      params_start,
      method='L-BFGS-B',
      bounds=bounds,
      callback=self._callback
    ).x

class EllipticOptimizer(BaseOptimizer):
  def __init__(self, X_data: np.ndarray, targets: np.ndarray, bounds: Optional[List[Tuple[float, float]]]) -> None:
    super().__init__()
    self.X_data = X_data
    self.targets = targets
    self.bounds = bounds

  def predict(self, params: np.ndarray, X: np.ndarray) -> np.ndarray:
    x0, y0, z0, a, b, c = params[:6]
    dx, dy = X[:, 0] - x0, X[:, 1] - y0
    return a * dx**2 + b * dy**2 + c * dx * dy + z0

  def loss_function(self, params: np.ndarray) -> float:
    return float(np.mean((self.predict(params, self.X_data) - self.targets)**2))

  def optimize(self, params_start: np.ndarray) -> List[float]:
    self.loss_history = [self.loss_function(params_start)]
    return minimize(
      self.loss_function,
      params_start,
      method='L-BFGS-B',
      bounds=self.bounds,
      callback=self._callback
    ).x

class ConstantOptimizer(BaseOptimizer):
  def __init__(self, targets: np.ndarray, metric: str = 'MSE') -> None:
    super().__init__()
    self.targets = targets
    self.metric = metric.upper()

  def predict(self, params: np.ndarray, X: np.ndarray) -> np.ndarray:
    return np.full((len(X),), params[0])

  def loss_function(self, params: np.ndarray) -> float:
    val = params[0]
    if self.metric == 'MSE':
      return float(np.mean((self.targets - val)**2))
    return float(np.mean(np.abs(self.targets - val)))

  def get_model(self, params: np.ndarray) -> Callable[[np.ndarray, np.ndarray], np.ndarray]:
    def model(x_grid: np.ndarray, y_grid: np.ndarray) -> np.ndarray:
      return np.full(x_grid.shape, params[0])
    return model

  def optimize(self, params_start: np.ndarray) -> List[float]:
    self.loss_history = [self.loss_function(params_start)]
    if self.metric == 'MSE':
      avg_value = np.mean(self.targets)
      constant_params = np.zeros_like(params_start)
      constant_params[0] = avg_value
      
      return OptimizeResult(
        x=constant_params,
        fun=self.loss_function(constant_params),
        success=True,
        nit=0,
        nfev=1
      ).x
    median_value = np.median(self.targets)
    constant_params = np.zeros_like(params_start)
    constant_params[0] = median_value

    return OptimizeResult(
      x=constant_params,
      fun=self.loss_function(constant_params),
      success=True,
      nit=0,
      nfev=1
    ).x

class RBFOptimizer(BaseOptimizer):
  def __init__(self,
               X_data: np.ndarray,
               targets: np.ndarray,
               n_centers: int = 2,
               learning_rate: float = 0.2,
               n_iterations: int = 500) -> None:
    super().__init__()
    self.X_data = X_data
    self.targets = targets.flatten()
    self.n_centers = n_centers
    self.n_features = X_data.shape[1]
    
    self.w_len = n_centers + 1
    self.c_len = n_centers * self.n_features
    self.s_len = n_centers

    self.learning_rate = learning_rate
    self.n_iterations = n_iterations

  def _unpack_params(self, params: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    weights = params[:self.w_len]
    centers = params[self.w_len : self.w_len + self.c_len].reshape(self.n_centers, self.n_features)
    widths = params[self.w_len + self.c_len:]
    return weights, centers, widths

  def predict(self, params: np.ndarray, X: np.ndarray) -> np.ndarray:
    weights, centers, widths = self._unpack_params(params)
    n_samples = X.shape[0]

    hidden_output = np.zeros((n_samples, self.n_centers))
    for j in range(self.n_centers):
      dist_sq = np.sum((X - centers[j])**2, axis=1)
      hidden_output[:, j] = np.exp(-dist_sq / (2 * widths[j]**2 + 1e-12))

    phi_matrix = np.column_stack([np.ones(n_samples), hidden_output])

    return phi_matrix @ weights

  def loss_function(self, params: np.ndarray) -> float:
    predictions = self.predict(params, self.X_data)
    return float(np.mean((predictions - self.targets)**2))
  
  def _compute_gradients(self, params: np.ndarray) -> np.ndarray:
    weights, centers, widths = self._unpack_params(params)
    n_samples = self.X_data.shape[0]
    
    h_out = np.zeros((n_samples, self.n_centers))
    for j in range(self.n_centers):
      d_sq = np.sum((self.X_data - centers[j])**2, axis=1)
      h_out[:, j] = np.exp(-d_sq / (2 * widths[j]**2 + 1e-12))
    
    phi = np.column_stack([np.ones(n_samples), h_out])
    preds = phi @ weights
    err = preds - self.targets

    grad_w = (1.0 / n_samples) * (phi.T @ err)
    grad_c = np.zeros_like(centers)
    grad_s = np.zeros_like(widths)

    for j in range(self.n_centers):
      common = err * weights[j+1] * h_out[:, j]
      diff = self.X_data - centers[j]
      grad_c[j] = (1.0 / n_samples) * np.sum(common[:, np.newaxis] * (diff / (widths[j]**2 + 1e-12)), axis=0)
      
      dist_sq = np.sum(diff**2, axis=1)
      grad_s[j] = (1.0 / n_samples) * np.sum(common * (dist_sq / (widths[j]**3 + 1e-12)))

    return np.concatenate([grad_w, grad_c.flatten(), grad_s])
  
  def get_initial_params(self, random_state: int = 42) -> np.ndarray:
    np.random.seed(random_state)
    n_samples, _ = self.X_data.shape

    indices = np.random.choice(n_samples, self.n_centers, replace=False)
    centers = self.X_data[indices].copy()
    
    distances = np.zeros((n_samples, self.n_centers))
    for j in range(self.n_centers):
      distances[:, j] = np.sum((self.X_data - centers[j])**2, axis=1)
    labels = np.argmin(distances, axis=1)

    for _ in range(100):
      prev_centers = centers.copy()
      for j in range(self.n_centers):
        if np.sum(labels == j) > 0:
          centers[j] = np.mean(self.X_data[labels == j], axis=0)
      
      for j in range(self.n_centers):
        distances[:, j] = np.sum((self.X_data - centers[j])**2, axis=1)
      labels = np.argmin(distances, axis=1)

      if np.sum((centers - prev_centers)**2) < 1e-6:
        break

    widths = np.zeros(self.n_centers)
    for j in range(self.n_centers):
      dist_to_center = np.sqrt(np.sum((self.X_data - centers[j])**2, axis=1))
      if np.sum(labels == j) > 0:
        widths[j] = np.mean(dist_to_center[labels == j]) * 0.8
      else:
        widths[j] = np.mean(dist_to_center) * 0.5

    weights = np.random.randn(self.n_centers + 1) * 0.1
    return np.concatenate([weights, centers.flatten(), widths])

  def optimize(self, params_start: np.ndarray) -> List[float]:
    self.loss_history = [self.loss_function(params_start)]
    params = params_start.copy()
    
    for _ in range(self.n_iterations):
      grads = self._compute_gradients(params)
      params -= self.learning_rate * grads
      
      w_c_offset = self.w_len + self.c_len
      params[w_c_offset:] = np.maximum(params[w_c_offset:], 1e-3)
      self._callback(params)
    return params