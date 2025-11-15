import os
from dotenv import load_dotenv
from libsql_client import create_client

load_dotenv()

URL_TURSO = os.getenv("TURSO_DATABASE_URL")
TOKEN_TURSO = os.getenv("TURSO_AUTH_TOKEN")


def Conection():
    client = create_client(url=URL_TURSO, auth_token=TOKEN_TURSO)
    return client


