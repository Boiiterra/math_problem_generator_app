from requests.exceptions import RequestException
from tkinter import Button, Tk, Toplevel, Label
from tkinter.messagebox import askyesno
from pkg_resources import parse_version
from configparser import ConfigParser
from tkinter.ttk import Progressbar
from win32api import ShellExecute
from PIL import Image, ImageTk
from os import path as os_path
from threading import Thread
from requests import get
from pathlib import Path

__version__ = '0.8.01'
__author__ = "TerraBoii"
# If you want to get less automated version check this project: 
# https://github.com/vsantiago113/Tkinter-MyTestApp
_AppName_ = 'Math problem generator app'

parser = ConfigParser()
parser.read("data.txt")
lang = parser.get("language", "language")

# url for installer
url = "https://github.com/TerraBoii/math_problem_generator_app/raw/main/app_installer/mathproblemgenerator_setup.exe"
file_name = url.split('/')[-1].replace(" ", "_")
file_path = os_path.join("setup", file_name)


class UpdateManager(Toplevel):
    def __init__(self, parent):
        Toplevel.__init__(self, parent)

        self.transient(parent)
        self.attributes("-disabled", True)
        self.grab_set()
        self.geometry(f'{350}x{200}+{int((self.winfo_screenwidth() - 350) / 2)}+{int((self.winfo_screenheight() - 200) / 2)}')
        self.resizable(width=False, height=False)
        self.title('Update Manager')
        self.wm_iconbitmap('images/update_icon.ico')

        image = Image.open('images/update_manager.jpg')
        photo = ImageTk.PhotoImage(image)
        manager_holder = Label(self, image=photo)
        manager_holder.image = photo
        manager_holder.pack()

        def install_update():
            tmp.after(0, tmp.destroy)
            ShellExecute(0, 'open', file_path, None, None, 10)

        def start_update_manager():
            destination_folder = "setup"
            if not os_path.exists(destination_folder):
                destination_folder = str(Path.home() / "Downloads")  # create folder if it does not exist
            with get(url=url, stream=True) as r:
                self.progressbar['maximum'] = int(r.headers.get('Content-Length'))
                r.raise_for_status()
                with open(file_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=4096):
                        if chunk:  # filter out keep-alive new chunks
                            f.write(chunk)
                            self.progressbar['value'] += 4096
            self.attributes("-disabled", False)
            install_update()

        self.progressbar = Progressbar(self,
                                       orient='horizontal',
                                       length=200,
                                       mode='determinate',
                                       value=0,
                                       maximum=0)
        self.progressbar.place(relx=0.5, rely=0.5, anchor="center")
        self.wait_text = Button(self, text='Wait!', state="disabled")
        self.wait_text.place(x=-83, relx=1.0, y=-33, rely=1.0)

        self.start_manager = Thread(target=start_update_manager)
        self.start_manager.start()


def run(): # Execute main .exe and destroy tmp window
    tmp.after(0, tmp.destroy)
    ShellExecute(0, 'open', f'binaries\\{_AppName_}.exe', None, None, 10)


def update(tmp, data):
    parser = ConfigParser()
    parser.read("data.txt")
    if parser.get("info", "auto_update") == "False":
        if lang == "rus":
            title = 'Доступно обновление приложения!'
            text = f"{_AppName_} '{__version__}' должно быть обновлено до версии '{data}'." 
        else:
            title = 'Software update available!'
            text = f"{_AppName_} '{__version__}' needs to update to version '{data}'."
        get_update = askyesno(title, text)
        if get_update is True:
            UpdateManager(tmp)
        elif get_update is False:
            run()
    else:
        UpdateManager(tmp)


if __name__ == "__main__":

    tmp = Tk()  # Tmp -> short for temporary
    tmp.iconbitmap("images/update_icon.ico")
    # positioning window in middle of the screen with width = 650 and height = 400
    tmp.geometry(f"{650}x{400}+{int((tmp.winfo_screenwidth() - 650) / 2)}+{int((tmp.winfo_screenheight() - 400) / 2)}")
    tmp.withdraw()  # Making tmp window "invisible"

    try:

        response = get('https://raw.githubusercontent.com/TerraBoii/math_problem_generator_app/main/version.txt')
        data = response.text

        if parse_version(data) > parse_version(__version__):
            update(tmp, data)
        else:
            run()
    except RequestException:  # Something went wrong during requesting
        run()

    tmp.mainloop()
