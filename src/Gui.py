import tkinter as tk
from tkinter import filedialog
import FileCrypter
from Notifications import encrypted_successfully_alert, decrypted_successfully_alert


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

    button_font = ('Arial', 14)

    encrypt_but = tk.Button(win, text="Encrypt", font=button_font, command=lambda: execute(False, True))
    decrypt_but = tk.Button(win, text="Decrypt", font=button_font, command=lambda: execute(True, True))
    decrypt_external_file_but = tk.Button(win, text="Decrypt External file", font=button_font,
                                          command=lambda: execute(True, False))
    share_but = tk.Button(win, text="Share", font=button_font, command=lambda: execute(False, False))

    # placing

    encrypt_but.place(x=200, y=50)
    decrypt_but.place(x=200, y=150)
    decrypt_external_file_but.place(x=200, y=250)
    share_but.place(x=200, y=350)

    win.mainloop()
