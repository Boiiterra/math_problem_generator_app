from tkinter import TclError, Tk, Frame, Label, Button, Entry, Text, Toplevel
from pyautogui import position as mouse_pos
from tkinter.messagebox import showinfo
from configparser import ConfigParser
from webbrowser import open_new_tab
from platform import system
from pyperclip import copy

from modules import perimeter_task, area_task, square_equation, create_tool_tip, scale

__version__ = "0.7"
author = "TerraBoii"

# File reading section
parser = ConfigParser()
parser.read("data.txt")
# Parameters:
x_pos = parser.get('parameters', 'x')
y_pos = parser.get('parameters', 'y')
WIDTH = 950
_state = parser.get('parameters', 'zoomed')
HEIGHT = 650
scaling = scale(WIDTH, HEIGHT, 1) # Font scaling
# Language
lng_state = parser.get("language", 'state')
current_language = parser.get("language", "language")
# Colors and theme

T_FONT = ("Verdana", 45) # Title font
M_FONT = ("Verdana", 35) # Menu font
M_FONT1 = ("Times New Roman", 25) # Menu font 1
C_FONT = ("Tahoma", 15) # Creator font
A20 = ("Arial", 20)
A27 = ("Arial", 27)
A30 = ('Arial', 30)
A32 = ('Arial', 32)
A35 = ('Arial', 35)
A40 = ('Arial', 40)
A45 = ('Arial', 45)
A50 = ('Arial', 50)
A55 = ('Arial', 55)
V35 = ("Verdana", 35)

fg = "#000000"
afg = "#3F3F3F" # Active Foreground
dfg = "#696969" # Disabled foreground
bg = "#D9D9D9"
b_bg = "#BABABA" # Button background 1
b_bg1 = "#C5C5C5" # Button background 2
b_abg = "#CFCFCF" # Button active background 
e_bg = "#EAEAEA" # Entry background
e_hl = "#000000" # Entry highlight


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


def change_scaling(width: int, height: int):
    global scaling
    scaling = scale(width, height, scaling)


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


