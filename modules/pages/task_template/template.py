from tkinter import Frame, Button, Label, Entry, Text
from pyperclip import copy

from ...tooltip import create_tool_tip
from ...resolution import scale


class TaskPageTemplate(Frame):
    allowed = "0123456789-"
    exercise = None

    def __init__(self, parent: Frame, app, prev: Frame):
        Frame.__init__(self, parent)

        top = Frame(self)
        top.pack(fill="x", pady=8)

        e_label = Label(top)
        e_label.pack(side="left", padx=2, pady=5)

        def do_copy(_):
            if self.exercise is not None:
                copy(self.exercise)

        e_text = Text(top, borderwidth=0, height=1, state="disabled", cursor="", highlightthickness=0)
        e_text.pack(fill="x", pady=8, side='right')
        e_text.bind("<Button-1>", do_copy)

        task = Label(self, anchor='center')
        task.pack(pady=4, expand=True)

        b_cont = Label(self)
        b_cont.pack(fill="x", padx=15, side="bottom")

        cont = Frame(self)
        cont.pack(pady=(0, 6), side="bottom")

        a_label = Label(cont)
        a_label.grid(row=0, column=0)

        is_valid = (parent.register(self.validator), '%d', '%i', '%P') # '%d' -> action, '%i' -> index, '%P' -> value

        answer_field = Entry(cont, width=6, border=0, validatecommand=is_valid, validate="key")
        answer_field.grid(row=0, column=1, padx=15)

        confirm_btn = Button(cont, bd=0, state="disabled")
        confirm_btn.grid(row=0, column=2)

        def go_back():
            self.answer_field["state"] = "disabled"
            app.ch_page(prev, parent)

        back = Button(b_cont, bd=0, command=go_back)
        back.pack(side="left", ipady=5, fill="x", expand=True, padx=(0, 10))

        next = Button(b_cont, bd=0)
        next.pack(side="right", ipady=5, fill="x", expand=True, padx=(10, 0))

        def set_font(_):
            scaling = scale(app.winfo_width(), app.winfo_height())
            e_label.config(font=("Arial", int(27 * scaling)))
            e_text.config(font=("Arial", int(27 * scaling)))
            task.config(font=("Arial", int(20 * scaling)))
            answer_field.config(font=('Arial', int(32 * scaling)))
            a_label.config(font=('Arial', int(32 * scaling)))
            back.config(font=('Arial', int(32 * scaling)))
            next.config(font=('Arial', int(32 * scaling)))
            confirm_btn.config(font=('Arial', int(32 * scaling)))

        self.top = top
        self.e_label = e_label
        self.e_text = e_text
        self.task = task
        self.b_cont = b_cont
        self.cont = cont
        self.a_label = a_label
        self.answer_field = answer_field
        self.confirm_btn = confirm_btn
        self.back = back
        self.next = next

        self.bind("<Configure>", set_font)

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

    def change_ans_len(self, _to: int):
        self.answer_field.config(width=_to)

    def clear(self):
        self.answer_field.delete(0, "end")

    def validator(self, action, index, value):
        """Enter only integer values with length limit"""
        if value != "":
            if (index == "0" and value[0] == "0") or (index == "1" and value[0:2] == "-0"):
                return False
            if len(value) >= self.answer_field["width"] + 1:
                return False
        if index != "0" and value[-1] == "-" and action == "1":
            return False
        # Confirm button status
        if value == "" and index == "0" and all(symbol in self.allowed for symbol in value):
            self.confirm_btn.config(state="disabled")
        elif "0" == index < str(self.answer_field["width"]) and all(symbol in self.allowed for symbol in value):
            self.confirm_btn.config(state="normal")
        # Entry validation
        if len(self.answer_field.get()) >= self.answer_field["width"] and index != "5" and action == "1":  # Limiting input length
            return False
        elif all(symbol in self.allowed for symbol in value):  # Allowed values
            return True
        else:
            return False

    def set_theme(self, bg, fg, afg, dfg, b_bg, b_bg1, b_abg, e_bg, e_hl):
        self.config(bg=bg)
        self.top.config(bg=bg)
        self.e_label.config(bg=bg, fg=fg)
        self.e_text.config(bg=bg, fg=fg)
        self.task.config(bg=bg, fg=fg)
        self.b_cont.config(bg=bg)
        self.cont.config(bg=bg)
        self.a_label.config(bg=bg, fg=fg)
        self.confirm_btn.config(fg=fg, bg=b_bg, activebackground=b_abg, activeforeground=afg, disabledforeground=dfg)
        self.back.config(fg=fg, bg=b_bg, activebackground=b_abg, activeforeground=afg)
        self.next.config(fg=fg, bg=b_bg1, activebackground=b_abg, activeforeground=afg, disabledforeground=dfg)
        self.answer_field.config(fg=fg, highlightbackground=e_hl, bg=e_bg, insertbackground=fg, disabledbackground=e_bg)

    def set_lang(self, lang):
        if lang == "eng":
            self.e_label.config(text="Exercise:")
            self.a_label.config(text="Answer:")
            self.back.config(text="Back")
            self.next.config(text="New task")
            self.confirm_btn.config(text="Confirm")
            create_tool_tip(self.e_text, "Click to copy exercise number.", 10)
        elif lang == "rus":
            self.e_label.config(text="Номер:")
            self.a_label.config(text="Ответ:")
            self.back.config(text="Назад")
            self.next.config(text="Новая задача")
            self.confirm_btn.config(text="Подтвердить")
            create_tool_tip(self.e_text, "Нажмите, чтобы скопировать номер задачи.", 10)

