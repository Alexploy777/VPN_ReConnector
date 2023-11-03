import os
import time
import subprocess
from ping3 import ping

from config_read import Config
from show_message import show_message


class Reconnector:
    def __init__(self):
        super().__init__()
        conf = Config(config_file_list=config_file_list, config_file_name=config_file_name, config_file_required=config_file_required)
        conf.config_reader()

        self.gateway_host: str = conf.config_file_dict['gateway_host']
        self.timeout: int = int(conf.config_file_dict['timeout'])
        self.vpn_name: str = conf.config_file_dict['vpn_name']
        self.login: str = conf.config_file_dict['login']
        self.password: str = conf.config_file_dict['password']
        self.max_connection_attempts: int = int(conf.config_file_dict['max_connection_attempts'])

    def ping_gateway(self):
        try:
            response = ping(self.gateway_host)
            return response # is not False and response is not None
        except:
            print('Ошибка') # это принт !!!!!!!!!!!!!!!!!!!

    def connect_vpn(self):
        # Пример команды для подключения к VPN
        rasdial_path = os.path.normpath(os.getenv("windir") + '\\' + 'system32' + '\\' + 'rasdial.exe')
        command = f'{rasdial_path} {self.vpn_name} {self.login} {self.password}'
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='cp866')

        return result.stdout

    def main(self):
        connected_to_vpn = False

        max_connection_attempts = 3
        connection_attempts = 0

        while True:
            if ping_answer := self.ping_gateway():
                # Если есть пинг, продолжаем ждать
                print(f"Ping successful,time - {ping_answer}") # это принт !!!!!!!!!!!!!!!!!!!
                connected_to_vpn = False
            else:
                # Если пинг отсутствует, подключаемся к VPN (если ещё не подключены)
                if not connected_to_vpn:
                    print(f"No ping - {ping_answer}. Connecting to VPN...") # это принт !!!!!!!!!!!!!!!!!!!
                    result = self.connect_vpn()
                    if result == 0:
                        connected_to_vpn = True
                        print("Connecting to VPN") # это принт !!!!!!!!!!!!!!!!!!!
                    else:
                        title = "Проверьте корректность настроек!"
                        message = f'имя подключения - {self.vpn_name}\nлогин - {self.login}\nпароль - {self.password}\n{result}'
                        show_message(title=title, message=message, timeout=5)
                else:
                    print("Still no ping. Waiting...") # это принт !!!!!!!!!!!!!!!!!!!
                    connection_attempts += 1
                    if not connection_attempts < max_connection_attempts:
                        connected_to_vpn = False
                        connection_attempts = 0

            time.sleep(self.timeout)


if __name__ == '__main__':


    config_file_list = ['gateway_host',
                        'timeout', 'vpn_name',
                        'login', 'password',
                        'max_connection_attempts',
                        'no_message_mode'
                        ]
    config_file_required = {'timeout': '5',
                            'max_connection_attempts': '3',
                            'no_message_mode': 'True',
                            }
    config_file_name = 'reconnect_conf.ini'

    reconnect = Reconnector()
    reconnect.main()

    # conf = Config(config_file_list=config_file_list, config_file_name=config_file_name, config_file_required=config_file_required)
    # conf.config_reader()
    # print(conf.config_file_dict)

