from pydantic.env_settings import BaseSettings
from pydantic.fields import Field


class Configuration(BaseSettings):
    tg_token: str = Field(env='TG_TOKEN')
    redis_url: str = Field(default='redis://localhost:6379/1', env='REDIS_URL')

    class Config:
        env_file = '.env'
