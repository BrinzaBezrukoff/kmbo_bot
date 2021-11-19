import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///kmbo.db")
DATABASE_ECHO = os.getenv("DATABASE_ECHO", False)

BOT_TOKEN = os.getenv("BOT_TOKEN")
