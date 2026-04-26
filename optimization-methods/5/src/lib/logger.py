from typing import Protocol

class Logger(Protocol):
  def clean(self):
    ...

  def log(self, message: str):
    ...
  
  def mark_section(self, section_name: str):
    ...

class DefaultLogger:
  def __init__(self, log_file: str):
    self.log_file = log_file
  
  def clean(self):
    open(self.log_file, "w").close()

  def log(self, message: str):
    with open(self.log_file, "a") as f:
      f.write(f"{message}\n")
  
  def mark_section(self, section_name: str):
    self.log(f"\n## {section_name}")