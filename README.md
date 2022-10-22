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

Ensure RabbitMQ is properly configured via the environment variable CLOUDAMQP_URL & CLOUDAMQP_APIKEY OR LOCALAMQP_HOST & LOCALAMQP_PORT if locally hosted & that it is running
NOTE: The cloud setting will override the local settings if present

Start django + celery via heroku by running (without heroku)
heroku local

NOTE: In order to run heroku local without port issues on a Macbook, please update the Procfile web dyno as follows:
web: gunicorn --bind 0.0.0.0:8000 lifeingermany.wsgi --log-file -

OR

Without heroku, you can start each of them individually in two separate steps

Start django application by running
python manage.py runserver 8000 (locally)
Or by pushing the master branch to heroku e.g.

git push heroku main



Start Celery through (local)
celery -A lifeingermany worker -l INFO



Run command to start Django interactive shell (Needed for executing Celery)
python manage.py shell (without heroku or locally)
heroku run python manage.py shell (on heroku)


Then in the shell write
from quickstart.tasks import populate_database


Then write 
populate_database.delay()


Wait a few minutes while the task scrapes a few webpages to populate the database.


Login into the admin panel of the application and view the populated data i.e. The 16 German States & their icons, The Questions and their answers.