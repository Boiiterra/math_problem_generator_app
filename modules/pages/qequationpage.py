from tkinter import Frame

from ..generators import square_equation
from .task_template import TaskPageTemplate


class QEquationPage(Frame):
    task = {"eng": "Quadratic equation", "rus": "Квадратное уравнение"}
    subject = 0

    def __init__(self, parent, lang, version, prev, bg, fg, afg, dfg, b_bg, b_bg1, b_abg, e_bg, e_hl):
        Frame.__init__(self, parent)

        page = TaskPageTemplate(self, parent, prev)
        page.pack(fill="both", expand=True)

        self.exercise_no = None
        self.x1 = None
        self.x2 = None
        self.param = None
        self.answer = None
        self.text_e = None
        self.text_r = None
        self.task_type = None

        def new_task(full_reset: bool = True):
            if full_reset:
                task_data = square_equation(version, self.winfo_width(), self.winfo_height(), 
                                            self.winfo_screenwidth(), self.winfo_screenheight())
                self.x1 = task_data[0]
                self.x2 = task_data[1]

                if self.x1 != 0 and self.x2 != 0:
                    if self.x1 > self.x2:
                        self.answer = self.x2
                        self.task_type = 1
                    elif self.x1 < self.x2:
                        self.answer = self.x2
                        self.task_type = 2
                    else:
                        self.answer = self.x2
                        self.task_type = 3
                elif self.x1 == 0 and self.x2 > self.x1:
                    self.answer = self.x2
                    self.task_type = 2
                elif self.x1 == 0 and self.x2 < self.x1:
                    self.answer = self.x1
                    self.task_type = 1
                elif self.x2 == 0 and self.x1 > self.x2:
                    self.answer = self.x1
                    self.task_type = 2
                elif self.x2 == 0 and self.x1 < self.x2:
                    self.answer = self.x1
                    self.task_type = 1

                extra_text_e = ""
                extra_text_r = ""
                if self.task_type == 1:
                    extra_text_e = "Find the smallest equation's root."
                    extra_text_r = "Найдите наименьший корень уравнения."
                elif self.task_type == 2:
                    extra_text_e = "Find the biggest equation's root."
                    extra_text_r = "Найдите наибольший корень уравнения."
                elif self.task_type == 3:
                    extra_text_e = "Find any equation's root."
                    extra_text_r = "Найдите любой корень уравнения"

                self.exercise_no = task_data[-1]
                self.param = task_data[-2]
                self.text_e = f"{self.param}\n" + extra_text_e
                self.text_r = f"{self.param}\n" + extra_text_r

                page.set_exercise(self.exercise_no, "0005")

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

