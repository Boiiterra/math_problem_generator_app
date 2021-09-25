from tkinter import *
from configparser import ConfigParser

# Color section
parser = ConfigParser()

parser.read("data.txt")
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

        container = Frame(self, bg="black")
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        self.frames = {}

        frame_collection = (StartPage, TopicsPage)

        for frame in frame_collection:
            current_frame = frame(container, self)

            self.frames[frame] = current_frame

            current_frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(Frame):
    global parser

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=bg)

        question = Label(self, text="\nChoose language:", bg=bg, fg=fg, font=("Arial", 40))
        question.pack(side="top")

        bottom_ = Label(self, bg=bg, text="Note: you can always change\nlanguage in settings menu",
                        font=("Arial", 30), fg=active_fg)
        bottom_.pack(side="bottom")

        def chosen(_, lng: str):
            if lng == "rus":
                pass
            elif lng == "eng":
                print("Hello")

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

        russian.bind("<Enter>", lambda _: entered(_, btn=russian))
        russian.bind("<Leave>", lambda _: left(_, btn=russian))
        russian.bind("<Button-1>", lambda _: chosen(_, "rus"))
        english.bind("<Enter>", lambda _: entered(_, btn=english))
        english.bind("<Leave>", lambda _: left(_, btn=english))
        english.bind("<Button-1>", lambda _: chosen(_, "eng"))


class TopicsPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg=bg)


if __name__ == "__main__":
    MainAppBody().mainloop()