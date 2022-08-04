import tkinter.ttk
import tkinter as tk
from typing import Literal
import tkinter.font as tkfont


class IssueGui(tk.Tk):
    def __init__(self, win):
        super().__init__()

        self.grab_set()

        self.width = 600
        self.height = 350
        self.icon = tk.PhotoImage(file='res/logo.png', master=self)
        self.x = int(self.winfo_screenwidth() / 2 - (self.width / 2))
        self.y = int(self.winfo_screenheight() / 2 - (self.height / 2))

        self.title('Effettua una segnalazione...')
        self.geometry('{}x{}+{}+{}'.format(self.width, self.height, self.x, self.y))
        self.resizable(False, False)
        self.iconphoto(True, self.icon)

        # fonts

        self.title_font = tkfont.Font(family='Calibri', size=14)
        self.labels_font = tkfont.Font(family='Calibri', size=13)
        self.text_font = tkfont.Font(family='Calibri', size=11)

        # text variables

        self.labels_var = tk.StringVar()

        # widgets

        self.title = tk.Entry(self, font=self.title_font, width=21, foreground='gray')
        self.tags = ['Bug', 'Aiuto', 'Domanda', 'Suggerimento']
        self.labels = tk.ttk.Combobox(self, width=11, state='readonly', takefocus=0, font=self.labels_font,
                                      foreground='darkgray', values=self.tags)
        self.text = tk.Text(self, width=50, height=15, font=self.text_font, foreground='gray', wrap='word')

        # configuration and bindings

        self.title_default = 'Titolo'
        self.box_default = 'Tipo'
        self.text_default = 'Inserisci una descrizione generale del problema...'
        self.title.insert(0, self.title_default)
        self.labels.set(self.box_default)
        self.text.insert(1.0, self.text_default)

        self.title.bind('<KeyRelease>', lambda char: self.empty_widget('title', char))
        self.text.bind('<KeyRelease>', lambda char: self.empty_widget('text', char))
        self.title.bind("<FocusOut>", lambda _: self.handle_unfocused_widget('title'))
        self.text.bind("<FocusOut>", lambda _: self.handle_unfocused_widget('text'))
        self.title.bind("<Control-BackSpace>", lambda _: self.ctrldel_delete('title'))
        self.text.bind("<Control-BackSpace>", lambda _: self.ctrldel_delete('text'))

        self.option_add("*TCombobox*Listbox*Font", self.labels_font)
        self.labels.bind('<<ComboboxSelected>>', lambda _: self.focus())

        # placing

        self.title.place(x=20, y=25)
        self.labels.place(x=252, y=25)
        self.text.place(x=20, y=60)

        self.mainloop()

    def empty_widget(self, widget: Literal['title', 'text'], char: tk.Event) -> None:
        key = char.__getattribute__('char')

        if widget == 'title':
            if not self.title.cget('foreground') == 'black':
                self.title.delete(0, tk.END)
                self.title.config(foreground='black')
                self.title.insert(0, key)
        else:
            if not self.text.cget('foreground') == 'black':
                self.text.delete(1.0, tk.END)
                self.text.config(foreground='black')
                self.text.insert(1.0, key)

    def handle_unfocused_widget(self, widget: Literal['title', 'text']) -> None:
        if widget == 'title':
            if self.title.get() == '':
                self.title.insert(0, self.title_default)
                self.title.config(foreground='gray')
        else:
            if self.text.get(1.0, tk.END) == '\n':
                self.text.insert(1.0, self.text_default)
                self.text.config(foreground='gray')

    def ctrldel_delete(self, widget: Literal['title', 'text']) -> None:
        if widget == 'title':

            text = self.title.get()
            if text == '':
                return

            index = self.title.index(tk.INSERT)
            before_idx = text[:index:][::-1]  # Reversed to manipulate it more easily
            after_idx = text[index::]

            fixed_bef_idx = IssueGui.space_correction(before_idx)  # Remove spaces that mess up the slicing
            result = fixed_bef_idx[fixed_bef_idx.find(' ')::][::-1]

            self.title.delete(0, tk.END)
            self.title.insert(0, result + after_idx)
            self.title.icursor(len(result))
            if not self.title.index(tk.INSERT) == 1:
                self.title.insert(tk.INSERT, ' ')

        else:

            text = self.text.get(1.0, tk.END)
            if text == '\n':
                return

            index = int(self.text.index(tk.INSERT).split('.')[1])
            column = int(self.text.index(tk.INSERT).split('.')[0])
            before_idx = text[:index:][::-1]  # Reversed to manipulate it more easily
            after_idx = text[index::].strip('\n')

            fixed_bef_idx = IssueGui.space_correction(before_idx)  # Remove spaces that mess up the slicing
            result = fixed_bef_idx[fixed_bef_idx.find(' ')::][::-1]

            if not result[-1] == ' ':
                result = result[:-1:]

            self.text.delete(0.0, tk.END)
            self.text.insert(0.0, result + after_idx)
            self.text.mark_set("insert", "{}.{}".format(column, len(result)))
            if not self.text.index(tk.INSERT).split('.')[1] == 1:
                self.text.insert(tk.INSERT, ' ')

    @staticmethod
    def space_correction(string: str) -> str:
        """Returns the same string without any spaces at the beginning"""
        for i in string:
            if i != ' ':
                return string
            return IssueGui.space_correction(string[1::])
