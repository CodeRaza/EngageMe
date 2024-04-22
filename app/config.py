import os

DB_USER = os.getenv("DB_USER")
DB_PW = os.getenv("DB_PW")
DB_HOSTNAME = os.getenv("DB_HOSTNAME")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

MAIL_SERVER = os.getenv("MAIL_SERVER")
MAIL_PORT = os.getenv("MAIL_PORT")
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_USE_TLS = os.getenv("MAIL_USE_TLS")
MAIL_USE_SSL = os.getenv("MAIL_USE_SSL")
MAIL_SECRET_KEY = os.getenv("MAIL_SECRET_KEY")