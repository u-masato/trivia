import os
from dotenv import load_dotenv

# load environment variable from .env file

load_dotenv(verbose=True)

DB_PATH = os.environ.get("DB_PATH")
