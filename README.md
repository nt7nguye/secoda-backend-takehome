# Secoda backend take-home assignment

## Deployed version

Try the test database at `https://secoda-backend-takehome-928ddbfcc981.herokuapp.com/connect/postgresql+psycopg2://postgres:MB7fymjjBVNZGL8jnJEb@db.geqgitsqodgmqroopasx.supabase.co/postgres`

The server is hosted with heroku at `https://secoda-backend-takehome-928ddbfcc981.herokuapp.com/`.

The endpoint format is `/connect/dialect[+driver]://user:password@host/dbname`

Full response in `test_response.json`

## Reproduce steps to run the project locally
0. Clone the project
1. Run `pip install -r requirements.txt` to install neccessary deps
2. Run `python manage.py runserver` to start the Django server locally

## Sample API call: 

1. Navigate your browser or make a GET request to 
`http://127.0.0.1:8000/connect/postgresql+psycopg2://postgres:MB7fymjjBVNZGL8jnJEb@db.geqgitsqodgmqroopasx.supabase.co/postgres`

to connect to the test database.


## Remaining challenges and possible improvements:
1. We're passing password directly in the url which is not safe
2. We're approximating num_rows through `pg_stat_all_tables` table. It's much faster than querying `COUNT(*)` on every table but it's not completely accurate and doesn't contain every table.
3. Only work for PostGreSQL and requires `psycopg2` driver. The server doesn't have other drivers installed so using anything else would break it.
4. Abstracting the error messages would be more secure than passing them back directly, which exposes our internal implementation.


