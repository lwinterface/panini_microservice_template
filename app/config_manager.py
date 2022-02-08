import os
import argparse
import re
import dacite
import yaml
from typing import Dict, List
from dataclasses import dataclass
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

@dataclass
class PaniniConfig:
    service_name: str
    nats_servers: List
    monitoring_servers: List
    infrastructure: Dict
    custom: Dict
    nats_client_name: str = None

    def __post_init__(self):
        for n in self.nats_servers:
            PaniniConfig.validate_nats_server(n)

    @staticmethod
    def validate_nats_server(nats_server):
        port = nats_server.split(':')[-1]
        if re.match(r"[a-zA-Z0-9]+", port) is None:
            raise Exception(f'Wrong port {port}, expected nats broker format: nats://<host>:<port>')


class Environment:
    @staticmethod
    def load(env_name: str = None):
        if env_name:
            _env_file_name = f".env.{env_name}"
        elif os.environ.get("HOSTNAME"):
            _env_file_name = f".env.container"
        else:
            _env_file_name = ".env"
        load_dotenv(os.path.join(BASE_DIR, "environments", _env_file_name))

    @staticmethod
    def get_environment_variable(*args, **kwargs):
        return os.environ.get(*args, **kwargs)

    @staticmethod
    def get_config_path():
        return Environment.get_environment_variable("CONFIG_PATH")

    @staticmethod
    def get_main_config():
        return Environment.get_environment_variable("MAIN_CONFIG_FILE")

    @staticmethod
    def get_nats_config():
        return Environment.get_environment_variable("NATS_CONFIG_FILE")

    @staticmethod
    def get_infrastructure_config():
        return Environment.get_environment_variable("INFRASTRUCTURE_CONFIG_FILE")

    @staticmethod
    def get_custom_config():
        return Environment.get_environment_variable("CUSTOM_CONFIG_FILE")


def get_panini_config(env: str = None) -> PaniniConfig:
    Environment.load(env)
    panini_config = {}
    absolute_path = os.getcwd()
    if absolute_path.endswith('/app'):
        absolute_path = absolute_path.replace('/app','')
    config_path = absolute_path + Environment.get_config_path()
    main_config_filename = config_path + Environment.get_main_config()
    with open(main_config_filename, 'r') as file:
        main_config = yaml.load(file, Loader=yaml.FullLoader)
        panini_config.update(main_config)
    nats_config_filename = config_path + Environment.get_nats_config()
    with open(nats_config_filename, 'r') as file:
        nats_config = yaml.load(file, Loader=yaml.FullLoader)
        panini_config.update(nats_config)
    infrastructure_config_filename = config_path + Environment.get_infrastructure_config()
    with open(infrastructure_config_filename, 'r') as file:
        infrastructure_config = yaml.load(file, Loader=yaml.FullLoader)
        panini_config['infrastructure'] = infrastructure_config
    custom_config_filename = config_path + Environment.get_custom_config()
    with open(custom_config_filename, 'r') as file:
        custom_config = yaml.load(file, Loader=yaml.FullLoader)
        panini_config['custom'] = custom_config
    nats_client_name = get_nats_client_name_from_args()
    if nats_client_name:
        panini_config['nats_client_name'] = nats_client_name
    united_config = dacite.from_dict(
        data_class=PaniniConfig,
        data=panini_config,
    )
    return united_config


def get_nats_client_name_from_args():
    parser = argparse.ArgumentParser(description='NATS client watchdog')
    parser.add_argument('--nats_client_name', type=str, default=None,
                        help='A required argument under --nats_client_name flag')
    args = parser.parse_args()
    if args.nats_client_name:
        return args.nats_client_name
