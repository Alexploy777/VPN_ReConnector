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
        message_func(title, ' '.join(message.split()))
    else:
        raise ValueError(f"Неподдерживаемый тип сообщения: {message_type}")

if __name__ == '__main__':
    pass
