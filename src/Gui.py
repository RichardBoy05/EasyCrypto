import tkinter as tk
from tkinter import filedialog
from tkinter import Label
import FileCrypter
from Notifications import encrypted_successfully_alert, decrypted_successfully_alert


def init_window():
    win = tk.Tk()

    WIDTH = 675
    HEIGHT = 550
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

    x = int(win.winfo_screenwidth() / 2 - (WIDTH / 2))
    y = int(win.winfo_screenheight() / 2 - (HEIGHT / 2))

    win.title('EasyCrypto')
    win.geometry(str(WIDTH) + 'x' + str(HEIGHT) + '+' + str(x) + '+' + str(y))
    win.resizable(0, 0)
    win.iconphoto(True, WINDOW_ICON)

    # functions

    def execute(is_encrypted, is_internal):

        files = None

        if is_encrypted and not is_internal:
            files = [('Archivio EasyCrypto', '*' + FileCrypter.CRYPTO_ARCHIVE_EXT)]
        else:
            files = [('Tutti i file', '*.*')]

        path = filedialog.askopenfilenames(title='Seleziona uno o più file...', filetypes=files)

        if not path:
            return

        if not is_encrypted and is_internal:
            has_been_encrypted = None
            for i in path:
                has_been_encrypted = FileCrypter.encrypt(i)
            if has_been_encrypted:
                encrypted_successfully_alert(len(path))
            return

        if is_encrypted and is_internal:
            has_been_decrypted = None
            for i in path:
                has_been_decrypted = FileCrypter.decrypt(i)
            if has_been_decrypted:
                decrypted_successfully_alert(len(path))
            return

        if is_encrypted and not is_internal:
            for i in path:
                FileCrypter.decrypt_external_file(i)
            return

        if not is_encrypted and not is_internal:
            FileCrypter.share(path)
            return

    # widgets

    background_label = Label(win, image=BACKGROUND_IMAGE)
    encrypt_but = tk.Button(win, image=CRYPT_IMAGE, borderwidth=0, command=lambda: execute(False, True))
    decrypt_but = tk.Button(win, image=DECRYPT_IMAGE, borderwidth=0, command=lambda: execute(True, True))
    share_but = tk.Button(win, image=SHARE_IMAGE, borderwidth=0, command=lambda: execute(False, False))
    decrypt_external_file_but = tk.Button(win, image=DECRYPT_EXTERNAL_FILE_IMAGE, borderwidth=0, command=lambda: execute(True, False))

    # Hover events

    encrypt_but.bind("<Enter>", lambda x: encrypt_but.config(image=CRYPT_IMAGE_HOVERED))
    encrypt_but.bind("<Leave>", lambda x: encrypt_but.config(image=CRYPT_IMAGE))
    decrypt_but.bind("<Enter>", lambda x: decrypt_but.config(image=DECRYPT_IMAGE_HOVERED))
    decrypt_but.bind("<Leave>", lambda x: decrypt_but.config(image=DECRYPT_IMAGE))
    share_but.bind("<Enter>", lambda x: share_but.config(image=SHARE_IMAGE_HOVERED))
    share_but.bind("<Leave>", lambda x: share_but.config(image=SHARE_IMAGE))
    decrypt_external_file_but.bind("<Enter>", lambda x: decrypt_external_file_but.config(image=DECRYPT_EXTERNAL_FILE_IMAGE_HOVERED))
    decrypt_external_file_but.bind("<Leave>", lambda x: decrypt_external_file_but.config(image=DECRYPT_EXTERNAL_FILE_IMAGE))

    # placing

    background_label.place(x=-2, y=-2)
    encrypt_but.place(x=40, y=225)
    decrypt_but.place(x=300, y=225)
    decrypt_external_file_but.place(x=300, y=350)
    share_but.place(x=40, y=350)

    win.mainloop()
