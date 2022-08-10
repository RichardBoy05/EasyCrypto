import os
import web
import alerts as alt
import tkinter as tk
from config import Config
from typing import Literal
import local_crypter as lc
import passwordgui as pwgui
from counter import Counter
from rsa_utils import Share
import rsa_encryption as rsa
from tkinter import filedialog
from issuesgui import IssueGui
from getusernamegui import GetUsername


class MainGui(tk.Tk):
    """
    Structure of the EasyCrypto Main GUI

    Naming conventions:
    - Enc -> Encrypt
    - Dec -> Decrypt
    - Shr -> Share
    - Trs -> Translate

    """

    def __init__(self):
        super().__init__()

        # settings

        self.WIDTH = 450
        self.HEIGHT = 450
        self.x = int(self.winfo_screenwidth() / 2 - (self.WIDTH / 2))
        self.y = int(self.winfo_screenheight() / 2 - (self.HEIGHT / 2))

        self.title('EasyCrypto')
        self.geometry('{}x{}+{}+{}'.format(self.WIDTH, self.HEIGHT, self.x, self.y))
        self.resizable(False, False)
        self.iconphoto(True, tk.PhotoImage(file='res/logo.png', master=self))
        self.protocol("WM_DELETE_WINDOW", self.correct_closing)

        # images

        self.BG_IMG = tk.PhotoImage(file='res/background.png', master=self)
        self.ENC_IMG = tk.PhotoImage(file='res/encrypt.png', master=self)
        self.ENC_IMG_HOV = tk.PhotoImage(file='res/encrypt_hovered.png', master=self)
        self.DEC_IMG = tk.PhotoImage(file='res/decrypt.png', master=self)
        self.DEC_IMG_HOV = tk.PhotoImage(file='res/decrypt_hovered.png', master=self)
        self.SHR_IMG = tk.PhotoImage(file='res/share.png', master=self)
        self.SHR_IMG_HOV = tk.PhotoImage(file='res/share_hovered.png', master=self)
        self.TRS_IMG = tk.PhotoImage(file='res/translate.png', master=self)
        self.TRS_IMG_HOV = tk.PhotoImage(file='res/translate_hovered.png', master=self)
        self.INFO_IMG = tk.PhotoImage(file='res/info.png', master=self)
        self.INFO_IMG_HOV = tk.PhotoImage(file='res/info_hovered.png', master=self)
        self.GIT_IMG = tk.PhotoImage(file='res/github.png', master=self)
        self.GIT_IMG_HOV = tk.PhotoImage(file='res/github_hovered.png', master=self)
        self.ISSUE_IMG = tk.PhotoImage(file='res/issue_icon.png', master=self)
        self.ISSUE_IMG_HOV = tk.PhotoImage(file='res/issue_icon_hovered.png', master=self)

        # fonts and misc

        self.counters_font = ('Courier', 14)
        self.readme = 'https://github.com/RichardBoy05/EasyCrypto/blob/main/README.md'
        self.repo = 'https://github.com/RichardBoy05/EasyCrypto'
        self.explorer_files = [('Tutti i file', '*.*')]
        self.enc_text = Config.parse_with_key('TotalEncryptions', True)
        self.dec_text = Config.parse_with_key('TotalDecryptions', True)
        self.shr_text = Config.parse_with_key('TotalShares', True)
        self.trs_text = Config.parse_with_key('TotalTranslations', True)

        # widgets

        self.bg = tk.Canvas(self, width=450, height=450)
        self.bg.create_image(226, 226, image=self.BG_IMG)
        self.enc_count = self.bg.create_text(162, 161, text=self.enc_text, font=self.counters_font, anchor='center')
        self.dec_count = self.bg.create_text(412, 161, text=self.dec_text, font=self.counters_font, anchor='center')
        self.shr_count = self.bg.create_text(162, 200, text=self.shr_text, font=self.counters_font, anchor='center')
        self.trs_count = self.bg.create_text(412, 200, text=self.trs_text, font=self.counters_font, anchor='center')
        self.enc_but = tk.Button(self, image=self.ENC_IMG, bd=0, bg='#0c11a8', command=lambda: self.execute('enc'))
        self.dec_but = tk.Button(self, image=self.DEC_IMG, bd=0, bg='#f0a000', command=lambda: self.execute('dec'))
        self.shr_but = tk.Button(self, image=self.SHR_IMG, bd=0, bg='#0c11a8', command=lambda: self.execute('shr'))
        self.trs_but = tk.Button(self, image=self.TRS_IMG, bd=0, bg='#f0a000', command=lambda: self.execute('trs'))
        self.info_lab = tk.Label(self, image=self.INFO_IMG, bd=0, bg='#cbcbcb')
        self.git_lab = tk.Label(self, image=self.GIT_IMG, bd=0, bg='#cbcbcb')
        self.issue_lab = tk.Label(self, image=self.ISSUE_IMG, bd=0, bg='#cbcbcb')

        # tooltips

        # bindings

        self.enc_but.bind("<Enter>", lambda _: self.enc_but.config(image=self.ENC_IMG_HOV))
        self.enc_but.bind("<Leave>", lambda _: self.enc_but.config(image=self.ENC_IMG))
        self.dec_but.bind("<Enter>", lambda _: self.dec_but.config(image=self.DEC_IMG_HOV))
        self.dec_but.bind("<Leave>", lambda _: self.dec_but.config(image=self.DEC_IMG))
        self.shr_but.bind("<Enter>", lambda _: self.shr_but.config(image=self.SHR_IMG_HOV))
        self.shr_but.bind("<Leave>", lambda _: self.shr_but.config(image=self.SHR_IMG))
        self.trs_but.bind("<Enter>", lambda _: self.trs_but.config(image=self.TRS_IMG_HOV))
        self.trs_but.bind("<Leave>", lambda _: self.trs_but.config(image=self.TRS_IMG))
        self.info_lab.bind("<Enter>", lambda _: self.info_lab.config(image=self.INFO_IMG_HOV))
        self.info_lab.bind("<Leave>", lambda _: self.info_lab.config(image=self.INFO_IMG))
        self.git_lab.bind("<Enter>", lambda _: self.git_lab.config(image=self.GIT_IMG_HOV))
        self.git_lab.bind("<Leave>", lambda _: self.git_lab.config(image=self.GIT_IMG))
        self.issue_lab.bind("<Enter>", lambda _: self.issue_lab.config(image=self.ISSUE_IMG_HOV))
        self.issue_lab.bind("<Leave>", lambda _: self.issue_lab.config(image=self.ISSUE_IMG))
        self.info_lab.bind("<Button-1>", lambda _: web.Browser(self.readme).search())
        self.git_lab.bind("<Button-1>", lambda _: web.Browser(self.repo).search())
        self.issue_lab.bind("<Button-1>", lambda _: IssueGui(self))

        # placing

        self.bg.place(x=-2, y=-2)
        self.enc_but.place(x=28, y=237)
        self.dec_but.place(x=248, y=237)
        self.trs_but.place(x=248, y=337)
        self.shr_but.place(x=28, y=337)
        self.info_lab.place(x=362, y=428)
        self.git_lab.place(x=391, y=428)
        self.issue_lab.place(x=420, y=428)

        self.mainloop()

    # methods

    def execute(self, task: Literal['enc', 'dec', 'shr', 'trs']) -> None:
        """ Redirects the code flow to the matching action """

        path = tk.filedialog.askopenfilenames(title='Seleziona uno o più file...', filetypes=self.explorer_files)
        if not path:
            return

        if task == 'enc':
            self.encrypt(path)
        elif task == 'dec':
            self.decrypt(path)
        elif task == 'shr':
            self.share(path)
        elif task == 'trs':
            self.translate(path)

    def encrypt(self, path: str) -> None:
        """ Encrypts files with password """

        password, keepcopy = pwgui.ask_password(self, to_encrypt=True, one_file=True if len(path) == 1 else False)
        if not password:
            return

        has_been_encrypted = [lc.encrypt(self, path=i, pw=password.encode('utf-8'), keep_copy=keepcopy) for i in path]

        for i in has_been_encrypted:
            if i:
                Counter(self, self.bg.itemcget(self.enc_count, 'text'), self.enc_count).update('TotalEncryptions')

        if all(has_been_encrypted):
            alt.encrypted_successfully_alert(self, len(path))

    def decrypt(self, path: str) -> None:
        """ Decrypts files with password """

        password, keepcopy = pwgui.ask_password(self, to_encrypt=False, one_file=True if len(path) == 1 else False)
        if not password:
            return

        has_been_decrypted = [lc.decrypt(self, path=i, pw=password.encode('utf-8'), keep_copy=keepcopy) for i in path]

        for i in has_been_decrypted:
            if i:
                Counter(self, self.bg.itemcget(self.dec_count, 'text'), self.dec_count).update('TotalDecryptions')

        if all(has_been_decrypted):
            alt.decrypted_successfully_alert(self, len(path))

    def share(self, path: str) -> None:
        """ Shares encrypted files with someone given the receiver's nickname """

        fixed_path = [i for i in path if not Share(self).is_already_shared(i)]
        if len(fixed_path) == 0:
            return

        username = GetUsername().get_username()
        if username is None:
            return

        has_been_shared = [rsa.share(self, i, username) for i in fixed_path]

        for i in has_been_shared:
            if i:
                Counter(self, self.bg.itemcget(self.shr_count, 'text'), self.shr_count).update('TotalShares')

        if all(has_been_shared):
            alt.shared_successfully_alert(self, len(fixed_path))

    def translate(self, path: str) -> None:
        """ Translates encrypted files received by another user """

        has_been_translated = [rsa.translate(self, i) for i in path]

        for i in has_been_translated:
            if i:
                Counter(self, self.bg.itemcget(self.trs_count, 'text'), self.trs_count).update('TotalTranslations')

        if all(has_been_translated):
            alt.translated_successfully_alert(self, len(path))

    def correct_closing(self):
        PATH = os.path.join(os.getenv('APPDATA'), 'EasyCrypto')
        CRYPT_PATH = os.path.join(PATH, 'crypt')

        if os.path.exists(os.path.join(CRYPT_PATH, "firstboot")):
            os.remove(os.path.join(CRYPT_PATH, "firstboot"))

        self.destroy()


def init():
    MainGui()
