#!/usr/bin/env python

from tkinter import TclError, Tk, Frame, Label, Button, Toplevel
from pyautogui import position as mouse_pos
from tkinter.messagebox import showinfo
from configparser import ConfigParser
from webbrowser import open_new_tab
from pyperclip import paste
from platform import system

from modules import scale, Option, Gauss_Sum, SquaresAPage, SquaresPPage, RectanglesPPage, \
                    ArithmeticsPage, QEquationPage, RectanglesAPage, Lin_EquationPage, \
                    Pythagorean_TheoremPage, Sq_RootPage, Cb_RootPage, Power_NumberPage
from modules.pages.task_template import TaskPageTemplate


__version__ = "0.8"
author = "TerraBoii"
pages = {
    # code: Page
    "0000": ArithmeticsPage,
    "0001": Cb_RootPage,
    "0002": Gauss_Sum,
    "0003": Lin_EquationPage,
    "0004": Pythagorean_TheoremPage,
    "0005": QEquationPage,
    "0006": RectanglesAPage,
    "0007": RectanglesPPage,
    "0008": Sq_RootPage,
    "0009": SquaresAPage,
    "0010": SquaresPPage,
    "0011": Power_NumberPage,
}

# File reading section
parser = ConfigParser()
parser.read("data.txt")
# Parameters:
x_pos = parser.get('parameters', 'x')
y_pos = parser.get('parameters', 'y')
WIDTH = 950
_state = parser.get('parameters', 'zoomed')
HEIGHT = 650
scaling = scale(WIDTH, HEIGHT) # Font scaling
# Language
lng_state = parser.get("language", 'state')
current_language = parser.get("language", "language")
# Colors and theme
current_theme = parser.get("theme", "theme")
fg = parser.get("theme", "fg")
afg = parser.get("theme", "afg")
dfg = parser.get("theme", "dfg")
bg = parser.get("theme", "bg")
b_bg = parser.get("theme", "b_bg")
b_bg1 = parser.get("theme", "b_bg1")
b_abg = parser.get("theme", "b_abg")
e_bg = parser.get("theme", "e_bg")
e_hl = parser.get("theme", "e_hl")
lfg = parser.get("theme", "lfg")


def change_language(language: str):  # This function changes language for whole application
    global parser, current_language, lng_state

    parser.read('data.txt')
    parser.set("language", 'state', 'keep')

    if language == "rus":
        parser.set('language', "language", 'rus')
    elif language == "eng":
        parser.set('language', "language", 'eng')

    with open("data.txt", "w") as configfile:
        parser.write(configfile)
    lng_state = parser.get('language', 'state')
    current_language = parser.get('language', 'language')


def light_theme():
    global parser

    parser.set('theme', "theme", "light")
    parser.set("theme", "fg", "#000000")
    parser.set("theme", "afg", "#3F3F3F")
    parser.set("theme", "dfg", "#696969")
    parser.set("theme", "bg", "#D9D9D9")
    parser.set("theme", "b_bg", "#BABABA")
    parser.set("theme", "b_bg1", "#C5C5C5")
    parser.set("theme", "b_abg", "#CFCFCF")
    parser.set("theme", "e_bg", "#EAEAEA")
    parser.set("theme", "e_hl", "#000000")
    parser.set("theme", "lfg", "#213c91")


def dark_theme():
    global parser

    parser.set('theme', "theme", "dark")
    parser.set("theme", "fg", "#969696")
    parser.set("theme", "afg", "#505050")
    parser.set("theme", "dfg", "#303030")
    parser.set("theme", "bg", "#272727")
    parser.set("theme", "b_bg", "#373737")
    parser.set("theme", "b_bg1", "#424242")
    parser.set("theme", "b_abg", "#303030")
    parser.set("theme", "e_bg", "#151515")
    parser.set("theme", "e_hl", "#171717")
    parser.set("theme", "lfg", "#2f5ceb")


