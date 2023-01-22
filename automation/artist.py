#!/usr/bin/python

from sys import argv

to_add = argv[1]

text = f"from tkinter import Frame\n\nfrom ..generators import {to_add}\nfrom .task_template import TaskPageTemplate\n\n\nclass {to_add.title()}Page(Frame):\n"

start = '''\ttask = {"eng": "task_name", "rus": "task_name"}
\ttask_text = {"eng": "Task_text_english {}", "rus": "Task_text_russian {}"}
\tsubject = None # 0 -> algebra; 1 -> geometry

\tdef __init__(self, parent, lang, version, prev, bg, fg, afg, dfg, b_bg, b_bg1, b_abg, e_bg, e_hl):
\t\tFrame.__init__(self, parent)

\t\tpage = TaskPageTemplate(self, parent, prev)
\t\tpage.pack(fill="both", expand=True)

\t\tself.exercise_no = None
\t\tself.task = None
\t\tself.answer = None

\t\tdef new_task(full_reset: bool = True):
\t\t\tif full_reset:
'''

middle = f"\t\t\t\ttask_data = {to_add}(version, self.winfo_width(), self.winfo_height(),\n"

end = '''\t\t\t\t\t\t\t\t\t\t\tself.winfo_screenwidth(), self.winfo_screenheight())
\t\t\t\tself.task = task_data[1] # or better use self.param if one integer is passed
\t\t\t\tself.answer = task_data[0]
\t\t\t\tself.exercise_no = task_data[-1]

\t\t\t\tpage.set_exercise(self.exercise_no, code) # replace code with four digit number (go to main_app.py and check pages dictionary)
\t\t\t\tpage.change_task_text(self.task_text[lang].format(self.task))

\t\t\tif lang == "eng":
\t\t\t\tpage.confirm_btn.config(text="Confirm")
\t\t\telif lang == "rus":
\t\t\t\tpage.confirm_btn.config(text="Подтвердить")

\t\tdef activate():
\t\t\tpage.next.config(state='normal')
\t\t\tpage.answer_field.config(state='normal')

\t\tdef confirm():
\t\t\tpage.next.config(state='disabled')
\t\t\t_input = 0
\t\t\tif page.answer_field.get() != "-":
\t\t\t\t_input = int(page.answer_field.get())
\t\t\telse:
\t\t\t\tpage.answer_field.insert("end", 1)
\t\t\tpage.clear()
\t\t\tpage.answer_field.config(state='disabled')
\t\t\tself.after(1000, activate)
\t\t\tif _input == self.answer:
\t\t\t\tif lang == "eng":
\t\t\t\t\tpage.confirm_btn.config(text="Correct", state="disabled")
\t\t\t\telif lang == "rus":
\t\t\t\t\tpage.confirm_btn.config(text="Правильно", state="disabled")
\t\t\t\tself.after(500, new_task)
\t\t\telse:
\t\t\t\tif lang == "eng":
\t\t\t\t\tpage.confirm_btn.config(text="Wrong", state="disabled")
\t\t\t\telif lang == "rus":
\t\t\t\t\tpage.confirm_btn.config(text="Неправильно", state="disabled")
\t\t\t\tself.after(500, lambda: new_task(False))

\t\tself.confirm = confirm
\t\tself.new_task = new_task

\t\tpage.new_task_command(new_task)
\t\tpage.confirm_command(confirm)
\t\tpage.set_theme(bg, fg, afg, dfg, b_bg, b_bg1, b_abg, e_bg, e_hl)
\t\tpage.set_lang(lang)

\t\tparent.bind('<Return>', lambda _: page.confirm_btn.invoke())
\t\tparent.bind('<KP_Enter>', lambda _: page.confirm_btn.invoke())
'''

with open(f"./modules/pages/{to_add}_page.py", "w") as file:
    file.write(text+start+middle+end)