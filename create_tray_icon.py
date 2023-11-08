from pystray import MenuItem as item
from pystray import Icon, Menu
from PIL import Image
import threading

from config_read import Config


class TrayIcon:
    def __init__(self, main_script):
        self.main_script = main_script
    def on_exit(self):
        self.icon.stop()
        self.main_script.stop()

    def on_config(self):
        self.icon.stop()
        self.main_script.open_config()


    def create_tray_icon(self):
        image = Image.open("al.ico")  # Замените "path_to_your_icon.png" на путь к вашей иконке
        menu = (
                item('Настройки', self.on_config),
                item('Выход', self.on_exit),
                )
        self.icon = Icon("name", image, "title", menu=Menu(*menu))
        return self.icon


    def run(self):
        tray_icon = self.create_tray_icon()
        tray_icon.run()


if __name__ == '__main__':
    # Создаем объект TrayIcon и передаем ссылку на основной скрипт
    tray_icon = TrayIcon(main_script=None)

    # Запускаем иконку в трее в отдельном потоке
    tray_thread = threading.Thread(target=tray_icon.run)
    tray_thread.start()
