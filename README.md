# Secoda backend take-home assignment

## Reproduce steps to run the project locally
0. Clone the project
1. Run `pip install -r requirements.txt` to install neccessary deps
2. Run `python manage.py runserver` to start the Django server locally

## Sample API call: 

1. Navigate your browser or make a GET request to 
`http://127.0.0.1:8000/connect/postgresql+psycopg2://postgres:MB7fymjjBVNZGL8jnJEb@db.geqgitsqodgmqroopasx.supabase.co/postgres`

to connect to the test database.

The endpoint format is `/connect/dialect[+driver]://user:password@host/dbname`

## Remaining challenges and possible improvements:
1. We're passing password directly in the url which is not safe
2. We're approximating num_rows through `pg_stat_all_tables` table. It's much faster than querying `COUNT(*)` on every table but it's not completely accurate and doesn't contain every table.
3. Only work for PostGreSQL and requires `psycopg2` driver. The server doesn't have other drivers installed so using anything else would break it.
4. Abstracting the error messages would be more secure than passing them back directly, which exposes our internal implementation.

## Sample response 

![image](https://github.com/nt7nguye/secoda-backend-takehome/assets/45516852/64dc9027-b3c5-4e64-a677-e3d5d2de55b1)

Full response in `test_response.json`
