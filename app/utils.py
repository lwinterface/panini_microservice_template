import os
import yaml

from dotenv import load_dotenv

PATH = './config/' if 'HOSTNAME' in os.environ else '../config/'
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def load_env(is_test=False):
    if 'HOSTNAME' not in os.environ:
        if os.environ.get("PANINI_TEST_MODE") or is_test:
            load_dotenv(os.path.join(BASE_DIR, "environments", ".env.test"))
        else:
            load_dotenv(os.path.join(BASE_DIR, "environments", ".env.dev"))


def get_broker(is_test=False):
    load_env(is_test)
    broker_host = os.environ['BROKER_HOST']
    broker_port = os.environ['BROKER_PORT']
    return broker_host, broker_port


def get_config_path(is_test=False):
    load_env(is_test)
    return os.environ['CONFIG_PATH']


def get_config(config, path=PATH, return_config_if_upsent=None):
    if config is not None:
        path = path+config
    try:
        with open(path, 'r') as yaml_conf:
            yaml_config = yaml_conf.read()
            return yaml.load(yaml_config, Loader=yaml.FullLoader)
    except FileNotFoundError as e:
        if return_config_if_upsent is not None:
            return return_config_if_upsent
        raise Exception(e)
