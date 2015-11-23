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

Current Projects
----------
#### Website
The landing page of the website lists nearing events 
(events that are within a month of the current date) and a list of tasks.
Tasks that are done will be striked through.
If the checkbox of the to-do is checked, the box will strike out, 
but a check box is only visible if a user is logged in.

A user that is not registered can only access the read only portion of the landing page.
All other pages, API calls, and AJAX requests are denied.
A user can register by clicking in the top right of the site and clicking register.
The account then needs to be authorized by an admin.
Once logged in, the user can access settings in the top right.

###### Events
The event page lists all future events, deleted and non deleted.
To add an event, click the 'Add Event' button and fill in the details.
Clicking on an event will show its details.
You can also add tasks from the specific event page.

A specific events details can be seen by clicking on the link to it,
which will bring you to the /events/by-id/ page.
This page shows you any specific detail about the event including the time,
description, and any todos and tasks associated with the event.
The event can be edited and deleted from this page as well
Any deleted event is not permanently deleted,
just tagged with deleted and not shown on any other page except for the /events page.

###### Todos
Todos work in a similar way to events.
The /todos page (currently no link to it) will show all todos.
This page does not have an Add Todo button, this button resides on the landing page.
The /todos page will list the event it is associated with, if any, the task, if it is done, and the date done.
A strike through the whole row is added if the todo is done,
and a strike through the event and task if it is deleted.

The specifics of the todo is shown on the /todos/by-id/ page.
The todo can be edited and deleted from this page.
Like events, they are not deleted, just tagged with the deleted and not shown on any other page except /todos.
