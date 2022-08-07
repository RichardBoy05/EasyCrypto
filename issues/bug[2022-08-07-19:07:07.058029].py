import os
import web
import tkinter as tk
from logger import Logger
from user_utils import Username

PATH = os.path.join(os.getenv('APPDATA'), 'EasyCrypto')
CRYPT_PATH = os.path.join(PATH, 'crypt')
USERS_LIST = os.path.join(PATH, 'users_list.txt')


def set_username():
    log = Logger(__name__).default()

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
    win.resizable(False, False)
    win.iconphoto(True, WINDOW_ICON)

    def_font = ('Arial Baltic', 14)
    content = tk.StringVar()

    # functions

    storage = Username(win).get_users_list()

    if storage is None:
        return None

    def readme_redirect():
        x_coord = win.winfo_pointerx() - win.winfo_rootx()
        y_coord = win.winfo_pointery() - win.winfo_rooty()

        if 164 < x_coord < 282 and 301 < y_coord < 318:
            web.Browser('https://github.com/RichardBoy05/EasyCrypto/blob/main/README.md').search()

    # widgets

    background_canv = tk.Canvas(win, width=475, height=325)
    background_canv.create_image(239, 164, image=BACKGROUND_IMAGE)
    canva_id = background_canv.create_text(30, 202, text='Nickname troppo corto!', fill='red', anchor='w')
    user_entry = tk.Entry(win, width=19, font=def_font, relief='groove', textvariable=content)
    go_but = tk.Button(win, image=GO_IMAGE, borderwidth=0, bg='#160ca3',
                       command=lambda: Username(win).execute(win, content, True, background_canv, canva_id))
    # configuration and bindings

    background_canv.bind('<Button-1>', lambda _: readme_redirect())
    go_but.bind("<Enter>", lambda _: go_but.config(image=GO_IMAGE_HOVERED))
    go_but.bind("<Leave>", lambda _: go_but.config(image=GO_IMAGE))
    content.trace_add('write', lambda _, __, ___: Username.check_username(content.get(), True, background_canv, canva_id))
    user_entry.focus()

    # placing

    background_canv.place(x=-2, y=-2)
    user_entry.place(x=29, y=163)
    go_but.place(x=84, y=220)

    go_but.wait_window(win)

    try:
        if os.path.exists(USERS_LIST):
            os.remove(USERS_LIST)
    except PermissionError:
        log.warning("PermissionError", exc_info=True)

    try:
        return win, Username(win).username
    except AttributeError:
        log.warning("AttributeError", exc_info=True)
        return None
