import os
import configparser
import re

from show_message import show_message


class Config:
    def __init__(self, **kwargs):
        # получили имя конфига
        self.config_file_name = kwargs['config_file_name']
        # получили словарь для конфига
        self.config_file_dict = kwargs['config_file_dict']
        # получили список обязательных значений
        # self.config_file_required = kwargs['config_file_required']
        # сформировали команду для открытия файла конфига в блокноте
        self.osCommandString = f"notepad.exe {self.config_file_name}"
        self.config_file_dict_output = {}

    def config_file_open(self):
        os.system(self.osCommandString)

    def config_maker(self):
        try:
            self.config_obj = configparser.ConfigParser()
            self.config_obj['CONFIG'] = self.config_file_dict

            with open(self.config_file_name, 'w', encoding='utf-8') as f:
                self.config_obj.write(f)
            os.system(self.osCommandString)
            self.config_reader()

        except Exception as e:
            err = str(e)  # Получить текст исключения
            err_type = type(e)
            show_message(err_type, err, message_type='showerror')


    def config_reader(self):
        if os.path.isfile(self.config_file_name):
            try:
                config_obj = configparser.ConfigParser()
                config_obj.read(self.config_file_name, encoding="utf-8")
                section = config_obj.sections()[0]
                config_file_dict = config_obj[section]

                for key in config_file_dict:
                    if key not in self.config_file_dict or len(config_file_dict)< len(self.config_file_dict):
                        show_message('Ошибка!', f'Вы изменили имя поля!\nделаем заново..', timeout=None, message_type='showerror')
                        self.config_maker()
                        break

                for key, value in config_file_dict.items():
                    if not value:
                        show_message('Ошибка!', f'Поле < {key} > должно быть заполнено.', message_type='showerror')
                        os.system(self.osCommandString)
                        break

                    elif re.search('_int', key):
                        try:
                            self.config_file_dict_output[key] = config_obj.getint(section, key)
                        except Exception:
                            show_message('Ошибка!', f'Поле < {key} > должно быть целое число, а не <{value}>.', message_type='showerror')
                            os.system(self.osCommandString)
                            break
                    elif re.search('_bool', key):
                        try:
                            self.config_file_dict_output[key] = config_obj.getboolean(section, key)
                        except Exception:
                            show_message('Ошибка!', f'Поле < {key} > должно быть логическое значение, а не <{value}>.', message_type='showerror')
                            os.system(self.osCommandString)
                            break
                    else:
                        self.config_file_dict_output[key] = config_obj.get(section, key)
            except:
                show_message('Ошибка конфига!', f'Будем переделывать..',message_type='showerror')
                self.config_maker()
                # print(self.config_file_dict_output)  # Убрать потом!!!!!!!!!!!!
        else:
            self.config_maker()



if __name__ == '__main__':
    config_file_dict = {'gateway_host': '',
                        'timeout_int': 5,
                        'vpn_name': '',
                        'login': '',
                        'password': '',
                        'max_no_ping_attempts_int': 3,
                        'no_message_mode_bool': True,
                        'logging_mode_bool': True,
                        'file_log_mode': 'a',
                        'delay_int': 0,
                        }
    # config_file_list = ['gateway_host', 'timeout', 'vpn_name', 'login', 'password', 'max_connection_attempts']
    # config_file_required = {'timeout': '5', 'max_connection_attempts': '3'}
    config_file_name = 'reconnect_conf.ini'

    conf = Config(config_file_dict=config_file_dict, config_file_name=config_file_name)
    conf.config_reader()
    # conf.config_maker()
    print(conf.config_file_dict_output)


