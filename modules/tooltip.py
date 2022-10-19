from pyautogui import position as mouse_pos
from tkinter import Toplevel, Label


class ToolTip:
    def __init__(self, widget):
        self.tipwindow = None
        self.widget = widget
        self.x = self.y = 0
        self.id = id

    def showtip(self, text: str, f_size: int):
        self.text = text
        if self.tipwindow or not self.text:
            return

        self.tipwindow = tw = Toplevel(self.widget)

        mouse_x, mouse_y = mouse_pos()

        if (tw.winfo_screenwidth() - mouse_x) < (12 * len(self.text) // 1.5):
            x = int(tw.winfo_screenwidth() - ((12 * len(self.text) // 1.5)))
        else:
            x = mouse_x + 15
        y = mouse_y + 3

        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(
            tw,
            text=self.text,
            justify="left",
            background="#ffffe0",
            relief="solid",
            borderwidth=1,
            font=("tahoma", f_size, "normal"),
        )
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


def create_tool_tip(widget, text: str, f_size: int):
    toolTip = ToolTip(widget)
    widget.bind("<Enter>", lambda _: toolTip.showtip(text, f_size))
    widget.bind("<Leave>", lambda _: toolTip.hidetip())