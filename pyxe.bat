@echo off

pyinstaller -F -w -i="main_icon.ico" -n="Math problem generator app" .\main_app.py
pyinstaller -F -w -i="update_icon.ico" -n="Math problem generator launcher" .\launcher.py