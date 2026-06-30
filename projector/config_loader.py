import json
from pathlib import Path

class ConfigLoader:
    def load(self, config_path: str) -> dict:
        path = Path(config_path)
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        with open(path, "r", encoding="utf-8") as f:
            config = json.load(f)
        self.validate_config(config)
        return config

    def validate_config(self, config: dict):
        if "fields" not in config or not isinstance(config["fields"], list):
            raise ValueError("Config must contain a 'fields' list")
        for field in config["fields"]:
            if "path" not in field:
                raise ValueError("Every field in config must have a 'path'")
