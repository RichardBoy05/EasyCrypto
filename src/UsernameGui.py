import tkinter as tk
from tkinter import Label, Entry, Button
import FirebaseUtils
from os import getenv, remove
from os.path import join
from Alerts import username_already_exists_alert, username_does_not_exixst_alert

PATH = join(getenv('APPDATA'), 'EasyCrypto')


def ask_username(main_win, to_set):

    if to_set:
        win = tk.Tk()
    else:
        win = tk.Toplevel(main_win)
        win.grab_set()

    WIDTH = 185
    HEIGHT = 110

    WINDOW_ICON = tk.PhotoImage(file='res/logo.png', master=win)

    x = int(win.winfo_screenwidth() / 2 - (WIDTH / 2))
    y = int(win.winfo_screenheight() / 2 - (HEIGHT / 2))

    win.title('EasyCrypto')
    win.geometry(str(WIDTH) + 'x' + str(HEIGHT) + '+' + str(x) + '+' + str(y))
    win.resizable(0, 0)
    win.iconphoto(True, WINDOW_ICON)

    def_font = ('Arial Baltic', 10)

    # functions

    def execute():

        execute.username = user_entry.get()

        storage = FirebaseUtils.connect()
        if storage is None:
            return None

        FirebaseUtils.download(storage, 'users_list.txt', PATH, PATH + '\\users_list.txt')

        if to_set:
            while not FirebaseUtils.is_username_unique(PATH + '\\users_list.txt', execute.username):
                username_already_exists_alert(execute.username)
                return None
        else:
            while FirebaseUtils.is_username_unique(PATH + '\\users_list.txt', execute.username):
                username_does_not_exixst_alert(execute.username)
                return None

        if to_set:
            with open(PATH + '\\users_list.txt', 'a+') as file:

                file.seek(0)
                if len(file.read(1)) > 0:
                    file.write('\n')
                file.seek(0, 2)
                file.write(execute.username)

            FirebaseUtils.upload(storage, 'users_list.txt', PATH + '\\users_list.txt')

        remove(PATH + '\\users_list.txt')
        win.destroy()

    # widgets

    question_lab = Label(win, font=def_font)
    user_entry = Entry(win, font=def_font, relief='sunken')
    go_but = Button(win, text='Vai!', font=def_font, command=lambda: execute())

    # configuration and bindings

    if to_set:
        question_lab.config(text="Inserisci il tuo nome utente:")
    else:
        question_lab.config(text="Seleziona un utente:")

    # placing

    question_lab.place(x=20, y=10)
    user_entry.place(x=20, y=40)
    go_but.place(x=80, y=70)

    go_but.wait_window(win)

    try:
        return execute.username
    except AttributeError:
        return None