def change_theme(theme: str):
    global parser, current_theme,fg, afg, dfg, bg, b_bg, b_bg1, b_abg, e_bg, e_hl, lfg

    parser.read("data.txt")

    match theme:
        case "light":
            light_theme()
        case "dark":
            dark_theme()

    with open("data.txt", "w") as configfile:
        parser.write(configfile)

    current_theme = parser.get("theme", "theme")
    fg = parser.get("theme", "fg")
    afg = parser.get("theme", "afg")
    dfg = parser.get("theme", "dfg")
    bg = parser.get("theme", "bg")
    b_bg = parser.get("theme", "b_bg")
    b_bg1 = parser.get("theme", "b_bg1")
    b_abg = parser.get("theme", "b_abg")
    e_bg = parser.get("theme", "e_bg")
    e_hl = parser.get("theme", "e_hl")
    lfg = parser.get("theme", "lfg")


def change_scaling(width: int, height: int):
    global scaling
    scaling = scale(width, height)


def save_window_parameters(_width_, _height_, _x_, _y_, _state_):
    # Saves given params to data.txt file
    global parser
    parser.read("data.txt")
    if _state_ == "0":
        parser.set('parameters', 'height', _height_)
        parser.set('parameters', 'width', _width_)
        parser.set('parameters', 'x', _x_)
        parser.set('parameters', 'y', _y_)
    else:
        parser.set('parameters', 'height', HEIGHT)
        parser.set('parameters', 'width', WIDTH)
        parser.set('parameters', 'x', x_pos)
        parser.set('parameters', 'y', y_pos)
    parser.set('parameters', 'zoomed', _state)
    with open("data.txt", 'w') as configfile:
        parser.write(configfile)


class App(Tk):  # Main application with page logic
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title(f"Math problem generator - {__version__}")

        try:
            self.iconbitmap("images//main_icon.ico")
        except TclError:
            print("Unable to find icon file")

        self.geometry(f"{WIDTH}x{HEIGHT}+{int((self.winfo_screenwidth() - WIDTH) / 2)}+{int((self.winfo_screenheight() - HEIGHT) / 2)}")  # Middle pos on the screen
        self.maxsize(self.winfo_screenwidth(), self.winfo_screenheight() - 31)
        self.minsize(800, 600)

        # Rewriting default delete method in order to save window parameters
        if system() == "Windows":
            self.protocol('WM_DELETE_WINDOW', self.delete_window)
        if _state == 'yes':
            self.state('zoomed')

        if lng_state == "ask" or current_language == "unknown":
            self.ch_page(FLaunchPage)
        elif lng_state == "keep":
            self.ch_page(MainPage)

        def scaling_scale(size): # Yea it is a good name, trust me.
            change_scaling(self.winfo_width(), self.winfo_height())

        self.bind("<Configure>", scaling_scale)
        self.change_bg()


    def delete_window(self):  # saves parameters and then deletes window
        if self.wm_state() == "zoomed" and lng_state != "ask" and current_language != "unknown":
            save_window_parameters(str(self.winfo_width()), str(self.winfo_height()),
                                   str(self.winfo_rootx()), str(self.winfo_rooty()), '1')
        elif self.wm_state() != "zoomed" and lng_state != "ask" and current_language != "unknown":
            save_window_parameters(str(self.winfo_width()), str(self.winfo_height()),
                                   str(self.winfo_rootx()), str(self.winfo_rooty()), '0')
        self.destroy()


    def ch_page(self, new: Frame, prev: Frame = None):
        if prev is not None:
            prev.pack_forget()
        new(self, current_language, __version__, TasksPage, bg, fg, afg, dfg, b_bg, b_bg1, b_abg, e_bg, e_hl).pack(fill="both", expand=True)


    def change_bg(self): self.config(bg=bg)


