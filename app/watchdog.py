import time
import yaml
import requests
import argparse
from app.main import panini_config


class WatchDog:
    def __init__(self, nats_client_name: str, nats_monitoring_servers: list):
        self.nats_client_name = nats_client_name
        self.nats_monitoring_urls = [n+'/connz' for n in nats_monitoring_servers]

    def start_endless_watching(self):
        """ entrypoint to run endless checking """
        try:
            while True:
                self.check()
                time.sleep(1)
        except Exception as e:
            print(f"NATS client lost! Error: {str(e)}")
            exit(1)

    def start_one_time_check(self):
        """ entrypoint to run one time check """
        try:
            self.check()
            print('success!')
            exit()
        except Exception as e:
            print(str(e))
            exit(1)

    def check(self):
        nats_client_exist = self.find_nats_client()
        if not nats_client_exist:  # check it one more time to make sure
            time.sleep(1)
            assert self.find_nats_client(), "Can't find NATS client among given NATS brokers"  # raise Assertion Error if NATS client still absent


    def find_nats_client(self) -> bool:
        all_servers_result = [self.check_nats_client(monitoring_url) for monitoring_url in self.nats_monitoring_urls]
        if not True in all_servers_result:
            return False
        client_found_num = len([r for r in all_servers_result if r is True])
        if client_found_num > 1:
            print(f'Expected 1 nats client with name {self.nats_client_name} but got {client_found_num}')
            return False
        return True

    def check_nats_client(self, monitoring_url: str) -> bool:
        response = requests.get(monitoring_url)
        if not response.status_code == 200:
            raise Exception(f"Cannot check NATS server {monitoring_url} ; Error: {response.reason} {response.text}")
        all_clients_raw = response.json()
        all_clients = []
        for client in all_clients_raw["connections"]:
            all_clients.append(client["name"])
        if self.nats_client_name in all_clients:
            return True

    def get_monitoring_servers(self, nats_servers_path: str) -> list:
        with open(nats_servers_path, 'r') as file:
            nats_config = yaml.load(file, Loader=yaml.FullLoader)
        monitoring_server_urls = []
        for base_url in nats_config['monitoring_servers']:
            connz_url = self.make_connz_url(base_url)
            monitoring_server_urls.append(connz_url)
        return monitoring_server_urls

    def make_connz_url(self, base_url):
        if base_url[-1] == '/':
            base_url = base_url[:-1]
        return base_url + '/connz'


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='NATS client watchdog')
    parser.add_argument('--nats_client_name', type=str, required=False,
                        help='A required argument under --nats_client_name flag')
    args = parser.parse_args()
    print('starting..')
    watchdog = WatchDog(
        nats_client_name=args.nats_client_name,
        nats_monitoring_servers=panini_config.monitoring_servers
    )
    print('endless watching...')
    time.sleep(5)
    watchdog.start_endless_watching()

