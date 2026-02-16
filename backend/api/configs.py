from dotenv import load_dotenv
import os
from pathlib import Path

# Load .env from backend directory
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)


class Config:
    def __init__(self) -> None:
        self.POSTGRES_DB = os.getenv("POSTGRES_DB")
        self.POSTGRES_USER = os.getenv("POSTGRES_USER")
        self.POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
        self.POSTGRES_PORT = os.getenv("POSTGRES_PORT")

    def get_sync_db_url(self) -> str:
        try:
            if not self.POSTGRES_DB:
                raise ValueError("DB name not found")
            if not self.POSTGRES_USER or not self.POSTGRES_PASSWORD:
                raise ValueError("User or Password fields are empty for postgres")
            if not self.POSTGRES_PORT:
                raise ValueError("Host port is not defined")
        except Exception as e:
            raise Exception(f"Error: {e}")
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@localhost:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