class FLaunchPage(Frame):  # This page launches when you need to choose language
    def __init__(self, parent, *_):
        Frame.__init__(self, parent, bg="black")
        self.parent = parent

        question = Label(self, text="\nChoose language:", bg="black", fg="#00ff00", font=('Arial', int(40 * scaling)))
        question.pack(side="top")

        bottom_ = Label(self, bg="black", text="Note: you can always change\nlanguage in settings menu", fg="#008000")
        bottom_.pack(side="bottom")

        lang_btn_container = Label(self, bg="black", justify="center")
        lang_btn_container.pack(expand=True)

        lang_btn_container.rowconfigure(0, weight=1)
        lang_btn_container.rowconfigure(1, weight=1)
        lang_btn_container.columnconfigure(0, weight=1)

        self.russian = Button(lang_btn_container, text="Русский", bg="black", fg="#00ff00",
                         activeforeground="#008000", bd=0, highlightbackground="black")
        self.russian.grid(row=0, column=0, sticky="nsew")

        self.english = Button(lang_btn_container, text="English", bg="black", fg="#00ff00",
                         activeforeground="#008000", bd=0, highlightbackground="black")
        self.english.grid(row=1, column=0, sticky="nsew")

        def entered(btn, lang: str):
            btn.config(bg="#008000", activebackground="#00ff00")
            _question_text = _hint_text = ''
            if lang == "eng":
                _question_text = "\nChoose language:"
                _hint_text = "You can always change\nlanguage in settings menu"
            elif lang == "rus":
                _question_text = "\nВыберите язык:"
                _hint_text = "Язык всегда можно\nизменить в настройках"
            question.config(text=_question_text)
            bottom_.config(text=_hint_text)

        def left(btn):
            btn.config(bg="black")

        self.english.bind("<Leave>", lambda _: left(btn=self.english))
        self.russian.bind("<Button-1>", lambda _: self.new_lang("rus", True))
        self.russian.bind("<Enter>", lambda _: entered(btn=self.russian, lang='rus'))
        self.english.bind("<Enter>", lambda _: entered(btn=self.english, lang='eng'))
        self.english.bind("<Button-1>", lambda _: self.new_lang("eng", True))
        self.russian.bind("<Leave>", lambda _: left(btn=self.russian))

        def font_resize_for_flaunchpage(width):
            if width.height <= 620:
                bottom_.config(font=('Arial', 30))
                question.config(font=('Arial', 40))
                self.russian.config(font=('Arial', 30))
                self.english.config(font=('Arial', 30))
            elif 620 < width.height <= 700:
                self.english.config(font=('Arial', 35))
                self.russian.config(font=('Arial', 35))
                question.config(font=('Arial', 45))
                bottom_.config(font=('Arial', 35))
            elif 700 < width.height <= 800:
                bottom_.config(font=('Arial', 40))
                question.config(font=('Arial', 50))
                self.russian.config(font=('Arial', 40))
                self.english.config(font=('Arial', 40))
            elif width.height > 800:
                self.english.config(font=('Arial', 45))
                self.russian.config(font=('Arial', 45))
                question.config(font=('Arial', 55))
                bottom_.config(font=('Arial', 45))

        self.bind("<Configure>", font_resize_for_flaunchpage)

    def new_lang(self, lang, this_page=False):
        change_language(lang)
        if this_page:
            self.parent.ch_page(MainPage, self)


