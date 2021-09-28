from tkinter import *
from configparser import ConfigParser

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


def change_lang(language: str):
    global parser, current_language, lng_state

    if language == "rus":
        parser.read('data.txt')
        parser.set('language', "language", 'rus')
        parser.set("language", 'state', 'keep')
        current_language = parser.get('language', 'language')
        lng_state = parser.get('language', 'state')
    elif language == "eng":
        parser.read('data.txt')
        parser.set('language', "language", 'eng')
        parser.set("language", 'state', 'keep')
        current_language = parser.get('language', 'language')
        lng_state = parser.get('language', 'state')


def neon_green_data():
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
    global bg, fg, active_fg, home_btn_fg, home_btn_active_fg, main_btn_bg, num_bg, num_fg, num_active_fg, current_theme
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


def dark_data():
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
    global bg, fg, active_fg, home_btn_fg, home_btn_active_fg, main_btn_bg, num_bg, num_fg, num_active_fg, current_theme
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


def light_data():
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
    global bg, fg, active_fg, home_btn_fg, home_btn_active_fg, main_btn_bg, num_bg, num_fg, num_active_fg, current_theme
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


class MainAppBody(Tk):

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

        frame_collection = (StartPage, TopicsPage, MainPage)

        for frame in frame_collection:
            current_frame = frame(container, self)

            self.frames[frame] = current_frame

            current_frame.grid(row=0, column=0, sticky="nsew")
        if lng_state == "ask":
            self.show_frame(StartPage)
        elif lng_state == "keep":
            self.show_frame(MainPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def get_page(self, page_class):
        return self.frames[page_class]


class StartPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=bg)
        self.controller = controller

        question = Label(self, text="\nChoose language:", bg=bg, fg=fg, font=("Arial", 40))
        question.pack(side="top")

        bottom_ = Label(self, bg=bg, text="Note: you can always change\nlanguage in settings menu",
                        font=("Arial", 30), fg=active_fg)
        bottom_.pack(side="bottom")

        lang_btn_container = Label(self, bg=bg, justify="center")
        lang_btn_container.pack(expand=True)

        lang_btn_container.rowconfigure(0, weight=1)
        lang_btn_container.rowconfigure(1, weight=1)
        lang_btn_container.columnconfigure(0, weight=1)

        russian = Button(lang_btn_container, text="Русский", bg=bg, fg=fg,
                         activeforeground=active_fg,
                         font=("Arial", 30), bd=0)
        russian.grid(row=0, column=0, sticky="nsew")

        english = Button(lang_btn_container, text="English", bg=bg, fg=fg,
                         activeforeground=active_fg,
                         font=("Arial", 30), bd=0)
        english.grid(row=1, column=0, sticky="nsew")

        def entered(_, btn):
            btn.config(bg=active_fg, activebackground=fg)

        def left(_, btn):
            btn.config(bg=bg)

        def new_lang(_, lang: str):
            change_lang(lang)
            controller.show_frame(MainPage)

        russian.bind("<Enter>", lambda _: entered(_, btn=russian))
        russian.bind("<Leave>", lambda _: left(_, btn=russian))
        russian.bind("<Button-1>", lambda _: new_lang(_, lang="rus"))
        english.bind("<Enter>", lambda _: entered(_, btn=english))
        english.bind("<Leave>", lambda _: left(_, btn=english))
        english.bind("<Button-1>", lambda _: new_lang(_, lang="eng"))


class MainPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=bg)
        self.controller = controller

        self.start_button = Button(self, text="Start", bg=num_bg, fg=fg, font=("Arial", 45),
                                   activeforeground=active_fg, activebackground=num_bg, bd=0,
                                   disabledforeground=num_bg, command=lambda: controller.show_frame(TopicsPage))
        self.start_button.pack(fill='both', pady=2, expand=True)

        self.settings_button = Button(self, text="Settings", bg=num_bg, fg=home_btn_fg, font=("Arial", 45),
                                      activeforeground=home_btn_active_fg, activebackground=num_bg, bd=0,
                                      disabledforeground=num_bg, command=lambda: controller.show_frame(SettingsPage))
        self.settings_button.pack(fill='both', side='bottom', expand=True)

    


class TopicsPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=bg)
        self.controller = controller


class SettingsPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=bg)
        self.controller = controller


if __name__ == "__main__":
    MainAppBody().mainloop()