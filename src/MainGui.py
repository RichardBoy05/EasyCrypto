import os.path

import web
import alerts
import tkinter as tk
import local_crypter as lc
import passwordgui as pwgui
from rsa_utils import Share
import rsa_encryption as rsa
from tkinter import filedialog
from getusernamegui import get_username


def init():
    win = tk.Tk()

    WIDTH = 450
    HEIGHT = 450

    WINDOW_ICON = tk.PhotoImage(file='res/logo.png', master=win)
    BACKGROUND_IMAGE = tk.PhotoImage(file='res/background.png', master=win)
    CRYPT_IMAGE = tk.PhotoImage(file='res/crypt.png', master=win)
    CRYPT_IMAGE_HOVERED = tk.PhotoImage(file='res/crypt_hovered.png', master=win)
    DECRYPT_IMAGE = tk.PhotoImage(file='res/decrypt.png', master=win)
    DECRYPT_IMAGE_HOVERED = tk.PhotoImage(file='res/decrypt_hovered.png', master=win)
    SHARE_IMAGE = tk.PhotoImage(file='res/share.png', master=win)
    SHARE_IMAGE_HOVERED = tk.PhotoImage(file='res/share_hovered.png', master=win)
    DECRYPT_EXTERNAL_FILE_IMAGE = tk.PhotoImage(file='res/decrypt_external_file.png', master=win)
    DECRYPT_EXTERNAL_FILE_IMAGE_HOVERED = tk.PhotoImage(file='res/decrypt_external_file_hovered.png', master=win)
    INFO_IMAGE = tk.PhotoImage(file='res/info.png', master=win)
    INFO_IMAGE_HOVERED = tk.PhotoImage(file='res/info_hovered.png', master=win)
    GITHUB_IMAGE = tk.PhotoImage(file='res/github.png', master=win)
    GITHUB_IMAGE_HOVERED = tk.PhotoImage(file='res/github_hovered.png', master=win)
    SETTINGS_IMAGE = tk.PhotoImage(file='res/settings.png', master=win)
    SETTINGS_IMAGE_HOVERED = tk.PhotoImage(file='res/settings_hovered.png', master=win)

    x = int(win.winfo_screenwidth() / 2 - (WIDTH / 2))
    y = int(win.winfo_screenheight() / 2 - (HEIGHT / 2))

    win.title('EasyCrypto')
    win.geometry(str(WIDTH) + 'x' + str(HEIGHT) + '+' + str(x) + '+' + str(y))
    win.resizable(False, False)
    win.iconphoto(True, WINDOW_ICON)
    win.protocol("WM_DELETE_WINDOW", lambda: correct_closing(win))

    # functions

    def execute(is_encrypted, is_internal):

        files = [('Tutti i file', '*.*')]
        path = tk.filedialog.askopenfilenames(title='Seleziona uno o più file...', filetypes=files)

        if not path:
            return

        if not is_encrypted and is_internal:
            result = pwgui.ask_password(win, True, True if len(path) == 1 else False)
            password = result[0]
            keep_copy = result[1]

            if not password:
                return

            has_been_encrypted = [lc.encrypt(i, password.encode('utf-8'), keep_copy) for i in path]
            if all(has_been_encrypted):
                alerts.encrypted_successfully_alert(len(path))
            return

        if is_encrypted and is_internal:
            result = pwgui.ask_password(win, False, True if len(path) == 1 else False)
            password = result[0]
            keep_copy = result[1]

            if not password:
                return

            has_been_decrypted = [lc.decrypt(i, password.encode('utf-8'), keep_copy) for i in path]

            if all(has_been_decrypted):
                alerts.decrypted_successfully_alert(len(path))
            return

        if not is_encrypted and not is_internal:

            fixed_path = [i for i in path if not Share.is_already_shared(i)]
            if len(fixed_path) == 0:
                return

            username = get_username(win)
            if username is None:
                return

            has_been_shared = [rsa.share(i, username) for i in fixed_path]

            if all(has_been_shared):
                alerts.shared_successfully_alert(len(fixed_path))
            return

        if is_encrypted and not is_internal:

            has_been_translated = [rsa.translate(i) for i in path]

            if all(has_been_translated):
                alerts.translated_successfully_alert(len(path))
            return

    def show_settings():
        pass

    # widgets

    background_lab = tk.Label(win, image=BACKGROUND_IMAGE)
    encrypt_but = tk.Button(win, image=CRYPT_IMAGE, borderwidth=0, bg='#0c11a8', command=lambda: execute(False, True))
    decrypt_but = tk.Button(win, image=DECRYPT_IMAGE, borderwidth=0, bg='#f0a000', command=lambda: execute(True, True))
    share_but = tk.Button(win, image=SHARE_IMAGE, borderwidth=0, bg='#0c11a8', command=lambda: execute(False, False))
    decrypt_external_file_but = tk.Button(win, image=DECRYPT_EXTERNAL_FILE_IMAGE, borderwidth=0, bg='#f0a000',
                                          command=lambda: execute(True, False))
    info_lab = tk.Label(win, image=INFO_IMAGE, borderwidth=0, bg='#cbcbcb')
    github_lab = tk.Label(win, image=GITHUB_IMAGE, borderwidth=0, bg='#cbcbcb')
    settings_lab = tk.Label(win, image=SETTINGS_IMAGE, borderwidth=0, bg='#cbcbcb')

    # Hover events

    encrypt_but.bind("<Enter>", lambda _: encrypt_but.config(image=CRYPT_IMAGE_HOVERED))
    encrypt_but.bind("<Leave>", lambda _: encrypt_but.config(image=CRYPT_IMAGE))
    decrypt_but.bind("<Enter>", lambda _: decrypt_but.config(image=DECRYPT_IMAGE_HOVERED))
    decrypt_but.bind("<Leave>", lambda _: decrypt_but.config(image=DECRYPT_IMAGE))
    share_but.bind("<Enter>", lambda _: share_but.config(image=SHARE_IMAGE_HOVERED))
    share_but.bind("<Leave>", lambda _: share_but.config(image=SHARE_IMAGE))
    decrypt_external_file_but.bind("<Enter>", lambda _: decrypt_external_file_but.config(
        image=DECRYPT_EXTERNAL_FILE_IMAGE_HOVERED))
    decrypt_external_file_but.bind("<Leave>",
                                   lambda _: decrypt_external_file_but.config(image=DECRYPT_EXTERNAL_FILE_IMAGE))
    info_lab.bind("<Enter>", lambda _: info_lab.config(image=INFO_IMAGE_HOVERED))
    info_lab.bind("<Leave>", lambda _: info_lab.config(image=INFO_IMAGE))
    info_lab.bind("<Button-1>",
                  lambda _: web.Browser('https://github.com/RichardBoy05/EasyCrypto/blob/main/README.md').search())
    github_lab.bind("<Enter>", lambda _: github_lab.config(image=GITHUB_IMAGE_HOVERED))
    github_lab.bind("<Leave>", lambda _: github_lab.config(image=GITHUB_IMAGE))
    github_lab.bind("<Button-1>", lambda _: web.Browser('https://github.com/RichardBoy05/EasyCrypto').search())
    settings_lab.bind("<Enter>", lambda _: settings_lab.config(image=SETTINGS_IMAGE_HOVERED))
    settings_lab.bind("<Leave>", lambda _: settings_lab.config(image=SETTINGS_IMAGE))
    settings_lab.bind("<Button-1>", lambda _: show_settings())

    # placing

    background_lab.place(x=-2, y=-2)
    encrypt_but.place(x=34, y=230)
    decrypt_but.place(x=244, y=230)
    decrypt_external_file_but.place(x=244, y=330)
    share_but.place(x=34, y=330)
    info_lab.place(x=363, y=428)
    github_lab.place(x=391, y=428)
    settings_lab.place(x=419, y=428)

    win.mainloop()


def correct_closing(win):
    PATH = os.path.join(os.getenv('APPDATA'), 'EasyCrypto')
    CRYPT_PATH = os.path.join(PATH, 'crypt')

    if os.path.exists(os.path.join(CRYPT_PATH, "firstboot")):
        os.remove(os.path.join(CRYPT_PATH, "firstboot"))

    win.destroy()
