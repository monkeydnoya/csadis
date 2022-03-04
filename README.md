**This is a REST API for a CSADIS testing project with FastAPI, SQLAlchemy and PostgreSQL.**

**How to run the project**

1. Install PostgreSql (for the convenience of viewing the database, also install pgAdmin 4)
2. Install Python (in this project used the version 3.9.7)
3. Git clone the project with https://github.com/monkeydnoya/csadis.git
4. Create your virtual environment and activate it
5. Install the requirements with pip install -r requirements.txt
6. Create new database or set up your own and change path to database url

   DATABASE_URL = "postgresql://postgres:<password>@localhost/<database name>"

7. Create database by python create_db.py
8. Make initial migration alembic revision --autogenerate -m '<migration name>'
9. Migrate alembic upgrade head
10. run application uvicorn main:app --reload
