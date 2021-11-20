import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///kmbo.db")
DATABASE_ECHO = os.getenv("DATABASE_ECHO", False)

BOT_TOKEN = os.getenv("BOT_TOKEN")

ALLOW_ID = os.getenv("ALLOW_ID", True)
DEFAULT_ROLE = os.getenv("DEFAULT_ROLE", 1)
