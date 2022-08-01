import os
import web
import alerts as alt
import tkinter as tk
from config import Config
import local_crypter as lc
import passwordgui as pwgui
from counter import Counter
from rsa_utils import Share
import rsa_encryption as rsa
from tkinter import filedialog
from getusernamegui import get_username


class MainGui:

    def __init__(self):

        self.win = tk.Tk()

        self.WIDTH = 450
        self.HEIGHT = 450
        self.WINDOW_ICON = tk.PhotoImage(file='res/logo.png', master=self.win)
        self.BACKGROUND_IMAGE = tk.PhotoImage(file='res/background.png', master=self.win)
        self.x = int(self.win.winfo_screenwidth() / 2 - (self.WIDTH / 2))
        self.y = int(self.win.winfo_screenheight() / 2 - (self.HEIGHT / 2))

        self.win.title('EasyCrypto')
        self.win.geometry(str(self.WIDTH) + 'x' + str(self.HEIGHT) + '+' + str(self.x) + '+' + str(self.y))
        self.win.resizable(False, False)
        self.win.iconphoto(True, self.WINDOW_ICON)
        self.win.protocol("WM_DELETE_WINDOW", lambda: self.correct_closing())
        self.bg = tk.Canvas(self.win, width=450, height=450)
        self.bg.create_image(226, 226, image=self.BACKGROUND_IMAGE)

        self.counter_font = ('Courier', 14)
        self.readme = 'https://github.com/RichardBoy05/EasyCrypto/blob/main/README.md'
        self.explorer_files = [('Tutti i file', '*.*')]

        enc_text = Config.parse_with_key('TotalEncryptions', True)
        dec_text = Config.parse_with_key('TotalDecryptions', True)
        shr_text = Config.parse_with_key('TotalShares', True)
        trs_text = Config.parse_with_key('TotalTranslations', True)
        self.encrypt_count = self.bg.create_text(162, 161, text=enc_text, font=self.counter_font, anchor='center')
        self.decrypt_count = self.bg.create_text(412, 161, text=dec_text, font=self.counter_font, anchor='center')
        self.share_count = self.bg.create_text(162, 200, text=shr_text, font=self.counter_font, anchor='center')
        self.translate_count = self.bg.create_text(412, 200, text=trs_text, font=self.counter_font, anchor='center')

        ENC_IMG = tk.PhotoImage(file='res/crypt.png', master=self.win)
        ENC_IMG_HOV = tk.PhotoImage(file='res/crypt_hovered.png', master=self.win)
        DEC_IMG = tk.PhotoImage(file='res/decrypt.png', master=self.win)
        DEC_IMG_HOV = tk.PhotoImage(file='res/decrypt_hovered.png', master=self.win)
        SHR_IMG = tk.PhotoImage(file='res/share.png', master=self.win)
        SHR_IMG_HOV = tk.PhotoImage(file='res/share_hovered.png', master=self.win)
        TRS_IMG = tk.PhotoImage(file='res/translate.png', master=self.win)
        TRS_IMG_HOV = tk.PhotoImage(file='res/translate_hovered.png', master=self.win)
        INFO_IMG = tk.PhotoImage(file='res/info.png', master=self.win)
        INFO_IMG_HOV = tk.PhotoImage(file='res/info_hovered.png', master=self.win)
        GIT_IMG = tk.PhotoImage(file='res/github.png', master=self.win)
        GIT_IMG_HOV = tk.PhotoImage(file='res/github_hovered.png', master=self.win)
        SETTINGS_IMG = tk.PhotoImage(file='res/settings.png', master=self.win)
        SETTINGS_IMG_HOV = tk.PhotoImage(file='res/settings_hovered.png', master=self.win)

        # widgets

        enc_but = tk.Button(self.win, image=ENC_IMG, bd=0, bg='#0c11a8', command=lambda: self.execute('encrypt'))
        dec_but = tk.Button(self.win, image=DEC_IMG, bd=0, bg='#f0a000', command=lambda: self.execute('decrypt'))
        shr_but = tk.Button(self.win, image=SHR_IMG, bd=0, bg='#0c11a8', command=lambda: self.execute('share'))
        trs_but = tk.Button(self.win, image=TRS_IMG, bd=0, bg='#f0a000', command=lambda: self.execute('translate'))
        info_lab = tk.Label(self.win, image=INFO_IMG, bd=0, bg='#cbcbcb')
        git_lab = tk.Label(self.win, image=GIT_IMG, bd=0, bg='#cbcbcb')
        settings_lab = tk.Label(self.win, image=SETTINGS_IMG, bd=0, bg='#cbcbcb')

        # Hover events

        enc_but.bind("<Enter>", lambda _: enc_but.config(image=ENC_IMG_HOV))
        enc_but.bind("<Leave>", lambda _: enc_but.config(image=ENC_IMG))
        dec_but.bind("<Enter>", lambda _: dec_but.config(image=DEC_IMG_HOV))
        dec_but.bind("<Leave>", lambda _: dec_but.config(image=DEC_IMG))
        shr_but.bind("<Enter>", lambda _: shr_but.config(image=SHR_IMG_HOV))
        shr_but.bind("<Leave>", lambda _: shr_but.config(image=SHR_IMG))
        trs_but.bind("<Enter>", lambda _: trs_but.config(image=TRS_IMG_HOV))
        trs_but.bind("<Leave>", lambda _: trs_but.config(image=TRS_IMG))
        info_lab.bind("<Enter>", lambda _: info_lab.config(image=INFO_IMG_HOV))
        info_lab.bind("<Leave>", lambda _: info_lab.config(image=INFO_IMG))
        info_lab.bind("<Button-1>", lambda _: web.Browser(self.readme).search())
        git_lab.bind("<Enter>", lambda _: git_lab.config(image=GIT_IMG_HOV))
        git_lab.bind("<Leave>", lambda _: git_lab.config(image=GIT_IMG))
        git_lab.bind("<Button-1>", lambda _: web.Browser('https://github.com/RichardBoy05/EasyCrypto').search())
        settings_lab.bind("<Enter>", lambda _: settings_lab.config(image=SETTINGS_IMG_HOV))
        settings_lab.bind("<Leave>", lambda _: settings_lab.config(image=SETTINGS_IMG))

        # placing

        self.bg.place(x=-2, y=-2)
        enc_but.place(x=28, y=237)
        dec_but.place(x=248, y=237)
        trs_but.place(x=248, y=337)
        shr_but.place(x=28, y=337)
        info_lab.place(x=363, y=428)
        git_lab.place(x=391, y=428)
        settings_lab.place(x=419, y=428)

        self.win.mainloop()

    def execute(self, task):

        path = tk.filedialog.askopenfilenames(title='Seleziona uno o più file...', filetypes=self.explorer_files)

        if not path:
            return

        if task == 'encrypt':
            result = pwgui.ask_password(self.win, True, True if len(path) == 1 else False)
            password, keepcopy = result
            if not password:
                return

            has_been_encrypted = [lc.encrypt(self.win, i, password.encode('utf-8'), keepcopy) for i in path]

            for i in has_been_encrypted:
                if i:
                    Counter(self.win, self.bg.itemcget(self.encrypt_count, 'text'),
                            self.encrypt_count).update('TotalEncryptions')

            if all(has_been_encrypted):
                alt.encrypted_successfully_alert(len(path))
            return

        if task == 'decrypt':
            result = pwgui.ask_password(self.win, False, True if len(path) == 1 else False)
            password, keepcopy = result
            if not password:
                return

            has_been_decrypted = [lc.decrypt(self.win, i, password.encode('utf-8'), keepcopy) for i in path]

            for i in has_been_decrypted:
                if i:
                    Counter(self.win, self.bg.itemcget(self.decrypt_count, 'text'),
                            self.decrypt_count).update('TotalDecryptions')

            if all(has_been_decrypted):
                alt.decrypted_successfully_alert(len(path))
            return

        if task == 'share':

            fixed_path = [i for i in path if not Share.is_already_shared(i)]
            if len(fixed_path) == 0:
                return

            username = get_username(self.win)
            if username is None:
                return

            has_been_shared = [rsa.share(i, username) for i in fixed_path]

            for i in has_been_shared:
                if i:
                    Counter(self.win, self.bg.itemcget(self.share_count, 'text'), self.share_count).update('TotalShares')

            if all(has_been_shared):
                alt.shared_successfully_alert(len(fixed_path))
            return

        if task == 'translate':

            has_been_translated = [rsa.translate(i) for i in path]

            for i in has_been_translated:
                if i:
                    Counter(self.win, self.bg.itemcget(self.share_count, 'text'),
                            self.translate_count).update('TotalTranslations')

            if all(has_been_translated):
                alt.translated_successfully_alert(len(path))
            return

    def correct_closing(self):
        PATH = os.path.join(os.getenv('APPDATA'), 'EasyCrypto')
        CRYPT_PATH = os.path.join(PATH, 'crypt')

        if os.path.exists(os.path.join(CRYPT_PATH, "firstboot")):
            os.remove(os.path.join(CRYPT_PATH, "firstboot"))

        self.win.destroy()


def init():
    MainGui()
