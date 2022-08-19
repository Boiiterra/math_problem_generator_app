from tkinter import TclError, Tk, Frame, Label, Button, Entry, Text, Toplevel
from generators import perimeter_task, area_task, square_equation
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
_width = parser.get('parameters', 'width')
_state = parser.get('parameters', 'zoomed')
_height = parser.get('parameters', 'height')
# Language
lng_state = parser.get("language", 'state')
current_language = parser.get("language", "language")
# Colors and theme
home_btn_active_fg = parser.get("colors", "home_bts_active_fore")
num_active_fg = parser.get("colors", "num_btn_active_fore")
active_fg = parser.get("colors", "active_foreground")
current_theme = parser.get('theme', "current_theme")
home_btn_fg = parser.get("colors", "home_btn_fore")
main_btn_bg = parser.get("colors", "main_btn_back")
num_bg = parser.get("colors", "num_btn_back")
num_fg = parser.get("colors", "num_btn_fore")
fg = parser.get("colors", "foreground")
bg = parser.get("colors", "background")


def set_theme():  # This function updates colors after theme changed
    global current_theme, bg, fg, active_fg, home_btn_active_fg, home_btn_fg, main_btn_bg, num_bg, num_fg, num_active_fg
    home_btn_active_fg = parser.get("colors", "home_bts_active_fore")
    num_active_fg = parser.get("colors", "num_btn_active_fore")
    active_fg = parser.get("colors", "active_foreground")
    current_theme = parser.get('theme', "current_theme")
    home_btn_fg = parser.get("colors", "home_btn_fore")
    main_btn_bg = parser.get("colors", "main_btn_back")
    num_bg = parser.get("colors", "num_btn_back")
    num_fg = parser.get("colors", "num_btn_fore")
    fg = parser.get("colors", "foreground")
    bg = parser.get("colors", "background")


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


def dark_theme():  # This function changes colors and theme to dark and saves changes to file
    global parser
    parser.read("data.txt")
    parser.set("theme", "current_theme", "dark")
    parser.set("colors", "background", "#000000")
    parser.set("colors", "num_btn_back", "#0a0a0a")
    parser.set("colors", "home_btn_fore", "#474747")
    parser.set("colors", "active_foreground", "#5e5e5e")
    parser.set("colors", "home_bts_active_fore", "#333333")
    parser.set("colors", "num_btn_active_fore", "#5e5e5e")
    parser.set("colors", "main_btn_back", "#000000")
    parser.set("colors", "num_btn_fore", "#8c8c8c")
    parser.set("colors", "foreground", "#ffffff")
    with open("data.txt", 'w') as configfile:
        parser.write(configfile)
    # Set colors
    parser.read("data.txt")
    set_theme()


def light_theme():  # This function changes colors and theme to light and saves changes to file
    global parser
    parser.read("data.txt")
    parser.set('theme', "current_theme", "light")
    parser.set("colors", "num_btn_back", "#999999")
    parser.set("colors", "home_btn_fore", "#404040")
    parser.set("colors", "active_foreground", "#000000")
    parser.set("colors", "home_bts_active_fore", "#5e5e5e")
    parser.set("colors", "num_btn_active_fore", "#787878")
    parser.set("colors", "main_btn_back", "#292929")
    parser.set("colors", "num_btn_fore", "#4d4d4d")
    parser.set("colors", "foreground", "#000000")
    parser.set("colors", "background", "#bababa")
    with open("data.txt", 'w') as configfile:
        parser.write(configfile)
    # Set colors
    parser.read("data.txt")
    set_theme()


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
        parser.set('parameters', 'height', _height)
        parser.set('parameters', 'width', _width)
        parser.set('parameters', 'x', x_pos)
        parser.set('parameters', 'y', y_pos)
    parser.set('parameters', 'zoomed', _state)
    with open("data.txt", 'w') as configfile:
        parser.write(configfile)


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


class MainAppBody(Tk):  # Main application with page logic

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title(f"Math problem generator - {__version__}")
        try:
            self.iconbitmap("images//main_icon.ico")
        except TclError:
            print("Unable to find icon file")
        # Setting max and min sizes for the app
        self.minsize(width=800, height=600)
        self.maxsize(self.winfo_screenwidth(), self.winfo_screenheight())

        # creating window:
        if current_language == "unknown" or lng_state == "ask" or system() == "Linux":
            middle_x = int((self.winfo_screenwidth() - 800) / 2)
            middle_y = int((self.winfo_screenheight() - 600) / 2)
            self.geometry(f"{800}x{600}+{middle_x}+{middle_y}")  # Middle pos on the screen
        else:
            self.geometry(f"{int(_width)}x{int(_height)}+{int(x_pos) - 8}+{(int(y_pos))-31}")  # (- 8) and (- 31) is important

        # Rewriting default delete method in order to save window parameters
        if system() == "Windows":
            self.protocol('WM_DELETE_WINDOW', self.delete_window)
        if _state == 'yes':
            self.state('zoomed')


        container = Frame(self, bg="black")
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.frames = {}

        frame_collection = (FLaunchPage, GeometryPage, MainPage, SettingsPage, AreasPage, PerimetersPage, SquaresAPage, 
                            RectanglesAPage, SquaresPPage, RectanglesPPage, SubjectsPage, AlgebraPage, SqEquationPage,
                            TaskCreationPage, ShowTaskPage)

        for frame in frame_collection:
            current_frame = frame(container, self)

            self.frames[frame] = current_frame

            current_frame.grid(row=0, column=0, sticky="nsew")
        if lng_state == "ask" or current_language == "unknown":
            self.show_frame(FLaunchPage)
        elif lng_state == "keep":
            self.show_frame(MainPage)

    def delete_window(self):  # saves parameters and then deletes window
        if self.wm_state() == "zoomed" and lng_state != "ask" and current_language != "unknown":
            save_window_parameters(str(self.winfo_width()), str(self.winfo_height()),
                                   str(self.winfo_rootx()), str(self.winfo_rooty()), '1')
        elif self.wm_state() != "zoomed" and lng_state != "ask" and current_language != "unknown":
            save_window_parameters(str(self.winfo_width()), str(self.winfo_height()),
                                   str(self.winfo_rootx()), str(self.winfo_rooty()), '0')
        self.destroy()

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def get_page(self, page_class):
        return self.frames[page_class]


