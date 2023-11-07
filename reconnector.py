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
        # self.no_message_mode : str = conf.config_file_dict['no_message_mode']
        self.no_message_mode: bool = False if conf.config_file_dict['no_message_mode'].lower() == 'false' else True

    def ping_gateway(self):
        try:
            response = ping(self.gateway_host)
            return response
        except:
            return None

    def connect_vpn(self):
        print('Начинаю подключение к VPN') # Убрать потом!!!!!!!!!!!!
        rasdial_path = os.path.normpath(os.getenv("windir") + '\\' + 'system32' + '\\' + 'rasdial.exe')
        command = f'{rasdial_path} {self.vpn_name} {self.login} {self.password}'
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='cp866')

        ansfer_code = result.returncode
        ansfer_text = result.stdout

        if ansfer_code == 0:
            self.flag_vpn_connected = True
        else:
            self.flag_vpn_connected = False

            title = "Проверьте корректность настроек!"
            message = f'имя подключения - {self.vpn_name}\nлогин - {self.login}\nпароль - {self.password}\n{ansfer_text}'
            if self.no_message_mode is False:
                show_message(title=title, message=message, timeout=5)
            else:
                print(f'{title}\n{message}') # Убрать потом!!!!!!!!!!!!


    def disconnect_vpn(self):
        print('Начинаю отключение от VPN')  # Убрать потом!!!!!!!!!!!!
        rasdial_path = os.path.normpath(os.getenv("windir") + '\\' + 'system32' + '\\' + 'rasdial.exe')
        command = f'{rasdial_path} {self.vpn_name} /disconnect'
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='cp866')

        ansfer_code = result.returncode
        ansfer_text = result.stdout

        if ansfer_code == 0:
            self.flag_vpn_connected = False
            self.no_ping_counter = 0
        else:
            title = "Отключение не подтвердилось!"
            message = ansfer_text
            if self.no_message_mode is False:
                show_message(title=title, message=message, timeout=5)
            else:
                print(f'{title}\n{message}') # Убрать потом!!!!!!!!!!!!

        time.sleep(self.timeout)


    def start(self):
        max_no_ping_attempts = 3
        self.no_ping_counter = 0
        self.flag_vpn_connected = False
        while True:
            if ping_answer := self.ping_gateway(): # Пинг есть!
                print(f'Пинг есть! Задержка = {ping_answer}') # Убрать потом!!!!!!!!!!!!
                self.no_ping_counter = 0 # счетчик отсутствия пинга
                ping_is_down = False # статус "падения" пинга

            elif self.no_ping_counter < max_no_ping_attempts:
                self.no_ping_counter += 1
                print(f'сообщение из < elif >, пинга не было {self.no_ping_counter} раз..')
                ping_is_down = False

            else:
                self.no_ping_counter += 1
                print(f'сообщение из < else >, пинга не было {self.no_ping_counter} раз!!')
                ping_is_down = True
                self.no_ping_counter = 0

            if not ping_is_down:
                time.sleep(self.timeout)
                continue
            elif not self.flag_vpn_connected:
                self.connect_vpn()
            else:
                self.disconnect_vpn()

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
    reconnect.start()

    # conf = Config(config_file_list=config_file_list, config_file_name=config_file_name, config_file_required=config_file_required)
    # conf.config_reader()
    # print(conf.config_file_dict)

