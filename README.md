# COM5043-asignment-wms
This is the repository for the warehouse management system, that i have been assigned to do as the assignment for COM5043 object oriented programming

super user credentaials
username: superroot
password: postgres

i have made the migration file warehouse/migrations/0001_initial.py, but new owners of the system will have to run the migration commands
`docker compose up --build`

`docker compose exec web python manage.py migrate`

testing:
pytest
Will be used using Github actions or in-container testing too `docker compose run web pytest`