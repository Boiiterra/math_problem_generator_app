from tkinter import Frame

from ..generators import arithmetics
from .task_template import TaskPageTemplate


class ArithmeticsPage(Frame):
    task = {"eng": "Arithmetics", "rus": "Арифметика"}
    subject = 0

    def __init__(self, parent, lang, version, prev, bg, fg, afg, dfg, b_bg, b_bg1, b_abg, e_bg, e_hl):
        Frame.__init__(self, parent)

        page = TaskPageTemplate(self, parent, prev)
        page.pack(fill="both", expand=True)

        self.exercise_no = None
        self.task = None
        self.answer = None
        self.text_e = None
        self.text_r = None

        def new_task(full_reset: bool = True):
            if full_reset:
                task_data = arithmetics(version, self.winfo_width(), self.winfo_height(), 
                                            self.winfo_screenwidth(), self.winfo_screenheight())
                self.task = task_data[0]
                self.answer = task_data[1]
                self.exercise_no = task_data[-1]
                self.text_e = f"What does this equals to\n(\" * \" means multiplication; \" / \" means division)\n{self.task}"
                self.text_r = f"Чему равно данное выражение\n(\" * \" - умножение; \" / \" - деление)\n{self.task}"

                page.set_exercise(self.exercise_no)

                if lang == "eng":
                    page.change_task_text(self.text_e)
                elif lang == "rus":
                    page.change_task_text(self.text_r)

            if lang == "eng":
                page.confirm_btn.config(text="Confirm")
            elif lang == "rus":
                page.confirm_btn.config(text="Подтвердить")

        def activate():
            page.next.config(state='normal')
            page.answer_field.config(state='normal')

        def confirm():
            page.next.config(state='disabled')
            _input = 0
            if page.answer_field.get() != "-":
                _input = int(page.answer_field.get())
            else:
                page.answer_field.insert("end", 1)
            page.clear()
            page.answer_field.config(state='disabled')
            self.after(1000, activate)
            if _input == self.answer:
                if lang == "eng":
                    page.confirm_btn.config(text="Correct", state="disabled")
                elif lang == "rus":
                    page.confirm_btn.config(text="Правильно", state="disabled")
                self.after(500, new_task)
            else:
                if lang == "eng":
                    page.confirm_btn.config(text="Wrong", state="disabled")
                elif lang == "rus":
                    page.confirm_btn.config(text="Неправильно", state="disabled")
                self.after(500, lambda: new_task(False))

        self.new_task = new_task
        self.confirm = confirm

        page.new_task_command(new_task)
        page.confirm_command(confirm)
        page.set_theme(bg, fg, afg, dfg, b_bg, b_bg1, b_abg, e_bg, e_hl)
        page.set_lang(lang)

        parent.bind('<Return>', lambda _: page.confirm_btn.invoke())
        parent.bind('<KP_Enter>', lambda _: page.confirm_btn.invoke())

