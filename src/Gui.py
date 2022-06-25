import tkinter as tk
import File as fl


def init_window():
    WIDTH = 500
    HEIGHT = 500

    win = tk.Tk()

    x = int(win.winfo_screenwidth() / 2 - (WIDTH / 2))
    y = int(win.winfo_screenheight() / 2 - (HEIGHT / 2))

    win.title('EasyCrypto')
    win.geometry(str(WIDTH) + 'x' + str(HEIGHT) + '+' + str(x) + '+' + str(y))

    # TODO: add icon

    # functions

    def execute(is_encrypted, is_internal):
        file = fl.File('da_criptare', '.txt', 'D:\\richard\\programmazione\\python', is_encrypted, is_internal)
        print(file.is_encrypted)
        print(file.is_internal)

    # widgets

    button_font = ('Arial', 14)

    encrypt_but = tk.Button(win, text="Encrypt", font=button_font, command=lambda: execute(False, True))
    decrypt_but = tk.Button(win, text="Decrypt", font=button_font, command=lambda: execute(True, True))
    decrypt_external_file_but = tk.Button(win, text="Decrypt External file", font=button_font, command=lambda: execute(True, False))
    share_but = tk.Button(win, text="Share", font=button_font, command=lambda: execute(False, False))

    # placing

    encrypt_but.place(x=200, y=50)
    decrypt_but.place(x=200, y=150)
    decrypt_external_file_but.place(x=200, y=250)
    share_but.place(x=200, y=350)

    win.mainloop()
