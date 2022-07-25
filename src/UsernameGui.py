import tkinter as tk
import winsound
import os
import FirebaseUtils as Fb
from Links import search_info

PATH = os.path.join(os.getenv('APPDATA'), 'EasyCrypto')


def ask_username(main_win, to_set):
    if to_set:
        return set_username()
    else:
        return get_username(main_win)


def set_username():
    win = tk.Tk()
    WIDTH = 475
    HEIGHT = 325

    WINDOW_ICON = tk.PhotoImage(file='res/logo.png', master=win)
    BACKGROUND_IMAGE = tk.PhotoImage(file='res/set_username_background.png', master=win)
    GO_IMAGE = tk.PhotoImage(file='res/set_username_but.png', master=win)
    GO_IMAGE_HOVERED = tk.PhotoImage(file='res/set_username_but_hovered.png', master=win)

    x = int(win.winfo_screenwidth() / 2 - (WIDTH / 2))
    y = int(win.winfo_screenheight() / 2 - (HEIGHT / 2))

    win.title('EasyCrypto')
    win.geometry(str(WIDTH) + 'x' + str(HEIGHT) + '+' + str(x) + '+' + str(y))
    win.resizable(0, 0)
    win.iconphoto(True, WINDOW_ICON)

    def_font = ('Arial Baltic', 14)
    data = tk.StringVar()

    # functions

    storage = Fb.connect()
    if storage is None:
        return None
    filepath = PATH + '\\users_list.txt'
    Fb.download(storage, 'users_list.txt', PATH, filepath)

    def readme_redirect():
        x_coord = win.winfo_pointerx() - win.winfo_rootx()
        y_coord = win.winfo_pointery() - win.winfo_rooty()

        if 164 < x_coord < 282 and 301 < y_coord < 318:
            search_info()

    # widgets

    background_canv = tk.Canvas(win, width=475, height=325)
    background_canv.create_image(239, 164, image=BACKGROUND_IMAGE)
    canva_id = background_canv.create_text(30, 202, text='Nickname troppo corto!', fill='red', anchor='w')
    user_entry = tk.Entry(win, width=19, font=def_font, relief='groove', textvariable=data)
    go_but = tk.Button(win, image=GO_IMAGE, borderwidth=0, bg='#160ca3',
                       command=lambda: execute(win, storage, user_entry.get(), True, background_canv, canva_id))

    # configuration and bindings

    background_canv.bind('<Button-1>', lambda _: readme_redirect())
    go_but.bind("<Enter>", lambda _: go_but.config(image=GO_IMAGE_HOVERED))
    go_but.bind("<Leave>", lambda _: go_but.config(image=GO_IMAGE))
    data.trace_add('write', lambda _, __, ___: check_username(data.get(), True, background_canv, canva_id))
    user_entry.focus()

    # placing

    background_canv.place(x=-2, y=-2)
    user_entry.place(x=29, y=163)
    go_but.place(x=84, y=220)

    go_but.wait_window(win)
    os.remove(filepath)

    try:
        return execute.username
    except AttributeError:
        return None


def get_username(main_win):
    # win = tk.Toplevel(main_win)
    # win.grab_set()

    win = tk.Tk()

    WIDTH = 475
    HEIGHT = 325

    WINDOW_ICON = tk.PhotoImage(file='res/logo.png', master=win)
    BACKGROUND_IMAGE = tk.PhotoImage(file='res/set_username_background.png', master=win)
    GO_IMAGE = tk.PhotoImage(file='res/set_username_but.png', master=win)
    GO_IMAGE_HOVERED = tk.PhotoImage(file='res/set_username_but_hovered.png', master=win)

    x = int(win.winfo_screenwidth() / 2 - (WIDTH / 2))
    y = int(win.winfo_screenheight() / 2 - (HEIGHT / 2))

    win.title('EasyCrypto')
    win.geometry(str(WIDTH) + 'x' + str(HEIGHT) + '+' + str(x) + '+' + str(y))
    win.resizable(0, 0)
    win.iconphoto(True, WINDOW_ICON)

    win.mainloop()


def execute(win, storage, nickname, to_set, background_canva, canva_id):

    if background_canva.itemcget(canva_id, 'text') != 'Nickname valido!':
        winsound.PlaySound('SystemHand', winsound.SND_ASYNC)
        return

    execute.username = nickname
    filepath = PATH + '\\users_list.txt'

    if to_set:
        with open(filepath, 'a+') as file:

            file.seek(0)
            if len(file.read(1)) > 0:
                file.write('\n')
            file.seek(0, 2)
            file.write(execute.username)

        Fb.upload(storage, 'users_list.txt', filepath)

    win.destroy()


def check_username(username, to_set, canva, canva_id):

    if len(username) < 3:
        canva.itemconfig(canva_id, text='Nickname troppo corto!', fill='red')
        return

    if len(username) > 40:
        canva.itemconfig(canva_id, text='Nickname troppo lungo!', fill='red')
        return

    invalid_characters = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']

    for i in username:
        if i in invalid_characters:
            canva.itemconfig(canva_id, text='Il carattere ' + i + ' non è utilizzabile!', fill='red')
            return

    filepath = PATH + '\\users_list.txt'

    if to_set:
        if not Fb.is_username_unique(filepath, username):
            canva.itemconfig(canva_id, text='Nickname già esistente!', fill='red')
            return
    else:
        if Fb.is_username_unique(filepath, username):
            canva.itemconfig(canva_id, text='Questo utente non esiste!', fill='red')
            return

    canva.itemconfig(canva_id, text='Nickname valido!', fill='green')
