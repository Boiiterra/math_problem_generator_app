from tkinter import TclError, Tk, Frame, Label, Button, Entry, Text, Toplevel
from modules import perimeter_task, area_task, square_equation
from pyautogui import position as mouse_pos
from tkinter.messagebox import showinfo
from configparser import ConfigParser
from webbrowser import open_new_tab
from platform import system
from pyperclip import copy

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
# Language
lng_state = parser.get("language", 'state')
current_language = parser.get("language", "language")
# Colors and theme

M_FONT = ("Verdana", 35) # Menu font

# fg = "#3f3f3f" # Foreground active
# bg = "#cfcfcf" # Background color 
# bg1 = "#bababa" # Background color 1
# bg2 = "#c5c5c5" # Background color 2


bg = "#bababa"
fg = "#000000"
active_fg = "#000000"
home_btn_fg = "#404040"
main_btn_bg = "#292929"
num_bg = "#999999"
num_fg = "#4d4d4d"
num_active_fg = "#787878"
home_btn_active_fg = "#5e5e5e"

def change_language(language: str):  # This function changes language for whole application
    global parser, current_language, lng_state

    if language == "rus":
        parser.read('data.txt')
        parser.set("language", 'state', 'keep')
        parser.set('language', "language", 'rus')
        with open("data.txt", "w") as configfile:
            parser.write(configfile)
        lng_state = parser.get('language', 'state')
        current_language = parser.get('language', 'language')
    elif language == "eng":
        parser.read('data.txt')
        parser.set("language", 'state', 'keep')
        parser.set('language', "language", 'eng')
        with open("data.txt", "w") as configfile:
            parser.write(configfile)
        lng_state = parser.get('language', 'state')
        current_language = parser.get('language', 'language')


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
    exercise = None
    allowed = "0123456789-"

    def __init__(self, parent: Frame, app):
        Frame.__init__(self, parent)

        top = Frame(self)
        top.pack(fill="x", pady=8)

        e_label = Label(top, font=('Arial', 27), text="Exercise:")
        e_label.pack(side="left", padx=2, pady=5)

        def do_copy(_):
            if self.exercise is not None:
                copy(self.exercise)

        e_text = Text(top, font=('Arial', 27), borderwidth=0, height=1, state="disabled", cursor="")
        e_text.pack(fill="x", pady=8, side='right')
        e_text.bind("<Button-1>", do_copy)

        task = Label(self, font=('Arial', 20), anchor='center')
        task.pack(pady=4, expand=True)

        b_cont = Label(self)
        b_cont.pack(fill="x", padx=15, side="bottom")

        cont = Label(self, anchor='w')
        cont.pack(pady=(0, 6), side="bottom")

        a_label = Label(cont, font=("Arial", 32))
        a_label.grid(row=0, column=0)

        is_valid = (parent.register(self.validator), '%d', '%i', '%P') # '%d' -> action, '%i' -> index, '%P' -> value

        answer_field = Entry(cont, font=("Arial", 32), width=6, validatecommand=is_valid, validate="key")
        answer_field.grid(row=0, column=1, padx=15)

        confirm_btn = Button(cont, font=('Arial', 32), bd=0, state="disabled")
        confirm_btn.grid(row=0, column=2)

        def go_back():
            self.answer_field["state"] = "disabled"
            app.ch_page(TasksPage, parent)

        back = Button(b_cont, font=("Arial", 35), bd=0, command=go_back)
        back.pack(side="left", ipady=5, fill="x", expand=True, padx=(0, 10))

        next = Button(b_cont, font=("Arial", 35), bd=0)
        next.pack(side="right", ipady=5, fill="x", expand=True, padx=(10, 0))

        self.e_label = e_label
        self.e_text = e_text
        self.task = task
        self.a_label = a_label
        self.answer_field = answer_field
        self.confirm_btn = confirm_btn
        self.back = back
        self.next = next

        self.set_lang()

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

    def set_lang(self):
        if current_language == "eng":
            self.e_label.config(text="Exercise:")
            self.a_label.config(text="Answer:")
            self.back.config(text="Back")
            self.next.config(text="New task")
            self.confirm_btn.config(text="Confirm")
        elif current_language == "rus":
            self.e_label.config(text="Номер:")
            self.a_label.config(text="Ответ:")
            self.back.config(text="Назад")
            self.next.config(text="Новая задача")
            self.confirm_btn.config(text="Подтвердить")


class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        mouse_x, mouse_y = mouse_pos()
        if mouse_x <= 1700 and current_language == "eng":
            x = mouse_x + 8
            y = mouse_y + 1
        elif mouse_x <= 1600 and current_language == "rus":
            x = mouse_x + 8
            y = mouse_y + 1
        elif mouse_x > 1700 and current_language == "eng":
            x = mouse_x - 200
            y = mouse_y + 1
        elif mouse_x > 1600 and current_language == "rus":
            x = mouse_x - 312
            y = mouse_y + 1
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify="left",
                      background="#ffffe0", relief="solid", borderwidth=1,
                      font=("tahoma", "10", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(_):
        toolTip.showtip(text)
    def leave(_):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)


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

        question = Label(self, text="\nChoose language:", bg="black", fg="#00ff00", font=("Arial", 40))
        question.pack(side="top")

        bottom_ = Label(self, bg="black", text="Note: you can always change\nlanguage in settings menu", font=("Arial", 30), fg="#008000")
        bottom_.pack(side="bottom")

        lang_btn_container = Label(self, bg="black", justify="center")
        lang_btn_container.pack(expand=True)

        lang_btn_container.rowconfigure(0, weight=1)
        lang_btn_container.rowconfigure(1, weight=1)
        lang_btn_container.columnconfigure(0, weight=1)

        self.russian = Button(lang_btn_container, text="Русский", bg="black", fg="#00ff00",
                         activeforeground="#008000", font=("Arial", 30), bd=0, highlightbackground="black")
        self.russian.grid(row=0, column=0, sticky="nsew")

        self.english = Button(lang_btn_container, text="English", bg="black", fg="#00ff00",
                         activeforeground="#008000", font=("Arial", 30), bd=0, highlightbackground="black")
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
                bottom_.config(font=("Arial", 30))
                question.config(font=('Arial', 40))
                self.russian.config(font=('Arial', 30))
                self.english.config(font=('Arial', 30))
            elif 620 < width.height <= 700:
                self.english.config(font=('Arial', 35))
                self.russian.config(font=('Arial', 35))
                question.config(font=('Arial', 45))
                bottom_.config(font=("Arial", 35))
            elif 700 < width.height <= 800:
                bottom_.config(font=("Arial", 40))
                question.config(font=('Arial', 50))
                self.russian.config(font=('Arial', 40))
                self.english.config(font=('Arial', 40))
            elif width.height > 800:
                self.english.config(font=('Arial', 45))
                self.russian.config(font=('Arial', 45))
                question.config(font=('Arial', 55))
                bottom_.config(font=("Arial", 45))

        self.bind("<Configure>", font_resize_for_flaunchpage)

    def new_lang(self, lang, this_page=False):
        change_language(lang)
        if this_page:
            self.parent.ch_page(MainPage, self)


