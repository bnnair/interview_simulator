from pathlib import Path
from loguru import logger
import yaml
import os

class ConfigError(Exception):
    pass


class ConfigManager:
    
    @staticmethod
    def validate_yaml_file(yaml_path: Path) -> dict:
        try:
            with open(yaml_path, 'r') as stream:
                return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise ConfigError(f"Error reading file {yaml_path}: {exc}")
        except FileNotFoundError:
            raise ConfigError(f"File not found: {yaml_path}")
        
    @staticmethod
    def update_config() -> tuple:
        secrets_file = Path(__file__).resolve().parent.parent / 'models' / 'data' / 'secrets.yaml'
        # logger.debug(f"secrets_file : {secrets_file}")
        
        if not secrets_file.exists():
            raise FileNotFoundError(
                f"Secrets file not found: {secrets_file}")

        secrets = ConfigManager.validate_yaml_file(secrets_file)
        config_list = []

        for v in secrets['llm_model_type']:
            config = {}
            # logger.debug(f" model types : {v}")
            config.update({"name" : v.get("name")})
            config.update({"model_name" : v.get("model_name")})
            api_str = v.get("api_key_string")
            api_key = os.environ[api_str]
            # logger.debug(f"api_key : {api_key}")
            config.update({"api_key" : api_key})
            config_list.append(config)
            # logger.debug(f"model_name : {model_name}")
            # logger.debug(f"api_key_string : {api_str}")    
        logger.debug(f"config :{config_list}")    
        return config_list
