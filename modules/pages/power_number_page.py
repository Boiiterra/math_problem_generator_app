from tkinter import Frame

from ..generators import power_number
from .task_template import TaskPageTemplate


class Power_NumberPage(Frame):
	task = {"eng": "Exponents", "rus": "Степени"}
	ttask = {"eng": "{} to the power of {}",
			 "rus": "{} в степени {}"}
	subject = 0 

	def __init__(self, parent, lang, version, prev, bg, fg, afg, dfg, b_bg, b_bg1, b_abg, e_bg, e_hl):
		Frame.__init__(self, parent)

		page = TaskPageTemplate(self, parent, prev)
		page.pack(fill="both", expand=True)

		self.exercise_no = None
		self.number = None
		self.exponent = None
		self.answer = None

		def new_task(full_reset: bool = True):
			if full_reset:
				task_data = power_number(version, self.winfo_width(), self.winfo_height(),
										 self.winfo_screenwidth(), self.winfo_screenheight())
				self.number = task_data[1]
				self.exponent = task_data[2]
				self.answer = task_data[0]
				self.exercise_no = task_data[-1]

				page.set_exercise(self.exercise_no, "0011")
				page.change_task_text(self.ttask[lang].format(self.number, self.exponent))

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

		self.confirm_c = confirm
		self.new_task_c = new_task

		page.new_task_command(new_task)
		page.confirm_command(confirm)
		page.set_theme(bg, fg, afg, dfg, b_bg, b_bg1, b_abg, e_bg, e_hl)
		page.set_lang(lang)

		parent.bind('<Return>', lambda _: page.confirm_btn.invoke())
		parent.bind('<KP_Enter>', lambda _: page.confirm_btn.invoke())
