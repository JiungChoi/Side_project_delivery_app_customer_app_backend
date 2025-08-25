import os
import dotenv
from utility.logger import logger

# .env |X X� �| \�i��
ENVFILE = os.getenv("ENVFILE_PATH")

if ENVFILE:
    dotenv.load_dotenv(ENVFILE)
    logger.info(f"ENVFILE_PATH: {ENVFILE}")
else:
    dotenv.load_dotenv("./environments/.env.local")
    logger.info(f"ENVFILE_PATH: ./environments/.env.local")

# Database
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL", "postgresql://digitrack:digitrack@postgres:5432/digitrack")