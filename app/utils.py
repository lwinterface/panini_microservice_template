import os
import yaml

PATH = './config/' if 'HOSTNAME' in os.environ else '../config/'

def get_broker():
    broker_host = os.environ['BROKER_HOST'] if 'HOSTNAME' in os.environ and 'BROKER_HOST' in os.environ else '127.0.0.1'
    broker_port = os.environ['BROKER_PORT'] if 'BROKER_PORT' in os.environ else '4222'
    config_path = os.environ['CONFIG_PATH']
    return broker_host, broker_port, config_path

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
