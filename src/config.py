from pydantic.env_settings import BaseSettings
from pydantic.fields import Field


class Configuration(BaseSettings):
    tg_token: str = Field(env='TG_TOKEN')

    redis_host: str = Field(default='localhost', env='REDIS_HOST')
    redis_port: int = Field(default=6379, env='REDIS_PORT')
    redis_db: int = Field(default=1, env='REDIS_DB')

    @property
    def redis_url(self) -> str:
        return "redis://{0}:{1}/{2}".format(
            self.redis_host,
            self.redis_port,
            self.redis_db
        )

    class Config:
        env_file = '../.env'
