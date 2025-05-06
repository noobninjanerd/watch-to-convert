#!/bin/bash

# create virtual environment
python3 -m venv pyenv_for_w2c

# activate virtual environment
source pyenv_for_w2c/bin/activate

# install the required dependencies in the virtual environment
pip install markdown
pip install watchdog
pip install git+https://github.com/mitya57/python-markdown-math.git

# once the script finishes, the pyenv_for_w2c will close
# restart it using the same command: source pyenv_for_w2c/bin/activate
# confirm that your shell changes -> this means you are in the virtual env


