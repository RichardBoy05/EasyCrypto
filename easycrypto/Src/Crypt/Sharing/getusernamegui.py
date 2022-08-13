import os
import tkinter as tk
from logger import Logger
from user_utils import Username

PATH = os.path.join(os.getenv('APPDATA'), 'EasyCrypto')
USERS_LIST = os.path.join(PATH, 'users_list.txt')


class GetUsername(tk.Toplevel):

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.parent.withdraw()  # hiding parent window

        self.__username = None  # username string
        self.__user_object = Username(self)  # username instance (from: src/user_utils.py -> Username())

        # settings

        self.grab_set()

        self.WIDTH = 425
        self.HEIGHT = 200
        self.x = int(self.winfo_screenwidth() / 2 - (self.WIDTH / 2))
        self.y = int(self.winfo_screenheight() / 2 - (self.HEIGHT / 2))

        self.title('EasyCrypto')
        self.geometry('{}x{}+{}+{}'.format(self.WIDTH, self.HEIGHT, self.x, self.y))
        self.resizable(False, False)
        self.iconphoto(True, tk.PhotoImage(file='resources/logo.png', master=self))
        self.protocol("WM_DELETE_WINDOW", self.correct_closing)
        self.log = Logger(__name__).default()

        # check internet connection

        if self.__user_object.get_users_list() is None:
            self.__username = None
            self.destroy()

        # images

        self.BG_IMG = tk.PhotoImage(file='resources/get_username_background.png', master=self)
        self.GO_IMG = tk.PhotoImage(file='resources/get_username_but.png', master=self)
        self.GO_IMAGE_HOV = tk.PhotoImage(file='resources/get_username_but.png', master=self)
        self.BACK_IMG = tk.PhotoImage(file='resources/backbut_little.png', master=self)

        # fonts and misc

        self.def_font = ('Arial Baltic', 16)
        self.explorer_files = [('Tutti i file', '*.*')]
        self.attachments = []
        self.data = tk.StringVar()

        # widgets

        self.bg = tk.Canvas(self, width=425, height=200)
        self.bg.create_image(214, 102, image=self.BG_IMG)
        self.back_id = self.bg.create_image(20, 185, image=self.BACK_IMG, tags='backbut')
        self.canva_id = self.bg.create_text(22, 153, text='Nickname troppo corto!', fill='red', anchor='w')
        self.entry = tk.Entry(self, width=19, font=self.def_font, relief='ridge', bd=2, textvariable=self.data)
        self.go_but = tk.Button(self, image=self.GO_IMG, borderwidth=0, bg='#160ca3', command=lambda: self.__go())

        # configuration and bindings

        self.go_but.bind("<Enter>", lambda _: self.go_but.config(image=self.GO_IMAGE_HOV))
        self.go_but.bind("<Leave>", lambda _: self.go_but.config(image=self.GO_IMG))
        self.data.trace_add('write', lambda *args: Username.check_nick(self.entry.get(), False, self.bg, self.canva_id))
        self.entry.focus_force()

        # placing

        self.bg.place(x=-2, y=-2)
        self.entry.place(x=20, y=105)
        self.go_but.place(x=297, y=105)

        # wait window event

        self.go_but.wait_window(self)

        try:
            if os.path.exists(USERS_LIST):
                os.remove(USERS_LIST)
        except PermissionError:
            self.log.warning("PermissionError", exc_info=True)

        self.__username = self.__user_object.username
        self.parent.deiconify()

    # methods

    def __go(self) -> None:
        """ Sets the nickname for the current user """
        self.__user_object.execute(self, entry=self.data, to_set=False, canva=self.bg, canva_id=self.canva_id)

    def get_username(self) -> str | None:
        """ Returns the username value """
        return self.__username

    def correct_closing(self) -> None:
        """ Closes the window after assigning the username value to None """
        self.__user_object.username = None
        self.destroy()
