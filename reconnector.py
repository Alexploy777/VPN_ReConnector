import os
import time
import subprocess

import tkinter
from tkinter import messagebox
from ping3 import ping
from dataclasses import dataclass
import configparser


class Config:
    config_file_name = 'reconnect_conf.ini'
    config_file_required_list = ['gateway_host', 'vpn_name', 'login', 'password']

    def __init__(self):
        self.config_obj = configparser.ConfigParser()
        self.osCommandString = f"notepad.exe {self.config_file_name}"

        root = tkinter.Tk()
        root.withdraw()  # эта функция скрывает основное окно программы, можете её убрать
        root.attributes("-topmost", True) # окна поверх других окон

    def check_config_file(self):
        if os.path.isfile(self.config_file_name):
            print('file is true') # это принт !!!!!!!!!!!!!!!!!!!
            self.config_reader()
        else:
            self.config_maker()
            print('file is false') # это принт !!!!!!!!!!!!!!!!!!!

    def config_reader(self):
        try:
            self.config_obj.read(self.config_file_name, encoding="utf-8")
            self.config_file_dict = {
            'gateway_host' : self.config_obj.get('DEFAULT', 'gateway_host'),
            'timeout' : int(self.config_obj.get('DEFAULT', 'timeout')),
            'vpn_name' : self.config_obj.get('DEFAULT', 'vpn_name'),
            'login' : self.config_obj.get('DEFAULT', 'login'),
            'password' : self.config_obj.get('DEFAULT', 'password'),
            'max_connection_attempts' : int(self.config_obj.get('DEFAULT', 'max_connection_attempts')),
            }

            for required_item in self.config_file_dict:
                if required_item in self.config_file_required_list and not self.config_file_dict[required_item]:
                    print(required_item, '=', self.config_file_dict[required_item]) # это принт !!!!!!!!!!!!!!!!!!!
                    messagebox.showerror("Ошибка", f"Заполните поле {required_item}")
                    os.system(self.osCommandString)
                    self.config_reader()
        except:
            self.config_maker()


    def config_maker(self):
        self.config_obj.read(self.config_file_name, encoding="utf-8")
        self.gateway_host = self.config_obj.set('DEFAULT', 'gateway_host', '')
        self.timeout = self.config_obj.set('DEFAULT', 'timeout', '5')
        self.vpn_name = self.config_obj.set('DEFAULT', 'vpn_name', '')
        self.login = self.config_obj.set('DEFAULT', 'login', '')
        self.password = self.config_obj.set('DEFAULT', 'password', '')
        self.max_connection_attempts = self.config_obj.set('DEFAULT', 'max_connection_attempts', '3')
        with open(self.config_file_name, 'w', encoding='utf-8') as f:
            self.config_obj.write(f)

        messagebox.showwarning("Предупреждение", "Заполните все поля!")
        os.system(self.osCommandString)
        self.config_reader()


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
        conf.check_config_file()

        self.gateway_host: str = conf.gateway_host
        self.timeout: int = conf.timeout
        self.vpn_name: str = conf.vpn_name
        self.login: str = conf.login
        self.password: str = conf.password
        self.max_connection_attempts: int = conf.max_connection_attempts

    def ping_gateway(self):
        try:
            response = ping(self.gateway_host)
            return response is not None
        except:
            print('Ошибка') # это принт !!!!!!!!!!!!!!!!!!!

    def connect_vpn(self):
        # Пример команды для подключения к VPN
        rasdial_path = os.path.normpath(os.getenv("windir") + '\\' + 'system32' + '\\' + 'rasdial.exe')
        command = f'{rasdial_path} {self.vpn_name} {self.login} {self.password}'
        subprocess.run(command, shell=True, text=True, encoding='utf-8')

    def main(self):
        connected_to_vpn = False

        max_connection_attempts = 3
        connection_attempts = 0

        while True:
            if self.ping_gateway():
                # Если есть пинг, продолжаем ждать
                print("Ping successful") # это принт !!!!!!!!!!!!!!!!!!!
                connected_to_vpn = False
            else:
                # Если пинг отсутствует, подключаемся к VPN (если ещё не подключены)
                if not connected_to_vpn:
                    print("No ping. Connecting to VPN...") # это принт !!!!!!!!!!!!!!!!!!!
                    self.connect_vpn()
                    connected_to_vpn = True
                    print("Connecting to VPN") # это принт !!!!!!!!!!!!!!!!!!!
                else:
                    print("Still no ping. Waiting...") # это принт !!!!!!!!!!!!!!!!!!!
                    connection_attempts += 1
                    if not connection_attempts < max_connection_attempts:
                        connected_to_vpn = False
                        connection_attempts = 0

            time.sleep(self.timeout)


if __name__ == '__main__':
    gateway_host = "10.7.11.1"
    timeout = 5  # Интервал в секундах
    vpn_name = "deg"
    login = "solomon"
    password = "4ervjak0ed==23"
    max_connection_attempts = 3

    # reconnect = Reconnector()
    # reconnect.main()

    conf = Config()
    conf.check_config_file()