class TaskPageTemplate(Frame):
    allowed = "0123456789-"
    exercise = None

    def __init__(self, parent: Frame, app):
        Frame.__init__(self, parent)

        top = Frame(self)
        top.pack(fill="x", pady=8)

        e_label = Label(top, font=A27)
        e_label.pack(side="left", padx=2, pady=5)

        def do_copy(_):
            if self.exercise is not None:
                copy(self.exercise)

        e_text = Text(top, font=A27, borderwidth=0, height=1, state="disabled", cursor="", highlightthickness=0)
        e_text.pack(fill="x", pady=8, side='right')
        e_text.bind("<Button-1>", do_copy)

        task = Label(self, font=A20, anchor='center')
        task.pack(pady=4, expand=True)

        b_cont = Label(self)
        b_cont.pack(fill="x", padx=15, side="bottom")

        cont = Frame(self)
        cont.pack(pady=(0, 6), side="bottom")

        a_label = Label(cont, font=A32)
        a_label.grid(row=0, column=0)

        is_valid = (parent.register(self.validator), '%d', '%i', '%P') # '%d' -> action, '%i' -> index, '%P' -> value

        answer_field = Entry(cont, font=A32, width=6, border=0, validatecommand=is_valid, validate="key")
        answer_field.grid(row=0, column=1, padx=15)

        confirm_btn = Button(cont, font=A32, bd=0, state="disabled")
        confirm_btn.grid(row=0, column=2)

        def go_back():
            self.answer_field["state"] = "disabled"
            app.ch_page(TasksPage, parent)

        back = Button(b_cont, font=A32, bd=0, command=go_back)
        back.pack(side="left", ipady=5, fill="x", expand=True, padx=(0, 10))

        next = Button(b_cont, font=A32, bd=0)
        next.pack(side="right", ipady=5, fill="x", expand=True, padx=(10, 0))

        self.top = top
        self.e_label = e_label
        self.e_text = e_text
        self.task = task
        self.b_cont = b_cont
        self.cont = cont
        self.a_label = a_label
        self.answer_field = answer_field
        self.confirm_btn = confirm_btn
        self.back = back
        self.next = next

        self.set_lang()
        self.set_theme()

    def set_exercise(self, exercise: float):
        self.exercise = exercise
        self.e_text.config(state="normal")
        self.e_text.delete("0.0", "end")
        self.e_text.insert("end", exercise)
        self.e_text.config(state="disabled")

    def change_task_text(self, new_text: str):
        self.task.config(text=new_text)

    def new_task_command(self, command):
        self.next.config(command=command)

    def confirm_command(self, command):
        self.confirm_btn.config(command=command)

    def change_allowed(self, _to: str):
        self.allowed = _to

    def clear(self):
        self.answer_field.delete(0, "end")

    def validator(self, action, index, value):
        """Enter only integer values with length limit"""
        if value != "":
            if (index == "0" and value[0] == "0") or (index == "1" and value[0:2] == "-0"):
                return False
            if len(value) >= 7:
                return False
        if index != "0" and value[-1] == "-" and action == "1":
            return False
        # Confirm button status
        if value == "" and index == "0" and all(symbol in self.allowed for symbol in value):
            self.confirm_btn.config(state="disabled")
        elif "0" == index < "6" and all(symbol in self.allowed for symbol in value):
            self.confirm_btn.config(state="normal")
        # Entry validation
        if len(self.answer_field.get()) >= 6 and index != "5" and action == "1":  # Limiting input length
            return False
        elif all(symbol in self.allowed for symbol in value):  # Allowed values
            return True
        else:
            return False

    def set_theme(self):
        self.config(bg=bg)
        self.top.config(bg=bg)
        self.e_label.config(bg=bg, fg=fg)
        self.e_text.config(bg=bg, fg=fg)
        self.task.config(bg=bg, fg=fg)
        self.b_cont.config(bg=bg)
        self.cont.config(bg=bg)
        self.a_label.config(bg=bg, fg=fg)
        self.confirm_btn.config(fg=fg, bg=b_bg, activebackground=b_abg, activeforeground=afg, disabledforeground=dfg)
        self.back.config(fg=fg, bg=b_bg, activebackground=b_abg, activeforeground=afg)
        self.next.config(fg=fg, bg=b_bg1, activebackground=b_abg, activeforeground=afg, disabledforeground=dfg)
        self.answer_field.config(fg=fg, highlightbackground=e_hl, bg=e_bg)

    def set_lang(self):
        if current_language == "eng":
            self.e_label.config(text="Exercise:")
            self.a_label.config(text="Answer:")
            self.back.config(text="Back")
            self.next.config(text="New task")
            self.confirm_btn.config(text="Confirm")
            create_tool_tip(self.e_text, "Click to copy exercise number.", 10)
        elif current_language == "rus":
            self.e_label.config(text="Номер:")
            self.a_label.config(text="Ответ:")
            self.back.config(text="Назад")
            self.next.config(text="Новая задача")
            self.confirm_btn.config(text="Подтвердить")
            create_tool_tip(self.e_text, "Нажмите, чтобы скопировать номер задачи.", 10)


class Option(Button):
    def __init__(self, parent: Frame, _from: Frame, destination: Frame, number: int, _app):
        Button.__init__(self, parent, text=destination.task[current_language], font=M_FONT1, bd=0, fg=fg, bg=(b_bg if number % 2 == 0 else b_bg1), activebackground=b_abg, activeforeground=afg, command=lambda: _app.ch_page(destination, _from))

    def grid(self, **kwargs):
        self.grid_configure(kwargs)


class App(Tk):  # Main application with page logic

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title(f"Math problem generator - {__version__}")
        try:
            self.iconbitmap("images//main_icon.ico")
        except TclError:
            print("Unable to find icon file")
        self.geometry(f"{WIDTH}x{HEIGHT}+{int((self.winfo_screenwidth() - WIDTH) / 2)}+{int((self.winfo_screenheight() - HEIGHT) / 2)}")  # Middle pos on the screen
        self.resizable(0, 0)

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
        new(self).pack(fill="both", expand=True)


