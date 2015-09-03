Awesome House Tools
===================
This repository contains the tools used at Awesome House, or the house rented up in Rochester.
It currently contains a website for interfacing with in house systems and information.

Setup
-------
The project is setup with a virtual environment.  
To use:
* make a virtual environment (preferably in `env`)  
`virtualenv env`
* activate it  
`source env/bin/activate` if on linux  
`env\Scripts\activate.bat` if on windows
* install the requirement file  
`pip install -r env/requirements.txt`

This will install all dependencies for all the projects. The virtual environment must be activated for all projects.

Current Projects
----------

#### Website
The first step is to initialize the database. This can be done by executing models.py  
```bash
cd website
python models.py
```
Then, simply run the run.py file in the website folder.  
`python website/run.py`  
or  
`python run.py` if in the website folder