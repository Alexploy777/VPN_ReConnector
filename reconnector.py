import os
import re
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
        self.no_message_mode : str = conf.config_file_dict['no_message_mode']

    def ping_gateway(self):
        try:
            response = ping(self.gateway_host)
            # self.ping_status = True  # Есть пинг!
            # print(f'print(response) = {response}')
            return response # is not False and response is not None
        except:
            print('Ошибка', ) # это принт !!!!!!!!!!!!!!!!!!!

    def connect_vpn(self):
        # Пример команды для подключения к VPN
        rasdial_path = os.path.normpath(os.getenv("windir") + '\\' + 'system32' + '\\' + 'rasdial.exe')
        command = f'{rasdial_path} {self.vpn_name} {self.login} {self.password}'
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='cp866')

        # print(f'def connect_vpn -  {result.stdout}, {type(result.stdout)}')
        print(result.returncode, result.stdout)
        return result.returncode, result.stdout

    def disconnect_vpn(self):
        rasdial_path = os.path.normpath(os.getenv("windir") + '\\' + 'system32' + '\\' + 'rasdial.exe')
        command = f'{rasdial_path} {self.vpn_name} /disconnect'
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                encoding='cp866')

        # print(f'def disconnect_vpn -  {result.stdout}')
        # return print(result.stdout)
        print(f'отключаемся - {result.stdout}')
        time.sleep(self.timeout)
        self.no_ping_counter = 0
        self.flag_vpn_connected = False

        # return result.stdout


    def start(self):
        self.flag_vpn_connected = False
        flag_ping_down = False
        max_no_ping_attempts = 3
        self.no_ping_counter = 0
        max_connection_attempts = 3
        connection_attempts_counter = 0
        pattern = r'\d{3}'

        while True:
            if self.ping_gateway() is not None:
                print(f'no_ping_counter if = {self.no_ping_counter}, {self.ping_gateway()}')
                self.no_ping_counter = 0
                ping_is_down = False
                self.flag_vpn_connected = True
            elif self.no_ping_counter < max_no_ping_attempts:
                print(f'no_ping_counter elif = {self.no_ping_counter}')
                self.no_ping_counter += 1
                ping_is_down = False
            else:
                print(f'no_ping_counter else = {self.no_ping_counter}')
                self.no_ping_counter += 1
                ping_is_down = True
                self.flag_vpn_connected = False

            if ping_is_down and self.flag_vpn_connected is False:
                print('Начинаем подключаться к VPN')
                vpn_connect_code = self.connect_vpn()[0]
                vpn_connect_status = self.connect_vpn()[1]
                print(f'vpn_connect_status = {vpn_connect_status}, {type(vpn_connect_status)}')
                if vpn_connect_code == 0:
                    self.flag_vpn_connected = True
                    print("flag_vpn_connected = True")  # это принт !!!!!!!!!!!!!!!!!!!

                else:
                    self.flag_vpn_connected = False
                    title = "Проверьте корректность настроек!"
                    message = f'имя подключения - {self.vpn_name}\nлогин - {self.login}\nпароль - {self.password}\n{vpn_connect_status}'
                    if self.no_message_mode == "False":
                        show_message(title=title, message=message, timeout=5)
                    else:
                        print(message)

            elif ping_is_down and self.flag_vpn_connected is True:
                    self.disconnect_vpn()


            time.sleep(self.timeout)



    # def main(self):
    #     connected_to_vpn = False
    #
    #     max_connection_attempts = 3
    #     connection_attempts = 0
    #
    #     while True:
    #         if ping_answer := self.ping_gateway():
    #             # Если есть пинг, продолжаем ждать
    #             print(f"Ping successful,time - {ping_answer}") # это принт !!!!!!!!!!!!!!!!!!!
    #             connected_to_vpn = False
    #         else:
    #             # Если пинг отсутствует, подключаемся к VPN (если ещё не подключены)
    #             if not connected_to_vpn:
    #                 print(f"No ping - {ping_answer}. Connecting to VPN...") # это принт !!!!!!!!!!!!!!!!!!!
    #                 result = self.connect_vpn()
    #                 if result == 0:
    #                     connected_to_vpn = True
    #                     print("Connecting to VPN") # это принт !!!!!!!!!!!!!!!!!!!
    #                 else:
    #                     title = "Проверьте корректность настроек!"
    #                     message = f'имя подключения - {self.vpn_name}\nлогин - {self.login}\nпароль - {self.password}\n{result}'
    #                     show_message(title=title, message=message, timeout=5)
    #             else:
    #                 print("Still no ping. Waiting...") # это принт !!!!!!!!!!!!!!!!!!!
    #                 connection_attempts += 1
    #                 if not connection_attempts < max_connection_attempts:
    #                     connected_to_vpn = False
    #                     connection_attempts = 0
    #
    #         time.sleep(self.timeout)


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
    # reconnect.main()
    reconnect.start()

    # conf = Config(config_file_list=config_file_list, config_file_name=config_file_name, config_file_required=config_file_required)
    # conf.config_reader()
    # print(conf.config_file_dict)

