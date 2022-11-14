from tkinter import Button


class Option(Button):
    def __init__(self, parent, _from, destination, number: int, _app, lang, fg, b_bg, b_bg1, b_abg, afg):
        Button.__init__(self, parent, text=destination.task[lang], bd=0, fg=fg, bg=(b_bg if number % 2 == 0 else b_bg1), activebackground=b_abg, activeforeground=afg, command=lambda: _app.ch_page(destination, _from))

    def grid(self, **kwargs):
        self.grid_configure(kwargs)