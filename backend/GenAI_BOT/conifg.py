from os import getenv
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env', override=True)

TOKEN = getenv("TOKEN")
