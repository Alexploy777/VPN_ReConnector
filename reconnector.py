import os
import sys
import time
import subprocess

import tkinter
from tkinter import messagebox
from ping3 import ping


from config_read import Config


class Reconnector:
    # gateway_host: str
    # timeout: int
    # vpn_name: str
    # login: str
    # password: str
    # max_connection_attempts: int

    def __init__(self):
        super().__init__()
        conf = Config()
        conf.config_reader()

        self.gateway_host: str = conf.config_file_dict['gateway_host']
        self.timeout: int = conf.config_file_dict['timeout']
        self.vpn_name: str = conf.config_file_dict['vpn_name']
        self.login: str = conf.config_file_dict['login']
        self.password: str = conf.config_file_dict['password']
        self.max_connection_attempts: int = conf.config_file_dict['max_connection_attempts']

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

        # Изменяем кодировку вывода для PyCharm
        # sys.stdout.buffer.write(result.stdout.encode('utf-8'))
        # sys.stdout.flush()

        # return print(result.returncode)
        # return print(result.stdout)
        return result.stdout

    def show_message(self, title, message):
        root = tkinter.Tk()
        root.withdraw()  # эта функция скрывает основное окно программы, можете её убрать
        root.attributes("-topmost", True) # окна поверх других окон
        root.after(self.timeout*1000, root.destroy)
        messagebox.showwarning(title, message)


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
                        self.show_message(title=title, message=message)
                else:
                    print("Still no ping. Waiting...") # это принт !!!!!!!!!!!!!!!!!!!
                    connection_attempts += 1
                    if not connection_attempts < max_connection_attempts:
                        connected_to_vpn = False
                        connection_attempts = 0

            time.sleep(self.timeout)


if __name__ == '__main__':
    # gateway_host = "10.7.11.1"
    # timeout = 5  # Интервал в секундах
    # vpn_name = "deg"
    # login = "solomon"
    # password = "4ervjak0ed==23"
    # max_connection_attempts = 3

    # reconnect = Reconnector()
    # reconnect.main()
    #

    config_file_list = ['gateway_host', 'timeout', 'vpn_name', 'login', 'password', 'max_connection_attempts']
    config_file_required = {'timeout': '5', 'max_connection_attempts': '3'}
    config_file_name = 'reconnect_conf.ini'

    conf = Config(config_file_list=config_file_list, config_file_name=config_file_name, config_file_required=config_file_required)
    conf.config_reader()
    print(conf.config_file_dict)

