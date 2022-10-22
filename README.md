# leben-in-deutschland-python
Django app for managing the backend of the leben in deutschland mobile app

**NOTE:**

- The project contains the following important setup files: _requirements.text_, _runtime.txt_.
These two files define the python environment used and the respective libraries used in the project.

- You will need to define a _.env_ file in the root of the repository that will be used in the settings.py file. This file is excluded from version control since it is only meant to be used for development purposes and should store private developer settings. Look at the _.env.example_ for an example of such a file


- How to run Celery Populate Database task

Ensure the python environment is correctly installed based on the requirements.txt


Ensure you have the same runtime setup i.e. See runtime.txt


Ensure you set up the Environment variables
See the .env.example file for the environment variables you need to setup. Note, you do not have to AWS if you do not want.

Start django application by running
python manage runserver

Ensure RabbitMQ is properly configured via the environment variable CLOUDAMQP_URL & CLOUDAMQP_APIKEY OR LOCALAMQP_HOST & LOCALAMQP_PORT if locally hosted.
NOTE: The cloud setting will override the local settings if present

Start Celery through
celery worker -A lifeingermany -l info

Run command to start Django interactive shell (Needed for executing Celery)
python manage.py shell


Then in the shell write
from quickstart.tasks import populate_database


Then write 
populate_database.delay()