class MainPage(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent

        title = Label(self, font=("Verdana", 45))
        title.pack(fill="both", expand=True)

        settings = Button(self, bd=0, bg="#bababa", activebackground="#cfcfcf", activeforeground="#3f3f3f", font=M_FONT, command=lambda: parent.ch_page(SettingsPage, self))
        settings.pack(side="bottom", fill="both", ipady=30, pady=10)

        tasks = Button(self, bd=0, font=M_FONT, bg="#c5c5c5", activebackground="#cfcfcf", activeforeground="#3f3f3f", command=lambda: parent.ch_page(TaskCreationPage, self))
        tasks.pack(side="bottom", fill="x", ipady=20)

        game = Button(self, bd=0, font=M_FONT, bg="#bababa", activebackground="#cfcfcf", activeforeground="#3f3f3f", command=lambda: parent.ch_page(GameOptPage, self))
        game.pack(side="bottom", fill="x", ipady=20, pady=10)

        self.title = title
        self.settings = settings
        self.tasks = tasks
        self.game = game

        self.set_lang()

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

        tasks_list = Button(options, bd=0, font=("Times New Roman", 25), bg="#bababa", activebackground="#cfcfcf", activeforeground="#3f3f3f", command=lambda: other_page(0))
        tasks_list.pack(fill="both", expand=True, pady=(0, 5))
        tasks_list.bind("<Enter>", lambda _: show_description(0, tasks_list))

        show_task = Button(options, bd=0, font=("Times New Roman", 25), bg="#c5c5c5", activebackground="#cfcfcf", activeforeground="#3f3f3f", command=lambda: other_page(1))
        show_task.pack(fill="both", expand=True, pady=10)
        show_task.bind("<Enter>", lambda _: show_description(1, show_task))

        back_btn = Button(options, font=("Times New Roman", 25, "bold"), bd=0, bg="#bababa", activebackground="#cfcfcf", activeforeground="#3f3f3f", command=lambda: other_page(2))
        back_btn.pack(fill="both", expand=True, pady=(15, 0))
        back_btn.bind("<Enter>", lambda _: show_description(2, back_btn))

        info_c = Frame(container) # Info Container
        info_c.pack(side="right", padx=(0, 90))

        info = Label(info_c, font=("Times New Roman", 25))
        info.pack()

        self.back_btn = back_btn
        self.tasks_list = tasks_list
        self.show_task = show_task
        self.info = info

        self.set_lang()

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


class TasksPage(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        top = Frame(self)
        top.pack(pady=10, padx=(65, 65), fill="x")

        back = Button(top, font=("Times New Roman", 25), bd=0, bg="#c5c5c5", activebackground="#cfcfcf", activeforeground="#3f3f3f", command=lambda: parent.ch_page(GameOptPage, self))
        back.pack(side="left")

        _filter = Button(top, font=("Times New Roman", 25), bd=0, bg="#bababa", activebackground="#cfcfcf", activeforeground="#3f3f3f")
        _filter.pack(side="right")

        options = [QEquationPage, SquaresAPage, SquaresPPage, RectanglesAPage, RectanglesPPage]

        menu = Frame(self)
        menu.pack(pady=(10, 0))

        one = Button(menu, text="Quadratic equation", font=("Times New Roman", 25), bd=0, bg="#bababa", activebackground="#cfcfcf", activeforeground="#3f3f3f", command=lambda: parent.ch_page(QEquationPage, self))
        one.grid(row=0, column=0, padx=(0, 10))

        two = Button(menu, text="Area of a square", font=("Times New Roman", 25), bd=0, bg="#bababa", activebackground="#cfcfcf", activeforeground="#3f3f3f", command=lambda: parent.ch_page(SquaresAPage, self))
        two.grid(row=0, column=2, padx=(10, 0))

        self.back = back
        self._filter = _filter

        self.set_lang()

    def set_lang(self):
        if current_language == "eng":
            self.back.config(text="Back")
            self._filter.config(text="Filter")
        elif current_language == "rus":
            self.back.config(text='Назад')
            self._filter.config(text="Фильтр")


class QEquationPage(Frame):
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
                    extra_text_r = "Найлите наибольший корень уравнения."
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
                    page.confirm_btn.config(text="Confirm")
                elif current_language == "rus":
                    page.change_task_text(self.text_r)
                    page.confirm_btn.config(text="Подтвердить")
            else:
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
                    page.confirm_btn.config(text=" Correct", state="disabled")
                elif current_language == "rus":
                    page.confirm_btn.config(text=" Правильно", state="disabled")
                self.after(500, new_task)
            else:
                if current_language == "eng":
                    page.confirm_btn.config(text=" Wrong", state="disabled")
                elif current_language == "rus":
                    page.confirm_btn.config(text=" Неправильно", state="disabled")
                self.after(500, lambda: new_task(False))

        page.new_task_command(new_task)
        page.confirm_command(confirm)


class TaskPage(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        page = TaskPageTemplate(self, parent)
        page.set_exercise(1)
        page.new_task_command(lambda: print("generated"))
        page.confirm_command(lambda: print(page.answer_field.get()))
        page.change_task_text("Hello I am the task")
        parent.bind('<Return>', lambda _: page.confirm_btn.invoke())
        parent.bind('<KP_Enter>', lambda _: page.confirm_btn.invoke())
        page.pack(fill="both", expand=True)

        self.set_lang()

    def set_lang(self):
        ...


class SquaresAPage(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent, bg=bg)
        self.parent = parent
        self.parent = parent

        # Variables:
        self.exercise_no = 0
        self.param = None
        self.answer = None
        self.text_e = None
        self.text_r = None
        self.start = 0

        def container_reset():
            self.container.pack_forget()
            self.container.pack(pady=6, side='bottom')

        def update_task(full_reset=None):
            if self.start == 0:
                container_reset()
                self.start = 1
            if full_reset is None:
                task_data = area_task('square', __version__, self.winfo_width(), self.winfo_height(), 
                                      self.winfo_screenwidth(), self.winfo_screenheight())
                self.exercise_no = task_data[-1]
                self.answer = task_data[1]
                self.param = task_data[0]
                self.text_e = f"Your goal is to find square's area.\nIts side is {self.param}."
                self.text_r = f"Чему равна площадь квадрата,\nесли его сторона равна {self.param}."
                self.exercise.config(state='normal')
                self.exercise.delete("0.0", 'end')
                if current_language == "eng":
                    self.text_label.config(text=self.text_e)
                    self.exercise.insert("0.0", f"  Exercise: {self.exercise_no}")
                    self.confirm_btn.config(text=" Confirm", disabledforeground=active_fg)
                elif current_language == "rus":
                    self.confirm_btn.config(text=" Подтвердить", disabledforeground=active_fg)
                    self.exercise.insert("0.0", f"  Номер: {self.exercise_no}")
                    self.text_label.config(text=self.text_r)
                self.exercise.config(state='disabled')
            else:
                if current_language == "eng":
                    self.confirm_btn.config(text=" Confirm", disabledforeground=active_fg)
                elif current_language == "rus":
                    self.confirm_btn.config(text=" Подтвердить", disabledforeground=active_fg)

        self.update_task = update_task

        self.exercise = Text(self, bg=bg, fg=fg, font=('Arial', 27), borderwidth=0, height=1, highlightbackground=bg,
                             highlightcolor=bg)
        self.exercise.pack(fill="x", pady=8, side='top')
        self.exercise.bind("<Button-1>", lambda _: copy(self.exercise_no))

        self.text_label = Label(self, bg=bg, fg=fg, font=('Arial', 20), anchor='center')
        self.text_label.pack(pady=4, expand=True)

        # Containers:
        self.btn_container = Label(self, bg=bg)
        self.btn_container.pack(side="bottom", fill="x")

        self.btn_container.rowconfigure(0, weight=1)
        self.btn_container.columnconfigure(0, weight=1)
        self.btn_container.columnconfigure(1, weight=1)

        self.container = Label(self, bg=bg, anchor='w')
        self.container.pack(pady=6, side='bottom')

        self.container.rowconfigure(0, weight=1)
        self.container.columnconfigure(0, weight=1)
        self.container.columnconfigure(1, weight=1)
        self.container.columnconfigure(2, weight=1)

        self.answer_txt = Button(self.container, bg=bg, disabledforeground=fg, state="disabled", bd=0, font=("Arial", 32),
                                 highlightbackground=bg)
        self.answer_txt.grid(row=0, column=0)

        is_valid = (parent.register(self.validate), '%d', '%i', '%P') # action, index, value

        def click(_):
            self.answer_field.config(state='normal')

        def confirm():
            self.next_btn.config(state='disabled')
            _input = int(self.answer_field.get())
            self.answer_field.delete(0, "end")
            self.answer_field.config(state='disabled')
            self.after(1000, self.next_btn.config(state='normal'))
            if _input == self.answer:
                if current_language == "eng":
                    self.confirm_btn.config(text=" Correct", state="disabled", disabledforeground=active_fg)
                elif current_language == "rus":
                    self.confirm_btn.config(text=" Правильно", state="disabled", disabledforeground=active_fg)
                self.after(500, update_task)
            else:
                if current_language == "eng":
                    self.confirm_btn.config(text=" Wrong", state="disabled", disabledforeground=active_fg)
                elif current_language == "rus":
                    self.confirm_btn.config(text=" Неправильно", state="disabled", disabledforeground=active_fg)
                self.after(500, lambda: update_task(True))
            self.after(505, container_reset)

        def new_task():
            self.next_btn.config(state='disabled')
            update_task()
            self.after(1000, self.next_btn.config(state='normal'))

        self.answer_field = Entry(self.container, font=("Arial", 32), validatecommand=is_valid, validate="key", width=6,
                                  bg=bg, fg=fg, insertbackground=fg, disabledbackground=bg, disabledforeground=fg,
                                  highlightbackground=bg, highlightcolor=bg)
        self.answer_field.grid(row=0, column=1)

        self.answer_field.bind('<Button-1>', click)
        self.container.pack_forget()

        self.confirm_btn = Button(self.container, font=('Arial', 32), command=confirm, bd=0, disabledforeground=active_fg,
                                  bg=bg, fg=fg, activebackground=bg, activeforeground=active_fg, state="disabled",
                                  highlightbackground=bg)
        self.confirm_btn.grid(row=0, column=2)

        self.return_btn = Button(self.btn_container, font=("Arial", 35), command=lambda: self.return_back(), bd=0,
                                 bg=num_bg, activebackground=num_bg, fg=home_btn_fg, activeforeground=home_btn_active_fg,
                                 highlightbackground=num_bg)
        self.return_btn.grid(row=0, column=0, ipady=5, sticky="nsew", padx=1)

        self.next_btn = Button(self.btn_container, font=("Arial", 35), bd=0, disabledforeground=active_fg,
                               bg=bg, activebackground=bg, fg=num_fg, activeforeground=num_active_fg, command=new_task,
                               highlightbackground=bg)
        self.next_btn.grid(row=0, column=1, ipady=5, sticky="nsew", padx=1)

        self.set_lang_squaresapage()

    def return_back(self):
        self.answer_field.config(state='normal', fg=fg)
        self.answer_field.delete(0, "end")
        self.answer_field.config(state='disabled')
        self.container.pack_forget()
        if current_language == "eng":
            self.confirm_btn.config(text=" Confirm", disabledforeground=active_fg)
        elif current_language == "rus": 
            self.confirm_btn.config(text=" Подтвердить", disabledforeground=active_fg)
        self.container.pack(pady=6, side='bottom')
        if self.start == 0:
            self.container.pack_forget()
        self.parent.ch_page(TasksPage, self)

    def validate(self, action, index, value):
        """Enter only integer values"""
        # Integers does not start from zero and there is input limit
        if value != "":
            if index == "0" and value[0] == "0":
                return False
            if len(value) >= 7:
                return False
        # Confirm button status
        if value == "" and index == "0" and all(_ in "0123456789" for _ in value):
            self.confirm_btn.config(state="disabled")
        elif "0" == index < "6" and all(_ in "0123456789" for _ in value):
            self.confirm_btn.config(state="normal")
        # Entry validation
        if len(self.answer_field.get()) >= 6 and index != "5" and action =="1":  # Limiting input length
            return False
        elif all(_ in "0123456789" for _ in value):  # Allowed values
            return True
        else:
            return False

    def set_lang_squaresapage(self):
        self.exercise.config(state='normal')
        self.exercise.delete("0.0", 'end')
        if current_language == "eng":
            self.return_btn.config(text='Return')
            self.next_btn.config(text='New task')
            self.answer_txt.config(text='Answer: ')
            self.text_label.config(text=self.text_e)
            self.confirm_btn.config(text=" Confirm")
            self.exercise.insert("0.0", f"  Exercise: {self.exercise_no}")
            CreateToolTip(self.exercise, text="Click to copy exercise number")
        elif current_language == 'rus':
            CreateToolTip(self.exercise, text="Нажмите, чтобы скопировать номер задачи")
            self.exercise.insert("0.0", f"  Номер: {self.exercise_no}")
            self.confirm_btn.config(text=" Подтвердить")
            self.next_btn.config(text='Новое задание')
            self.text_label.config(text=self.text_r)
            self.answer_txt.config(text='Ответ: ')
            self.return_btn.config(text='Назад')
        self.exercise.config(state='disabled')


class RectanglesAPage(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent, bg=bg)
        self.parent = parent
        self.parent = parent

        # Variables:
        self.exercise_no = 0
        self.param = None
        self.answer = None
        self.text_e = None
        self.text_r = None
        self.start = 0

        def container_reset():
            self.container.pack_forget()
            self.container.pack(pady=6, side='bottom')

        def update_task(full_reset=None):
            if self.start == 0:
                container_reset()
                self.start = 1
            if full_reset is None:
                task_data = area_task('rectangle', __version__, self.winfo_width(), self.winfo_height(), 
                                        self.winfo_screenwidth(), self.winfo_screenheight())
                self.answer = task_data[2]
                self.exercise_no = task_data[-1]
                self.param = (task_data[0], task_data[1])
                self.text_e = "Your goal is to find rectangle's area." \
                              f"\nIts height is {self.param[0]} and width is {self.param[1]}."
                self.text_r = "Чему равна площадь прямоугольника,\nесли его высота равна " \
                              f"{self.param[0]}, а ширина {self.param[1]}."
                self.exercise.config(state='normal')
                self.exercise.delete("0.0", 'end')
                if current_language == "eng":
                    self.text_label.config(text=self.text_e)
                    self.exercise.insert("0.0", f"  Exercise: {self.exercise_no}")
                    self.confirm_btn.config(text=" Confirm", disabledforeground=active_fg)
                elif current_language == "rus":
                    self.confirm_btn.config(text=" Подтвердить", disabledforeground=active_fg)
                    self.exercise.insert("0.0", f"  Номер: {self.exercise_no}")
                    self.text_label.config(text=self.text_r)
                self.exercise.config(state='disabled')
            else:
                if current_language == "eng":
                    self.confirm_btn.config(text=" Confirm", disabledforeground=active_fg)
                elif current_language == "rus":
                    self.confirm_btn.config(text=" Подтвердить", disabledforeground=active_fg)

        self.update_task = update_task

        def new_task():
            self.next_btn.config(state='disabled')
            update_task()
            self.after(1000, self.next_btn.config(state='normal'))


        self.exercise = Text(self, bg=bg, fg=fg, font=('Arial', 27), borderwidth=0, height=1, highlightbackground=bg,
                             highlightcolor=bg)
        self.exercise.pack(fill="x", pady=8, side='top')
        self.exercise.bind("<Button-1>", lambda _: copy(self.exercise_no))

        self.text_label = Label(self, bg=bg, fg=fg, font=('Arial', 20), anchor='center')
        self.text_label.pack(pady=4, expand=True)

        # Containers:
        self.btn_container = Label(self, bg=bg)
        self.btn_container.pack(side="bottom", fill="x")

        self.btn_container.rowconfigure(0, weight=1)
        self.btn_container.columnconfigure(0, weight=1)
        self.btn_container.columnconfigure(1, weight=1)

        self.container = Label(self, bg=bg, anchor='w')
        self.container.pack(pady=6, side='bottom')

        self.container.rowconfigure(0, weight=1)
        self.container.columnconfigure(0, weight=1)
        self.container.columnconfigure(1, weight=1)
        self.container.columnconfigure(2, weight=1)

        self.answer_txt = Button(self.container, bg=bg, disabledforeground=fg, state="disabled", bd=0, font=("Arial", 32),
                                 highlightbackground=bg)
        self.answer_txt.grid(row=0, column=0)

        is_valid = (parent.register(self.validate), '%d', '%i', '%P') # action, index, value

        def click(_):
            self.answer_field.config(state='normal')

        def confirm():
            self.next_btn.config(state='disabled')
            _input = int(self.answer_field.get())
            self.answer_field.delete(0, 'end')
            self.answer_field.config(state='disabled')
            self.after(1000, self.next_btn.config(state='normal'))
            if _input == self.answer:
                if current_language == "eng":
                    self.confirm_btn.config(text=" Correct", state="disabled", disabledforeground=active_fg)
                elif current_language == "rus":
                    self.confirm_btn.config(text=" Правильно", state="disabled", disabledforeground=active_fg)
                self.after(500, update_task)
            else:
                if current_language == "eng":
                    self.confirm_btn.config(text=" Wrong", state="disabled", disabledforeground=active_fg)
                elif current_language == "rus":
                    self.confirm_btn.config(text=" Неправильно", state="disabled", disabledforeground=active_fg)
                self.after(500, lambda: update_task(False))
            self.after(505, container_reset)

        self.answer_field = Entry(self.container, font=("Arial", 32), validatecommand=is_valid, validate="key", width=6,
                                  bg=bg, fg=fg, insertbackground=fg, disabledbackground=bg, disabledforeground=fg, 
                                  highlightbackground=bg, highlightcolor=bg)
        self.answer_field.grid(row=0, column=1)

        self.confirm_btn = Button(self.container, font=('Arial', 32), command=confirm, bd=0, disabledforeground=active_fg,
                                  bg=bg, fg=fg, activebackground=bg, activeforeground=active_fg, state="disabled",
                                  highlightbackground=bg)
        self.confirm_btn.grid(row=0, column=2)
        
        self.answer_field.bind('<Button-1>', click)
        self.container.pack_forget()

        self.back_btn = Button(self.btn_container, font=("Arial", 35), command=self.return_back, bd=0,
                               bg=num_bg, activebackground=num_bg, fg=home_btn_fg, activeforeground=home_btn_active_fg,
                               highlightbackground=num_bg)
        self.back_btn.grid(row=0, column=0, ipady=5, sticky="nsew", padx=1)

        self.next_btn = Button(self.btn_container, font=("Arial", 35), bd=0, disabledforeground=active_fg,
                               bg=bg, activebackground=bg, fg=num_fg, activeforeground=num_active_fg, command=new_task,
                               highlightbackground=bg)
        self.next_btn.grid(row=0, column=1, ipady=5, sticky="nsew", padx=1)

        self.set_lang_rectanglesaspage()

    def return_back(self):
        self.answer_field.config(state='normal', fg=fg)
        self.answer_field.delete(0, "end")
        self.answer_field.config(state='disabled')
        self.container.pack_forget()
        if current_language == "eng":
            self.confirm_btn.config(text=" Confirm", disabledforeground=active_fg)
        elif current_language == "rus": 
            self.confirm_btn.config(text=" Подтвердить", disabledforeground=active_fg)
        self.container.pack(pady=6, side='bottom')
        if self.start == 0:
            self.container.pack_forget()
        self.parent.ch_page(TasksPage, self)

    def validate(self, action, index, value):
        """Enter only integer values"""
        # Integers does not start from zero and there is input limit
        if value != "":
            if index == "0" and value[0] == "0":
                return False
            if len(value) >= 7:
                return False
        # Confirm button status
        if value == "" and index == "0" and all(_ in "0123456789" for _ in value):
            self.confirm_btn.config(state="disabled")
        elif "0" == index < "6" and all(_ in "0123456789" for _ in value):
            self.confirm_btn.config(state="normal")
        # Entry validation
        if len(self.answer_field.get()) >= 6 and index != "5" and action == "1":  # Limiting input length
            return False
        elif all(_ in "0123456789" for _ in value):  # Allowed values
            return True
        else:
            return False

    def set_lang_rectanglesaspage(self):
        self.exercise.config(state='normal')
        self.exercise.delete("0.0", 'end')
        if current_language == "eng":
            self.back_btn.config(text='Back')
            self.next_btn.config(text="New task")
            self.answer_txt.config(text='Answer: ')
            self.text_label.config(text=self.text_e)
            self.confirm_btn.config(text=" Confirm")
            self.exercise.insert("0.0", f"  Exercise: {self.exercise_no}")
            CreateToolTip(self.exercise, text="Click to copy exercise number")
        elif current_language == 'rus':
            CreateToolTip(self.exercise, text="Нажмите, чтобы скопировать номер задачи")
            self.exercise.insert("0.0", f"  Номер: {self.exercise_no}")
            self.confirm_btn.config(text=" Подтвердить")
            self.next_btn.config(text="Новое задание")
            self.text_label.config(text=self.text_r)
            self.answer_txt.config(text='Ответ: ')
            self.back_btn.config(text='Назад')
        self.exercise.config(state='disabled')


class SquaresPPage(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent, bg=bg)
        self.parent = parent
        self.parent = parent

        # Variables:
        self.exercise_no = 0
        self.param = None
        self.answer = None
        self.text_e = None
        self.text_r = None
        self.start = 0

        def container_reset():
            self.container.pack_forget()
            self.container.pack(pady=6, side='bottom')

        def update_task(full_reset=None):
            if self.start == 0:
                container_reset()
                self.start = 1
            if full_reset is None:
                task_data = perimeter_task('square', __version__, self.winfo_width(), self.winfo_height(), 
                                           self.winfo_screenwidth(), self.winfo_screenheight())
                self.exercise_no = task_data[-1]
                self.answer = task_data[1]
                self.param = task_data[0]
                self.text_e = f"Your goal is to find square's perimeter.\nIts side is {self.param}."
                self.text_r = f"Чему равен периметр квадрата,\nесли его сторона равна {self.param}."
                self.exercise.config(state='normal')
                self.exercise.delete("0.0", 'end')
                if current_language == "eng":
                    self.text_label.config(text=self.text_e)
                    self.exercise.insert("0.0", f"  Exercise: {self.exercise_no}")
                    self.confirm_btn.config(text=" Confirm", disabledforeground=active_fg)
                elif current_language == "rus":
                    self.confirm_btn.config(text=" Подтвердить", disabledforeground=active_fg)
                    self.exercise.insert("0.0", f"  Номер: {self.exercise_no}")
                    self.text_label.config(text=self.text_r)
                self.exercise.config(state='disabled')
            else:
                if current_language == "eng":
                    self.confirm_btn.config(text=" Confirm", disabledforeground=active_fg)
                elif current_language == "rus":
                    self.confirm_btn.config(text=" Подтвердить", disabledforeground=active_fg)

        self.update_task = update_task

        self.exercise = Text(self, bg=bg, fg=fg, font=('Arial', 27), borderwidth=0, height=1, highlightbackground=bg,
                             highlightcolor=bg)
        self.exercise.pack(fill="x", pady=8, side='top')
        self.exercise.bind("<Button-1>", lambda _: copy(self.exercise_no))

        self.text_label = Label(self, bg=bg, fg=fg, font=('Arial', 20), anchor='center')
        self.text_label.pack(pady=4, expand=True)

        # Containers:
        self.btn_container = Label(self, bg=bg)
        self.btn_container.pack(side="bottom", fill="x")

        self.btn_container.rowconfigure(0, weight=1)
        self.btn_container.columnconfigure(0, weight=1)
        self.btn_container.columnconfigure(1, weight=1)

        self.container = Label(self, bg=bg, anchor='w')
        self.container.pack(pady=6, side='bottom')

        self.container.rowconfigure(0, weight=1)
        self.container.columnconfigure(0, weight=1)
        self.container.columnconfigure(1, weight=1)
        self.container.columnconfigure(2, weight=1)

        self.answer_txt = Button(self.container, bg=bg, disabledforeground=fg, state="disabled", bd=0, font=("Arial", 32),
                                 highlightbackground=bg)
        self.answer_txt.grid(row=0, column=0)

        is_valid = (parent.register(self.validate), '%d', '%i', '%P') # action, index, value

        def click(_):
            self.answer_field.config(state='normal')

        def confirm():
            self.next_btn.config(state='disabled')
            _input = int(self.answer_field.get())
            self.answer_field.delete(0, "end")
            self.answer_field.config(state='disabled')
            self.after(1000, self.next_btn.config(state='normal'))
            if _input == self.answer:
                if current_language == "eng":
                    self.confirm_btn.config(text=" Correct", state="disabled", disabledforeground=active_fg)
                elif current_language == "rus":
                    self.confirm_btn.config(text=" Правильно", state="disabled", disabledforeground=active_fg)
                self.after(500, update_task)
            else:
                if current_language == "eng":
                    self.confirm_btn.config(text=" Wrong", state="disabled", disabledforeground=active_fg)
                elif current_language == "rus":
                    self.confirm_btn.config(text=" Неправильно", state="disabled", disabledforeground=active_fg)
                self.after(500, lambda: update_task(True))
            self.after(505, container_reset)

        def new_task():
            self.next_btn.config(state='disabled')
            update_task()
            self.after(1000, self.next_btn.config(state='normal'))


        self.answer_field = Entry(self.container, font=("Arial", 32), validatecommand=is_valid, validate="key", width=6,
                                  bg=bg, fg=fg, insertbackground=fg, disabledbackground=bg, disabledforeground=fg,
                                  highlightbackground=bg, highlightcolor=bg)
        self.answer_field.grid(row=0, column=1)

        self.answer_field.bind('<Button-1>', click)
        self.container.pack_forget()

        self.confirm_btn = Button(self.container, font=('Arial', 32), command=confirm, bd=0, disabledforeground=active_fg,
                                  bg=bg, fg=fg, activebackground=bg, activeforeground=active_fg, state="disabled",
                                  highlightbackground=bg)
        self.confirm_btn.grid(row=0, column=2)

        self.return_btn = Button(self.btn_container, font=("Arial", 35), command=lambda: self.return_back(), bd=0,
                                 bg=num_bg, activebackground=num_bg, fg=home_btn_fg, activeforeground=home_btn_active_fg,
                                 highlightbackground=num_bg)
        self.return_btn.grid(row=0, column=0, ipady=5, sticky="nsew", padx=1)

        self.next_btn = Button(self.btn_container, font=("Arial", 35), bd=0, disabledforeground=active_fg,
                               bg=bg, activebackground=bg, fg=num_fg, activeforeground=num_active_fg, command=new_task,
                               highlightbackground=bg)
        self.next_btn.grid(row=0, column=1, ipady=5, sticky="nsew", padx=1)

        self.set_lang_squaresppage()

    def return_back(self):
        self.answer_field.config(state='normal', fg=fg)
        self.answer_field.delete(0, "end")
        self.answer_field.config(state='disabled')
        self.container.pack_forget()
        if current_language == "eng":
            self.confirm_btn.config(text=" Confirm", disabledforeground=active_fg)
        elif current_language == "rus": 
            self.confirm_btn.config(text=" Подтвердить", disabledforeground=active_fg)
        self.container.pack(pady=6, side='bottom')
        if self.start == 0:
            self.container.pack_forget()
        self.parent.ch_page(TasksPage, self)

    def validate(self, action, index, value):
        """Enter only integer values"""
        # Integers does not start from zero and there is input limit
        if value != "":
            if index == "0" and value[0] == "0":
                return False
            if len(value) >= 7:
                return False
        # Confirm button status
        if value == "" and index == "0" and all(_ in "0123456789" for _ in value):
            self.confirm_btn.config(state="disabled")
        elif "0" == index < "6" and all(_ in "0123456789" for _ in value):
            self.confirm_btn.config(state="normal")
        # Entry validation
        if len(self.answer_field.get()) >= 6 and index != "5" and action =="1":  # Limiting input length
            return False
        elif all(_ in "0123456789" for _ in value):  # Allowed values
            return True
        else:
            return False

    def set_lang_squaresppage(self):
        self.exercise.config(state='normal')
        self.exercise.delete("0.0", 'end')
        if current_language == "eng":
            self.next_btn.config(text="New task")
            self.return_btn.config(text='Return')
            self.answer_txt.config(text='Answer: ')
            self.text_label.config(text=self.text_e)
            self.confirm_btn.config(text=" Confirm")
            self.exercise.insert("0.0", f"  Exercise: {self.exercise_no}")
            CreateToolTip(self.exercise, text="Click to copy exercise number")
        elif current_language == 'rus':
            CreateToolTip(self.exercise, text="Нажмите, чтобы скопировать номер задачи")
            self.exercise.insert("0.0", f"  Номер: {self.exercise_no}")
            self.confirm_btn.config(text=" Подтвердить")
            self.next_btn.config(text="Новое задание")
            self.text_label.config(text=self.text_r)
            self.answer_txt.config(text='Ответ: ')
            self.return_btn.config(text='Назад')
        self.exercise.config(state='disabled')


class RectanglesPPage(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent, bg=bg)
        self.parent = parent

        # Variables:
        self.exercise_no = 0
        self.param = None
        self.answer = None
        self.text_e = None
        self.text_r = None
        self.start = 0

        def container_reset():
            self.container.pack_forget()
            self.container.pack(pady=6, side='bottom')

        def update_task(full_reset=None):
            if self.start == 0:
                container_reset()
                self.start = 1
            if full_reset is None:
                task_data = perimeter_task('rectangle', __version__, self.winfo_width(), self.winfo_height(), 
                                           self.winfo_screenwidth(), self.winfo_screenheight())
                self.answer = task_data[2]
                self.exercise_no = task_data[-1]
                self.param = (task_data[0], task_data[1])
                self.text_e = "Your goal is to find rectangle's perimeter." \
                              f"\nIts height is {self.param[0]} and width is {self.param[1]}."
                self.text_r = "Чему равен периметр прямоугольника,\nесли его высота равна " \
                              f"{self.param[0]}, а ширина {self.param[1]}."
                self.exercise.config(state='normal')
                self.exercise.delete("0.0", 'end')
                if current_language == "eng":
                    self.text_label.config(text=self.text_e)
                    self.exercise.insert("0.0", f"  Exercise: {self.exercise_no}")
                    self.confirm_btn.config(text=" Confirm", disabledforeground=active_fg)
                elif current_language == "rus":
                    self.confirm_btn.config(text=" Подтвердить", disabledforeground=active_fg)
                    self.exercise.insert("0.0", f"  Номер: {self.exercise_no}")
                    self.text_label.config(text=self.text_r)
                self.exercise.config(state='disabled')
            else:
                if current_language == "eng":
                    self.confirm_btn.config(text=" Confirm", disabledforeground=active_fg)
                elif current_language == "rus":
                    self.confirm_btn.config(text=" Подтвердить", disabledforeground=active_fg)

        self.update_task = update_task

        self.exercise = Text(self, bg=bg, fg=fg, font=('Arial', 27), borderwidth=0, height=1, highlightbackground=bg,
                             highlightcolor=bg)
        self.exercise.pack(fill="x", pady=8, side='top')
        self.exercise.bind("<Button-1>", lambda _: copy(self.exercise_no))

        self.text_label = Label(self, bg=bg, fg=fg, font=('Arial', 20), anchor='center')
        self.text_label.pack(pady=4, expand=True)

        # Containers:
        self.btn_container = Label(self, bg=bg)
        self.btn_container.pack(side="bottom", fill="x")

        self.btn_container.rowconfigure(0, weight=1)
        self.btn_container.columnconfigure(0, weight=1)
        self.btn_container.columnconfigure(1, weight=1)

        self.container = Label(self, bg=bg, anchor='w')
        self.container.pack(pady=6, side='bottom')

        self.container.rowconfigure(0, weight=1)
        self.container.columnconfigure(0, weight=1)
        self.container.columnconfigure(1, weight=1)
        self.container.columnconfigure(2, weight=1)

        self.answer_txt = Button(self.container, bg=bg, disabledforeground=fg, state="disabled", bd=0, font=("Arial", 32),
                                 highlightbackground=bg)
        self.answer_txt.grid(row=0, column=0)

        is_valid = (parent.register(self.validate), '%d', '%i', '%P') # action, index, value

        def click(_):
            self.answer_field.config(state='normal')

        def confirm():
            self.next_btn.config(state='disabled')
            _input = int(self.answer_field.get())
            self.answer_field.delete(0, "end")
            self.answer_field.config(state='disabled')
            self.after(1000, self.next_btn.config(state='normal'))
            if _input == self.answer:
                if current_language == "eng":
                    self.confirm_btn.config(text=" Correct", state="disabled", disabledforeground=active_fg)
                elif current_language == "rus":
                    self.confirm_btn.config(text=" Правильно", state="disabled", disabledforeground=active_fg)
                self.after(500, update_task)
            else:
                if current_language == "eng":
                    self.confirm_btn.config(text=" Wrong", state="disabled", disabledforeground=active_fg)
                elif current_language == "rus":
                    self.confirm_btn.config(text=" Неправильно", state="disabled", disabledforeground=active_fg)
                self.after(500, lambda: update_task(True))
            self.after(505, container_reset)

        def new_task():
            self.next_btn.config(state='disabled')
            update_task()
            self.after(1000, self.next_btn.config(state='normal'))

        self.answer_field = Entry(self.container, font=("Arial", 32), validatecommand=is_valid, validate="key", width=6,
                                  bg=bg, fg=fg, insertbackground=fg, disabledbackground=bg, disabledforeground=bg,
                                  highlightbackground=bg, highlightcolor=bg)
        self.answer_field.grid(row=0, column=1)

        self.confirm_btn = Button(self.container, font=('Arial', 32), command=confirm, bd=0, disabledforeground=active_fg,
                                  bg=bg, fg=fg, activebackground=bg, activeforeground=active_fg, state="disabled",
                                  highlightbackground=bg)
        self.confirm_btn.grid(row=0, column=2)
        
        self.answer_field.bind('<Button-1>', click)
        self.container.pack_forget()

        self.back_btn = Button(self.btn_container, font=("Arial", 35), command=self.return_back, bd=0, highlightbackground=num_bg,
                               bg=num_bg, activebackground=num_bg, fg=home_btn_fg, activeforeground=home_btn_active_fg)
        self.back_btn.grid(row=0, column=0, ipady=5, sticky="nsew", padx=1)

        self.next_btn = Button(self.btn_container, font=("Arial", 35), bd=0, disabledforeground=active_fg,
                               bg=bg, activebackground=bg, fg=num_fg, activeforeground=num_active_fg, command=new_task,
                               highlightbackground=bg)
        self.next_btn.grid(row=0, column=1, ipady=5, sticky="nsew", padx=1)

        self.set_lang_rectanglesppage()

    def return_back(self):
        self.answer_field.config(state='normal', fg=fg)
        self.answer_field.delete(0, "end")
        self.answer_field.config(state='disabled')
        self.container.pack_forget()
        if current_language == "eng":
            self.confirm_btn.config(text=" Confirm", disabledforeground=active_fg)
        elif current_language == "rus": 
            self.confirm_btn.config(text=" Подтвердить", disabledforeground=active_fg)
        self.container.pack(pady=6, side='bottom')
        if self.start == 0:
            self.container.pack_forget()
        self.parent.ch_page(TasksPage, self)

    def validate(self, action, index, value):
        """Enter only integer values"""
        # Integers does not start from zero and there is input limit
        if value != "":
            if index == "0" and value[0] == "0":
                return False
            if len(value) >= 7:
                return False
        # Confirm button status
        if value == "" and index == "0" and all(_ in "0123456789" for _ in value):
            self.confirm_btn.config(state="disabled")
        elif "0" == index < "6" and all(_ in "0123456789" for _ in value):
            self.confirm_btn.config(state="normal")
        # Entry validation
        if len(self.answer_field.get()) >= 6 and index != "5" and action =="1":  # Limiting input length
            return False
        elif all(_ in "0123456789" for _ in value):  # Allowed values
            return True
        else:
            return False

    def set_lang_rectanglesppage(self):
        self.exercise.config(state='normal')
        self.exercise.delete("0.0", 'end')
        if current_language == "eng":
            self.back_btn.config(text='Back')
            self.next_btn.config(text="New task")
            self.answer_txt.config(text='Answer: ')
            self.text_label.config(text=self.text_e)
            self.confirm_btn.config(text=" Confirm")
            self.exercise.insert("0.0", f"  Exercise: {self.exercise_no}")
            CreateToolTip(self.exercise, text="Click to copy exercise number")
        elif current_language == 'rus':
            CreateToolTip(self.exercise, text="Нажмите, чтобы скопировать номер задачи")
            self.exercise.insert("0.0", f"  Номер: {self.exercise_no}")
            self.confirm_btn.config(text=" Подтвердить")
            self.next_btn.config(text="Новое задание")
            self.text_label.config(text=self.text_r)
            self.answer_txt.config(text='Ответ: ')
            self.back_btn.config(text='Назад')
        self.exercise.config(state='disabled')


class TaskCreationPage(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent

        back = Button(self, font=("Verdana", 35), command=lambda: parent.ch_page(MainPage, self))
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

        btn_container = Label(self, bg=bg)
        btn_container.pack(side="bottom", fill="x")
        self.btn_container = btn_container

        btn_container.rowconfigure(0, weight=1)
        btn_container.columnconfigure(0, weight=1)
        btn_container.columnconfigure(1, weight=1)
        btn_container.columnconfigure(2, weight=1)

        is_valid = (parent.register(self.validate), '%d', '%i', '%P') # action, index, value

        exercise = Entry(self, bg=bg, fg=fg, font=('Arial', 27), borderwidth=0, highlightthickness=0, validatecommand=is_valid, validate="key")
        exercise.pack(fill="x", pady=8, side='top')
        self.exercise = exercise

        return_btn = Button(btn_container, font=("Arial", 35), command=lambda: parent.ch_page(MainPage, self), bd=0, bg=num_bg,
                            activebackground=num_bg, fg=home_btn_fg, activeforeground=home_btn_active_fg, highlightbackground=num_bg)
        return_btn.grid(row=0, column=0, sticky='nsew', ipady=5, padx=1)
        self.return_btn = return_btn

        rand_btn = Button(btn_container, font=("Arial", 35), bd=0, highlightbackground=bg, bg=num_bg, fg=num_fg,
                               activebackground=num_bg, activeforeground=num_active_fg, command=rand_task)
        rand_btn.grid(row=0, column=2, ipady=5, sticky="nsew", padx=1)
        self.rand_btn = rand_btn

        load_btn = Button(btn_container, font=("Arial", 35), bd=0, highlightbackground=bg, bg=bg, state="disabled",
                               activebackground=bg, fg=num_fg, activeforeground=num_active_fg, command=load_task)
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
            created_by.config(font=("Tahoma", 15, "underline"))

        def leave(_):
            created_by.config(font=("Tahoma", 15))

        created_by = Label(self, fg="#213c91", text="Created by: TerraBoii", font=("Tahoma", 15), cursor='hand2')
        created_by.pack(side="top")
        created_by.bind("<Enter>", enter)
        created_by.bind("<Leave>", leave)
        created_by.bind("<Button-1>", call_link)

        _return = Button(self, font=("Times New Roman", 25), command=lambda: parent.ch_page(MainPage, self),
                      bd=0, activeforeground="#3f3f3f", bg="#bababa", activebackground="#cfcfcf")
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

        lang_o = Button(container, font=("Times New Roman", 25), command=lambda: show_opts(1),
                      bd=0, activeforeground="#3f3f3f", bg="#bababa", activebackground="#cfcfcf")
        lang_o.grid(row=0, column=0, sticky="nsew", pady=(0, 5), ipadx=65)

        theme_o = Button(container, font=("Times New Roman", 25), command=lambda: show_opts(2), state="disabled",
                       bd=0, activeforeground="#3f3f3f", bg="#c5c5c5", activebackground="#cfcfcf")
        theme_o.grid(row=1, column=0, sticky="nsew", pady=(0, 5))

        l_cont = Frame(self)

        l_title = Label(l_cont, font=("Times New Roman", 25), text="Change language to")
        l_title.grid(row=0, column=0, sticky="nsew", pady=(0, 10))

        states = ("normal", "disabled")

        english = Button(l_cont, font=("Times New Roman", 25), command=lambda: change_lang("eng"), text="English", state=states[current_language=="eng"],
                         bd=0, activeforeground="#3f3f3f", bg="#c5c5c5", activebackground="#cfcfcf")
        english.grid(row=1, column=0, sticky="nsew", pady=(0, 5), ipadx=130)

        russian = Button(l_cont, font=("Times New Roman", 25), command=lambda: change_lang("rus"), text="Русский", state=states[current_language=="rus"],
                         bd=0, activeforeground="#3f3f3f", bg="#bababa", activebackground="#cfcfcf")
        russian.grid(row=2, column=0, sticky="nsew", pady=(0, 5))

        back = Button(l_cont, font=("Times New Roman", 25), command=lambda: show_opts(0), text="Back",
                      bd=0, activeforeground="#3f3f3f", bg="#c5c5c5", activebackground="#cfcfcf")
        back.grid(row=3, column=0, sticky="nsew", pady=(10, 0))

        self._return = _return
        self.lang_o = lang_o
        self.theme_o = theme_o
        self.l_title = l_title
        self.back = back

        self.set_lang()

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


if __name__ == "__main__":
    App().mainloop()  # Launch application