class FLaunchPage(Frame):  # This page launches when you need to choose language

    def __init__(self, parent):
        Frame.__init__(self, parent, bg="black")
        self.parent = parent

        question = Label(self, text="\nChoose language:", bg="black", fg="#00ff00", font=A40)
        question.pack(side="top")

        bottom_ = Label(self, bg="black", text="Note: you can always change\nlanguage in settings menu", font=A30, fg="#008000")
        bottom_.pack(side="bottom")

        lang_btn_container = Label(self, bg="black", justify="center")
        lang_btn_container.pack(expand=True)

        lang_btn_container.rowconfigure(0, weight=1)
        lang_btn_container.rowconfigure(1, weight=1)
        lang_btn_container.columnconfigure(0, weight=1)

        self.russian = Button(lang_btn_container, text="Русский", bg="black", fg="#00ff00",
                         activeforeground="#008000", font=A30, bd=0, highlightbackground="black")
        self.russian.grid(row=0, column=0, sticky="nsew")

        self.english = Button(lang_btn_container, text="English", bg="black", fg="#00ff00",
                         activeforeground="#008000", font=A30, bd=0, highlightbackground="black")
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
                bottom_.config(font=A30)
                question.config(font=A40)
                self.russian.config(font=A30)
                self.english.config(font=A30)
            elif 620 < width.height <= 700:
                self.english.config(font=A35)
                self.russian.config(font=A35)
                question.config(font=A45)
                bottom_.config(font=A35)
            elif 700 < width.height <= 800:
                bottom_.config(font=A40)
                question.config(font=A50)
                self.russian.config(font=A40)
                self.english.config(font=A40)
            elif width.height > 800:
                self.english.config(font=A45)
                self.russian.config(font=A45)
                question.config(font=A55)
                bottom_.config(font=A45)

        self.bind("<Configure>", font_resize_for_flaunchpage)

    def new_lang(self, lang, this_page=False):
        change_language(lang)
        if this_page:
            self.parent.ch_page(MainPage, self)


