import yaml
import os
from typing import Any, Dict

class ConfigLoadError(Exception):
  pass

def load(file_path: str = "config.yaml") -> Dict[str, Any]:
  if not os.path.exists(file_path):
    raise FileNotFoundError(f"Config file not found: {file_path}")

  try:
    with open(file_path, "r") as f:
      config = yaml.safe_load(f)
      if config is None:
        raise ConfigLoadError(f"Config file is empty: {file_path}")
      return {**config}
  except (yaml.YAMLError, IOError) as e:
    raise ConfigLoadError(f"Failed to load config: {e}")