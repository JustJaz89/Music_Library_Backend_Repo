# FlaskRestAPI_PY_Starter

Setup:

1. Download and extract zip file, open in VS Code.

2. Create your own Github repo with a Python gitignore and your own README, push the code up. Be sure not to upload this README to your own repo.

3. Create a MySQL Database with an appropriate name

4. Change the password and db_name in the .env file to your MySQL password and the database you just created.
 - NOTE: Some special characters in the password (especially @ and /) must be url escaped. For a @, use `%40`. For a /, use `%2F`

5. Create your virtual environment with:
 - `pipenv install`
 - `pipenv shell`
 - Once the venv is created, you can start the app at any time with `flask run`

6. Create your database model(s) in app.py with the required properties, then run
 - `flask db init` (Creates tables)
 - `flask db migrate -m "Init"` (Creates migration)
 - `flask db upgrade` (Runs migration)

5. Create Marshmallow Schemas in app.py

6. Continue on to create Resource classes and Routes, making sure to test each in Postman!
