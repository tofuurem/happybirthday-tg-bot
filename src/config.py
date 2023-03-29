from pydantic import Field, BaseSettings
from sqlalchemy import URL


class PostgresConfig(BaseSettings):
    host: str = Field(env='PG_HOST')
    port: int = Field(env='PG_PORT')
    db: str = Field(env='PG_DB')
    schema_db: str = Field(env='PG_SCHEMA')
    user: str = Field(env='PG_USER')
    password: str = Field(env='PG_PASSWORD')

    @property
    def connection_string(self) -> str:
        return URL.create(
            "postgresql+asyncpg",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.db,
        ).__str__()

    class Config:
        env_file = '.env'


class Configuration(BaseSettings):
    tg_token: str = Field(env='TG_TOKEN')
    pg: PostgresConfig = Field(default_factory=PostgresConfig)

    class Config:
        env_file = '.env'