class MainPage(Frame):
    def __init__(self, parent, *_):
        Frame.__init__(self, parent)
        self.parent = parent

        title = Label(self)
        title.pack(fill="both", expand=True)

        settings = Button(self, bd=0, command=lambda: parent.ch_page(SettingsPage, self))
        settings.pack(side="bottom", fill="both", ipady=20, pady=10)

        tasks = Button(self, bd=0, command=lambda: parent.ch_page(TaskCreationPage, self))
        tasks.pack(side="bottom", fill="x", ipady=20)

        game = Button(self, bd=0, command=lambda: parent.ch_page(GameOptPage, self))
        game.pack(side="bottom", fill="x", ipady=20, pady=10)

        self.title = title
        self.settings = settings
        self.tasks = tasks
        self.game = game

        def font_scaling(_):
            title.config(font=("Verdana", int(45 * scaling)))
            settings.config(font=("Verdana", int(35 * scaling)))
            tasks.config(font=("Verdana", int(35 * scaling)))
            game.config(font=("Verdana", int(35 * scaling)))

        self.bind("<Configure>", font_scaling)

        self.set_lang()
        self.set_theme()

    def set_lang(self):
        if current_language == "eng":
            self.title.config(text="Math problem generator")
            self.settings.config(text="Settings")
            self.tasks.config(text="Print tasks")
            self.game.config(text="Play the game")
        elif current_language == "rus":
            self.title.config(text="Генератор задач\nпо математике")
            self.settings.config(text="Настройки")
            self.tasks.config(text="Печатать задачи")
            self.game.config(text="Играть в игру")

    def set_theme(self):
        self.config(bg=bg)
        self.title.config(bg=bg, fg=fg)
        self.settings.config(bg=b_bg, fg=fg, activebackground=b_abg, activeforeground=afg)
        self.tasks.config(bg=b_bg1, fg=fg, activebackground=b_abg, activeforeground=afg)
        self.game.config(bg=b_bg, fg=fg, activebackground=b_abg, activeforeground=afg)


class GameOptPage(Frame): # Game Options Page

    def __init__(self, parent, *_):
        Frame.__init__(self, parent)
        self.parent = parent

        def other_page(code):

            match code:
                case 0:
                    page = TasksPage
                case 1:
                    page = ShowTaskPage
                case 2:
                    page = MainPage

            self.set_lang() # To reset info text
            parent.ch_page(page, self)

        def show_description(which:int, btn: Button):
            match current_language, which:
                case "eng", 0:
                    description = "Gives you list of all available\ntasks to choose from."
                case "rus", 0:
                    description = "Предоставляет вам список\nвсех возможных задач\nдля выбора одной."
                case "eng", 1:
                    description = "Allows you to get previously\ngenerated task or\ngenerate random one."
                case "rus", 1:
                    description = "Позволяет получить задачу\nпо её номеру, или создать\nодну совершенно случайную."
                case "eng", 2:
                    description = "Allows you to go back\nto previous page"
                case "rus", 2:
                    description = "Позволяет вернуться\nна предыдущую страницу"
            info.config(text="\"{}\"\n{}".format(btn['text'].replace('\n', ' '), description))

        container = Frame(self)
        container.pack(fill="both", expand=True, pady=(20, 20))

        options = Frame(container)
        options.pack(side="left", padx=(35, 0))

        tasks_list = Button(options, bd=0, command=lambda: other_page(0))
        tasks_list.pack(fill="both", expand=True, pady=(0, 5))
        tasks_list.bind("<Enter>", lambda _: show_description(0, tasks_list))

        show_task = Button(options, bd=0, command=lambda: other_page(1), state="disabled")
        show_task.pack(fill="both", expand=True, pady=10)
        show_task.bind("<Enter>", lambda _: show_description(1, show_task))

        back_btn = Button(options, bd=0, command=lambda: other_page(2))
        back_btn.pack(fill="both", expand=True, pady=(15, 0))
        back_btn.bind("<Enter>", lambda _: show_description(2, back_btn))

        info_c = Frame(container) # Info Container
        info_c.pack(side="right", padx=(0, 90))

        info = Label(info_c)
        info.pack()

        self.container = container
        self.options = options
        self.tasks_list = tasks_list
        self.show_task = show_task
        self.back_btn = back_btn
        self.info_c = info_c
        self.info = info

        def font_scaling(_):
            tasks_list.config(font=("Times New Roman", int(25 * scaling)))
            show_task.config(font=("Times New Roman", int(25 * scaling)))
            back_btn.config(font=("Times New Roman", int(25 * scaling), "bold"))
            info.config(font=("Times New Roman", int(25 * scaling)))

        self.bind("<Configure>", font_scaling)

        self.set_lang()
        self.set_theme()

    def set_lang(self):
        if current_language == "eng":
            self.back_btn.config(text="Back")
            self.tasks_list.config(text="List of all tasks")
            self.show_task.config(text="Show task by number")
            self.info.config(text="Hover over options on the left\nto see their description here.")
        elif current_language == "rus":
            self.back_btn.config(text="Назад")
            self.tasks_list.config(text="Список всех задач")
            self.show_task.config(text="Получить задачу\nпо номеру")
            self.info.config(text="Наведите курсор на один\nиз вариантов слева\nчтобы увидеть описание.")

    def set_theme(self):
        self.config(bg=bg)
        self.container.config(bg=bg)
        self.options.config(bg=bg)
        self.tasks_list.config(bg=b_bg, fg=fg, activebackground=b_abg, activeforeground=afg)
        self.show_task.config(bg=b_bg1, fg=fg, activebackground=b_abg, activeforeground=afg)
        self.back_btn.config(bg=b_bg, fg=fg, activebackground=b_abg, activeforeground=afg)
        self.info_c.config(bg=bg)
        self.info.config(bg=bg, fg=fg)


