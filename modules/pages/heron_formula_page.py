from tkinter import Frame

from ..generators import heron_formula
from .task_template import TaskPageTemplate


class Heron_FormulaPage(Frame):
	task = {"eng": "Heron's formula", "rus": "Формула Герона"}
	task_text = {"eng": "Given a random triangle with sides:\na = {}, b = {}, c = {}.\n" \
						"Calculate its area. Round the result to integer.",
				 "rus": "Дан произвольный треугольник со сторонами:\na = {}, b = {}, c = {}.\n" \
				 		"Чему равна площать данного треугольника?\nРезультат округлить до целых."}
	subject = 1 # 0 -> algebra; 1 -> geometry

	def __init__(self, parent, lang, version, prev, bg, fg, afg, dfg, b_bg, b_bg1, b_abg, e_bg, e_hl):
		Frame.__init__(self, parent)

		page = TaskPageTemplate(self, parent, prev)
		page.pack(fill="both", expand=True)
		page.change_allowed("0123456789")
		page.change_ans_len(4)

		self.exercise_no = None
		self.a = None
		self.b = None
		self.c = None
		self.answer = None

		def new_task(full_reset: bool = True):
			if full_reset:
				task_data = heron_formula(version, self.winfo_width(), self.winfo_height(),
										  self.winfo_screenwidth(), self.winfo_screenheight())
				self.a = task_data[1]
				self.b = task_data[2]
				self.c = task_data[3]
				self.answer = task_data[0]
				print(self.answer)
				self.exercise_no = task_data[-1]

				page.set_exercise(self.exercise_no, "0012") # replace code with four digit number (go to main_app.py and check pages dictionary)
				page.change_task_text(self.task_text[lang].format(self.a, self.b, self.c))

			if lang == "eng":
				page.confirm_btn.config(text="Confirm", background=b_bg)
			elif lang == "rus":
				page.confirm_btn.config(text="Подтвердить", background=b_bg)

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
					page.confirm_btn.config(text="Correct", state="disabled", background="green")
				elif lang == "rus":
					page.confirm_btn.config(text="Правильно", state="disabled", background="green")
				self.after(500, new_task)
			else:
				if lang == "eng":
					page.confirm_btn.config(text="Wrong", state="disabled", background="red")
				elif lang == "rus":
					page.confirm_btn.config(text="Неправильно", state="disabled", background="red")
				self.after(500, lambda: new_task(False))

		self.confirm = confirm
		self.new_task = new_task

		page.new_task_command(new_task)
		page.confirm_command(confirm)
		page.set_theme(bg, fg, afg, dfg, b_bg, b_bg1, b_abg, e_bg, e_hl)
		page.set_lang(lang)

		parent.bind('<Return>', lambda _: page.confirm_btn.invoke())
		parent.bind('<KP_Enter>', lambda _: page.confirm_btn.invoke())
