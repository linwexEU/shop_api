import os
from typing import Literal

from dotenv import find_dotenv, load_dotenv
from pydantic_settings import BaseSettings

current_dir = os.path.dirname(os.path.abspath(__file__))

os.chdir(current_dir)

dotenv_path = find_dotenv(".env")
load_dotenv(dotenv_path)


class Settings(BaseSettings):
    MODE: Literal["TEST", "DEV"]

    SECRET_KEY: str
    ALGORITHM: str
    TOKEN_EXPIRE: int

    ADMIN_TOKEN: str

    CLIENT_ID: str
    CLIENT_SECRET: str

    DB_NAME: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str

    TEST_DB_NAME: str
    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str

    REDIS_HOST: str
    REDIS_PORT: int

    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    RABBITMQ_USER: str
    RABBITMQ_PASS: str

    AWS_SECRET_KEY: str
    AWS_ACCESS_KEY: str
    AWS_REGION: str
    AWS_EMAIL: str

    X_RAPIDAPI_HOST: str
    X_RAPIDAPI_KEY: str

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def TEST_DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASS}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"

    @property
    def REDIS_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    @property
    def RABBITMQ_URL(self) -> str:
        return f"amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASS}@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}"

    @property
    def COMPUTERS_URL(self) -> str:
        return "https://hard.rozetka.com.ua/ua/computers/c80095/page=1/"

    @property
    def PHONES_URL(self) -> str:
        return "https://rozetka.com.ua/ua/mobile-phones/c80003/page=1/"

    @property
    def MONITORS_URL(self) -> str:
        return "https://hard.rozetka.com.ua/ua/monitors/c80089/page=1;preset=game/"

    @property
    def LEGOS_URL(self) -> str:
        return "https://rozetka.com.ua/ua/building_kits/c97420/page=1;producer=lego/"

    @property
    def BOOKS_URL(self) -> str:
        return "https://rozetka.com.ua/ua/knigi-dlya-biznesa/c4620235/page=1/"

    @property
    def KEYBOARDS_URL(self) -> str:
        return "https://rozetka.com.ua/ua/igrovie-klaviaturi/c4673273/page=1/"

    @property
    def MOUSES_URL(self) -> str:
        return "https://rozetka.com.ua/ua/igrovie-mishi/c4673278/page=1/"

    @property
    def ELECTRONICS_URL(self) -> str:
        return "https://rozetka.com.ua/ua/elektrotransport/c4625901/page=1/"

    class ConfigDict:
        env_file = dotenv_path


settings = Settings()
