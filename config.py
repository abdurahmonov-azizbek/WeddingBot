import os
from dotenv import load_dotenv

load_dotenv(override=True)

TOKEN = os.getenv("TOKEN", "ENTER YOUR BOT TOKEN HERE")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

DB_CONF = {
    "user": DB_USER,
    "password": DB_PASSWORD,
    "database": DB_NAME,
    "host": DB_HOST,
    "port": DB_PORT
}

ADMINS = [int(admin_id) for admin_id in os.getenv("ADMINS", "").split(",") if admin_id.isdigit()]
HOSTESS = [int(hostess_id) for hostess_id in os.getenv("HOSTESS", "").split(",") if hostess_id.isdigit()]