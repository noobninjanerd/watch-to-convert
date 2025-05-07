# Watch-to-Convert
This python script observes a directory and on creation/modification of markdown files, converts them to html and places them into a target directory. 

This can be utilized in the backend of your personal blog, where you can edit and create your markdown files, and have them instantly be available for publishing on your website. 

## How to use?
1. Certain python modules are required to run this script. You can run `create_venv.sh` which creates a virtual python environment and then installs the required dependencies.
2. Activate the virtual environment using `source pyenv_for_w2c/bin/activate`
3. Make sure your shell prompt changes, indicating that you are in the virtual environment. Run the script by giving it a target directory to observe or by-default it will observe the current working directory: `python3 w2c.py path/to/target_diretory`


## To-do
1. ~~add scripts for adding necessary css code and title-card ~~
2. ~~add feature to take the directory-to-copy-files to as an arguement~~
3. ~~a script which creates a virtual python env (if not already avaialable) and then runs this~~
4. generate file.log