class MainPage(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent

        title = Label(self, font=T_FONT)
        title.pack(fill="both", expand=True)

        settings = Button(self, bd=0, font=M_FONT, command=lambda: parent.ch_page(SettingsPage, self))
        settings.pack(side="bottom", fill="both", ipady=30, pady=10)

        tasks = Button(self, bd=0, font=M_FONT, command=lambda: parent.ch_page(TaskCreationPage, self))
        tasks.pack(side="bottom", fill="x", ipady=20)

        game = Button(self, bd=0, font=M_FONT, command=lambda: parent.ch_page(GameOptPage, self))
        game.pack(side="bottom", fill="x", ipady=20, pady=10)

        self.title = title
        self.settings = settings
        self.tasks = tasks
        self.game = game

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
        self.settings.config(bg=b_bg, activebackground=b_abg, activeforeground=afg)
        self.tasks.config(bg=b_bg1, activebackground=b_abg, activeforeground=afg)
        self.game.config(bg=b_bg, activebackground=b_abg, activeforeground=afg)


class GameOptPage(Frame): # Game Options Page

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent

        def other_page(code):

            match code:
                case 0:
                    page = TasksPage
                case 1:
                    page = TaskCreationPage#ShowTaskPage
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

        tasks_list = Button(options, bd=0, font=M_FONT1, command=lambda: other_page(0))
        tasks_list.pack(fill="both", expand=True, pady=(0, 5))
        tasks_list.bind("<Enter>", lambda _: show_description(0, tasks_list))

        show_task = Button(options, bd=0, font=M_FONT1, command=lambda: other_page(1))
        show_task.pack(fill="both", expand=True, pady=10)
        show_task.bind("<Enter>", lambda _: show_description(1, show_task))

        back_btn = Button(options, font=M_FONT1+("bold",), bd=0, command=lambda: other_page(2))
        back_btn.pack(fill="both", expand=True, pady=(15, 0))
        back_btn.bind("<Enter>", lambda _: show_description(2, back_btn))

        info_c = Frame(container) # Info Container
        info_c.pack(side="right", padx=(0, 90))

        info = Label(info_c, font=M_FONT1)
        info.pack()

        self.container = container
        self.options = options
        self.tasks_list = tasks_list
        self.show_task = show_task
        self.back_btn = back_btn
        self.info_c = info_c
        self.info = info

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
    def __init__(self, parent):
        Frame.__init__(self, parent)

        top = Frame(self)
        top.pack(pady=10, padx=65, fill="x")

        back = Button(top, font=M_FONT1, bd=0, command=lambda: parent.ch_page(GameOptPage, self))
        back.pack(side="left")

        _filter = Button(top, font=M_FONT1, bd=0)
        _filter.pack(side="right")

        options = [QEquationPage, RectanglesAPage, RectanglesPPage, SquaresAPage, SquaresPPage]

        menu = Frame(self)
        menu.pack(pady=(20, 0))

        for i in range(len(options)):
            Option(menu, self, options[i], i, parent).grid(row=(i % 8), column=(i // 8), padx=(0, 10), pady=(0, 15), sticky="snew")

        self.top = top
        self.back = back
        self._filter = _filter
        self.menu = menu

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


class QEquationPage(Frame):
    task = {"eng": "Quadratic equation", "rus": "Квадратное уравнение"}

    def __init__(self, parent):
        Frame.__init__(self, parent)

        page = TaskPageTemplate(self, parent)
        page.pack(fill="both", expand=True)

        self.exercise_no = None
        self.x1 = None
        self.x2 = None
        self.param = None
        self.answer = None
        self.text_e = None
        self.text_r = None
        self.task_type = None

        def new_task(full_reset: bool = True):
            if full_reset:
                task_data = square_equation(__version__, self.winfo_width(), self.winfo_height(), 
                                            self.winfo_screenwidth(), self.winfo_screenheight())
                self.x1 = task_data[0]
                self.x2 = task_data[1]

                if self.x1 != 0 and self.x2 != 0:
                    if self.x1 > self.x2:
                        self.answer = self.x2
                        self.task_type = 1
                    elif self.x1 < self.x2:
                        self.answer = self.x2
                        self.task_type = 2
                    else:
                        self.answer = self.x2
                        self.task_type = 3
                elif self.x1 == 0 and self.x2 > self.x1:
                    self.answer = self.x2
                    self.task_type = 2
                elif self.x1 == 0 and self.x2 < self.x1:
                    self.answer = self.x1
                    self.task_type = 1
                elif self.x2 == 0 and self.x1 > self.x2:
                    self.answer = self.x1
                    self.task_type = 2
                elif self.x2 == 0 and self.x1 < self.x2:
                    self.answer = self.x1
                    self.task_type = 1

                extra_text_e = ""
                extra_text_r = ""
                if self.task_type == 1:
                    extra_text_e = "Find the smallest equation's root."
                    extra_text_r = "Найдите наименьший корень уравнения."
                elif self.task_type == 2:
                    extra_text_e = "Find the biggest equation's root."
                    extra_text_r = "Найдите наибольший корень уравнения."
                elif self.task_type == 3:
                    extra_text_e = "Find any equation's root."
                    extra_text_r = "Найдите любой корень уравнения"

                self.exercise_no = task_data[-1]
                self.param = task_data[-2]
                self.text_e = f"{self.param}\n" + extra_text_e
                self.text_r = f"{self.param}\n" + extra_text_r

                page.set_exercise(self.exercise_no)

                if current_language == "eng":
                    page.change_task_text(self.text_e)
                elif current_language == "rus":
                    page.change_task_text(self.text_r)

            if current_language == "eng":
                page.confirm_btn.config(text="Confirm")
            elif current_language == "rus":
                page.confirm_btn.config(text="Подтвердить")

        def activate():
            page.next.config(state='normal')
            page.answer_field.config(state='normal')

        def confirm():
            page.next.config(state='disabled')
            _input = 0
            if page.answer_field.get() != "-":
                _input = int(page.answer_field.get())
            else:
                page.answer_field.insert("end", 1)
            page.clear()
            page.answer_field.config(state='disabled')
            self.after(1000, activate)
            if _input == self.answer:
                if current_language == "eng":
                    page.confirm_btn.config(text="Correct", state="disabled")
                elif current_language == "rus":
                    page.confirm_btn.config(text="Правильно", state="disabled")
                self.after(500, new_task)
            else:
                if current_language == "eng":
                    page.confirm_btn.config(text="Wrong", state="disabled")
                elif current_language == "rus":
                    page.confirm_btn.config(text="Неправильно", state="disabled")
                self.after(500, lambda: new_task(False))

        page.new_task_command(new_task)
        page.confirm_command(confirm)

        parent.bind('<Return>', lambda _: page.confirm_btn.invoke())
        parent.bind('<KP_Enter>', lambda _: page.confirm_btn.invoke())


class SquaresAPage(Frame):
    task = {"eng": "Square's area", "rus": "Площадь квадрата"}

    def __init__(self, parent):
        Frame.__init__(self, parent)

        page = TaskPageTemplate(self, parent)
        page.pack(fill="both", expand=True)
        page.change_allowed("0123456789")

        self.exercise_no = None
        self.param = None
        self.answer = None
        self.text_e = None
        self.text_r = None

        def new_task(full_reset: bool = True):
            if full_reset:
                task_data = area_task('square', __version__, self.winfo_width(), self.winfo_height(), 
                                      self.winfo_screenwidth(), self.winfo_screenheight())
                self.exercise_no = task_data[-1]
                self.answer = task_data[1]
                self.param = task_data[0]
                self.text_e = f"Your goal is to find square's area.\nIts side is {self.param}."
                self.text_r = f"Чему равна площадь квадрата,\nесли его сторона равна {self.param}."
                page.set_exercise(self.exercise_no)
                if current_language == "eng":
                    page.change_task_text(self.text_e)
                elif current_language == "rus":
                    page.change_task_text(self.text_r)

            if current_language == "eng":
                page.confirm_btn.config(text="Confirm")
            elif current_language == "rus":
                page.confirm_btn.config(text="Подтвердить")

        def activate():
            page.next.config(state='normal')
            page.answer_field.config(state='normal')

        def confirm():
            page.next.config(state='disabled')
            _input = int(page.answer_field.get())
            page.clear()
            page.answer_field.config(state='disabled')
            self.after(1000, activate)
            if _input == self.answer:
                if current_language == "eng":
                    page.confirm_btn.config(text="Correct", state="disabled")
                elif current_language == "rus":
                    page.confirm_btn.config(text="Правильно", state="disabled")
                self.after(500, new_task)
            else:
                if current_language == "eng":
                    page.confirm_btn.config(text="Wrong", state="disabled")
                elif current_language == "rus":
                    page.confirm_btn.config(text="Неправильно", state="disabled")
                self.after(500, lambda: new_task(False))

        page.new_task_command(new_task)
        page.confirm_command(confirm)

        parent.bind('<Return>', lambda _: page.confirm_btn.invoke())
        parent.bind('<KP_Enter>', lambda _: page.confirm_btn.invoke())


class RectanglesAPage(Frame):
    task = {"eng": "Rectangle's area", "rus": "Площадь прямоугольника"}

    def __init__(self, parent):
        Frame.__init__(self, parent)

        page = TaskPageTemplate(self, parent)
        page.pack(fill="both", expand=True)
        page.change_allowed("0123456789")

        self.exercise_no = None
        self.param = None
        self.answer = None
        self.text_e = None
        self.text_r = None

        def new_task(full_reset: bool = True):
            if full_reset:
                task_data = area_task('rectangle', __version__, self.winfo_width(), self.winfo_height(), 
                                        self.winfo_screenwidth(), self.winfo_screenheight())
                self.answer = task_data[2]
                self.exercise_no = task_data[-1]
                self.param = (task_data[0], task_data[1])
                self.text_e = "Your goal is to find rectangle's area." \
                              f"\nIts height is {self.param[0]} and width is {self.param[1]}."
                self.text_r = "Чему равна площадь прямоугольника,\nесли его высота равна " \
                              f"{self.param[0]}, а ширина {self.param[1]}."
                page.set_exercise(self.exercise_no)
                if current_language == "eng":
                    page.change_task_text(self.text_e)
                elif current_language == "rus":
                    page.change_task_text(self.text_r)

            if current_language == "eng":
                page.confirm_btn.config(text="Confirm")
            elif current_language == "rus":
                page.confirm_btn.config(text="Подтвердить")

        def activate():
            page.next.config(state='normal')
            page.answer_field.config(state='normal')

        def confirm():
            page.next.config(state='disabled')
            _input = int(page.answer_field.get())
            page.clear()
            page.answer_field.config(state='disabled')
            self.after(1000, activate)
            if _input == self.answer:
                if current_language == "eng":
                    page.confirm_btn.config(text="Correct", state="disabled")
                elif current_language == "rus":
                    page.confirm_btn.config(text="Правильно", state="disabled")
                self.after(500, new_task)
            else:
                if current_language == "eng":
                    page.confirm_btn.config(text="Wrong", state="disabled")
                elif current_language == "rus":
                    page.confirm_btn.config(text="Неправильно", state="disabled")
                self.after(500, lambda: new_task(False))

        page.new_task_command(new_task)
        page.confirm_command(confirm)

        parent.bind('<Return>', lambda _: page.confirm_btn.invoke())
        parent.bind('<KP_Enter>', lambda _: page.confirm_btn.invoke())


class SquaresPPage(Frame):
    task = {"eng": "Square's perimeter", "rus": "Периметр квадрата"}

    def __init__(self, parent):
        Frame.__init__(self, parent)

        page = TaskPageTemplate(self, parent)
        page.pack(fill="both", expand=True)
        page.change_allowed("0123456789")

        self.exercise_no = None
        self.param = None
        self.answer = None
        self.text_e = None
        self.text_r = None

        def new_task(full_reset: bool = True):
            if full_reset:
                task_data = perimeter_task('square', __version__, self.winfo_width(), self.winfo_height(), 
                                           self.winfo_screenwidth(), self.winfo_screenheight())
                self.exercise_no = task_data[-1]
                self.answer = task_data[1]
                self.param = task_data[0]
                self.text_e = f"Your goal is to find square's perimeter.\nIts side is {self.param}."
                self.text_r = f"Чему равен периметр квадрата,\nесли его сторона равна {self.param}."
                page.set_exercise(self.exercise_no)
                if current_language == "eng":
                    page.change_task_text(self.text_e)
                elif current_language == "rus":
                    page.change_task_text(self.text_r)

            if current_language == "eng":
                page.confirm_btn.config(text="Confirm")
            elif current_language == "rus":
                page.confirm_btn.config(text="Подтвердить")

        def activate():
            page.next.config(state='normal')
            page.answer_field.config(state='normal')

        def confirm():
            page.next.config(state='disabled')
            _input = int(page.answer_field.get())
            page.clear()
            page.answer_field.config(state='disabled')
            self.after(1000, activate)
            if _input == self.answer:
                if current_language == "eng":
                    page.confirm_btn.config(text="Correct", state="disabled")
                elif current_language == "rus":
                    page.confirm_btn.config(text="Правильно", state="disabled")
                self.after(500, new_task)
            else:
                if current_language == "eng":
                    page.confirm_btn.config(text="Wrong", state="disabled")
                elif current_language == "rus":
                    page.confirm_btn.config(text="Неправильно", state="disabled")
                self.after(500, lambda: new_task(False))

        page.new_task_command(new_task)
        page.confirm_command(confirm)

        parent.bind('<Return>', lambda _: page.confirm_btn.invoke())
        parent.bind('<KP_Enter>', lambda _: page.confirm_btn.invoke())


class RectanglesPPage(Frame):
    task = {"eng": "Rectangle's perimeter", "rus": "Периметр прямоугольника"}

    def __init__(self, parent):
        Frame.__init__(self, parent)

        page = TaskPageTemplate(self, parent)
        page.pack(fill="both", expand=True)

        # Variables:
        self.exercise_no = None
        self.param = None
        self.answer = None
        self.text_e = None
        self.text_r = None

        def new_task(full_reset: bool = True):
            if full_reset:
                task_data = perimeter_task('rectangle', __version__, self.winfo_width(), self.winfo_height(), 
                                           self.winfo_screenwidth(), self.winfo_screenheight())
                self.answer = task_data[2]
                self.exercise_no = task_data[-1]
                self.param = (task_data[0], task_data[1])
                self.text_e = "Your goal is to find rectangle's perimeter." \
                              f"\nIts height is {self.param[0]} and width is {self.param[1]}."
                self.text_r = "Чему равен периметр прямоугольника,\nесли его высота равна " \
                              f"{self.param[0]}, а ширина {self.param[1]}."
                page.set_exercise(self.exercise_no)
                if current_language == "eng":
                    page.change_task_text(self.text_e)
                elif current_language == "rus":
                    page.change_task_text(self.text_r)

            if current_language == "eng":
                page.confirm_btn.config(text="Confirm")
            elif current_language == "rus":
                page.confirm_btn.config(text="Подтвердить")

        def activate():
            page.answer_field.config(state='normal')
            page.next.config(state='normal')

        def confirm():
            page.next.config(state='disabled')
            _input = int(page.answer_field.get())
            page.clear()
            page.answer_field.config(state='disabled')
            self.after(1000, activate)
            if _input == self.answer:
                if current_language == "eng":
                    page.confirm_btn.config(text="Correct", state="disabled")
                elif current_language == "rus":
                    page.confirm_btn.config(text="Правильно", state="disabled")
                self.after(500, new_task)
            else:
                if current_language == "eng":
                    page.confirm_btn.config(text="Wrong", state="disabled")
                elif current_language == "rus":
                    page.confirm_btn.config(text="Неправильно", state="disabled")
                self.after(500, lambda: new_task(False))

        page.new_task_command(new_task)
        page.confirm_command(confirm)

        parent.bind('<Return>', lambda _: page.confirm_btn.invoke())
        parent.bind('<KP_Enter>', lambda _: page.confirm_btn.invoke())


class TaskCreationPage(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent

        back = Button(self, font=V35, command=lambda: parent.ch_page(MainPage, self))
        back.pack(fill="both", expand=True)

        self.back = back

        self.set_lang()

    def set_lang(self):
        if current_language == "rus":
            self.back.config(text="В разработке")
        if current_language == "eng":
            self.back.config(text="Under maintenance")


class ShowTaskOptions(Toplevel):

    def __init__(self, parent):
        Toplevel.__init__(self, parent)

        self.title("Show tasks for generation")
        self.geometry("400x400")
        self.transient(parent)
        self.grab_set()


class ShowTaskPage(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent

        def load_task():
            print("Task loaded.")

        def rand_task():
            print("Random task is generated.")

        btn_container = Label(self)
        btn_container.pack(side="bottom", fill="x")
        self.btn_container = btn_container

        btn_container.rowconfigure(0, weight=1)
        btn_container.columnconfigure(0, weight=1)
        btn_container.columnconfigure(1, weight=1)
        btn_container.columnconfigure(2, weight=1)

        is_valid = (parent.register(self.validate), '%d', '%i', '%P') # action, index, value

        exercise = Entry(self, font=A27, borderwidth=0, highlightthickness=0, validatecommand=is_valid, validate="key")
        exercise.pack(fill="x", pady=8, side='top')
        self.exercise = exercise

        return_btn = Button(btn_container, font=A32, command=lambda: parent.ch_page(MainPage, self), bd=0)
        return_btn.grid(row=0, column=0, sticky='nsew', ipady=5, padx=1)
        self.return_btn = return_btn

        rand_btn = Button(btn_container, font=A32, bd=0, command=rand_task)
        rand_btn.grid(row=0, column=2, ipady=5, sticky="nsew", padx=1)
        self.rand_btn = rand_btn

        load_btn = Button(btn_container, font=A32, bd=0, state="disabled", command=load_task)
        load_btn.grid(row=0, column=1, ipady=5, sticky="nsew", padx=1)
        self.load_btn = load_btn

        self.set_lang_showtaskpage()

    def set_lang_showtaskpage(self):
        if current_language == "eng":
            self.return_btn.config(text="Back")
            self.exercise.insert(0, " Exercise: ")
            self.load_btn.config(text="Load task")
            self.rand_btn.config(text="Random task")
        elif current_language == "rus":
            self.return_btn.config(text="Назад")
            self.exercise.insert(0, "    Номер: ")
            self.load_btn.config(text="Загрузить")
            self.rand_btn.config(text="Случайное")


    def validate(self, action, index, value):
        # Insert phrase
        if index == "0" and (value == " Exercise: " or value == "    Номер: ") and action == "1":
            return True
        # Remove ability to edit phrase 
        if int(index) < 11 and ((value[:11] != " Exercise: " or value[:11] != "    Номер: ") or (value[:10] == "" and index == "0" and action == "0")):
            return False
        # Integers does not start from zero
        if len(value) != 11 and index == "11" and value[11] == "0":
            return False
        # Load task button activation
        if len(value[11:]) >= 5 and all(symbol in "0123456789" for symbol in value[11:]):
            self.load_btn.config(state="normal")
        else:
            self.load_btn.config(state="disabled")
        # Entry validation
        if len(value) > 42 and action == "1":  # Limiting input length
            return False
        elif all(symbol in "0123456789" for symbol in value[11:]):  # Allowed values
            return True
        else:
            return False


class SettingsPage(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        def call_link(_):
            open_new_tab("https://github.com/TerraBoii")

        def enter(_):
            created_by.config(font=C_FONT+("underline",))

        def leave(_):
            created_by.config(font=C_FONT)

        created_by = Label(self, text="Created by: TerraBoii", font=C_FONT, cursor='hand2')
        created_by.pack(side="top")
        created_by.bind("<Enter>", enter)
        created_by.bind("<Leave>", leave)
        created_by.bind("<Button-1>", call_link)

        _return = Button(self, font=M_FONT1, command=lambda: parent.ch_page(MainPage, self), bd=0)
        _return.pack(side='bottom', pady=(0, 45), ipadx=45)

        def show_opts(_for):
            match _for:
                case 0:
                    container.pack(pady=(80, 15))
                    l_cont.pack_forget()
                case 1:
                    container.pack_forget()
                    l_cont.pack(pady=(80, 15))
                case 2:
                    ...

        def change_lang(lang):
            FLaunchPage.new_lang(None, lang)
            english.config(state=states[current_language=="eng"])
            russian.config(state=states[current_language=="rus"])
            self.set_lang()

        container = Frame(self)
        container.pack(pady=(80, 15))

        lang_o = Button(container, font=M_FONT1, command=lambda: show_opts(1), bd=0)
        lang_o.grid(row=0, column=0, sticky="nsew", pady=(0, 5), ipadx=65)

        theme_o = Button(container, font=M_FONT1, command=lambda: show_opts(2), state="disabled", bd=0)
        theme_o.grid(row=1, column=0, sticky="nsew", pady=(0, 5))

        l_cont = Frame(self)

        l_title = Label(l_cont, font=M_FONT1, text="Change language to")
        l_title.grid(row=0, column=0, sticky="nsew", pady=(0, 10))

        states = ("normal", "disabled")

        english = Button(l_cont, font=M_FONT1, command=lambda: change_lang("eng"), text="English", state=states[current_language=="eng"], bd=0)
        english.grid(row=1, column=0, sticky="nsew", pady=(0, 5), ipadx=130)

        russian = Button(l_cont, font=M_FONT1, command=lambda: change_lang("rus"), text="Русский", state=states[current_language=="rus"], bd=0)
        russian.grid(row=2, column=0, sticky="nsew", pady=(0, 5))

        back = Button(l_cont, font=M_FONT1, command=lambda: show_opts(0), text="Back", bd=0)
        back.grid(row=3, column=0, sticky="nsew", pady=(10, 0))

        self.created_by = created_by
        self._return = _return
        self.container = container
        self.lang_o = lang_o
        self.theme_o = theme_o
        self.l_cont = l_cont
        self.l_title = l_title
        self.english = english
        self.russian = russian
        self.back = back

        self.set_lang()
        self.set_theme()

    def set_lang(self):
        if current_language == "eng":
            self._return.config(text="Go to the main page")
            self.lang_o.config(text="Change language")
            self.theme_o.config(text="Change theme")
            self.l_title.config(text="Change language to")
            self.back.config(text="Back")
        elif current_language == "rus":
            self._return.config(text="На главную страницу")
            self.lang_o.config(text="Изменить язык")
            self.theme_o.config(text="Изменить тему")
            self.l_title.config(text="Изменить язык на")
            self.back.config(text="Назад")

    def set_theme(self):
        self.config(bg=bg)
        self.created_by.config(bg=bg, fg="#213c91")
        self._return.config(fg=fg, bg=b_bg, activeforeground=afg, activebackground=b_abg)
        self.container.config(bg=bg)
        self.lang_o.config(fg=fg, activeforeground=afg, bg=b_bg, activebackground=b_abg)
        self.theme_o.config(fg=fg, activeforeground=afg, bg=b_bg1, activebackground=b_abg)
        self.l_cont.config(bg=bg)
        self.l_title.config(bg=bg, fg=fg)
        self.english.config(fg=fg, bg=b_bg1, activeforeground=afg, activebackground=b_abg)
        self.russian.config(fg=fg, bg=b_bg, activeforeground=afg, activebackground=b_abg)
        self.back.config(fg=fg, activeforeground=afg, bg=b_bg1, activebackground=b_abg)


if __name__ == "__main__":
    App().mainloop()  # Launch application