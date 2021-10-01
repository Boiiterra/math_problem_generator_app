from tkinter import *
from configparser import ConfigParser
from webbrowser import open_new_tab

author = "TerraBoii"

# File reading section
parser = ConfigParser()
parser.read("data.txt")
current_language = parser.get("language", "language")
lng_state = parser.get("language", 'state')
current_theme = parser.get('theme', "current_theme")
bg = parser.get("colors", "background")
fg = parser.get("colors", "foreground")
active_fg = parser.get("colors", "active_foreground")
home_btn_fg = parser.get("colors", "home_btn_fore")
home_btn_active_fg = parser.get("colors", "home_bts_active_fore")
main_btn_bg = parser.get("colors", "main_btn_back")
num_bg = parser.get("colors", "num_btn_back")
num_fg = parser.get("colors", "num_btn_fore")
num_active_fg = parser.get("colors", "num_btn_active_fore")

# This function updates colors after theme changed
def set_theme():
    global current_theme, bg, fg, active_fg, home_btn_active_fg, home_btn_fg, main_btn_bg, num_bg, num_fg, num_active_fg
    current_theme = parser.get('theme', "current_theme")
    bg = parser.get("colors", "background")
    fg = parser.get("colors", "foreground")
    active_fg = parser.get("colors", "active_foreground")
    home_btn_fg = parser.get("colors", "home_btn_fore")
    home_btn_active_fg = parser.get("colors", "home_bts_active_fore")
    main_btn_bg = parser.get("colors", "main_btn_back")
    num_bg = parser.get("colors", "num_btn_back")
    num_fg = parser.get("colors", "num_btn_fore")
    num_active_fg = parser.get("colors", "num_btn_active_fore")

# This function changes language for whole application
def change_language(language: str):
    global parser, current_language, lng_state

    if language == "rus":
        parser.read('data.txt')
        parser.set('language', "language", 'rus')
        parser.set("language", 'state', 'keep')
        with open("data.txt", "w") as configfile:
            parser.write(configfile)
        parser.read("data.txt")
        current_language = parser.get('language', 'language')
        lng_state = parser.get('language', 'state')
    elif language == "eng":
        parser.read('data.txt')
        parser.set('language', "language", 'eng')
        parser.set("language", 'state', 'keep')
        with open("data.txt", "w") as configfile:
            parser.write(configfile)
        current_language = parser.get('language', 'language')
        lng_state = parser.get('language', 'state')

# This function changes colors and theme to neon green and saves changes to file
def neon_green_theme():
    global parser
    parser.read("data.txt")
    parser.set('theme', "current_theme", "neon_green")
    parser.set("colors", "background", "#000000")
    parser.set("colors", "foreground", "#00ff00")
    parser.set("colors", "active_foreground", "#008000")
    parser.set("colors", "home_btn_fore", "#0000FF")
    parser.set("colors", "home_bts_active_fore", "#00008B")
    parser.set("colors", "main_btn_back", "#000000")
    parser.set("colors", "num_btn_back", "#0a0a0a")
    parser.set("colors", "num_btn_fore", "#00ff00")
    parser.set("colors", "num_btn_active_fore", "#008000")
    with open("data.txt", "w") as configfile:
        parser.write(configfile)
    # Set colors
    parser.read("data.txt")
    set_theme()

# This function changes colors and theme to dark and saves changes to file
def dark_theme():
    global parser
    parser.read("data.txt")
    parser.set("theme", "current_theme", "dark")
    parser.set("colors", "background", "#000000")
    parser.set("colors", "foreground", "#ffffff")
    parser.set("colors", "active_foreground", "#5e5e5e")
    parser.set("colors", "home_btn_fore", "#474747")
    parser.set("colors", "home_bts_active_fore", "#333333")
    parser.set("colors", "main_btn_back", "#000000")
    parser.set("colors", "num_btn_back", "#0a0a0a")
    parser.set("colors", "num_btn_fore", "#8c8c8c")
    parser.set("colors", "num_btn_active_fore", "#5e5e5e")
    with open("data.txt", 'w') as configfile:
        parser.write(configfile)
    # Set colors
    parser.read("data.txt")
    set_theme()

