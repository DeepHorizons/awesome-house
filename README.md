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

Next, set an environmental variable of `AWESOME_HOUSE_WEBSITE_CONFIG_SETTINGS` to point to a configuration file containing your settings.  
`export AWESOME_HOUSE_WEBSITE_CONFIG_SETTINGS=/path/to/config.py` if on linux  
`set AWESOME_HOUSE_WEBSITE_CONFIG_SETTINGS=\path\to\config.py` if on windows  
A sample config has been provided that sets the site to run in production mode.
Note that you **must** change the `SECRET_KEY` key for security reasons.

Then, simply run the run.py file in the website folder.  
`python website/run.py`  
or  
`python run.py` if in the website folder

##### uWSGI and NGINX / Production
In order to use the site in production (on the nets) uWSGI and NGINX should be set up
To use uWSGI and NGINX, simply symlink `uwsgi.ini` in the website/config to the uWSGI enabled folder (or available folder and then to the enabled folder),
and symlink the `nginx.ini` to the NGINX enabled folder (or same for uwsgi).
The ini files need to be set, in the `nginx.ini`
* <site name>: the url of the site
* <socket fle in uwsgi.ini>: the socket file location and name

In the `uwsgi.ini` file,
* <path to venv>: The full path to the virtual environment
* <path to working directory>: The full path to the website/ folder (This includes the website folder)
* <sock file>: A path to the socket file. This must be the same as in the `nginx.ini` file

##### SSL cert
The site can be encrypted using SSL/TLS.
To do this, Get a certificate (Lets Encrypt is free) and comment the HTTP section and uncomment the HTTPS section
Usefull tutorials are as follows:  
https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-14-04  
http://nginx.org/en/docs/http/configuring_https_servers.html  
https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-14-04  
https://letsencrypt.org/howitworks/  


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