class FLaunchPage(Frame):  # This page launches when you need to choose language

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg="black")
        self.controller = controller

        question_text = "\nChoose language:"

        question = Label(self, text=question_text, bg="black", fg="#00ff00", font=("Arial", 40))
        question.pack(side="top")

        hint_text = "Note: you can always change\nlanguage in settings menu"

        bottom_ = Label(self, bg="black", text=hint_text, font=("Arial", 30), fg="#008000")
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

        def entered(_, btn, lang: str):
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

        def left(_, btn):
            btn.config(bg="black")

        self.english.bind("<Leave>", lambda _: left(_, btn=self.english))
        self.russian.bind("<Button-1>", lambda _: self.new_lang(_, lang="rus"))
        self.russian.bind("<Enter>", lambda _: entered(_, btn=self.russian, lang='rus'))
        self.english.bind("<Enter>", lambda _: entered(_, btn=self.english, lang='eng'))
        self.english.bind("<Button-1>", lambda _: self.new_lang(_, lang="eng"))
        self.russian.bind("<Leave>", lambda _: left(_, btn=self.russian))

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

    def new_lang(self, _, lang: str, _from = None):
        change_language(lang)
        self.controller.get_page(RectanglesAPage).set_lang_rectanglesaspage()
        self.controller.get_page(RectanglesPPage).set_lang_rectanglesppage()
        self.controller.get_page(SqEquationPage).set_lang_sqequationpage()
        self.controller.get_page(PerimetersPage).set_lang_perimeterspage()
        self.controller.get_page(ShowTaskPage).set_lang_showtaskpage()
        self.controller.get_page(SettingsPage).set_lang_settingspage()
        self.controller.get_page(SquaresAPage).set_lang_squaresapage()
        self.controller.get_page(SquaresPPage).set_lang_squaresppage()
        self.controller.get_page(GeometryPage).set_lang_geometrypage()
        self.controller.get_page(SubjectsPage).set_lang_subjectspage()
        self.controller.get_page(AlgebraPage).set_lang_algebrapage()
        self.controller.get_page(AreasPage).set_lang_squarespage()
        self.controller.get_page(MainPage).set_lang_mainpage()

        if _from is None:  # We don't need to go to main page after switching language in settings
            self.controller.show_frame(MainPage)


class MainPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=bg)
        self.controller = controller

        self.text_label = Label(self, font=("Verdana", 45), bg=bg, fg=fg)
        self.text_label.pack(fill='both', expand=True)

        self.start_button = Button(self, bg=num_bg, fg=fg, font=("Arial", 45),
                                   activeforeground=active_fg, activebackground=num_bg, bd=0, highlightbackground=num_bg,
                                   disabledforeground=num_bg, command=lambda: controller.show_frame(SubjectsPage))
        self.start_button.pack(fill='both', pady=2, expand=True)

        self.settings_button = Button(self, bg=num_bg, fg=home_btn_fg, font=("Arial", 45),
                                      activeforeground=home_btn_active_fg, activebackground=num_bg, bd=0,
                                      disabledforeground=num_bg, command=lambda: controller.show_frame(SettingsPage),
                                      highlightbackground=num_bg)
        self.settings_button.pack(fill='both', side='bottom', expand=True)

        def font_resize_mainpage(_):
            pass

        self.bind("<Configure>", font_resize_mainpage)

        self.set_lang_mainpage()

    def set_lang_mainpage(self):
        if current_language == "eng":
            self.text_label.config(text='Math problem\ngenerator')
            self.start_button.config(text="Begin")
            self.settings_button.config(text="Settings")
        elif current_language == 'rus':
            self.text_label.config(text='Генератор задач по\nматематике')
            self.start_button.config(text="Начать")
            self.settings_button.config(text="Настройки")

    def main_page_theme_update(self):
        self.config(bg=bg)
        self.text_label.config(bg=bg, fg=fg)
        self.start_button.config(bg=num_bg, fg=fg, activeforeground=num_active_fg, activebackground=num_bg,
                                 highlightbackground=num_bg)
        self.settings_button.config(bg=num_bg, fg=home_btn_fg, activeforeground=home_btn_active_fg, activebackground=num_bg,
                                    highlightbackground=num_bg)


class SubjectsPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=bg)
        self.controller = controller

        self.back_btn = Button(self, font=("Arial", 35), command=lambda: controller.show_frame(MainPage), bd=0,
                               bg=num_bg, activebackground=num_bg, fg=home_btn_fg, activeforeground=home_btn_active_fg,
                               highlightbackground=num_bg)
        self.back_btn.pack(side='bottom', fill='x', ipady=5)

        self.subjects_info = Label(self, font=('Arial', 25), bg=bg, fg=fg)
        self.subjects_info.pack()

        self.placeholder = Label(self, font=('Arial', 5), bg=bg)
        self.placeholder.pack(side='bottom')

        self.subjects_container = Label(self, bg=bg)
        self.subjects_container.pack(side="left", expand=True, fill="both", padx=2)

        self.subjects_container.rowconfigure(0, weight=1)
        self.subjects_container.rowconfigure(1, weight=1)
        self.subjects_container.columnconfigure(0, weight=1)
        self.subjects_container.columnconfigure(1, weight=1)

        self.algebra = Button(self.subjects_container, bd=0, font=('Arial', 25),
                              bg=bg, fg=fg, activebackground=bg, activeforeground=active_fg,
                              command=lambda: controller.show_frame(AlgebraPage), highlightbackground=bg)
        self.algebra.grid(row=0, column=0, sticky='nsew')
        
        self.geometry = Button(self.subjects_container, bd=0, font=('Arial', 25),
                               bg=num_bg, fg=fg, activebackground=num_bg, activeforeground=num_active_fg,
                               command=lambda: controller.show_frame(GeometryPage), highlightbackground=num_bg)
        self.geometry.grid(row=0, column=1, sticky='nsew')
        
        self.custom = Button(self.subjects_container, text='Figure perimeter', bd=0, state='disabled',
                             disabledforeground=bg, bg=bg, highlightbackground=bg)
        self.custom.grid(row=1, column=0, sticky='nsew')
        
        self.number = Button(self.subjects_container, text='Figure square', bd=0, state='disabled',
                             disabledforeground=bg, bg=bg, highlightbackground=bg)
        self.number.grid(row=1, column=1, sticky='nsew')

        self.set_lang_subjectspage()

    def set_lang_subjectspage(self):
        if current_language == "eng":
            self.back_btn.config(text='Back')
            self.subjects_info.config(text="Choose subject:")
            self.algebra.config(text="Algebra")
            self.geometry.config(text="Geometry")

        elif current_language == "rus":
            self.back_btn.config(text='Назад')
            self.subjects_info.config(text="Вибери предмет:")
            self.algebra.config(text="Алгебра")
            self.geometry.config(text="Геометрия")

    def subjects_page_theme_update(self):
        self.config(bg=bg)
        self.placeholder.config(bg=bg)
        self.subjects_container.config(bg=bg)
        self.subjects_info.config(bg=bg, fg=fg)
        self.custom.config(disabledforeground=bg, bg=bg, highlightbackground=bg)
        self.number.config(disabledforeground=bg, bg=bg, highlightbackground=bg)
        self.algebra.config(bg=bg, fg=fg, activebackground=bg, activeforeground=active_fg, highlightbackground=bg)
        self.geometry.config(bg=num_bg, fg=fg, activebackground=num_bg, activeforeground=num_active_fg, highlightbackground=num_bg)
        self.back_btn.config(bg=num_bg, activebackground=num_bg, fg=home_btn_fg, activeforeground=home_btn_active_fg, highlightbackground=num_bg)


class AlgebraPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=bg)
        self.controller = controller 

        self.back_btn = Button(self, font=("Arial", 35), command=lambda: controller.show_frame(SubjectsPage), bd=0,
                               bg=num_bg, activebackground=num_bg, fg=home_btn_fg, activeforeground=home_btn_active_fg,
                               highlightbackground=num_bg)
        self.back_btn.pack(side='bottom', fill='x', ipady=5)

        self.algebra_info = Label(self, font=('Arial', 25), bg=bg, fg=fg)
        self.algebra_info.pack()

        self.placeholder = Label(self, font=('Arial', 5), bg=bg)
        self.placeholder.pack(side='bottom')

        self.algebra_container = Label(self, bg=bg)
        self.algebra_container.pack(side="left", expand=True, fill="both", padx=2)

        self.algebra_container.rowconfigure(0, weight=1)
        self.algebra_container.rowconfigure(1, weight=1)
        self.algebra_container.columnconfigure(0, weight=1)
        self.algebra_container.columnconfigure(1, weight=1)

        self.square_equation = Button(self.algebra_container, bd=0, font=('Arial', 25),
                                     bg=num_bg, fg=fg, activebackground=num_bg, activeforeground=num_active_fg,
                                     command=lambda: controller.show_frame(SqEquationPage), highlightbackground=num_bg)
        self.square_equation.grid(row=0, column=0, sticky='nsew')
        
        self.figure_perimeters = Button(self.algebra_container, text='Figure square', bd=0, state='disabled',
                                        disabledforeground=bg, bg=bg, highlightbackground=bg)
        self.figure_perimeters.grid(row=0, column=1, sticky='nsew')
        
        self.figure_perimeter = Button(self.algebra_container, text='Figure perimeter', bd=0, state='disabled',
                                       disabledforeground=bg, bg=bg, highlightbackground=bg)
        self.figure_perimeter.grid(row=1, column=0, sticky='nsew')
        
        self.figure_square = Button(self.algebra_container, text='Figure square', bd=0, state='disabled',
                                    disabledforeground=bg, bg=bg, highlightbackground=bg)
        self.figure_square.grid(row=1, column=1, sticky='nsew')

        self.set_lang_algebrapage()

    def set_lang_algebrapage(self):
        if current_language == "eng":
            self.back_btn.config(text="Back")
            self.algebra_info.config(text='Choose topic:')
            self.square_equation.config(text='Square\nequations')

        elif current_language == "rus":
            self.back_btn.config(text="Назад")
            self.algebra_info.config(text='Выбери тему:')
            self.square_equation.config(text='Квадратные\nуравнения')

    def algebra_page_theme_update(self):
        self.config(bg=bg)
        self.placeholder.config(bg=bg)
        self.algebra_container.config(bg=bg)
        self.algebra_info.config(bg=bg, fg=fg)
        self.figure_square.config(disabledforeground=bg, bg=bg, highlightbackground=bg)
        self.figure_perimeter.config(disabledforeground=bg, bg=bg, highlightbackground=bg)
        self.figure_perimeters.config(disabledforeground=bg, bg=bg, highlightbackground=bg)
        self.square_equation.config(bg=num_bg, fg=fg, activebackground=num_bg, activeforeground=num_active_fg, highlightbackground=num_bg)
        self.back_btn.config(bg=num_bg, activebackground=num_bg, fg=home_btn_fg, activeforeground=home_btn_active_fg, highlightbackground=num_bg)


class SqEquationPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=bg)
        self.controller = controller
        self.parent = parent

        # Variables:
        self.exercise_no = 0
        self.x1 = None
        self.x2 = None
        self.param = None
        self.answer = None
        self.text_e = None
        self.text_r = None
        self.start = 0
        self.task_type = None

        def container_reset():
            self.container.pack_forget()
            self.container.pack(pady=6, side='bottom')

        def update_task(full_reset=None):
            if self.start == 0:
                container_reset()
                self.start = 1
            if full_reset is None:
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
            _input = 0
            if self.answer_field.get() != "-":
                _input = int(self.answer_field.get())
            else:
                self.answer_field.insert("end", 1)
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

        self.next_btn = Button(self.btn_container, font=("Arial", 35), bd=0, highlightbackground=bg, bg=bg, 
                               activebackground=bg, fg=num_fg, activeforeground=num_active_fg, command=new_task,)
        self.next_btn.grid(row=0, column=1, ipady=5, sticky="nsew", padx=1)

        self.set_lang_sqequationpage()

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
        self.controller.show_frame(AlgebraPage)

    def validate(self, action, index, value):
        """Enter only integer values"""
        # Integers does not start from zero and there is input limit
        if value != "":
            if (index == "0" and value[0] == "0") or (index == "1" and value[0:2] == "-0"):
                return False
            if len(value) >= 7:
                return False
        
        if index != "0" and value[-1] == "-" and action == "1":
            return False
        # Confirm button status
        if value == "" and index == "0" and all(_ in "0123456789-" for _ in value):
            self.confirm_btn.config(state="disabled")
        elif "0" == index < "6" and all(_ in "0123456789-" for _ in value):
            self.confirm_btn.config(state="normal")
        # Entry validation
        if len(self.answer_field.get()) >= 6 and index != "5" and action == "1":  # Limiting input length
            return False
        elif all(_ in "0123456789-" for _ in value):  # Allowed values
            return True
        else:
            return False

    def sq_equation_page_theme_update(self):
        self.config(bg=bg)
        self.container.config(bg=bg)
        self.btn_container.config(bg=bg)
        self.text_label.config(bg=bg, fg=fg)
        self.answer_txt.config(bg=bg, disabledforeground=fg, highlightbackground=bg)
        self.exercise.config(bg=bg, fg=fg, highlightbackground=bg, highlightcolor=bg)
        self.back_btn.config(bg=num_bg, activebackground=num_bg, fg=home_btn_fg, activeforeground=home_btn_active_fg,
                             highlightbackground=num_bg)
        self.confirm_btn.config(bg=bg, fg=fg, activebackground=bg, activeforeground=active_fg, disabledforeground=bg,
                                highlightbackground=bg)
        self.next_btn.config(bg=bg, activebackground=bg, fg=num_fg, activeforeground=num_active_fg, disabledforeground=active_fg,
                             highlightbackground=bg)
        self.answer_field.config(bg=bg, fg=fg, insertbackground=fg, disabledbackground=bg, disabledforeground=fg,
                                 highlightbackground=bg, highlightcolor=bg)

    def set_lang_sqequationpage(self):
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


class GeometryPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=bg)
        self.controller = controller

        self.back_btn = Button(self, font=("Arial", 35), command=lambda: controller.show_frame(SubjectsPage), bd=0,
                               bg=num_bg, activebackground=num_bg, fg=home_btn_fg, activeforeground=home_btn_active_fg,
                               highlightbackground=num_bg)
        self.back_btn.pack(side='bottom', fill='x', ipady=5)

        self.geometry_info = Label(self, font=('Arial', 25), bg=bg, fg=fg)
        self.geometry_info.pack()

        self.placeholder = Label(self, font=('Arial', 5), bg=bg)
        self.placeholder.pack(side='bottom')

        self.geometry_container = Label(self, bg=bg)
        self.geometry_container.pack(side="left", expand=True, fill="both", padx=2)

        self.geometry_container.rowconfigure(0, weight=1)
        self.geometry_container.rowconfigure(1, weight=1)
        self.geometry_container.columnconfigure(0, weight=1)
        self.geometry_container.columnconfigure(1, weight=1)

        self.figure_squares = Button(self.geometry_container, bd=0, font=('Arial', 25),
                                     bg=num_bg, fg=fg, activebackground=num_bg, activeforeground=num_active_fg,
                                     command=lambda: controller.show_frame(AreasPage), highlightbackground=num_bg)
        self.figure_squares.grid(row=0, column=0, sticky='nsew')
        
        self.figure_perimeters = Button(self.geometry_container, bd=0, font=('Arial', 25),
                                        bg=bg, fg=fg, activebackground=bg, activeforeground=num_active_fg,
                                        command=lambda: controller.show_frame(PerimetersPage), highlightbackground=bg)
        self.figure_perimeters.grid(row=0, column=1, sticky='nsew')
        
        self.figure_perimeter = Button(self.geometry_container, text='Figure perimeter', bd=0, state='disabled',
                                       disabledforeground=bg, bg=bg, highlightbackground=bg)
        self.figure_perimeter.grid(row=1, column=0, sticky='nsew')
        
        self.figure_square = Button(self.geometry_container, text='Figure square', bd=0, state='disabled',
                                    disabledforeground=bg, bg=bg, highlightbackground=bg)
        self.figure_square.grid(row=1, column=1, sticky='nsew')

        self.set_lang_geometrypage()

    def set_lang_geometrypage(self):
        if current_language == "eng":
            self.back_btn.config(text='Back')
            self.geometry_info.config(text='Choose topic:')
            self.figure_squares.config(text='Figure\n squares ')
            self.figure_perimeters.config(text='Figure\nperimeters')

        elif current_language == 'rus':
            self.back_btn.config(text='Назад')
            self.geometry_info.config(text='Выбери тему:')
            self.figure_squares.config(text='Площади \nфигур')
            self.figure_perimeters.config(text='Периметр\nфигур')

    def geometry_page_theme_update(self):
        self.config(bg=bg)
        self.placeholder.config(bg=bg)
        self.geometry_container.config(bg=bg)
        self.geometry_info.config(bg=bg, fg=fg)
        self.figure_square.config(disabledforeground=bg, bg=bg, highlightbackground=bg)
        self.figure_perimeter.config(disabledforeground=bg, bg=bg, highlightbackground=bg)
        self.figure_perimeters.config(bg=bg, fg=fg, activebackground=bg, activeforeground=num_active_fg,
                                      highlightbackground=bg)
        self.figure_squares.config(bg=num_bg, fg=fg, activebackground=num_bg, activeforeground=num_active_fg,
                                   highlightbackground=num_bg)
        self.back_btn.config(bg=num_bg, activebackground=num_bg, fg=home_btn_fg, activeforeground=home_btn_active_fg,
                             highlightbackground=num_bg)


class AreasPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=bg)
        self.controller = controller

        self.back_btn = Button(self, font=("Arial", 35), command=lambda: controller.show_frame(GeometryPage), bd=0,
                               bg=num_bg, activebackground=num_bg, fg=home_btn_fg, activeforeground=home_btn_active_fg,
                               highlightbackground=num_bg)
        self.back_btn.pack(side='bottom', fill='x', ipady=5)
        
        self.areas_info = Label(self, font=('Arial', 25), bg=bg, fg=fg)
        self.areas_info.pack()

        self.placeholder = Label(self, font=('Arial', 5), bg=bg)
        self.placeholder.pack(side='bottom')

        self.figures_container = Label(self, bg=bg)
        self.figures_container.pack(side="left", expand=True, fill="both", padx=2)

        self.figures_container.rowconfigure(0, weight=1)
        self.figures_container.rowconfigure(1, weight=1)
        self.figures_container.columnconfigure(0, weight=1)
        self.figures_container.columnconfigure(1, weight=1)
        
        self.rectangles_a = Button(self.figures_container, bd=0, font=('Arial', 25),
                                        bg=bg, fg=fg, activebackground=bg, activeforeground=num_active_fg,
                                        command=lambda: controller.show_frame(RectanglesAPage), highlightbackground=bg)
        self.rectangles_a.grid(row=0, column=0, sticky='nsew')

        self.squares_a = Button(self.figures_container, bd=0, font=('Arial', 25),
                                bg=num_bg, fg=fg, activebackground=num_bg, activeforeground=num_active_fg,
                                command=lambda: controller.show_frame(SquaresAPage), highlightbackground=num_bg)
        self.squares_a.grid(row=0, column=1, sticky='nsew')
        
        self.figure_perimeter = Button(self.figures_container, text='Figure perimeter', bd=0, state='disabled',
                                       disabledforeground=bg, bg=bg, highlightbackground=bg)
        self.figure_perimeter.grid(row=1, column=0, sticky='nsew')
        
        self.figure_square = Button(self.figures_container, text='Figure square', bd=0, state='disabled',
                                    disabledforeground=bg, bg=bg, highlightbackground=bg)
        self.figure_square.grid(row=1, column=1, sticky='nsew')

        self.set_lang_squarespage()

    def set_lang_squarespage(self):
        if current_language == "eng":
            self.back_btn.config(text='Back')
            self.squares_a.config(text="Square's\narea")
            self.areas_info.config(text='Choose the figure:')
            self.rectangles_a.config(text="Rectangele's\narea")
        elif current_language == 'rus':
            self.rectangles_a.config(text='Площадь\nпрямоугольника')
            self.areas_info.config(text='Выберите фигуру:')
            self.squares_a.config(text='Площадь\nквадрата')
            self.back_btn.config(text='Назад')

    def areas_page_theme_update(self):
        self.config(bg=bg)
        self.placeholder.config(bg=bg)
        self.areas_info.config(bg=bg, fg=fg)
        self.figures_container.config(bg=bg)
        self.figure_square.config(disabledforeground=bg, bg=bg, highlightbackground=bg)
        self.figure_perimeter.config(disabledforeground=bg, bg=bg, highlightbackground=bg)
        self.rectangles_a.config(bg=bg, fg=fg, activebackground=bg, activeforeground=num_active_fg,
                                 highlightbackground=bg)
        self.squares_a.config(bg=num_bg, fg=fg, activebackground=num_bg, activeforeground=num_active_fg,
                              highlightbackground=num_bg)
        self.back_btn.config(bg=num_bg, activebackground=num_bg, fg=home_btn_fg, activeforeground=home_btn_active_fg,
                             highlightbackground=num_bg)


class SquaresAPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=bg)
        self.controller = controller
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
        self.controller.show_frame(AreasPage)

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

    def squares_a_page_theme_update(self):
        self.config(bg=bg)
        self.container.config(bg=bg)
        self.btn_container.config(bg=bg)
        self.text_label.config(bg=bg, fg=fg)
        self.answer_txt.config(bg=bg, disabledforeground=fg, highlightbackground=bg)
        self.exercise.config(bg=bg, fg=fg, highlightbackground=bg, highlightcolor=bg)
        self.return_btn.config(bg=num_bg, activebackground=num_bg, fg=home_btn_fg, activeforeground=home_btn_active_fg,
                               highlightbackground=num_bg)
        self.confirm_btn.config(bg=bg, fg=fg, activebackground=bg, activeforeground=active_fg, disabledforeground=active_fg,
                                highlightbackground=bg)
        self.next_btn.config(bg=bg, activebackground=bg, fg=num_fg, activeforeground=num_active_fg, disabledforeground=active_fg,
                             highlightbackground=bg)
        self.answer_field.config(bg=bg, fg=fg, insertbackground=fg, disabledbackground=bg, disabledforeground=fg,
                                 highlightbackground=bg, highlightcolor=bg)

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

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=bg)
        self.controller = controller
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
        self.controller.show_frame(AreasPage)

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

    def rectangles_a_page_theme_update(self):
        self.config(bg=bg)
        self.container.config(bg=bg)
        self.btn_container.config(bg=bg)
        self.text_label.config(bg=bg, fg=fg)
        self.answer_txt.config(bg=bg, disabledforeground=fg, highlightbackground=bg)
        self.exercise.config(bg=bg, fg=fg, highlightbackground=bg, highlightcolor=bg)
        self.back_btn.config(bg=num_bg, activebackground=num_bg, fg=home_btn_fg, activeforeground=home_btn_active_fg,
                             highlightbackground=num_bg)
        self.confirm_btn.config(bg=bg, fg=fg, activebackground=bg, activeforeground=active_fg, disabledforeground=active_fg,
                                highlightbackground=bg)
        self.next_btn.config(bg=bg, activebackground=bg, fg=num_fg, activeforeground=num_active_fg, disabledforeground=active_fg,
                             highlightbackground=bg)
        self.answer_field.config(bg=bg, fg=fg, insertbackground=fg, disabledbackground=bg, disabledforeground=fg,
                                 highlightbackground=bg, highlightcolor=bg)

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


class PerimetersPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=bg)
        self.controller = controller

        self.return_btn = Button(self, font=("Arial", 35), command=lambda: controller.show_frame(GeometryPage), bd=0,
                                 bg=num_bg, activebackground=num_bg, fg=home_btn_fg, activeforeground=home_btn_active_fg,
                                 highlightbackground=num_bg)
        self.return_btn.pack(side='bottom', fill='x', ipady=5)
        
        self.perimeters_info = Label(self, font=('Arial', 25), bg=bg, fg=fg)
        self.perimeters_info.pack()

        self.placeholder = Label(self, font=('Arial', 5), bg=bg)
        self.placeholder.pack(side='bottom')

        self.figures_container = Label(self, bg=bg)
        self.figures_container.pack(side="left", expand=True, fill="both", padx=2)

        self.figures_container.rowconfigure(0, weight=1)
        self.figures_container.rowconfigure(1, weight=1)
        self.figures_container.columnconfigure(0, weight=1)
        self.figures_container.columnconfigure(1, weight=1)

        self.squares_p = Button(self.figures_container, bd=0, font=('Arial', 25),
                                bg=bg, fg=fg, activebackground=bg, activeforeground=num_active_fg,
                                command=lambda: controller.show_frame(SquaresPPage), highlightbackground=bg)
        self.squares_p.grid(row=0, column=0, sticky='nsew')
        
        self.rectangles_p = Button(self.figures_container, bd=0, font=('Arial', 25),
                                   bg=num_bg, fg=fg, activebackground=num_bg, activeforeground=num_active_fg,
                                   command=lambda: controller.show_frame(RectanglesPPage), highlightbackground=num_bg)
        self.rectangles_p.grid(row=0, column=1, sticky='nsew')
        
        self.figure_perimeter = Button(self.figures_container, text='Figure perimeter', bd=0, state='disabled',
                                       disabledforeground=bg, bg=bg, highlightbackground=bg)
        self.figure_perimeter.grid(row=1, column=0, sticky='nsew')
        
        self.figure_square = Button(self.figures_container, text='Figure square', bd=0, state='disabled',
                                    disabledforeground=bg, bg=bg, highlightbackground=bg)
        self.figure_square.grid(row=1, column=1, sticky='nsew')

        self.set_lang_perimeterspage()

    def set_lang_perimeterspage(self):
        if current_language == "eng":
            self.return_btn.config(text='Return')
            self.squares_p.config(text="Square's\nperimeter")
            self.perimeters_info.config(text='Choose the figure:')
            self.rectangles_p.config(text="Rectangele's\nperimeter")
        elif current_language == 'rus':
            self.rectangles_p.config(text="Периметр\nпрямоугольника")
            self.perimeters_info.config(text='Выберите фигуру:')
            self.squares_p.config(text="Периметр\nквадрата")
            self.return_btn.config(text='Назад')

    def perimeters_page_theme_update(self):
        self.config(bg=bg)
        self.placeholder.config(bg=bg)
        self.figures_container.config(bg=bg)
        self.perimeters_info.config(bg=bg, fg=fg)
        self.figure_square.config(disabledforeground=bg, bg=bg, highlightbackground=bg)
        self.figure_perimeter.config(disabledforeground=bg, bg=bg, highlightbackground=bg)
        self.squares_p.config(bg=bg, fg=fg, activebackground=bg, activeforeground=num_active_fg, highlightbackground=bg)
        self.rectangles_p.config(bg=num_bg, fg=fg, activebackground=num_bg, activeforeground=num_active_fg,
                                 highlightbackground=num_bg)
        self.return_btn.config(bg=num_bg, activebackground=num_bg, fg=home_btn_fg, activeforeground=home_btn_active_fg,
                               highlightbackground=num_bg)


class SquaresPPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=bg)
        self.controller = controller
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
        self.controller.show_frame(PerimetersPage)

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

    def squares_p_page_theme_update(self):
        self.config(bg=bg)
        self.container.config(bg=bg)
        self.btn_container.config(bg=bg)
        self.text_label.config(bg=bg, fg=fg)
        self.answer_txt.config(bg=bg, disabledforeground=fg, highlightbackground=bg)
        self.exercise.config(bg=bg, fg=fg, highlightbackground=bg, highlightcolor=bg)
        self.return_btn.config(bg=num_bg, activebackground=num_bg, fg=home_btn_fg, activeforeground=home_btn_active_fg,
                               highlightbackground=num_bg)
        self.confirm_btn.config(bg=bg, fg=fg, activebackground=bg, activeforeground=active_fg, disabledforeground=active_fg,
                                highlightbackground=bg)
        self.next_btn.config(bg=bg, activebackground=bg, fg=num_fg, activeforeground=num_active_fg, disabledforeground=active_fg,
                             highlightbackground=bg)
        self.answer_field.config(bg=bg, fg=fg, insertbackground=fg, disabledbackground=bg, disabledforeground=fg,
                                 highlightbackground=bg, highlightcolor=bg)

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

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=bg)
        self.controller = controller

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
        self.controller.show_frame(PerimetersPage)

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

    def rectangles_p_page_theme_update(self):
        self.config(bg=bg)
        self.container.config(bg=bg)
        self.btn_container.config(bg=bg)
        self.text_label.config(bg=bg, fg=fg)
        self.answer_txt.config(bg=bg, disabledforeground=fg, highlightbackground=bg)
        self.exercise.config(bg=bg, fg=fg, highlightbackground=bg, highlightcolor=bg)
        self.back_btn.config(bg=num_bg, activebackground=num_bg, fg=home_btn_fg, activeforeground=home_btn_active_fg,
                             highlightbackground=num_bg)
        self.confirm_btn.config(bg=bg, fg=fg, activebackground=bg, activeforeground=active_fg, disabledforeground=active_fg,
                                highlightbackground=bg)
        self.next_btn.config(bg=bg, activebackground=bg, fg=num_fg, activeforeground=num_active_fg, disabledforeground=active_fg,
                             highlightbackground=bg)
        self.answer_field.config(bg=bg, fg=fg, insertbackground=fg, disabledbackground=bg, disabledforeground=fg,
                                 highlightbackground=bg, highlightcolor=bg)

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

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller


class ShowTaskOptions(Toplevel):

    def __init__(self, parent):
        Toplevel.__init__(self, parent)

        self.title("Show tasks for generation")
        self.geometry("400x400")
        self.transient(parent)
        self.grab_set()


class ShowTaskPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

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

        return_btn = Button(btn_container, font=("Arial", 35), command=lambda: controller.show_frame(MainPage), bd=0, bg=num_bg,
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

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=bg)
        self.controller = controller
        def call_link(_):
            open_new_tab("https://github.com/TerraBoii")

        def enter(_):
            self.created_by.config(font=("Tahoma", 15, "underline"))

        def leave(_):
            self.created_by.config(font=("Tahoma", 15))

        self.created_by= Label(self, bg=bg, fg="#213c91", text="Created by: TerraBoii", 
                               font=("Tahoma", 15), cursor='hand2')
        self.created_by.pack(side='top')
        self.created_by.bind("<Enter>", enter)
        self.created_by.bind("<Leave>", leave)
        self.created_by.bind("<Button-1>", call_link)

        # Separator or placeholder
        self.place_h0 = Label(self, bg=bg, font=('Arial', 25))
        self.place_h0.pack()

        self.language_changers_container = Label(self, bg=bg)
        self.language_changers_container.pack(anchor='n')

        self.language_changers_container.rowconfigure(0, weight=1)
        self.language_changers_container.columnconfigure(0, weight=1)
        self.language_changers_container.columnconfigure(1, weight=1)
        self.language_changers_container.columnconfigure(2, weight=1)

        self.language_info = Button(self.language_changers_container, bg=bg, disabledforeground=fg,
                                    font=("Arial", 35), state='disabled', bd=0, highlightbackground=bg)
        self.language_info.grid(row=0, column=0, sticky="nsew")

        self.english_lang_btn = Button(self.language_changers_container, text="English", bg=num_bg, fg=num_fg,
                                       font=("Arial", 35), disabledforeground=num_bg, highlightbackground=num_bg,
                                       activeforeground=num_active_fg, activebackground=num_bg, bd=0,
                                       command=lambda: self.language_changer(_lang_="eng"))
        self.english_lang_btn.grid(row=0, column=1)

        self.russian_lang_btn = Button(self.language_changers_container, text="Русский", bg=bg, fg=fg,
                                       font=("Arial", 35), disabledforeground=bg, highlightbackground=bg,
                                       activeforeground=active_fg, activebackground=bg, bd=0,
                                       command=lambda: self.language_changer(_lang_="rus"))
        self.russian_lang_btn.grid(row=0, column=2)

        # Separator or placeholder
        self.place_h1 = Label(self, bg=bg, font=('Arial', 30))
        self.place_h1.pack()

        self.themes_changers_container = Label(self, bg=bg)
        self.themes_changers_container.pack(anchor='n')

        self.themes_changers_container.rowconfigure(0, weight=1)
        self.themes_changers_container.columnconfigure(0, weight=1)
        self.themes_changers_container.columnconfigure(1, weight=1)
        self.themes_changers_container.columnconfigure(2, weight=1)
        self.themes_changers_container.columnconfigure(3, weight=1)
        
        self.theme_info = Label(self.themes_changers_container, bg=bg, fg=fg, font=("Arial", 35))
        self.theme_info.grid(row=0, column=0, sticky="nsew")

        self.dark_theme_btn = Button(self.themes_changers_container, text="Dark", bg=num_bg, fg=num_fg,
                                     font=("Arial", 40), command=self.change_theme_to_dark, bd=0, highlightbackground=num_bg,
                                     activeforeground=num_active_fg, activebackground=num_bg, disabledforeground=num_bg)
        self.dark_theme_btn.grid(row=0, column=1, sticky='nsew')

        self.light_theme_btn = Button(self.themes_changers_container, text="Light", bg=bg, fg=fg,
                                      font=("Arial", 40), highlightbackground=bg,
                                      activeforeground=active_fg, activebackground=bg, bd=0, disabledforeground=bg,
                                      command=self.change_theme_to_light)
        self.light_theme_btn.grid(row=0, column=3, sticky='nsew')

        # Separator or placeholder
        self.place_h2 = Label(self, bg=bg, font=('Arial', 20))
        self.place_h2.pack()

        self.home_button = Button(self, text="Home", bg=num_bg, fg=home_btn_fg, font=("Arial", 45),
                                  activeforeground=home_btn_active_fg, activebackground=num_bg, bd=0,
                                  disabledforeground=num_bg, command=lambda: controller.show_frame(MainPage),
                                  highlightbackground=num_bg)
        self.home_button.pack(fill='both', side='bottom', expand=True)

        # Checking for current theme
        if current_theme == 'dark':
            self.dark_theme_btn.config(state='disabled', cursor="")
            self.light_theme_btn.config(state='normal', cursor="hand2")
        elif current_theme == 'light':
            self.dark_theme_btn.config(state='normal', cursor="hand2")
            self.light_theme_btn.config(state='disabled', cursor="")

        self.bind("<Configure>", lambda params: self.font_changer(params.width))

        self.set_lang_settingspage()

    def font_changer(self, width):
        """Changing font size based on window width"""
        if width <= 959:
            self.theme_info.config(font=('Arial', 42))
            self.home_button.config(font=('Arial', 45))
            self.dark_theme_btn.config(font=('Arial', 42))
            self.light_theme_btn.config(font=('Arial', 42))
        elif 959 < width <= 1160:
            self.light_theme_btn.config(font=('Arial', 50))
            self.dark_theme_btn.config(font=('Arial', 50))
            self.home_button.config(font=('Arial', 55))
            self.theme_info.config(font=('Arial', 50))
        elif width > 1160:
            self.theme_info.config(font=('Arial', 55))
            self.home_button.config(font=('Arial', 55))
            self.dark_theme_btn.config(font=('Arial', 55))
            self.light_theme_btn.config(font=('Arial', 55))

    def language_changer(self, _lang_: str):
        """Changes language from setting page and fixes its font"""
        _page = self.controller.get_page(FLaunchPage)  # Getting access to FLaunchPage in oreder to use new_lang method
        _page.new_lang('', lang=_lang_, _from='')
        self.font_changer(self.winfo_width())  # Changing font size so everything will fit in the window

    def set_lang_settingspage(self):
        if current_language == "eng":
            self.russian_lang_btn.config(state='normal', cursor="hand2")
            self.english_lang_btn.config(state='disabled', cursor="")
            self.language_info.config(text='Language:')
            self.light_theme_btn.config(text='Light')
            self.dark_theme_btn.config(text='Dark')
            self.theme_info.config(text='Theme:')
            self.home_button.config(text='Home')
        elif current_language == 'rus':
            self.theme_info.config(text='Тема:')
            self.home_button.config(text='Назад')
            self.language_info.config(text='Язык:')
            self.dark_theme_btn.config(text='Тёмная')
            self.light_theme_btn.config(text='Светлая')
            self.russian_lang_btn.config(state='disabled', cursor="")
            self.english_lang_btn.config(state='normal', cursor="hand2")
        self.font_changer(self.winfo_width())

    def settings_page_theme_update(self):
        self.config(bg=bg)
        self.place_h0.config(bg=bg)
        self.place_h1.config(bg=bg)
        self.place_h2.config(bg=bg)
        self.created_by.config(bg=bg)
        self.theme_info.config(bg=bg, fg=fg)
        self.themes_changers_container.config(bg=bg)
        self.language_changers_container.config(bg=bg)
        self.language_info.config(bg=bg, disabledforeground=fg, highlightbackground=bg)
        self.light_theme_btn.config(bg=bg, fg=fg, activeforeground=active_fg, activebackground=bg, disabledforeground=bg,
                                    highlightbackground=bg)
        self.russian_lang_btn.config(bg=bg, fg=fg, disabledforeground=bg, activeforeground=active_fg, activebackground=bg,
                                     highlightbackground=bg)
        self.dark_theme_btn.config(bg=num_bg, fg=num_fg, activeforeground=num_active_fg, activebackground=num_bg,
                                   disabledforeground=num_bg, highlightbackground=num_bg)
        self.english_lang_btn.config(bg=num_bg, fg=num_fg, disabledforeground=num_bg, activeforeground=num_active_fg,
                                     activebackground=num_bg, highlightbackground=num_bg)
        self.home_button.config(bg=num_bg, fg=home_btn_fg, activeforeground=home_btn_active_fg, activebackground=num_bg,
                                disabledforeground=num_bg, highlightbackground=num_bg)

    def pages_update(self):
        # Get page's method that changes its theme
        self.controller.get_page(RectanglesAPage).rectangles_a_page_theme_update()
        self.controller.get_page(RectanglesPPage).rectangles_p_page_theme_update()
        self.controller.get_page(SqEquationPage).sq_equation_page_theme_update()
        self.controller.get_page(PerimetersPage).perimeters_page_theme_update()
        self.controller.get_page(SquaresPPage).squares_p_page_theme_update()
        self.controller.get_page(SquaresAPage).squares_a_page_theme_update()
        self.controller.get_page(SettingsPage).settings_page_theme_update()
        self.controller.get_page(SubjectsPage).subjects_page_theme_update()
        self.controller.get_page(GeometryPage).geometry_page_theme_update()
        self.controller.get_page(AlgebraPage).algebra_page_theme_update()
        self.controller.get_page(AreasPage).areas_page_theme_update()
        self.controller.get_page(MainPage).main_page_theme_update()

    def change_theme_to_dark(self):
        self.light_theme_btn.config(state='normal', cursor="hand2")
        self.dark_theme_btn.config(state='disabled', cursor="")
        dark_theme()
        self.pages_update()

    def change_theme_to_light(self):
        self.dark_theme_btn.config(state='normal', cursor="hand2")
        self.light_theme_btn.config(state='disabled', cursor="")
        light_theme()
        self.pages_update()


class ExtraSettings(Toplevel):
    
    def __init__(self, parent):
        Toplevel.__init__(self, parent, bg=bg)


if __name__ == "__main__":
    MainAppBody().mainloop()  # Launch application