import os
import web
import tkinter as tk
from logger import Logger
from user_utils import Username

PATH = os.path.join(os.getenv('APPDATA'), 'EasyCrypto')
CRYPT_PATH = os.path.join(PATH, 'crypt')
USERS_LIST = os.path.join(PATH, 'users_list.txt')


class SetUsernameGui(tk.Tk):

    def __init__(self):
        super().__init__()
        self.username = None
        self.username_obj = Username(self)

        # settings

        self.WIDTH = 475
        self.HEIGHT = 325
        self.x = int(self.winfo_screenwidth() / 2 - (self.WIDTH / 2))
        self.y = int(self.winfo_screenheight() / 2 - (self.HEIGHT / 2))

        self.title('EasyCrypto')
        self.geometry('{}x{}+{}+{}'.format(self.WIDTH, self.HEIGHT, self.x, self.y))
        self.resizable(False, False)
        self.icon = tk.PhotoImage(file='res/logo.png', master=self)
        self.iconphoto(True, self.icon)
        self.log = Logger(__name__).default()

        # images

        self.BACKGROUND_IMAGE = tk.PhotoImage(file='res/set_username_background.png', master=self)
        self.GO_IMAGE = tk.PhotoImage(file='res/set_username_but.png', master=self)
        self.GO_IMAGE_HOVERED = tk.PhotoImage(file='res/set_username_but_hovered.png', master=self)

        # fonts

        self.def_font = ('Arial Baltic', 14)

        # check connection

        self.storage = self.username_obj.get_users_list()

        if self.storage is None:
            self.username = None
            return

        # widgets

        self.bg = tk.Canvas(self, width=475, height=325)
        self.bg.create_image(239, 164, image=self.BACKGROUND_IMAGE)
        self.canva_id = self.bg.create_text(30, 202, text='Nickname troppo corto!', fill='red', anchor='w')
        self.content = tk.StringVar()
        self.user_entry = tk.Entry(self, width=19, font=self.def_font, relief='groove', textvariable=self.content)
        self.go_but = tk.Button(self, image=self.GO_IMAGE, borderwidth=0, bg='#160ca3',
                                command=lambda: self.username_obj.execute(self, self.content, True, self.bg,
                                                                          self.canva_id))
        # configuration and bindings

        self.bg.bind('<Button-1>', lambda _: self.__readme_redirect())
        self.go_but.bind("<Enter>", lambda _: self.go_but.config(image=self.GO_IMAGE_HOVERED))
        self.go_but.bind("<Leave>", lambda _: self.go_but.config(image=self.GO_IMAGE))

        self.content.trace_add('write', lambda _, __, ___: Username.check_username(self.content.get(), True, self.bg,
                                                                                   self.canva_id))
        self.user_entry.focus()

        # placing

        self.bg.place(x=-2, y=-2)
        self.user_entry.place(x=29, y=163)
        self.go_but.place(x=67, y=228)

        # button event

        self.go_but.wait_window(self)

        try:
            if os.path.exists(USERS_LIST):
                os.remove(USERS_LIST)
        except PermissionError:
            self.log.warning("PermissionError", exc_info=True)

        try:
            self.username = self, self.username_obj.username
        except AttributeError:
            self.log.warning("AttributeError", exc_info=True)
            self.username = None

    def __readme_redirect(self) -> None:
        """Redirects the user to the EasyCrypto GitHub readme"""
        x_coord = self.winfo_pointerx() - self.winfo_rootx()
        y_coord = self.winfo_pointery() - self.winfo_rooty()

        if 352 < x_coord < 465 and 301 < y_coord < 318:
            web.Browser('https://github.com/RichardBoy05/EasyCrypto/blob/main/README.md').search()

    def get(self) -> tuple[tk.Tk, str | None] | None:
        """Returns the username value"""
        return self.username
