
# built-in modules
import os
import tkinter as tk

# app modules
from easycrypto.Src.Utils import web
from easycrypto.Src.Utils.logger import Logger
from easycrypto.Src.Utils.user_utils import Username
from easycrypto.Src.Utils.paths import ROOT,  USERS_LIST


class SetUsernameGui(tk.Tk):
    """ Defines the structure of the SetUsername GUI """

    def __init__(self):
        super().__init__()

        self.__username = Username(self)  # private member, instance of the Username class (Utils/users_list.py)

        # settings

        self.WIDTH = 475
        self.HEIGHT = 325
        self.x = int(self.winfo_screenwidth() / 2 - (self.WIDTH / 2))
        self.y = int(self.winfo_screenheight() / 2 - (self.HEIGHT / 2))

        self.title('EasyCrypto')
        self.geometry('{}x{}+{}+{}'.format(self.WIDTH, self.HEIGHT, self.x, self.y))
        self.resizable(False, False)
        self.iconphoto(True, tk.PhotoImage(file=f'{ROOT}/Resources/General/logo.png', master=self))
        self.log = Logger(__name__).default()

        # check internet connection

        if self.__username.get_users_list() is None:
            self.__username.username = None
            return

        # images

        self.BG_IMG = tk.PhotoImage(file=f'{ROOT}/Resources/SetUsernameGUI/set_username_background.png', master=self)
        self.GO_IMG = tk.PhotoImage(file=f'{ROOT}/Resources/SetUsernameGUI/set_username_but.png', master=self)
        self.GO_IMG_HOV = tk.PhotoImage(file=f'{ROOT}/Resources/SetUsernameGUI/set_username_but_hov.png', master=self)
        self.GUIDE_IMG = tk.PhotoImage(file=f'{ROOT}/Resources/SetUsernameGUI/check_guide.png', master=self)
        self.GUIDE_IMG_HOV = tk.PhotoImage(file=f'{ROOT}/Resources/SetUsernameGUI/check_guide_hov.png', master=self)

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
        self.bg.tag_bind('guide', "<Button-1>", lambda _: self.__readme_redirect(), add='+')
        self.bg.tag_bind('guide', "<Enter>", lambda _: self.bg.itemconfig('guide', image=self.GUIDE_IMG_HOV), add='+')
        self.bg.tag_bind('guide', "<Leave>", lambda _: self.bg.itemconfig('guide', image=self.GUIDE_IMG), add='+')
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

    # methods

    def __go(self) -> None:
        """ Sets the nickname for the current user """
        self.__username.execute(self, entry=self.text, to_set=True, canva=self.bg, canva_id=self.nik_id)

    def get_username(self) -> tuple[tk.Tk, str | None] | None:
        """ Returns the username value """
        return self, self.__username.username

    @staticmethod
    def __readme_redirect() -> None:
        """ Redirects the user to the EasyCrypto GitHub readme file """
        web.Browser('https://github.com/RichardBoy05/EasyCrypto/blob/main/README.md').search()
