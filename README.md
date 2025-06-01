# COM5043-asignment-wms
This is the repository for the warehouse management system (wms), that i have been assigned to do as the assignment for COM5043 object oriented programming


Step for inital setting up this WMS.
1.  `git clone https://github.com/YufanKambang/COM5043-asignment-wms.git`
    or if you have pasword protected ssh set up `git@github.com:YufanKambang/COM5043-asignment-wms.git`

2.  Move into the main/root directory of the repository
    `cd COM5043-asignment-wms`

3.  make sure you have docker and docker compose installed with `docker --versions` and 
    `docker compose version` or `docker-compose version`
    regarding using docker compose or docker-compose, i cant know which one will work for you.
    however, if you need docker-compose then for the future step replace where relevent.
    
    build the django and database container using
    `docker compose up --build`
    here sometimes if you have already built the container there may be orphan container in that case run this command to clean them
    `docker compose up --build --remove-orphans`

    this will install the dependencies anbd start the webservice at `http://localhost:8000`

4.  run initial migration for the models into your database container. 
    You should do this in a seperate terminal tabl but in the main directory of the same repository, and run this command
    `docker compose exec web python manage.py migrate`

5.  create a superuser to access the admin dashboard with this:
    `docker compose exec web python manage.py createsuperuser`
    Now only need to follow the promts, please note your login details securely
    use your login detail at `http://localhost:8000/admin/`

6.  if you want to locally run tests use this command in a seperate terminal with your container up and running, and with a vitual environment set up:
    within the main directory of the repository, it is python3 more my terminal but this may differ between machines:
    `python3 -m venv venv`

    Activate the virtual environment:
    `source venv/bin/activate`

    now install the required dependencies within your venv:
    `python3 -m pip install --upgrade pip` then --> 
    `python3 -m pip install -r requirements.txt`

    finally to see run unit test and see code coverage summary:
    `docker compose exec web pytest --cov=warehouse --cov-report=term-missing`

I have made the migration file warehouse/migrations/0001_initial.py, but new owners of the system will have to run the migration commands
so that the classes in warehouse/models.py get registered as tables in the database for the wms to function

`docker compose up --build`

`docker compose exec web python manage.py migrate`

testing:
pytest, in the form of continuos integrated (CI) testing
The steps done to run the test locally.

1. first enter into the root directory of the repo and do the run the command
    `docker compose up --build`

2. In another terminal tab with the same operating system you used for step 1 run command 
    `docker compose run web pytest`
