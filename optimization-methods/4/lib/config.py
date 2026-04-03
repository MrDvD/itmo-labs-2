class Config:
  def __init__(self):
    self.precision = 4
    self.epsilon = 0.0001
    self.max_iterations = 100
    
    self.variant = 3
    
    self.func_a = 1.0
    self.func_b = 2.0
    self.func_c = 1.0
    self.func_d = -9.0
    self.func_e = -15.0
    self.func_f = 36.0
    
    self.initial_x = (-1.0, -2.0)
    
    self.gd_learning_rate = 0.5
    
    self.output_file = "report.tex"
    self.templates_dir = "templates"