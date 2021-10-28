from tkinter import Tk, Frame, Label, Button, Entry, Text
from generators import perimeter_task, area_task
from configparser import ConfigParser
from webbrowser import open_new_tab

__version__ = '0.1'
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
    parser.set('parameters', 'height', _height_)
    parser.set('parameters', 'zoomed', _state_)
    parser.set('parameters', 'width', _width_)
    parser.set('parameters', 'x', _x_)
    parser.set('parameters', 'y', _y_)
    with open("data.txt", "w") as configfile:
        parser.write(configfile)


class MainAppBody(Tk):  # Main application with page logic

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("Math problem generator")
        self.iconbitmap("images//main_icon.ico")
        # Setting max and min sizes for the app
        self.minsize(width=800, height=600)
        self.maxsize(self.winfo_screenwidth(), self.winfo_screenheight())

        # creating window:
        if current_language == "unknown" or lng_state == "ask":
            middle_x = int((self.winfo_screenwidth() - 800) / 2)
            middle_y = int((self.winfo_screenheight() - 600) / 2)
            self.geometry(f"{800}x{600}+{middle_x}+{middle_y}")  # Middle pos on the screen
        else:
            self.geometry(f"{int(_width)}x{int(_height)}+{int(x_pos) - 8}+{(int(y_pos))-31}")  # (- 8) and (- 31) is important

        # Rewriting default delete method in order to save window parameters
        self.protocol('WM_DELETE_WINDOW', self.delete_window)
        if _state == 'yes':
            self.state('zoomed')


        container = Frame(self, bg="black")
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.frames = {}

        frame_collection = (FLaunchPage, TopicsPage, MainPage, SettingsPage, AreasPage, PerimetersPage, SquaresAPage, 
                            RectanglesAPage, SquaresPPage, RectanglesPPage)

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
                                   str(self.winfo_rootx()), str(self.winfo_rooty()), 'yes')
        elif self.wm_state() != "zoomed" and lng_state != "ask" and current_language != "unknown":
            save_window_parameters(str(self.winfo_width()), str(self.winfo_height()),
                                   str(self.winfo_rootx()), str(self.winfo_rooty()), 'no')
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
                         activeforeground="#008000", font=("Arial", 30), bd=0)
        self.russian.grid(row=0, column=0, sticky="nsew")

        self.english = Button(lang_btn_container, text="English", bg="black", fg="#00ff00",
                         activeforeground="#008000", font=("Arial", 30), bd=0)
        self.english.grid(row=1, column=0, sticky="nsew")

        def entered(_, btn, lang: str):
            btn.config(bg="#008000", activebackground="#00ff00")
            _question_text = _hint_text = ''
            if lang == "eng":
                _question_text = "\nChoose language:"
                _hint_text = "Note: you can always change\nlanguage in settings menu"
            elif lang == "rus":
                _question_text = "\nВыберите язык:"
                _hint_text = "Подсказка: всегда можно\nизменить язык в настройках"
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
        page = self.controller.get_page(RectanglesAPage)
        page.set_lang_rectanglesaspage()
        page = self.controller.get_page(RectanglesPPage)
        page.set_lang_rectanglesppage()
        page = self.controller.get_page(PerimetersPage)
        page.set_lang_perimeterspage()
        page = self.controller.get_page(SettingsPage)
        page.set_lang_settingspage()
        page = self.controller.get_page(SquaresAPage)
        page.set_lang_squaresapage()
        page = self.controller.get_page(SquaresPPage)
        page.set_lang_squaresppage()
        page = self.controller.get_page(AreasPage)
        page.set_lang_squarespage()
        page = self.controller.get_page(TopicsPage)
        page.set_lang_topicspage()
        page = self.controller.get_page(MainPage)
        page.set_lang_mainpage()

        if _from is None:  # We don't need to go to main page after switching language in settings
            self.controller.show_frame(MainPage)


class MainPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=bg)
        self.controller = controller

        self.text_label = Label(self, font=("Verdana", 45), bg=bg, fg=fg)
        self.text_label.pack(fill='both', expand=True)

        self.start_button = Button(self, bg=num_bg, fg=fg, font=("Arial", 45),
                                   activeforeground=active_fg, activebackground=num_bg, bd=0,
                                   disabledforeground=num_bg, command=lambda: controller.show_frame(TopicsPage))
        self.start_button.pack(fill='both', pady=2, expand=True)

        self.settings_button = Button(self, bg=num_bg, fg=home_btn_fg, font=("Arial", 45),
                                      activeforeground=home_btn_active_fg, activebackground=num_bg, bd=0,
                                      disabledforeground=num_bg, command=lambda: controller.show_frame(SettingsPage))
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
        self.start_button.config(bg=num_bg, fg=fg, activeforeground=num_active_fg, activebackground=num_bg)
        self.settings_button.config(bg=num_bg, fg=home_btn_fg, activeforeground=home_btn_active_fg, activebackground=num_bg)


class TopicsPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=bg)
        self.controller = controller

        self.home_btn = Button(self, font=("Arial", 35), command=lambda: controller.show_frame(MainPage), bd=0,
                               bg=num_bg, activebackground=num_bg, fg=home_btn_fg, activeforeground=home_btn_active_fg)
        self.home_btn.pack(side='bottom', fill='x', ipady=5)

        self.topics_info = Label(self, font=('Arial', 25), bg=bg, fg=fg)
        self.topics_info.pack()

        self.placeholder = Label(self, font=('Arial', 5), bg=bg)
        self.placeholder.pack(side='bottom')

        self.topics_container = Label(self, bg=bg)
        self.topics_container.pack(side="left", expand=True, fill="both", padx=2)

        self.topics_container.rowconfigure(0, weight=1)
        self.topics_container.rowconfigure(1, weight=1)
        self.topics_container.columnconfigure(0, weight=1)
        self.topics_container.columnconfigure(1, weight=1)

        self.figure_squares = Button(self.topics_container, bd=0, font=('Arial', 25),
                                     bg=num_bg, fg=fg, activebackground=num_bg, activeforeground=num_active_fg,
                                     command=lambda: controller.show_frame(AreasPage))
        self.figure_squares.grid(row=0, column=0, sticky='nsew')
        
        self.figure_perimeters = Button(self.topics_container, bd=0, font=('Arial', 25),
                                        bg=bg, fg=fg, activebackground=bg, activeforeground=num_active_fg,
                                        command=lambda: controller.show_frame(PerimetersPage))
        self.figure_perimeters.grid(row=0, column=1, sticky='nsew')
        
        self.figure_perimeter = Button(self.topics_container, text='Figure perimeter', bd=0, state='disabled',
                                       disabledforeground=bg, bg=bg)
        self.figure_perimeter.grid(row=1, column=0, sticky='nsew')
        
        self.figure_square = Button(self.topics_container, text='Figure square', bd=0, state='disabled',
                                    disabledforeground=bg, bg=bg)
        self.figure_square.grid(row=1, column=1, sticky='nsew')

        self.set_lang_topicspage()

    def set_lang_topicspage(self):
        if current_language == "eng":
            self.home_btn.config(text='Home')
            self.topics_info.config(text='Choose topic:')
            self.figure_squares.config(text='Figure\n squares ')
            self.figure_perimeters.config(text='Figure\nperimeters')

        elif current_language == 'rus':
            self.home_btn.config(text='Назад')
            self.topics_info.config(text='Выбери тему:')
            self.figure_squares.config(text='Площади \nфигур')
            self.figure_perimeters.config(text='Периметр\nфигур')

    def topics_page_theme_update(self):
        self.config(bg=bg)
        self.placeholder.config(bg=bg)
        self.topics_container.config(bg=bg)
        self.topics_info.config(bg=bg, fg=fg)
        self.figure_square.config(disabledforeground=bg, bg=bg)
        self.figure_perimeter.config(disabledforeground=bg, bg=bg)
        self.figure_perimeters.config(bg=bg, fg=fg, activebackground=bg, activeforeground=num_active_fg)
        self.figure_squares.config(bg=num_bg, fg=fg, activebackground=num_bg, activeforeground=num_active_fg)
        self.home_btn.config(bg=num_bg, activebackground=num_bg, fg=home_btn_fg, activeforeground=home_btn_active_fg)


class AreasPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=bg)
        self.controller = controller

        self.back_btn = Button(self, font=("Arial", 35), command=lambda: controller.show_frame(TopicsPage), bd=0,
                               bg=num_bg, activebackground=num_bg, fg=home_btn_fg, activeforeground=home_btn_active_fg)
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
                                        command=lambda: controller.show_frame(RectanglesAPage))
        self.rectangles_a.grid(row=0, column=0, sticky='nsew')

        self.squares_a = Button(self.figures_container, bd=0, font=('Arial', 25),
                                     bg=num_bg, fg=fg, activebackground=num_bg, activeforeground=num_active_fg,
                                     command=lambda: controller.show_frame(SquaresAPage))
        self.squares_a.grid(row=0, column=1, sticky='nsew')
        
        self.figure_perimeter = Button(self.figures_container, text='Figure perimeter', bd=0, state='disabled',
                                       disabledforeground=bg, bg=bg)
        self.figure_perimeter.grid(row=1, column=0, sticky='nsew')
        
        self.figure_square = Button(self.figures_container, text='Figure square', bd=0, state='disabled',
                                    disabledforeground=bg, bg=bg)
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
        self.figure_square.config(disabledforeground=bg, bg=bg)
        self.figure_perimeter.config(disabledforeground=bg, bg=bg)
        self.rectangles_a.config(bg=bg, fg=fg, activebackground=bg, activeforeground=num_active_fg)
        self.squares_a.config(bg=num_bg, fg=fg, activebackground=num_bg, activeforeground=num_active_fg)
        self.back_btn.config(bg=num_bg, activebackground=num_bg, fg=home_btn_fg, activeforeground=home_btn_active_fg)


class SquaresAPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=bg)
        self.controller = controller

        task_data = area_task('square', __version__, self.winfo_width(), self.winfo_height(), 
                                self.winfo_screenwidth(), self.winfo_screenheight())

        # Variables:
        self.exercise_no = task_data[-1]
        self.param = task_data[0]

        self.exercise = Label(self, bg=bg, fg=fg, font=('Arial', 27), anchor='w')
        self.exercise.pack(fill="x", pady=8, side='top')

        self.text_label = Label(self, bg=bg, fg=fg, font=('Arial', 20))
        self.text_label.pack(pady=4)

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

        self.answer_txt = Button(self.container, bg=bg, disabledforeground=fg, state="disabled", bd=0, font=("Arial", 32))
        self.answer_txt.grid(row=0, column=0)

        is_valid = (parent.register(self.validate), '%i', '%P') # index, value

        def click(_):
            # Reset entry widget
            self.answer_field.config(state='normal')
            self.answer_field.unbind('<Button-1>')
            self.answer_field.delete(0, 'end')

        self.answer_field = Entry(self.container, font=("Arial", 32), validatecommand=is_valid, validate="key", width=6,
                                  bg=bg, fg=fg, insertbackground=fg, disabledbackground=bg, disabledforeground=fg)
        self.answer_field.grid(row=0, column=1)

        self.placeholder = Label(self.container, font=('Arial', 32), bg=bg, fg=bg)
        self.placeholder.grid(row=0, column=2)
        
        self.clicked = self.answer_field.bind('<Button-1>', click)

        self.return_btn = Button(self.btn_container, font=("Arial", 35), command=lambda: self.return_back(), bd=0,
                                 bg=num_bg, activebackground=num_bg, fg=home_btn_fg, activeforeground=home_btn_active_fg)
        self.return_btn.grid(row=0, column=0, ipady=5, sticky="nsew", padx=1)

        self.next_btn = Button(self.btn_container, font=("Arial", 35), bd=0,
                               bg=num_bg, activebackground=num_bg, fg=num_fg, activeforeground=num_active_fg)
        self.next_btn.grid(row=0, column=1, ipady=5, sticky="nsew", padx=1)

        self.set_lang_squaresapage()

    def return_back(self):
        self.clicked
        self.answer_field.delete(0, "end")
        self.answer_field.config(state='disabled')
        self.controller.show_frame(AreasPage)

    def validate(self, index, value):
        """Enter only integer values"""
        if len(self.answer_field.get()) >= 6 and index != "5":  # Limiting input length
            return False
        elif all(_ in "0123456789" for _ in value):  # Allowed values
            return True
        else:
            return False

    def squares_a_page_theme_update(self):
        self.config(bg=bg)
        self.container.config(bg=bg)
        self.text_label.config(bg=bg, fg=fg)
        self.btn_container.config(bg=bg)
        self.exercise.config(bg=bg, fg=fg)
        self.placeholder.config(bg=bg, fg=bg)
        self.answer_txt.config(bg=bg, disabledforeground=fg)
        self.next_btn.config(bg=num_bg, activebackground=num_bg, fg=num_fg, activeforeground=num_active_fg)
        self.answer_field.config(bg=bg, fg=fg, insertbackground=fg, disabledbackground=bg, disabledforeground=fg)
        self.return_btn.config(bg=num_bg, activebackground=num_bg, fg=home_btn_fg, activeforeground=home_btn_active_fg)

    def set_lang_squaresapage(self):
        if current_language == "eng":
            self.answer_txt.config(text='Answer: ')
            self.return_btn.config(text='Return')
            self.next_btn.config(text="New task")
            self.placeholder.config(text="oooo")
            self.text_label.config(text="Find square's area")
            self.exercise.config(text=f"  Exercise: {self.exercise_no}")
        elif current_language == 'rus':
            self.exercise.config(text=f"  Номер: {self.exercise_no}")
            self.next_btn.config(text="Новое задание")
            self.placeholder.config(text="ooooooooo")
            self.text_label.config(text="Условие задачи")
            self.return_btn.config(text='Назад')
            self.answer_txt.config(text='Ответ: ')


class RectanglesAPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=bg)
        self.controller = controller

        task_data = area_task('rectangle', __version__, self.winfo_width(), self.winfo_height(), 
                                self.winfo_screenwidth(), self.winfo_screenheight())

        # Variables:
        self.exercise_no = task_data[-1]
        self.param = (task_data[0], task_data[1])
        self.answer = task_data[2]
        self.text_e = "Your goal is to find rectangle's area." \
                      f"\nIts height is {self.param[0]} and width is {self.param[1]}."
        self.text_r = "Чему равна площадь прямоугольника,\nесли его высота равна " \
                      f"{self.param[0]}, а ширина {self.param[1]}."

        def container_reset():
            self.container.pack_forget()
            self.container.pack(pady=6, side='bottom')

        def update_task(full_reset=None):
            if full_reset is None:
                task_data = area_task('rectangle', __version__, self.winfo_width(), self.winfo_height(), 
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

        self.exercise = Text(self, bg=bg, fg=fg, font=('Arial', 27), borderwidth=0, height=1)
        self.exercise.pack(fill="x", pady=8, side='top')
        self.exercise.configure(inactiveselectbackground=self.exercise.cget("selectbackground"))

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

        self.answer_txt = Button(self.container, bg=bg, disabledforeground=fg, state="disabled", bd=0, font=("Arial", 32))
        self.answer_txt.grid(row=0, column=0)

        is_valid = (parent.register(self.validate), '%d', '%i', '%P') # action, index, value

        def click(_):
            self.answer_field.config(state='normal')

        def confirm():
            _input = int(self.answer_field.get())
            self.answer_field.delete(0, 'end')
            self.answer_field.config(state='disabled')
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
            self.after(501, container_reset)

        self.answer_field = Entry(self.container, font=("Arial", 32), validatecommand=is_valid, validate="key", width=6,
                                  bg=bg, fg=fg, insertbackground=fg, disabledbackground=bg, disabledforeground=fg)
        self.answer_field.grid(row=0, column=1)

        self.confirm_btn = Button(self.container, font=('Arial', 32), command=confirm, bd=0, disabledforeground=active_fg,
                                  bg=bg, fg=fg, activebackground=bg, activeforeground=active_fg, state="disabled")
        self.confirm_btn.grid(row=0, column=2)
        
        self.answer_field.bind('<Button-1>', click)

        self.back_btn = Button(self.btn_container, font=("Arial", 35), command=self.return_back, bd=0,
                               bg=num_bg, activebackground=num_bg, fg=home_btn_fg, activeforeground=home_btn_active_fg)
        self.back_btn.grid(row=0, column=0, ipady=5, sticky="nsew", padx=1)

        self.next_btn = Button(self.btn_container, font=("Arial", 35), bd=0,
                               bg=num_bg, activebackground=num_bg, fg=num_fg, activeforeground=num_active_fg)
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

    def rectangles_a_page_theme_upgrade(self):
        self.config(bg=bg)
        self.container.config(bg=bg)
        self.btn_container.config(bg=bg)
        self.text_label.config(bg=bg, fg=fg)
        self.exercise.config(bg=bg, disabledforeground=fg)
        self.answer_txt.config(bg=bg, disabledforeground=fg)
        self.next_btn.config(bg=bg, activebackground=bg, fg=num_fg, activeforeground=num_active_fg)
        self.answer_field.config(bg=bg, fg=fg, insertbackground=fg, disabledbackground=bg, disabledforeground=fg)
        self.back_btn.config(bg=num_bg, activebackground=num_bg, fg=home_btn_fg, activeforeground=home_btn_active_fg)
        self.confirm_btn.config(bg=bg, fg=fg, activebackground=bg, activeforeground=active_fg, disabledforeground=active_fg)

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
        elif current_language == 'rus':
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

        self.return_btn = Button(self, font=("Arial", 35), command=lambda: controller.show_frame(TopicsPage), bd=0,
                               bg=num_bg, activebackground=num_bg, fg=home_btn_fg, activeforeground=home_btn_active_fg)
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
                                     bg=num_bg, fg=fg, activebackground=num_bg, activeforeground=num_active_fg,
                                     command=lambda: controller.show_frame(SquaresPPage))
        self.squares_p.grid(row=0, column=0, sticky='nsew')
        
        self.rectangles_p = Button(self.figures_container, bd=0, font=('Arial', 25),
                                        bg=bg, fg=fg, activebackground=bg, activeforeground=num_active_fg,
                                        command=lambda: controller.show_frame(RectanglesPPage))
        self.rectangles_p.grid(row=0, column=1, sticky='nsew')
        
        self.figure_perimeter = Button(self.figures_container, text='Figure perimeter', bd=0, state='disabled',
                                       disabledforeground=bg, bg=bg)
        self.figure_perimeter.grid(row=1, column=0, sticky='nsew')
        
        self.figure_square = Button(self.figures_container, text='Figure square', bd=0, state='disabled',
                                    disabledforeground=bg, bg=bg)
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
        self.figure_square.config(disabledforeground=bg, bg=bg)
        self.figure_perimeter.config(disabledforeground=bg, bg=bg)
        self.rectangles_p.config(bg=bg, fg=fg, activebackground=bg, activeforeground=num_active_fg)
        self.squares_p.config(bg=num_bg, fg=fg, activebackground=num_bg, activeforeground=num_active_fg)
        self.return_btn.config(bg=num_bg, activebackground=num_bg, fg=home_btn_fg, activeforeground=home_btn_active_fg)


class SquaresPPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=bg)
        self.controller = controller

        task_data = perimeter_task('square', __version__, self.winfo_width(), self.winfo_height(), 
                                self.winfo_screenwidth(), self.winfo_screenheight())

        # Variables:
        self.exercise_no = task_data[-1]
        self.param = task_data[0]

        self.exercise = Label(self, bg=bg, fg=fg, font=('Arial', 27), anchor='w')
        self.exercise.pack(fill="x", pady=8, side='top')

        self.text_label = Label(self, bg=bg, fg=fg, font=('Arial', 20))
        self.text_label.pack(pady=4)

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

        self.answer_txt = Button(self.container, bg=bg, disabledforeground=fg, state="disabled", bd=0, font=("Arial", 32))
        self.answer_txt.grid(row=0, column=0)

        is_valid = (parent.register(self.validate), '%d', '%i', '%P') # action, index, value

        def click(_):
            self.answer_field.config(state='normal')

        self.answer_field = Entry(self.container, font=("Arial", 32), validatecommand=is_valid, validate="key", width=6,
                                  bg=bg, fg=fg, insertbackground=fg, disabledbackground=bg, disabledforeground=fg)
        self.answer_field.grid(row=0, column=1)

        self.placeholder = Label(self.container, font=('Arial', 32), bg=bg, fg=bg)
        self.placeholder.grid(row=0, column=2)
        
        self.answer_field.bind('<Button-1>', click)

        self.return_btn = Button(self.btn_container, font=("Arial", 35), command=lambda: self.return_back(), bd=0,
                                 bg=num_bg, activebackground=num_bg, fg=home_btn_fg, activeforeground=home_btn_active_fg)
        self.return_btn.grid(row=0, column=0, ipady=5, sticky="nsew", padx=1)

        self.next_btn = Button(self.btn_container, font=("Arial", 35), bd=0,
                               bg=num_bg, activebackground=num_bg, fg=num_fg, activeforeground=num_active_fg)
        self.next_btn.grid(row=0, column=1, ipady=5, sticky="nsew", padx=1)

        self.set_lang_squaresppage()

    def return_back(self):
        self.answer_field.delete(0, "end")
        self.answer_field.config(state='disabled')
        self.controller.show_frame(PerimetersPage)

    def validate(self, action, index, value):
        """Enter only integer values"""
        if len(self.answer_field.get()) >= 6 and index != "5" and action == "1":  # Limiting input length
            print('limit reached')
            return False
        elif all(_ in "0123456789" for _ in value):  # Allowed values
            return True
        else:
            return False

    def squares_p_page_theme_update(self):
        self.config(bg=bg)
        self.container.config(bg=bg)
        self.text_label.config(bg=bg, fg=fg)
        self.btn_container.config(bg=bg)
        self.exercise.config(bg=bg, fg=fg)
        self.placeholder.config(bg=bg, fg=bg)
        self.answer_txt.config(bg=bg, disabledforeground=fg)
        self.next_btn.config(bg=num_bg, activebackground=num_bg, fg=num_fg, activeforeground=num_active_fg)
        self.answer_field.config(bg=bg, fg=fg, insertbackground=fg, disabledbackground=bg, disabledforeground=fg)
        self.return_btn.config(bg=num_bg, activebackground=num_bg, fg=home_btn_fg, activeforeground=home_btn_active_fg)

    def set_lang_squaresppage(self):
        if current_language == "eng":
            self.answer_txt.config(text='Answer: ')
            self.return_btn.config(text='Return')
            self.next_btn.config(text="New task")
            self.placeholder.config(text="oooo")
            self.text_label.config(text="Find square's perimeter")
            self.exercise.config(text=f"  Exercise: {self.exercise_no}")
        elif current_language == 'rus':
            self.exercise.config(text=f"  Номер: {self.exercise_no}")
            self.next_btn.config(text="Новое задание")
            self.placeholder.config(text="ooooooooo")
            self.text_label.config(text="Условие задачи")
            self.return_btn.config(text='Назад')
            self.answer_txt.config(text='Ответ: ')


class RectanglesPPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=bg)
        self.controller = controller

        task_data = perimeter_task('rectangle', __version__, self.winfo_width(), self.winfo_height(), 
                                self.winfo_screenwidth(), self.winfo_screenheight())

        # Variables:
        self.exercise_no = task_data[-1]
        self.param = (task_data[0], task_data[1])
        self.answer = task_data[2]
        self.text_e = "Your goal is to find rectangle's perimeter." \
                      f"\nIts height is {self.param[0]} and width is {self.param[1]}."
        self.text_r = "Чему равен периметр прямоугольника,\nесли его высота равна " \
                      f"{self.param[0]}, а ширина {self.param[1]}."

        def container_reset():
            self.container.pack_forget()
            self.container.pack(pady=6, side='bottom')

        def update_task(full_reset=None):
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

        self.exercise = Text(self, bg=bg, fg=fg, font=('Arial', 27), borderwidth=0, height=1)
        self.exercise.pack(fill="x", pady=8, side='top')
        self.exercise.configure(inactiveselectbackground=self.exercise.cget("selectbackground"))

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

        self.answer_txt = Button(self.container, bg=bg, disabledforeground=fg, state="disabled", bd=0, font=("Arial", 32))
        self.answer_txt.grid(row=0, column=0)

        is_valid = (parent.register(self.validate), '%d', '%i', '%P') # action, index, value

        def click(_):
            self.answer_field.config(state='normal')

        def confirm():
            _input = int(self.answer_field.get())
            self.answer_field.delete(0, "end")
            self.answer_field.config(state='disabled')
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
            self.after(501, container_reset)


        self.answer_field = Entry(self.container, font=("Arial", 32), validatecommand=is_valid, validate="key", width=6,
                                  bg=bg, fg=fg, insertbackground=fg, disabledbackground=bg, disabledforeground=bg)
        self.answer_field.grid(row=0, column=1)

        self.confirm_btn = Button(self.container, font=('Arial', 32), command=confirm, bd=0, disabledforeground=active_fg,
                                  bg=bg, fg=fg, activebackground=bg, activeforeground=active_fg, state="disabled")
        self.confirm_btn.grid(row=0, column=2)
        
        self.answer_field.bind('<Button-1>', click)

        self.back_btn = Button(self.btn_container, font=("Arial", 35), command=self.return_back, bd=0,
                               bg=num_bg, activebackground=num_bg, fg=home_btn_fg, activeforeground=home_btn_active_fg)
        self.back_btn.grid(row=0, column=0, ipady=5, sticky="nsew", padx=1)

        self.next_btn = Button(self.btn_container, font=("Arial", 35), bd=0,
                               bg=bg, activebackground=bg, fg=num_fg, activeforeground=num_active_fg)
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

    def rectangles_p_page_theme_upgrade(self):
        self.config(bg=bg)
        self.container.config(bg=bg)
        self.btn_container.config(bg=bg)
        self.text_label.config(bg=bg, fg=fg)
        self.exercise.config(bg=bg, disabledforeground=fg)
        self.answer_txt.config(bg=bg, disabledforeground=fg)
        self.next_btn.config(bg=bg, activebackground=bg, fg=num_fg, activeforeground=num_active_fg)
        self.answer_field.config(bg=bg, fg=fg, insertbackground=fg, disabledbackground=bg, disabledforeground=fg)
        self.back_btn.config(bg=num_bg, activebackground=num_bg, fg=home_btn_fg, activeforeground=home_btn_active_fg)
        self.confirm_btn.config(bg=bg, fg=fg, activebackground=bg, activeforeground=active_fg, disabledforeground=active_fg)

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
        elif current_language == 'rus':
            self.exercise.insert("0.0", f"  Номер: {self.exercise_no}")
            self.confirm_btn.config(text=" Подтвердить")
            self.next_btn.config(text="Новое задание")
            self.text_label.config(text=self.text_r)
            self.answer_txt.config(text='Ответ: ')
            self.back_btn.config(text='Назад')
        self.exercise.config(state='disabled')


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
                                    font=("Arial", 35), state='disabled', bd=0)
        self.language_info.grid(row=0, column=0, sticky="nsew")

        self.english_lang_btn = Button(self.language_changers_container, text="English", bg=num_bg, fg=num_fg,
                                       font=("Arial", 35), disabledforeground=num_bg,
                                       activeforeground=num_active_fg, activebackground=num_bg, bd=0,
                                       command=lambda: self.language_changer(_lang_="eng"))
        self.english_lang_btn.grid(row=0, column=1)

        self.russian_lang_btn = Button(self.language_changers_container, text="Русский", bg=bg, fg=fg,
                                       font=("Arial", 35), disabledforeground=bg,
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
                                     font=("Arial", 40), command=self.change_theme_to_dark, bd=0,
                                     activeforeground=num_active_fg, activebackground=num_bg, disabledforeground=num_bg)
        self.dark_theme_btn.grid(row=0, column=1, sticky='nsew')

        self.light_theme_btn = Button(self.themes_changers_container, text="Light", bg=bg, fg=fg,
                                      font=("Arial", 40),
                                      activeforeground=active_fg, activebackground=bg, bd=0, disabledforeground=bg,
                                      command=self.change_theme_to_light)
        self.light_theme_btn.grid(row=0, column=3, sticky='nsew')

        # Separator or placeholder
        self.place_h2 = Label(self, bg=bg, font=('Arial', 20))
        self.place_h2.pack()

        self.home_button = Button(self, text="Home", bg=num_bg, fg=home_btn_fg, font=("Arial", 45),
                                  activeforeground=home_btn_active_fg, activebackground=num_bg, bd=0,
                                  disabledforeground=num_bg, command=lambda: controller.show_frame(MainPage))
        self.home_button.pack(fill='both', side='bottom', expand=True)

        # Checking for current theme
        if current_theme == 'dark':
            self.dark_theme_btn.config(state='disabled', cursor="arrow")
            self.light_theme_btn.config(state='normal', cursor="hand2")
        elif current_theme == 'light':
            self.dark_theme_btn.config(state='normal', cursor="hand2")
            self.light_theme_btn.config(state='disabled', cursor="arrow")

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
            self.english_lang_btn.config(state='disabled', cursor="arrow")
            self.russian_lang_btn.config(state='normal', cursor="hand2")
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
            self.english_lang_btn.config(state='normal', cursor="hand2")
            self.russian_lang_btn.config(state='disabled', cursor="arrow")
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
        self.language_info.config(bg=bg, disabledforeground=fg)
        self.dark_theme_btn.config(bg=num_bg, fg=num_fg, activeforeground=num_active_fg, activebackground=num_bg,
                                   disabledforeground=num_bg)
        self.light_theme_btn.config(bg=bg, fg=fg, activeforeground=active_fg, activebackground=bg,
                                    disabledforeground=bg)
        self.russian_lang_btn.config(bg=bg, fg=fg, disabledforeground=bg, activeforeground=active_fg,
                                     activebackground=bg)
        self.home_button.config(bg=num_bg, fg=home_btn_fg, activeforeground=home_btn_active_fg, activebackground=num_bg,
                                disabledforeground=num_bg)
        self.english_lang_btn.config(bg=num_bg, fg=num_fg, disabledforeground=num_bg, activeforeground=num_active_fg,
                                     activebackground=num_bg)

    def pages_update(self):
        page = self.controller.get_page(RectanglesAPage)
        page.rectangles_a_page_theme_upgrade()
        page = self.controller.get_page(RectanglesPPage)
        page.rectangles_p_page_theme_upgrade()
        page = self.controller.get_page(PerimetersPage)
        page.perimeters_page_theme_update()
        page = self.controller.get_page(SquaresPPage)
        page.squares_p_page_theme_update()
        page = self.controller.get_page(SquaresAPage)
        page.squares_a_page_theme_update()
        page = self.controller.get_page(SettingsPage)
        page.settings_page_theme_update()
        page = self.controller.get_page(TopicsPage)
        page.topics_page_theme_update()
        page = self.controller.get_page(AreasPage)
        page.areas_page_theme_update()
        page = self.controller.get_page(MainPage)
        page.main_page_theme_update()

    def change_theme_to_dark(self):
        self.dark_theme_btn.config(state='disabled', cursor="arrow")
        self.light_theme_btn.config(state='normal', cursor="hand2")
        dark_theme()
        self.pages_update()

    def change_theme_to_light(self):
        self.light_theme_btn.config(state='disabled', cursor="arrow")
        self.dark_theme_btn.config(state='normal', cursor="hand2")
        light_theme()
        self.pages_update()


if __name__ == "__main__":
    MainAppBody().mainloop()  # Launch application