#!/bin/bash

if [ -z $1 ]; then
    echo "No task name is entered"
    echo "Try: $0 <new-task-name>"
elif [[ $1 == *"."* ]]; then
    echo "Please do not secify file type or do not use dots"
else
    ./automation/writter.py $1
    echo "from .$1 import $1" >> ./modules/generators/__init__.py

    # adding generator
    touch ./modules/generators/$1.py
    echo "from random import seed, randint" >> ./modules/generators/$1.py
    echo >> ./modules/generators/$1.py
    echo "from .c_seed import create_seed" >> ./modules/generators/$1.py
    echo >> ./modules/generators/$1.py
    echo "def $1(app_version: str, app_width: int, app_height: int, screen_width: int, screen_height: int):" >> ./modules/generators/$1.py
    echo -e "\tnew_seed = create_seed(app_version, app_width, app_height, screen_width, screen_height)" >> ./modules/generators/$1.py
    echo -e "\tseed(new_seed)" >> ./modules/generators/$1.py
    echo -e "" >> ./modules/generators/$1.py
    echo -e "\treturn 'result', 'info to get result', new_seed" >> ./modules/generators/$1.py

    # adding new page
    touch ./modules/pages/$1_page.py
    ./automation/artist.py $1
fi
