import os
from dotenv import load_dotenv

load_dotenv()

db_settings = {
    "dbname": os.environ.get("DB_NAME"),
    "user": os.environ.get("USER"),
    "password": os.environ.get("PASSWORD"),
    "host": os.environ.get("HOST"),
    "port": os.environ.get("PORT"),
}
