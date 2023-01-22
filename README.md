<details>
<summary>Navigation</summary>

- [Math Problem Generator App](#math-problem-generator-app)
  - [Description](#description)
  - [Installation](#installation)
    - [Windows](#windows)
    - [Linux](#linux)
  - [Structure of the project](#structure-of-the-project)
    - [About generators](#about-generators)
    - [About pages](#about-pages)
    - [New task creation](#new-task-creation)
      - [Manual](#manual)
      - [Automatic](#automatic)

</details>

___

<p align="center">Description in another languages:</p>
<p align="center"> <strong>--</strong> <a href="https://github.com/TerraBoii/math_problem_generator_app/blob/main/README_ru.md", title="test">Russian</a> <strong>--</strong> </p>

___

<p align="center"><a href="https://terraboii.github.io/mpga_wp", title="Projects's website">Link to project's website</a></p>

___

# Math Problem Generator App

## Description

This application was created as school project and it generates certain math problems. Math problems has their unique number which allows you to return to that specific exercise at any time and solve it as many times as you want.

## Installation

### Windows

1. [Click me to start downloading "mathproblemgenerator_setup.exe" file](https://github.com/TerraBoii/math_problem_generator_app/raw/main/app_installer/mathproblemgenerator_setup.exe)
2. After download is finished open `mathproblemgenerator_setup.exe`
3. Complete installation by choosing options you like
4. After finishing this process app will be opened or you need to double click it on your desktop, start menu or find it in the destination folder you picked (Targeted file is `Math problem generator launcher.exe`)

### Linux

Currently working on it. But you can do this in console: \
SSH:

```sh
git clone git@github.com:TerraBoii/math_problem_generator_app.git
cd math_problem_generator_app
pip install -r requirements.txt
./main_app.py
```

HTTPS

```sh
git clone https://github.com/TerraBoii/math_problem_generator_app.git
cd math_problem_generator_app
pip install -r requirements.txt
./main_app.py
```

<p align="right">(<a href="#top" title="to the top of the page">back to top</a>)</p>

## Structure of the project

- ./
  - app_installer/
    - mathproblemgenerator_setup.exe
  - automation/
    - artist.py
    - writer.py
  - images/
    - main_icon.ico
    - uninstaller.ico
    - update_icon.ico
    - update_manager.jpg
  - modules/
    - [generators/](#about-generators)
    - [pages/](#about-pages)
    - \_\_init\_\_.py
    - option.py
    - resolution.py
    - tooltip.py
  - .gitignore
  - LICENSE
  - README.md
  - README_ru.md
  - add_task.sh
  - backup_data.txt
  - data.txt
  - defaults.txt
  - installer_icon.ico
  - launcher.py
  - main_app.py
  - main_icon.ico |--> used for pyinstaller
  - requirements.txt
  - update_icon.ico |--> used for pyinstaller
  - version.txt

<p align="right">(<a href="#top" title="to the top of the page">back to top</a>)</p>

### About generators

All generators are stored in `./modules/generators/` directory. I won't list them as they will increase over time. Generators are used in [task pages](#about-pages). In order to create new generator check: [how to create new task](#new-task-creation). \
! Do not create page without checking [New task creation](#new-task-creation) !

### About pages

All pages are stored in `./modules/pages/` directory. I won't list them as they will increase over time. Pages are used in [main_app.py](main_app.py). In order to create new page check: [how to create new task](#new-task-creation). \
! Do not create page without checking [New task creation](#new-task-creation) !

<p align="right">(<a href="#top" title="to the top of the page">back to top</a>)</p>

<br>

### New task creation

You can create pages manually or automatically.

#### Manual

Use [automatic](#automatic) please. \
Manual is harder than automatic.

#### Automatic

Works on Linux (probably on MacOS too): /
If your current working directory is `.../math_problem_generator_app/` then open terminal and type:

```bash
./add_task.sh <task_name>
```

Then you can open `./modules/pages/<Task_Name>Page.py` and `./modules/generators/<task_name>.py` and edit them. \
**Important note**: Make sure that you added `<Task_Name>Page.py` as import from modules into `main_app.py` + into `pages` dictionary (it is located under `__version__` and `author` variables).

If you use Windows - you probably need to google "how to run shell scripts" or create `.bat` ones and contribute them if you want.

<p align="right">(<a href="#top" title="to the top of the page">back to top</a>)</p>
