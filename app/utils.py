import os
import yaml

from dotenv import load_dotenv

PATH = "./config/" if "HOSTNAME" in os.environ else "../config/"
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class Environment:
    @staticmethod
    def load(env_name: str = "dev"):
        if os.environ.get("HOSTNAME"):
            return
        _env_file_name = f".env.{env_name}"
        load_dotenv(os.path.join(BASE_DIR, "environments", _env_file_name))

    @staticmethod
    def get_environment_variable(*args, **kwargs):
        return os.environ.get(*args, **kwargs)

    @staticmethod
    def get_broker():
        return Environment.get_broker_host(), Environment.get_broker_port()

    @staticmethod
    def get_broker_host():
        return Environment.get_environment_variable("BROKER_HOST")

    @staticmethod
    def get_broker_port():
        return Environment.get_environment_variable("BROKER_PORT")

    @staticmethod
    def get_config_path():
        return Environment.get_environment_variable("CONFIG_PATH")

    @staticmethod
    def get_config(config, path=PATH, return_config_if_absent=None):
        if config is not None:
            path = os.path.join(path, config)
        try:
            with open(path, "r") as yaml_conf:
                yaml_config = yaml_conf.read()
                return yaml.load(yaml_config, Loader=yaml.FullLoader)
        except FileNotFoundError as e:
            if return_config_if_absent is not None:
                return return_config_if_absent
            raise Exception(e)
