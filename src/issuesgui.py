import web
import tkinter.ttk
import tkinter as tk
from typing import Literal
import tkinter.font as tkfont
from tktooltip import ToolTip
from tkinter import filedialog


class IssueGui(
    tk.Toplevel):  # come evento aggiungi che copia link github negli appunti per esempio e vedi se fare che tsto default ritorna quando testo in binaoc
    def __init__(self, win):
        super().__init__()
        self.win = win
        win.withdraw()

        self.grab_set()

        self.width = 405
        self.height = 525
        self.icon = tk.PhotoImage(file='res/logo.png', master=self)
        self.x = int(self.winfo_screenwidth() / 2 - (self.width / 2))
        self.y = int(self.winfo_screenheight() / 2 - (self.height / 2))
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.explorer_files = [('Tutti i file', '*.*')]
        self.attachments = []

        self.title('Effettua una segnalazione...')
        self.geometry('{}x{}+{}+{}'.format(self.width, self.height, self.x, self.y))
        self.resizable(False, False)
        self.iconphoto(True, self.icon)

        # images

        self.BG_IMG = tk.PhotoImage(file='res/issuegui_background.png', master=self)
        self.BACKBUT_IMG = tk.PhotoImage(file='res/backbut.png', master=self)
        self.BACKBUT_IMG_HOV = tk.PhotoImage(file='res/backbut_hovered.png', master=self)
        self.SEND_IMG = tk.PhotoImage(file='res/send_issue_but.png', master=self)
        self.SEND_IMG_HOV = tk.PhotoImage(file='res/send_issue_but_hovered.png', master=self)
        self.MARKDOWN_IMG = tk.PhotoImage(file='res/markdown.png', master=self)
        self.MARKDOWN_IMG_HOV = tk.PhotoImage(file='res/markdown_hovered.png', master=self)

        # fonts

        self.title_font = tkfont.Font(family='Calibri', size=13)
        self.labels_font = tkfont.Font(family='Calibri', size=12)
        self.text_font = tkfont.Font(family='Calibri', size=11)

        # widgets

        self.bg = tk.Canvas(self, width=405, height=525)
        self.bg.create_image(204, 264, image=self.BG_IMG)
        self.mark_id = self.bg.create_image(269, 515, image=self.MARKDOWN_IMG, tags='markdown')
        self.title = tk.Entry(self, font=self.title_font, width=25, foreground='gray', relief='ridge', bd=2)
        self.tags = [' Bug', ' Aiuto', ' Domanda', ' Suggerimento']
        self.container = tk.Frame(self, width=120, height=27, relief='ridge', bd=1)
        self.labels = tk.ttk.Combobox(self.container, width=12, state='readonly', takefocus=0, font=self.labels_font,
                                      foreground='gray', values=self.tags)
        self.text = tk.Text(self, width=50, height=12, font=self.text_font, foreground='gray', wrap='word', padx=5,
                            pady=5, relief='ridge', bd=2)
        self.attach_but = tk.Button(self, width=35, height=1, command=self.get_attachments)
        self.remove_attach_but = tk.Button(self, width=5, height=1, command=self.remove_attachments)
        self.send_but = tk.Button(self, image=self.SEND_IMG, bd=0, bg='#1414b3', command=self.send_issue)
        self.back_lab = tk.Label(self, image=self.BACKBUT_IMG, bg='#f0f67c')

        # configuration and bindings

        self.title_default = ' Titolo'
        self.box_default = ' Tipo'
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
        self.back_lab.bind('<Button-1>', lambda _: self.close())
        self.back_lab.bind("<Enter>", lambda _: self.back_lab.config(image=self.BACKBUT_IMG_HOV))
        self.back_lab.bind("<Leave>", lambda _: self.back_lab.config(image=self.BACKBUT_IMG))
        self.send_but.bind("<Enter>", lambda _: self.send_but.config(image=self.SEND_IMG_HOV))
        self.send_but.bind("<Leave>", lambda _: self.send_but.config(image=self.SEND_IMG))
        self.bg.tag_bind('markdown', '<Button-1>', self.markdown_guide)
        self.bg.tag_bind('markdown', '<Enter>', lambda _: self.switch_markdown('hovered'))
        self.bg.tag_bind('markdown', '<Leave>', lambda _: self.switch_markdown('normal'))

        self.option_add("*TCombobox*Listbox*Font", self.labels_font)
        self.labels.bind('<<ComboboxSelected>>', lambda _: self.focus())

        # tooltips

        self.default_attach_text = 'Nessuno allegato selezionato!'
        self.attach_tip = ToolTip(self.attach_but, msg=self.default_attach_text, delay=0.5)

        # placing

        self.bg.place(x=-2, y=-2)
        self.title.place(x=20, y=122)
        self.container.place(x=262, y=122)
        self.labels.pack()
        self.text.place(x=20, y=158)
        self.attach_but.place(x=20, y=398)
        self.remove_attach_but.place(x=300, y=398)
        self.send_but.place(x=135, y=445)
        self.back_lab.place(x=6, y=480)

        self.mainloop()

    # functions

    def send_issue(self) -> None:
        pass

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

    def get_attachments(self) -> None:
        path = filedialog.askopenfilenames(title='Seleziona uno o più allegati...', filetypes=self.explorer_files)
        for i in path:
            if i not in self.attachments:
                self.attachments.append(i)

        self.attach_tip.__setattr__('msg', f'{len(self.attachments)} allegati: {str(self.attachments)}')

    def remove_attachments(self) -> None:

        self.attachments.clear()
        self.attach_tip.__setattr__('msg', self.default_attach_text)

    def switch_markdown(self, mode: Literal['normal', 'hovered']) -> None:

        if mode == 'normal':
            self.bg.itemconfig(self.mark_id, image=self.MARKDOWN_IMG)
        elif mode == 'hovered':
            self.bg.itemconfig(self.mark_id, image=self.MARKDOWN_IMG_HOV)

    @staticmethod
    def markdown_guide(*args) -> None:
        web.Browser(
            'https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax').search()

    def close(self) -> None:
        self.destroy()
        self.win.deiconify()
