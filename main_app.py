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

    # TODO: Redesign MainAppBody -> pages are separated, not contact together
    # ! (pressing tab ignores page sequence) 

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

    def ch_page(self, new:Frame, prev:Frame=None):
        print(new, prev)
        if prev is not None:
            prev.pack_forget()
        new(self).pack(fill="both", expand=True)


class FLaunchPage(Frame):  # This page launches when you need to choose language

    def __init__(self, parent):
        Frame.__init__(self, parent, bg="black")

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

        def new_lang(lang):
            change_language(lang)
            parent.ch_page(MainPage, self)

        self.english.bind("<Leave>", lambda _: left(btn=self.english))
        self.russian.bind("<Button-1>", lambda _: new_lang(lang="rus"))
        self.russian.bind("<Enter>", lambda _: entered(btn=self.russian, lang='rus'))
        self.english.bind("<Enter>", lambda _: entered(btn=self.english, lang='eng'))
        self.english.bind("<Button-1>", lambda _: new_lang(lang="eng"))
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


class MainPage(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent

        title = Label(self, font=("Verdana", 45))
        title.pack(fill="both", expand=True)

        settings = Button(self, bd=0, bg="#bababa", activebackground="#cfcfcf", activeforeground="#3f3f3f", font=M_FONT)#, command=lambda: parent.ch_page(SettingsPage, MainPage))
        settings.pack(side="bottom", fill="both", ipady=30, pady=10)

        tasks = Button(self, bd=0, font=M_FONT, bg="#c5c5c5", activebackground="#cfcfcf", activeforeground="#3f3f3f")#, command=lambda: parent.ch_page(TaskCreationPage, MainPage))
        tasks.pack(side="bottom", fill="x", ipady=20)

        game = Button(self, bd=0, font=M_FONT, bg="#bababa", activebackground="#cfcfcf", activeforeground="#3f3f3f")#, command=lambda: parent.ch_page(GameOptPage, MainPage))
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


if __name__ == "__main__":
    MainAppBody().mainloop()  # Launch application