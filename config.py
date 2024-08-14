from dotenv import load_dotenv
import os

load_dotenv()

TPLINK_URL = os.getenv("TPLINK_URL")
TPLINK_PASSWD = os.getenv("TPLINK_PASSWD")