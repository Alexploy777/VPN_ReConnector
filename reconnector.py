import logging
import os
import subprocess
import sys
import threading
import time

from ping3 import ping

from config_read import Config
from create_tray_icon import TrayIcon
from show_message import show_message


class Reconnector:
    def __init__(self):
        super().__init__()
        self.conf = Config(config_file_list=config_file_list, config_file_name=config_file_name,
                           config_file_required=config_file_required)
        self.conf.config_reader()
        self.running = True
        try:
            self.gateway_host: str = self.conf.config_file_dict['gateway_host']
            self.timeout: int = int(self.conf.config_file_dict['timeout'])
            self.vpn_name: str = self.conf.config_file_dict['vpn_name']
            self.login: str = self.conf.config_file_dict['login']
            self.password: str = self.conf.config_file_dict['password']
            self.max_no_ping_attempts: int = int(self.conf.config_file_dict['max_no_ping_attempts'])
            self.no_message_mode: bool = False if self.conf.config_file_dict['no_message_mode'].lower() == 'false' else True
            self.logging_mode: bool = False if self.conf.config_file_dict['logging_mode'].lower() == 'false' else True
            self.file_log_mode: str = self.conf.config_file_dict['file_log_mode']
            self.delay : int = int(self.conf.config_file_dict['delay'])

            logging.basicConfig(level=logging.INFO, filename="reconnect_log.log", filemode=self.file_log_mode,
                                format="%(asctime)s %(levelname)s %(message)s", encoding='utf-8')


        except (ValueError, AttributeError) as e:
            if e == ValueError:
                sys.exit()
            else:
                message = str(e)
                show_message(title=type(e), message=message, message_type='showerror')
                self.conf.config_file_open()
                sys.exit()

        self.log('START')

        self.tray_icon = TrayIcon(main_script=self)
        self.tray_thread = threading.Thread(target=self.tray_icon.run)
        self.tray_thread.start()

        # except:
        #     print('exept')

    def stop(self):
        # print('stop!!!!')  # Убрать потом!!!!!!!!!!!!
        self.log('STOP')
        global running_main
        running_main = False
        self.running = False


    def open_config(self):
        self.log('Изменение конфига')
        self.conf.config_file_open()
        self.running = False


    def ping_gateway(self):
        try:
            response = ping(self.gateway_host)
            return response
        except:
            return None

    def connect_vpn(self):
        self.log('Начинаю подключение к VPN')
        # print('Начинаю подключение к VPN') # Убрать потом!!!!!!!!!!!!
        rasdial_path = os.path.normpath(os.getenv("windir") + '\\' + 'system32' + '\\' + 'rasdial.exe')
        command = f'{rasdial_path} {self.vpn_name} {self.login} {self.password}'
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='cp866')

        ansfer_code = result.returncode
        ansfer_text = result.stdout

        if ansfer_code == 0:
            self.flag_vpn_connected = True
            self.log('Подключение успешно')
        else:
            self.flag_vpn_connected = False

            title = "Проверьте корректность настроек!"
            message = f'имя подключения - {self.vpn_name}\nлогин - {self.login}\nпароль - {self.password}\n{ansfer_text}'
            if self.no_message_mode is False:
                show_message(title=title, message=message, timeout=5)
            self.log(message, mode='error')


    def disconnect_vpn(self):
        self.log('Начинаю отключение от VPN')
        # print('Начинаю отключение от VPN')  # Убрать потом!!!!!!!!!!!!
        rasdial_path = os.path.normpath(os.getenv("windir") + '\\' + 'system32' + '\\' + 'rasdial.exe')
        command = f'{rasdial_path} {self.vpn_name} /disconnect'
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='cp866')

        ansfer_code = result.returncode
        ansfer_text = result.stdout

        if ansfer_code == 0:
            self.flag_vpn_connected = False
            self.no_ping_counter = 0
            self.log('Отключение успешно')
        else:
            title = "Отключение не подтвердилось!"
            message = ansfer_text
            if self.no_message_mode is False:
                show_message(title=title, message=message, timeout=5)
            self.log(message, mode='error')

        time.sleep(self.timeout)

    def log(self, message, mode='info'):
        message = ' '.join(message.split())
        if self.logging_mode is True:
            if mode == 'info':
                logging.info(message)
            elif mode == 'warning':
                logging.warning(message)
            elif mode == 'error':
                logging.error(message)


    def start(self):
        if self.delay:
            time.sleep(self.delay)
        max_no_ping_attempts = 3
        self.no_ping_counter = 0
        self.flag_vpn_connected = False
        while True:
            if not self.running:
                break
            if self.ping_gateway():  # Пинг есть!
                print(f'Пинг есть! Задержка = {self.ping_gateway()}')  # Убрать потом!!!!!!!!!!!!
                self.no_ping_counter = 0 # счетчик отсутствия пинга
                ping_is_down = False # статус "падения" пинга

            elif self.no_ping_counter < max_no_ping_attempts:
                self.no_ping_counter += 1
                message = f'сообщение из < elif >, пинга не было {self.no_ping_counter} раз..'
                self.log(message)
                # print(message)  # Убрать потом!!!!!!!!!!!!
                ping_is_down = False


            else:
                self.no_ping_counter += 1
                message = f'сообщение из < else >, пинга не было {self.no_ping_counter} раз!!'
                self.log(message)
                # print(message)  # Убрать потом!!!!!!!!!!!!
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
                        'max_no_ping_attempts',
                        'no_message_mode',
                        'logging_mode',
                        'file_log_mode',
                        'delay',
                        ]
    config_file_required = {'timeout': '5',
                            'max_no_ping_attempts': '3',
                            'no_message_mode': 'True',
                            'logging_mode': 'True',
                            'file_log_mode': 'a',
                            'delay': '',
                            }
    config_file_name = 'reconnect_conf.ini'

    running_main = True


    def main():
        reconnect = Reconnector()
        reconnect.start()


    while running_main:
        main()
