from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    def __init__(self) -> None:
        self.POSTGRES_DB = os.getenv("POSTGRES_DB", "metrics_db")
        self.POSTGRES_USER = os.getenv("POSTGRES_USER", "metrics_user")
        self.POSTGRES_PASSWORD = os.getenv(
            "POSTGRES_PASSWORD", "1437eec3072599442798c23c767909b1"
        )
        self.POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5433)

    def get_sync_db_url(self) -> str:
        try:
            if not self.POSTGRES_DB:
                raise ValueError("DB name not found")
            if not self.POSTGRES_USER and self.POSTGRES_PASSWORD:
                raise ValueError("User or Password fields are empty for postgres")
            if not self.POSTGRES_PORT:
                raise ValueError("Host port is not defined")
        except Exception as e:
            raise Exception(f"Error: {e}")
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_USER}@localhost:{self.POSTGRES_PORT}/{self.POSTGRES_PASSWORD}?sslmode=require"
