import os
import pathlib

from dotenv import load_dotenv

load_dotenv()

POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_USER = os.environ.get("POSTGRES_USER")

PRIVATE_KEY_PATH = pathlib.Path(os.environ.get("PRIVATE_KEY_PATH"))
PUBLIC_KEY_PATH = pathlib.Path(os.environ.get("PUBLIC_KEY_PATH"))

COOKIE_KEY_NAME = os.environ.get("COOKIE_KEY_NAME")

RMQ_USER = os.environ.get("RMQ_USER")
RMQ_PASS = os.environ.get("RMQ_PASS")
