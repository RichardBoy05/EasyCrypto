import os
import web
import tkinter as tk
from logger import Logger
from tktooltip import ToolTip
from user_utils import Username

PATH = os.path.join(os.getenv('APPDATA'), 'EasyCrypto')
CRYPT_PATH = os.path.join(PATH, 'crypt')
USERS_LIST = os.path.join(PATH, 'users_list.txt')


class SetUsernameGui(tk.Tk):
    """ Structure of the Set Username GUI """

    def __init__(self):
        super().__init__()

        self.__username = None  # username string
        self.__user_object = Username(self)  # username instance (from: src/user_utils.py -> Username())

        # settings

        self.WIDTH = 475
        self.HEIGHT = 325
        self.x = int(self.winfo_screenwidth() / 2 - (self.WIDTH / 2))
        self.y = int(self.winfo_screenheight() / 2 - (self.HEIGHT / 2))

        self.title('EasyCrypto')
        self.geometry('{}x{}+{}+{}'.format(self.WIDTH, self.HEIGHT, self.x, self.y))
        self.resizable(False, False)
        self.iconphoto(True, tk.PhotoImage(file='res/logo.png', master=self))
        self.log = Logger(__name__).default()

        # check internet connection

        if self.__user_object.get_users_list() is None:
            self.__username = None
            return

        # images

        self.BG_IMG = tk.PhotoImage(file='res/set_username_background.png', master=self)
        self.GO_IMG = tk.PhotoImage(file='res/set_username_but.png', master=self)
        self.GO_IMG_HOV = tk.PhotoImage(file='res/set_username_but_hovered.png', master=self)
        self.GUIDE_IMG = tk.PhotoImage(file='res/check_guide.png', master=self)
        self.GUIDE_IMG_HOV = tk.PhotoImage(file='res/check_guide_hovered.png', master=self)

        # fonts and misc

        self.def_font = ('Arial Baltic', 14)
        self.text = tk.StringVar()

        # widgets

        self.bg = tk.Canvas(self, width=475, height=325)
        self.bg.create_image(239, 164, image=self.BG_IMG)
        self.bg.create_image(413, 311, image=self.GUIDE_IMG, tags='guide')
        self.nik_id = self.bg.create_text(30, 202, text='Nickname troppo corto!', fill='red', anchor='w')
        self.entry = tk.Entry(self, width=19, font=self.def_font, relief='groove', textvariable=self.text)
        self.go_but = tk.Button(self, image=self.GO_IMG, borderwidth=0, bg='#160ca3', command=self.__go)

        # configuration and bindings

        self.go_but.bind("<Enter>", lambda _: self.go_but.config(image=self.GO_IMG_HOV))
        self.go_but.bind("<Leave>", lambda _: self.go_but.config(image=self.GO_IMG))
        self.bg.tag_bind('guide', "<Button-1>", lambda _: self.__readme_redirect())
        self.bg.tag_bind('guide', "<Enter>", lambda _: self.bg.itemconfig('guide', image=self.GUIDE_IMG_HOV))
        self.bg.tag_bind('guide', "<Leave>", lambda _: self.bg.itemconfig('guide', image=self.GUIDE_IMG))
        self.text.trace_add('write', lambda *args: Username.check_nick(self.text.get(), True, self.bg, self.nik_id))
        self.entry.focus()

        # placing

        self.bg.place(x=-2, y=-2)
        self.entry.place(x=29, y=163)
        self.go_but.place(x=67, y=228)

        # wait window event

        self.go_but.wait_window(self)

        try:
            if os.path.exists(USERS_LIST):
                os.remove(USERS_LIST)
        except PermissionError:
            self.log.warning("PermissionError", exc_info=True)

        self.__username = self, self.__user_object.username

    # methods

    def __go(self) -> None:
        """ Sets the nickname for the current user """
        self.__user_object.execute(self, entry=self.text, to_set=True, canva=self.bg, canva_id=self.nik_id)

    def get_username(self) -> tuple[tk.Tk, str | None] | None:
        """ Returns the username value """
        return self.__username

    @staticmethod
    def __readme_redirect() -> None:
        """ Redirects the user to the EasyCrypto GitHub readme file """
        web.Browser('https://github.com/RichardBoy05/EasyCrypto/blob/main/README.md').search()
