import os
import configparser
import tkinter
from tkinter import messagebox


def show_message(title, message, timeout=None, message_type='showwarning'):
    root = tkinter.Tk()
    root.withdraw()  # эта функция скрывает основное окно программы, можете её убрать
    root.attributes("-topmost", True)  # окна поверх других окон
    if timeout:
        root.after(timeout * 1000, root.destroy)
    message_types = {
        'showwarning': messagebox.showwarning,
        'showinfo': messagebox.showinfo,
        'showerror': messagebox.showerror,
    }
    message_func = message_types.get(message_type)
    if message_func:
        message_func(title, message)
    else:
        raise ValueError(f"Неподдерживаемый тип сообщения: {message_type}")

class Config:
    def __init__(self, **kwargs):
        self.config_file_name = kwargs['config_file_name']
        self.config_file_list = kwargs['config_file_list']
        self.config_file_required = kwargs['config_file_required']
        self.osCommandString = f"notepad.exe {self.config_file_name}"

    def config_maker(self):
        try:
            self.config_obj = configparser.ConfigParser()
            for item in self.config_file_list:
                value = ''
                if self.config_file_required and item in self.config_file_required:
                    value = self.config_file_required[item]
                self.config_obj.set('DEFAULT', item, value)
            with open(self.config_file_name, 'w', encoding='utf-8') as f:
                self.config_obj.write(f)
            os.system(self.osCommandString)
            self.config_reader()
        except Exception as e:
            err = str(e)  # Получить текст исключения
            err_type = type(e)
            show_message(err_type, err, message_type='showerror')
            self.config_maker()

    def config_reader(self):
        if os.path.isfile(self.config_file_name):
            try:
                self.config_obj = configparser.ConfigParser()
                self.config_obj.read(self.config_file_name, encoding="utf-8")
                config_file_dict = {}
                for item in self.config_file_list:
                    config_file_dict[item] = self.config_obj.get('DEFAULT', item)
                self.config_checker(config_file_dict)
            except:
                show_message('Ошибка!', 'Не меняйте название полей!\nделаем заново..', timeout=None, message_type='showerror')
                self.config_maker()
        else:
            self.config_maker()

    def config_checker(self, config_file_dict):
        self.flag = True
        for item in config_file_dict:
            if not config_file_dict[item]:
                self.flag = False
                show_message('Ошибка!', f'Поле < {item} > должно быть заполнено.', message_type='showerror')
                os.system(self.osCommandString)
                break
        if self.flag:
            self.config_file_dict = config_file_dict
        else:
            self.config_reader()

if __name__ == '__main__':
    config_file_list = ['gateway_host', 'timeout', 'vpn_name', 'login', 'password', 'max_connection_attempts']
    config_file_required = {'timeout': '5', 'max_connection_attempts': '3'}
    config_file_name = 'reconnect_conf.ini'
    # con_file_list = ['gateway_host', 'timeout', 'vpn_name', 'login', 'password', 'max_connection_attempts']
    # con_file_required = {}
    # con_file_name = 'reconnect_conf.ini'

    conf = Config(config_file_list=config_file_list, config_file_name=config_file_name, config_file_required=config_file_required)
    conf.config_reader()
    print(conf.config_file_dict)


