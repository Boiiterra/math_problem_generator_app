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

        # if lng_state == "ask" or current_language == "unknown":
        #     self.page = FLaunchPage(self)
        #     self.ch_page(self.page)
        # elif lng_state == "keep":
            # self.ch_page(MainPage)

    def delete_window(self):  # saves parameters and then deletes window
        if self.wm_state() == "zoomed" and lng_state != "ask" and current_language != "unknown":
            save_window_parameters(str(self.winfo_width()), str(self.winfo_height()),
                                   str(self.winfo_rootx()), str(self.winfo_rooty()), '1')
        elif self.wm_state() != "zoomed" and lng_state != "ask" and current_language != "unknown":
            save_window_parameters(str(self.winfo_width()), str(self.winfo_height()),
                                   str(self.winfo_rootx()), str(self.winfo_rooty()), '0')
        self.destroy()

    # def ch_page(self, new:Frame, prev:Frame=None):
    #     print(new, prev)
    #     if prev is not None:
    #         prev.pack_forget()
    #     if (not "flaunchpage" in str(new).lower()) and (not "mainpage" in str(new).lower()):
    #         new(self).pack(fill="both", expand=True)
    #     elif "flaunchpage" in str(new).lower():
    #         self.page.pack(fill="both", expand=True)

    # def get_page(self, page_class):
    #     return self.frames[page_class]


if __name__ == "__main__":
    MainAppBody().mainloop()  # Launch application