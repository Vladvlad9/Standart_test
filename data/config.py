import os
from dotenv import load_dotenv
from os import environ

load_dotenv(".env")
BOT_TOKEN = os.environ["BOT_TOKEN"]
DATABASE = os.environ["DATABASE"]

async def load_admins() -> tuple:
    return tuple(map(int, environ["ADMINS"].split(",")))
