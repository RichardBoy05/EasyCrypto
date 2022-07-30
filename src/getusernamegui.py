import os
import tkinter as tk
from logger import Logger
from user_utils import Username

PATH = os.path.join(os.getenv('APPDATA'), 'EasyCrypto')
USERS_LIST = os.path.join(PATH, 'users_list.txt')


def get_username(main_win):
    log = Logger(__name__).default()

    win = tk.Toplevel(main_win)
    win.grab_set()

    WIDTH = 425
    HEIGHT = 200

    WINDOW_ICON = tk.PhotoImage(file='res/logo.png', master=win)
    BACKGROUND_IMAGE = tk.PhotoImage(file='res/get_username_background.png', master=win)
    GO_IMAGE = tk.PhotoImage(file='res/set_username_but.png', master=win)
    GO_IMAGE_HOVERED = tk.PhotoImage(file='res/set_username_but_hovered.png', master=win)

    x = int(win.winfo_screenwidth() / 2 - (WIDTH / 2))
    y = int(win.winfo_screenheight() / 2 - (HEIGHT / 2))

    win.title('EasyCrypto')
    win.geometry(str(WIDTH) + 'x' + str(HEIGHT) + '+' + str(x) + '+' + str(y))
    win.resizable(False, False)
    win.iconphoto(True, WINDOW_ICON)
    win.protocol("WM_DELETE_WINDOW", lambda: correct_closing(win))

    data = tk.StringVar()
    def_font = ('Arial Baltic', 16)

    # functions

    storage = Username.get_users_list()

    if storage is None:
        win.destroy()
        return None

    # widgets

    background_canv = tk.Canvas(win, width=425, height=200)
    background_canv.create_image(214, 102, image=BACKGROUND_IMAGE)
    canva_id = background_canv.create_text(30, 158, text='Nickname troppo corto!', fill='red', anchor='w')
    username_entry = tk.Entry(win, width=19, font=def_font, relief='ridge', bd=2, textvariable=data)
    go_but = tk.Button(win, image=GO_IMAGE, borderwidth=0, bg='#160ca3',
                       command=lambda: Username.execute(win, data, False, background_canv, canva_id))

    # configuration and bindings

    go_but.bind("<Enter>", lambda _: go_but.config(image=GO_IMAGE_HOVERED))
    go_but.bind("<Leave>", lambda _: go_but.config(image=GO_IMAGE))
    data.trace_add('write',
                   lambda _, __, ___: Username.check_username(username_entry.get(), False, background_canv, canva_id))
    username_entry.focus()

    # placing

    background_canv.place(x=-2, y=-2)
    username_entry.place(x=27, y=115)
    go_but.place(x=291, y=109)

    go_but.wait_window(win)

    if os.path.exists(USERS_LIST):
        os.remove(USERS_LIST)

    try:
        return Username.username
    except AttributeError:
        log.warning("AttributeError", exc_info=True)
        return None


def correct_closing(win):
    Username.username = None
    win.destroy()