class TasksPage(Frame):
    def __init__(self, parent, *_):
        Frame.__init__(self, parent)

        self.fstate = 2

        def options(filter_t:bool=None):
            if filter_t is None:
                return list(pages.values())
            elif filter_t:
                return list(filter(lambda el: el.subject == 1, list(pages.values())))
            else:
                return list(filter(lambda el: el.subject == 0, list(pages.values())))

        def filter_():
            self.fstate += 1
            if self.fstate == 3:
                self.fstate = 0

            match self.fstate, current_language:
                case 0, "eng":
                    _filter.config(text="Algebra")
                case 0, "rus":
                    _filter.config(text="Алгебра")
                case 1, "eng":
                    _filter.config(text="Geometry")
                case 1, "rus":
                    _filter.config(text="Геометрия")
                case 2, "eng":
                    _filter.config(text="Filter")
                case 2, "rus":
                    _filter.config(text="Фильтр")
            self.task_pages = options(self.fstate if self.fstate != 2 else None)
            repack()

        def repack():
            for slave in menu.grid_slaves():
                slave.grid_forget()
            for i in range(len(self.task_pages[start:start + 16])):
                Option(menu, self, self.task_pages[i], i, parent, current_language, fg, b_bg, b_bg1, b_abg, afg).grid(row=(i % 8), column=(i // 8), padx=(0, 10), pady=(0, 15), sticky="snew")
            font_scaling(None)

        top = Frame(self)
        top.pack(pady=10, padx=65, fill="x")

        back = Button(top, bd=0, command=lambda: parent.ch_page(GameOptPage, self))
        back.pack(side="left")

        _filter = Button(top, bd=0, command=filter_)
        _filter.pack(side="right")

        self.task_pages = options()

        start = 0

        menu = Frame(self)
        menu.pack(pady=(20, 0))

        for i in range(len(self.task_pages[start:start + 16])):
            Option(menu, self, self.task_pages[i], i, parent, current_language, fg, b_bg, b_bg1, b_abg, afg).grid(row=(i % 6), column=(i // 6), padx=(0, 10), pady=(0, 15), sticky="snew")

        self.top = top
        self.back = back
        self._filter = _filter
        self.menu = menu

        def font_scaling(_):
            back.config(font=("Times New Roman", int(25 * scaling)))
            _filter.config(font=("Times New Roman", int(25 * scaling)))
            for slave in menu.grid_slaves():
                slave.config(font=("Times New Roman", int(25 * scaling)))

        self.bind("<Configure>", font_scaling)

        self.set_lang()
        self.set_theme()

    def set_lang(self):
        if current_language == "eng":
            self.back.config(text="Back")
            self._filter.config(text="Filter")
        elif current_language == "rus":
            self.back.config(text='Назад')
            self._filter.config(text="Фильтр")

    def set_theme(self):
        self.config(bg=bg)
        self.top.config(bg=bg)
        self.back.config(fg=fg, bg=b_bg1, activebackground=b_abg, activeforeground=afg)
        self._filter.config(fg=fg, bg=b_bg, activebackground=b_abg, activeforeground=afg)
        self.menu.config(bg=bg)


class TaskCreationPage(Frame):

    def __init__(self, parent, *_):
        Frame.__init__(self, parent)
        self.parent = parent

        back = Button(self, font=("Verdana", int(35 * scaling)), command=lambda: parent.ch_page(MainPage, self))
        back.pack(fill="both", expand=True)

        self.back = back

        self.set_lang()
        self.set_theme()

    def set_theme(self):
        self.config(bg=bg)
        self.back.config(bg=b_bg, fg=fg, activebackground=b_abg, activeforeground=afg)

    def set_lang(self):
        if current_language == "rus":
            self.back.config(text="В разработке  до 0.9")
        if current_language == "eng":
            self.back.config(text="Under maintenance untill 0.9")


class ShowTaskOptions(Toplevel):

    def __init__(self, parent):
        Toplevel.__init__(self, parent)

        self.title("Show tasks for generation")
        self.geometry("400x400")
        self.transient(parent)
        self.grab_set()


class ShowTaskPage(Frame):
    def __init__(self, parent, *_):
        Frame.__init__(self, parent)
        self.parent = parent

        page = TaskPageTemplate(self, parent, GameOptPage)
        page.pack(fill="both", expand=True)
        self.page = page

        def load_task():
            print("Task loaded.")
            ex = page.e_text.get("0.0", "end").replace("\n", "")
            task_seed, task_code = ex[:-4], ex[-4:]
            print(task_seed, task_code)
            # page.confirm_command(pages[task_code].confirm_c)
            # page.new_task_command(pages[task_code].new_task_c)
            print(pages[task_code].confirm)
            print("Nothing")

        def rand_task():
            print("Random task is generated.")

        def insert(_):
            if paste():
                print(paste())
                if all(el in page.allowed for el in paste()) and len(paste()) >= 5 and paste()[-4:] in pages.keys():
                    page.e_text.config(state='normal')
                    page.e_text.delete('0.0', "end")
                    page.e_text.insert('0.0', paste())
                    load_btn.config(state="normal")
                    page.e_text.config(state='disabled')

        # deconstruct page content in order to add new one 
        page.next.pack_forget()
        page.e_text.pack_forget()

        rand_btn = Button(page.b_cont, font=('Arial', int(32 * scaling)), bd=0, command=rand_task)
        rand_btn.pack(side="right", ipady=5, fill="x", expand=True, padx=(10, 0))

        page.next.pack(side="right", ipady=5, fill="x", expand=True, padx=0)

        load_btn = Button(page.top, font=('Arial', int(32 * scaling)), bd=0, state="disabled", command=load_task)
        load_btn.pack(pady=8, side='right')

        page.e_text.pack(fill="x", pady=8, side='right')
        page.e_text.bind("<1>", insert)

        self.rand_btn = rand_btn
        self.load_btn = load_btn

        self.set_lang()
        self.set_theme()


    def set_lang(self):
        self.page.set_lang(current_language, ["Click to paste exercise number.", "Нажмите, чтобы вставить номер задачи."])
        if current_language == "eng":
            self.load_btn.config(text="Load")
            self.rand_btn.config(text="Random task")
        elif current_language == "rus":
            self.load_btn.config(text="Загрузить")
            self.rand_btn.config(text="Случайное")


    def set_theme(self):
        self.page.set_theme(bg, fg, afg, dfg, b_bg, b_bg1, b_abg, e_bg, e_hl)
        self.load_btn.config(fg=fg, bg=b_bg, activebackground=b_abg, activeforeground=afg, disabledforeground=dfg)
        self.rand_btn.config(fg=fg, bg=b_bg, activebackground=b_abg, activeforeground=afg, disabledforeground=dfg)


class LangCont(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.states = ("normal", "disabled")

        self.l_title = Label(self)
        self.l_title.grid(row=0, column=0, sticky="nsew", pady=(0, 10))

        self.english = Button(self, command=lambda: parent.change_lang("eng"), text="English", state=self.states[current_language=="eng"], bd=0)
        self.english.grid(row=1, column=0, sticky="nsew", pady=(0, 5), ipadx=130)

        self.russian = Button(self, command=lambda: parent.change_lang("rus"), text="Русский", state=self.states[current_language=="rus"], bd=0)
        self.russian.grid(row=2, column=0, sticky="nsew", pady=(0, 5))

        self.back = Button(self, command=lambda: parent.show_opts(0), text="Back", bd=0)
        self.back.grid(row=3, column=0, sticky="nsew", pady=(10, 0))

    def lang(self):
        self.english.config(state=self.states[current_language=="eng"])
        self.russian.config(state=self.states[current_language=="rus"])
        if current_language == "eng":
            self.l_title.config(text="Change language to")
        elif current_language == "rus":
            self.l_title.config(text="Изменить язык на")

    def theme(self):
        self.config(bg=bg)
        self.l_title.config(bg=bg, fg=fg)
        self.english.config(fg=fg, bg=b_bg1, activeforeground=afg, activebackground=b_abg, disabledforeground=dfg)
        self.russian.config(fg=fg, bg=b_bg, activeforeground=afg, activebackground=b_abg, disabledforeground=dfg)
        self.back.config(fg=fg, activeforeground=afg, bg=b_bg1, activebackground=b_abg)


class ThemeCont(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.states = ("normal", "disabled")

        self.t_title = Label(self)
        self.t_title.grid(row=0, column=0, sticky="nsew", pady=(0, 10))

        self.light = Button(self, command=lambda: parent.change_theme_("light"), state=self.states[current_theme=="light"], bd=0)
        self.light.grid(row=1, column=0, sticky="nsew", pady=(0, 5), ipadx=130)

        self.dark = Button(self, command=lambda: parent.change_theme_("dark"), state=self.states[current_theme=="dark"], bd=0)
        self.dark.grid(row=2, column=0, sticky="nsew", pady=(0, 5))

        self.back = Button(self, command=lambda: parent.show_opts(0), text="Back", bd=0)
        self.back.grid(row=3, column=0, sticky="nsew", pady=(10, 0))

    def lang(self):
        if current_language == "eng":
            self.t_title.config(text="Change theme to")
            self.light.config(text="Light")
            self.dark.config(text="Dark")
        elif current_language == "rus":
            self.t_title.config(text="Изменить тему на")
            self.light.config(text="Светлая")
            self.dark.config(text="Тёмная")

    def theme(self):
        self.config(bg=bg)
        self.t_title.config(bg=bg, fg=fg)
        self.light.config(fg=fg, bg=b_bg1, activeforeground=afg, activebackground=b_abg, disabledforeground=dfg, state=self.states[current_theme=="light"])
        self.dark.config(fg=fg, bg=b_bg, activeforeground=afg, activebackground=b_abg, disabledforeground=dfg, state=self.states[current_theme=="dark"])
        self.back.config(fg=fg, activeforeground=afg, bg=b_bg1, activebackground=b_abg)


class SettingsPage(Frame):
    def __init__(self, parent, *_):
        Frame.__init__(self, parent)

        def call_link(_):
            open_new_tab("https://github.com/TerraBoii")

        def enter(_):
            created_by.config(font=("Tahoma", int(15 * scaling), "underline",))

        def leave(_):
            created_by.config(font=("Tahoma", int(15 * scaling)))

        created_by = Label(self, cursor='hand2')
        created_by.pack(side="top")
        created_by.bind("<Enter>", enter)
        created_by.bind("<Leave>", leave)
        created_by.bind("<Button-1>", call_link)

        _return = Button(self, command=lambda: parent.ch_page(MainPage, self), bd=0)
        _return.pack(side='bottom', pady=(0, 45), ipadx=45)

        def show_opts(_for):
            match _for:
                case 0:
                    container.pack(pady=(80, 15))
                    l_cont.pack_forget()
                    t_cont.pack_forget()
                case 1:
                    container.pack_forget()
                    l_cont.pack(pady=(80, 15))
                case 2:
                    container.pack_forget()
                    t_cont.pack(pady=(80, 15))
        self.show_opts = show_opts

        container = Frame(self)
        container.pack(pady=(80, 15))

        lang_o = Button(container, command=lambda: show_opts(1), bd=0)
        lang_o.grid(row=0, column=0, sticky="nsew", pady=(0, 5), ipadx=65)

        theme_o = Button(container, command=lambda: show_opts(2), bd=0)
        theme_o.grid(row=1, column=0, sticky="nsew", pady=(0, 5))

        l_cont = LangCont(self)

        t_cont = ThemeCont(self)

        self.created_by = created_by
        self._return = _return
        self.container = container
        self.lang_o = lang_o
        self.theme_o = theme_o
        self.l_cont = l_cont
        self.t_cont = t_cont

        def font_scaling(_):
            created_by.config(font=("Tahoma", int(15 * scaling)))
            _return.config(font=("Times New Roman", int(25 * scaling)))
            lang_o.config(font=("Times New Roman", int(25 * scaling)))
            theme_o.config(font=("Times New Roman", int(25 * scaling)))
            self.l_cont.l_title.config(font=("Times New Roman", int(25 * scaling)))
            self.l_cont.english.config(font=("Times New Roman", int(25 * scaling)))
            self.l_cont.russian.config(font=("Times New Roman", int(25 * scaling)))
            self.l_cont.back.config(font=("Times New Roman", int(25 * scaling)))
            self.t_cont.t_title.config(font=("Times New Roman", int(25 * scaling)))
            self.t_cont.light.config(font=("Times New Roman", int(25 * scaling)))
            self.t_cont.dark.config(font=("Times New Roman", int(25 * scaling)))
            self.t_cont.back.config(font=("Times New Roman", int(25 * scaling)))

        self.bind("<Configure>", font_scaling)

        self.set_lang()
        self.set_theme()

    def change_theme_(self, _to):
        change_theme(_to)
        self.set_theme()

    def change_lang(self, lang):
        FLaunchPage.new_lang(None, lang)
        self.l_cont.lang()
        self.set_lang()

    def set_lang(self):
        self.l_cont.lang()
        self.t_cont.lang()
        if current_language == "eng":
            self.created_by.config(text="Created by: TerraBoii")
            self._return.config(text="Go to the main page")
            self.lang_o.config(text="Change language")
            self.theme_o.config(text="Change theme")
        elif current_language == "rus":
            self.created_by.config(text="Создатель: TerraBoii")
            self._return.config(text="На главную страницу")
            self.lang_o.config(text="Изменить язык")
            self.theme_o.config(text="Изменить тему")

    def set_theme(self):
        self.config(bg=bg)
        self.created_by.config(bg=bg, fg=lfg)
        self._return.config(fg=fg, bg=b_bg, activeforeground=afg, activebackground=b_abg)
        self.container.config(bg=bg)
        self.lang_o.config(fg=fg, activeforeground=afg, bg=b_bg, activebackground=b_abg)
        self.theme_o.config(fg=fg, activeforeground=afg, bg=b_bg1, activebackground=b_abg)
        self.master.change_bg()
        self.l_cont.theme()
        self.t_cont.theme()


if __name__ == "__main__":
    App().mainloop()  # Launch application