# This function changes colors and theme to light and saves changes to file
def light_theme():
    global parser
    parser.read("data.txt")
    parser.set('theme', "current_theme", "light")
    parser.set("colors", "background", "#bababa")
    parser.set("colors", "foreground", "#000000")
    parser.set("colors", "active_foreground", "#000000")
    parser.set("colors", "home_btn_fore", "#404040")
    parser.set("colors", "home_bts_active_fore", "#5e5e5e")
    parser.set("colors", "main_btn_back", "#292929")
    parser.set("colors", "num_btn_back", "#999999")
    parser.set("colors", "num_btn_fore", "#4d4d4d")
    parser.set("colors", "num_btn_active_fore", "#787878")
    with open("data.txt", 'w') as configfile:
        parser.write(configfile)
    # Set colors
    parser.read("data.txt")
    set_theme()


class MainAppBody(Tk):  # Main application with page logic

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.geometry("800x600")
        self.title("math_problem generator")
        self.iconbitmap("images//main_icon.ico")
        self.minsize(width=800, height=600)
        self.maxsize(self.winfo_screenwidth(), self.winfo_screenheight())

        container = Frame(self, bg="black")
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.frames = {}

        frame_collection = (FLaunchPage, TopicsPage, MainPage, SettingsPage, SquaresPage, PerimetersPage)

        for frame in frame_collection:
            current_frame = frame(container, self)

            self.frames[frame] = current_frame

            current_frame.grid(row=0, column=0, sticky="nsew")
        if lng_state == "ask" or current_language == "unknown":
            self.show_frame(FLaunchPage)
        elif lng_state == "keep":
            self.show_frame(MainPage)

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

        bottom_ = Label(self, bg="black", text=hint_text,
                        font=("Arial", 30), fg="#008000")
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
            global question_text, hint_text
            if lang == "eng":
                question_text = "\nChoose language:"
                hint_text = "Note: you can always change\nlanguage in settings menu"
            elif lang == "rus":
                question_text = "\n Выберите язык: "
                hint_text = " Подсказка: всегда можно\nизменить язык в настройках"
            question.config(text=question_text)
            bottom_.config(text=hint_text)

        def left(_, btn):
            btn.config(bg="black")

        self.russian.bind("<Enter>", lambda _: entered(_, btn=self.russian, lang='rus'))
        self.russian.bind("<Leave>", lambda _: left(_, btn=self.russian))
        self.russian.bind("<Button-1>", lambda _: self.new_lang(_, lang="rus"))
        self.english.bind("<Enter>", lambda _: entered(_, btn=self.english, lang='eng'))
        self.english.bind("<Leave>", lambda _: left(_, btn=self.english))
        self.english.bind("<Button-1>", lambda _: self.new_lang(_, lang="eng"))

        def font_resize_for_flaunchpage(width):
            if width.height <= 620:
                question.config(font=('Arial', 40))
                bottom_.config(font=("Arial", 30))
                self.russian.config(font=('Arial, 30'))
                self.english.config(font=('Arial, 30'))
            elif 620 < width.height <= 700:
                question.config(font=('Arial', 45))
                bottom_.config(font=("Arial", 35))
                self.russian.config(font=('Arial', 35))
                self.english.config(font=('Arial', 35))
            elif 700 < width.height <= 800:
                question.config(font=('Arial', 50))
                bottom_.config(font=("Arial", 40))
                self.russian.config(font=('Arial', 40))
                self.english.config(font=('Arial', 40))
            elif width.height > 800:
                question.config(font=('Arial', 55))
                bottom_.config(font=("Arial", 45))
                self.russian.config(font=('Arial', 45))
                self.english.config(font=('Arial', 45))

        self.bind("<Configure>", font_resize_for_flaunchpage)

    def new_lang(self, _, lang: str, _from = None):
        change_language(lang)
        page = self.controller.get_page(PerimetersPage)
        page.set_lang_perimeterspage()
        page = self.controller.get_page(SettingsPage)
        page.set_lang_settingspage()
        page = self.controller.get_page(SquaresPage)
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
            self.start_button.config(text="Start")
            self.settings_button.config(text="Settings")
        elif current_language == 'rus':
            self.text_label.config(text='Генератор задач по\nматематике')
            self.start_button.config(text="Старт")
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

        self.placeholder = Label(self, font=('Arial', 5), bg=bg)
        self.placeholder.pack(side='bottom')

        self.topics_container = Label(self, bg=bg)
        self.topics_container.pack(side="left", expand=True, fill="both", padx=2)

        Grid.rowconfigure(self.topics_container, 0, weight=1)
        Grid.rowconfigure(self.topics_container, 1, weight=1)
        Grid.columnconfigure(self.topics_container, 0, weight=1)
        Grid.columnconfigure(self.topics_container, 1, weight=1)

        self.figure_squares = Button(self.topics_container, text='Figure squares', bd=0, font=('Arial', 25),
                                     bg=num_bg, fg=fg, activebackground=num_bg, activeforeground=num_active_fg,
                                     command=lambda: controller.show_frame(SquaresPage))
        self.figure_squares.grid(row=0, column=0, sticky='nsew')
        
        self.figure_perimeters = Button(self.topics_container, text='Figure perimeters', bd=0, font=('Arial', 25),
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

        elif current_language == 'rus':
            self.home_btn.config(text='Назад')

    def topics_page_theme_update(self):
        self.config(bg=bg)
        self.placeholder.config(bg=bg)
        self.topics_container.config(bg=bg)
        self.figure_square.config(disabledforeground=bg, bg=bg)
        self.figure_perimeter.config(disabledforeground=bg, bg=bg)
        self.figure_perimeters.config(bg=bg, fg=fg, activebackground=bg, activeforeground=num_active_fg)
        self.figure_squares.config(bg=num_bg, fg=fg, activebackground=num_bg, activeforeground=num_active_fg)
        self.home_btn.config(bg=num_bg, activebackground=num_bg, fg=home_btn_fg, activeforeground=home_btn_active_fg)


class SquaresPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=bg)
        self.controller = controller

        self.back_btn = Button(self, font=("Arial", 35), command=lambda: controller.show_frame(TopicsPage), bd=0,
                               bg=num_bg, activebackground=num_bg, fg=home_btn_fg, activeforeground=home_btn_active_fg)
        self.back_btn.pack(side='bottom', fill='x', ipady=5)

        self.set_lang_squarespage()

    def set_lang_squarespage(self):
        if current_language == "eng":
            self.back_btn.config(text='Back')

        elif current_language == 'rus':
            self.back_btn.config(text='Назад')


class PerimetersPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=bg)
        self.controller = controller

        self.return_btn = Button(self, font=("Arial", 35), command=lambda: controller.show_frame(TopicsPage), bd=0,
                               bg=num_bg, activebackground=num_bg, fg=home_btn_fg, activeforeground=home_btn_active_fg)
        self.return_btn.pack(side='bottom', fill='x', ipady=5)

        self.set_lang_perimeterspage()

    def set_lang_perimeterspage(self):
        if current_language == "eng":
            self.return_btn.config(text='Return')

        elif current_language == 'rus':
            self.return_btn.config(text='Назад')


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

        self.language_changers_container = Label(self, bg=num_bg)
        self.language_changers_container.pack(anchor='n')

        Grid.rowconfigure(self.language_changers_container, 0, weight=1)
        Grid.columnconfigure(self.language_changers_container, 0, weight=1)
        Grid.columnconfigure(self.language_changers_container, 1, weight=1)
        Grid.columnconfigure(self.language_changers_container, 2, weight=1)

        self.language_info = Button(self.language_changers_container, bg=bg, disabledforeground=fg,
                                    font=("Arial", 35), state='disabled', bd=0)
        self.language_info.grid(row=0, column=0, sticky="nsew")

        self.english_lang_btn = Button(self.language_changers_container, text="English", bg=num_bg, fg=num_fg,
                                       font=("Times New Roman", 50), disabledforeground=num_bg,
                                       activeforeground=num_active_fg, activebackground=num_bg, bd=0,
                                       command=lambda: self.language_changer(_lang_="eng"))
        self.english_lang_btn.grid(row=0, column=1)

        self.russian_lang_btn = Button(self.language_changers_container, text="Русский", bg=bg, fg=fg,
                                       font=("Times New Roman", 50), disabledforeground=bg,
                                       activeforeground=active_fg, activebackground=bg, bd=0,
                                       command=lambda: self.language_changer(_lang_="rus"))
        self.russian_lang_btn.grid(row=0, column=2)

        # Separator or placeholder
        self.place_h1 = Label(self, bg=bg, font=('Arial', 30))
        self.place_h1.pack()

        self.themes_changers_container = Label(self, bg=bg)
        self.themes_changers_container.pack(anchor='n')

        Grid.rowconfigure(self.themes_changers_container, 0, weight=1)
        Grid.columnconfigure(self.themes_changers_container, 0, weight=1)
        Grid.columnconfigure(self.themes_changers_container, 1, weight=1)
        Grid.columnconfigure(self.themes_changers_container, 2, weight=1)
        Grid.columnconfigure(self.themes_changers_container, 3, weight=1)
        
        self.theme_info = Label(self.themes_changers_container, bg=bg, fg=fg, font=("Arial", 35))
        self.theme_info.grid(row=0, column=0, sticky="nsew")

        self.neon_green_theme_btn = Button(self.themes_changers_container, text="Neon green", bg=num_bg, fg=num_fg,
                                           font=("Times New Roman", 55),
                                           activeforeground=num_active_fg, activebackground=num_bg, bd=0,
                                           disabledforeground=num_bg,
                                           command=self.change_theme_to_neon)
        self.neon_green_theme_btn.grid(row=0, column=2, sticky='nsew')

        self.dark_theme_btn = Button(self.themes_changers_container, text="Dark", bg=bg, fg=fg,
                                     font=("Times New Roman", 55),
                                     activeforeground=active_fg, activebackground=bg, bd=0, disabledforeground=bg,
                                     command=self.change_theme_to_dark)
        self.dark_theme_btn.grid(row=0, column=1, sticky='nsew')

        self.light_theme_btn = Button(self.themes_changers_container, text="Light", bg=bg, fg=fg,
                                      font=("Times New Roman", 55),
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
        if current_theme == "neon_green":
            self.dark_theme_btn.config(state='normal')
            self.light_theme_btn.config(state='normal')
            self.neon_green_theme_btn.config(state='disabled')
        elif current_theme == 'dark':
            self.neon_green_theme_btn.config(state='normal')
            self.dark_theme_btn.config(state='disabled')
            self.light_theme_btn.config(state='normal')
        elif current_theme == 'light':
            self.dark_theme_btn.config(state='normal')
            self.light_theme_btn.config(state='disabled')
            self.neon_green_theme_btn.config(state='normal')

        self.bind("<Configure>", lambda params: self.font_changer(params.width))

        self.set_lang_settingspage()

    def font_changer(self, width):
        """Changing font size based on window width"""
        # This changes font sizes, the same as above but after language switching
        if width <= 959 and current_language == 'eng':
            self.theme_info.config(font=('Arial', 42))
            self.home_button.config(font=('Arial', 45))
            self.dark_theme_btn.config(font=('Times New Roman', 42))
            self.light_theme_btn.config(font=('Times New Roman', 42))
            self.neon_green_theme_btn.config(font=('Times New Roman', 42))
        elif 959 < width <= 1160 and current_language == 'eng':
            self.theme_info.config(font=('Arial', 50))
            self.home_button.config(font=('Arial', 55))
            self.dark_theme_btn.config(font=('Times New Roman', 50))
            self.light_theme_btn.config(font=('Times New Roman', 50))
            self.neon_green_theme_btn.config(font=('Times New Roman', 50))
        elif width > 1160 and current_language == 'eng':
            self.theme_info.config(font=('Arial', 55))
            self.home_button.config(font=('Arial', 55))
            self.dark_theme_btn.config(font=('Times New Roman', 55))
            self.light_theme_btn.config(font=('Times New Roman', 55))
            self.neon_green_theme_btn.config(font=('Times New Roman', 55))
        elif width <= 959 and current_language == 'rus':
            self.theme_info.config(font=('Arial', 35))
            self.home_button.config(font=('Arial', 45))
            self.dark_theme_btn.config(font=('Times New Roman', 33))
            self.light_theme_btn.config(font=('Times New Roman', 33))
            self.neon_green_theme_btn.config(font=('Times New Roman', 33))
        elif 959 < width <= 1160 and current_language == 'rus':
            self.theme_info.config(font=('Arial', 44))
            self.home_button.config(font=('Arial', 55))
            self.dark_theme_btn.config(font=('Times New Roman', 39))
            self.light_theme_btn.config(font=('Times New Roman', 39))
            self.neon_green_theme_btn.config(font=('Times New Roman', 39))
        elif width > 1160 and current_language == 'rus':
            self.theme_info.config(font=('Arial', 50))
            self.home_button.config(font=('Arial', 55))
            self.dark_theme_btn.config(font=('Times New Roman', 46))
            self.light_theme_btn.config(font=('Times New Roman', 46))
            self.neon_green_theme_btn.config(font=('Times New Roman', 46))


    def language_changer(self, _lang_: str):
        '''Changes language from setting page and fixes its font'''
        _page = self.controller.get_page(FLaunchPage)  # Getting access to FLaunchPage in oreder to use new_lang method
        _page.new_lang('', lang=_lang_, _from='')
        self.font_changer(self.winfo_width())  # Changing font size so everything will fit in the window


    def set_lang_settingspage(self):
        if current_language == "eng":
            self.neon_green_theme_btn.config(text='Neon green')
            self.english_lang_btn.config(state='disabled')
            self.russian_lang_btn.config(state='normal')
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
            self.english_lang_btn.config(state='normal')
            self.russian_lang_btn.config(state='disabled')
            self.neon_green_theme_btn.config(text='Тёмно-зелёная')
        self.font_changer(self.winfo_width())


    def settings_page_theme_update(self):
        self.config(bg=bg)
        self.place_h0.config(bg=bg)
        self.place_h1.config(bg=bg)
        self.place_h2.config(bg=bg)
        self.created_by.config(bg=bg)
        self.theme_info.config(bg=bg, fg=fg)
        self.language_info.config(bg=bg, disabledforeground=fg)
        self.themes_changers_container.config(bg=bg)
        self.language_changers_container.config(bg=bg)
        self.dark_theme_btn.config(bg=bg, fg=fg, activeforeground=active_fg, activebackground=bg,
                                   disabledforeground=bg)
        self.light_theme_btn.config(bg=bg, fg=fg, activeforeground=active_fg, activebackground=bg,
                                    disabledforeground=bg)
        self.russian_lang_btn.config(bg=bg, fg=fg, disabledforeground=bg, activeforeground=active_fg,
                                     activebackground=bg)
        self.home_button.config(bg=num_bg, fg=home_btn_fg, activeforeground=home_btn_active_fg, activebackground=num_bg,
                                disabledforeground=num_bg)
        self.english_lang_btn.config(bg=num_bg, fg=num_fg, disabledforeground=num_bg, activeforeground=num_active_fg,
                                     activebackground=num_bg)
        self.neon_green_theme_btn.config(bg=num_bg, fg=num_fg, activeforeground=num_active_fg, activebackground=num_bg,
                                         disabledforeground=num_bg)

    def pages_update(self):
        page = self.controller.get_page(MainPage)
        page.main_page_theme_update()
        page = self.controller.get_page(SettingsPage)
        page.settings_page_theme_update()
        page = self.controller.get_page(TopicsPage)
        page.topics_page_theme_update()


    def change_theme_to_dark(self):
        self.neon_green_theme_btn.config(state='normal')
        self.dark_theme_btn.config(state='disabled')
        self.light_theme_btn.config(state='normal')
        dark_theme()
        self.pages_update()

    def change_theme_to_neon(self):
        self.neon_green_theme_btn.config(state='disabled')
        self.light_theme_btn.config(state='normal')
        self.dark_theme_btn.config(state='normal')
        neon_green_theme()
        self.pages_update()

    def change_theme_to_light(self):
        self.neon_green_theme_btn.config(state='normal')
        self.light_theme_btn.config(state='disabled')
        self.dark_theme_btn.config(state='normal')
        light_theme()
        self.pages_update()


if __name__ == "__main__":
    MainAppBody().mainloop()