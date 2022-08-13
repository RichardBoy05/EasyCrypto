import tkinter as tk
from logger import Logger
from alerts import empty_box_alert, different_passwords_alert


def ask_password(main_win, to_encrypt, one_file):
    log = Logger(__name__).default()

    win = tk.Toplevel(main_win)
    win.grab_set()

    WIDTH = 265
    HEIGHT = 145

    WINDOW_ICON = tk.PhotoImage(file='resources/logo.png', master=win)
    PADLOCK_CLOSED = tk.PhotoImage(file='resources/padlock_closed.png', master=win)
    PADLOCK_CLOSED_HOVERED = tk.PhotoImage(file='resources/padlock_closed_hov.png', master=win)
    PADLOCK_OPENED = tk.PhotoImage(file='resources/padlock_opened.png', master=win)
    PADLOCK_OPENED_HOVERED = tk.PhotoImage(file='resources/padlock_opened_hov.png', master=win)
    SHOW = tk.PhotoImage(file='resources/show.png', master=win)
    HIDE = tk.PhotoImage(file='resources/hide.png', master=win)

    x = int(win.winfo_screenwidth() / 2 - (WIDTH / 2))
    y = int(win.winfo_screenheight() / 2 - (HEIGHT / 2))

    win.title('EasyCrypto')
    win.geometry(str(WIDTH) + 'x' + str(HEIGHT) + '+' + str(x) + '+' + str(y))
    win.resizable(False, False)
    win.iconphoto(True, WINDOW_ICON)

    def_font = ('Arial Baltic', 10)

    # functions

    def execute():

        execute.password = None

        if not pass_box.get():
            empty_box_alert(win, "Password")
            execute.password = None
            return

        if not confirmpass_box.get():
            empty_box_alert(win, "Conferma password")
            execute.password = None
            return

        if pass_box.get() != confirmpass_box.get():
            different_passwords_alert(win)
            execute.password = None
            return

        execute.password = pass_box.get()
        win.destroy()

    def switch_icons(button, entry):
        if button.cget('image') == str(SHOW):
            entry.config(show="")
            button.config(image=HIDE)
        elif button.cget('image') == str(HIDE):
            entry.config(show=u'\u2022')
            button.config(image=SHOW)

    # widgets

    check_var = tk.BooleanVar()

    pass_lab = tk.Label(win, font=def_font, text='Password: ')
    confirmpass_lab = tk.Label(win, font=def_font, text=' Conferma password: ')
    pass_box = tk.Entry(win, relief='sunken', show=u'\u2022')
    confirmpass_box = tk.Entry(win, relief='sunken', show=u'\u2022')
    keep_copy = tk.Checkbutton(win, font=def_font, variable=check_var)
    showhide_pass_lab = tk.Label(win, borderwidth=0, image=SHOW)
    showhide_confirmpass_lab = tk.Label(win, borderwidth=0, image=SHOW)
    protect_but = tk.Button(win, font=def_font, borderwidth=0, command=lambda: execute())

    # configuration and bindings

    showhide_pass_lab.bind("<Button-1>", lambda _: switch_icons(showhide_pass_lab, pass_box))
    showhide_confirmpass_lab.bind("<Button-1>", lambda _: switch_icons(showhide_confirmpass_lab, confirmpass_box))

    if to_encrypt:
        protect_but.config(image=PADLOCK_CLOSED)
        protect_but.bind("<Enter>", lambda _: protect_but.config(image=PADLOCK_CLOSED_HOVERED))
        protect_but.bind("<Leave>", lambda _: protect_but.config(image=PADLOCK_CLOSED))

    else:
        protect_but.config(image=PADLOCK_OPENED)
        protect_but.bind("<Enter>", lambda _: protect_but.config(image=PADLOCK_OPENED_HOVERED))
        protect_but.bind("<Leave>", lambda _: protect_but.config(image=PADLOCK_OPENED))

    if one_file:
        if to_encrypt:
            keep_copy.config(text='Conserva una copia del file originale')
            check_var.set(True)
        else:
            keep_copy.config(text='Conserva una copia del file criptato')
            check_var.set(False)
    else:
        if to_encrypt:
            keep_copy.config(text='Conserva una copia dei file originali')
            check_var.set(True)
        else:
            keep_copy.config(text='Conserva una copia dei file criptati')
            check_var.set(False)

    # placing

    pass_lab.place(x=12, y=10)
    pass_box.place(x=15, y=30)
    confirmpass_lab.place(x=8, y=60)
    confirmpass_box.place(x=15, y=80)
    keep_copy.place(x=9, y=110)
    showhide_pass_lab.place(x=148, y=32)
    showhide_confirmpass_lab.place(x=148, y=82)
    protect_but.place(x=177, y=5)

    protect_but.wait_window(win)

    try:
        return execute.password, check_var.get()
    except AttributeError:
        log.warning("AttributeError", exc_info=True)
        return None, check_var.get()
