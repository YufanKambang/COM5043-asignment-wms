# COM5043-asignment-wms
This is the repository for the warehouse management system (wms), that i have been assigned to do as the assignment for COM5043 object oriented programming

super user credentaials
use at [BNU-WMS-admin-page](http://localhost:8000/admin/)
username: superroot
password: postgres

i have made the migration file warehouse/migrations/0001_initial.py, but new owners of the system will have to run the migration commands
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


todo list:
    frontend:
    - ui for users to see the service, text bases in blocks

    backend:
    - The logic for users to create an object, slect items to buy, and such need to be implemented
    - testing for code base

    dev:
    - i think a pre-commit test for linting and such to make codebase neater may be benificial 