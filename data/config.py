import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))

admins = [
    os.getenv("ADMIN_ID"),
]




ip = os.getenv("ip")
PGDATABASE = str(os.getenv("PGDATABASE"))
PGUSER = str(os.getenv("PGUSER"))
PGPASSWORD = str(os.getenv("PGPASSWORD"))

aiogram_redis = {
    'host': 'redis',
}

redis = {
    'address': ('redis', 6379),
    'encoding': 'utf8'
}

GROUP = str(os.getenv("GROUPID"))
CHANNEL = str(os.getenv("CHANNELID"))

INSTRUCTION_LINK = str(os.getenv("INSTRUCTION_LINK"))
SEARCH_LINK = str(os.getenv("SEARCH_LINK"))
