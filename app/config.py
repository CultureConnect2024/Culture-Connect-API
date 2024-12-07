import os
from dotenv import load_dotenv
from pathlib import Path

# # read .env file
# load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env", encoding="utf-8")

env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path, encoding="utf-8")

class Config:
    DB_NAME = os.getenv('DB_NAME')
    DB_HOST = os.getenv('DB_HOST_NETWORK','localhost')
    DB_USER = os.getenv('DB_USER','postgres')
    DB_PASS = os.getenv('DB_PASS')
    DB_PORT = os.getenv('DB_PORT','5432')

# create instance config
config = Config()