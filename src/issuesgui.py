import tkinter as tk
import tkinter.font as tkfont


class IssueGui(tk.Tk):
    def __init__(self, win):
        super().__init__()

        self.grab_set()

        self.width = 550
        self.height = 350
        self.icon = tk.PhotoImage(file='res/logo.png', master=self)
        self.x = int(self.winfo_screenwidth() / 2 - (self.width / 2))
        self.y = int(self.winfo_screenheight() / 2 - (self.height / 2))

        self.title('EasyCrypto')
        self.geometry('%ix%i+%i+%i' % (self.width, self.height, self.x, self.y))
        self.resizable(False, False)
        self.iconphoto(True, self.icon)

        # fonts

        self.text_font = tkfont.Font(family='Arial', size=10)
        self.bold_font = tkfont.Font(family='Arial', size=10, weight='bold')
        self.italic_font = tkfont.Font(family='Arial', size=10, slant='italic')
        self.underline_font = tkfont.Font(family='Arial', size=10, underline=True)
        self.bold_but_font = tkfont.Font(family='Verdana', size=14, weight='bold')
        self.italic_but_font = tkfont.Font(family='Verdana', size=14, slant='italic')
        self.underline_but_font = tkfont.Font(family='Verdana', size=14, underline=True)

        # widgets

        self.text_font = tkfont.Font(family='Arial', size=10)
        self.text = tk.Text(self, width=50, height=15, font=self.text_font)
        self.bold_but = tk.Button(self, text='B', font=self.bold_but_font, command=self.set_bold)
        self.italic_but = tk.Button(self, text='I', font=self.italic_but_font)
        self.underlined_but = tk.Button(self, text='U', font=self.underline_but_font)

        # placing

        self.text.place(x=50, y=50)
        self.bold_but.place(x=475, y=50)
        self.italic_but.place(x=475, y=100)
        self.underlined_but.place(x=475, y=150)

        self.mainloop()

    def set_bold(self):
        self.text.tag_add('bold', '1.1', '1.2')
        print('here')

        print(self.text.tag_cget('bold', 'font'))
        if self.text.tag_cget('bold', 'font') == 'font8':
            self.text.tag_config('bold', font=self.bold_font)
        else:
            self.text.tag_config('bold', font=self.text_font)

        self.text.tag_delete('bold')
