
from pydantic import ( BaseModel, PostgresDsn, computed_field )
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    host: str = "localhost"
    port: int = 8000

class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"

class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()

class DatabaseConfig(BaseModel):
    server: str
    port: int = 5432
    user: str
    password: str
    database: str
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }

    @computed_field
    @property
    def url(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg", 
            username=self.user,
            password=self.password,
            host=self.server,
            port=self.port,
            path=self.database
        )
    
    @computed_field
    @property
    def sync_url(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql", 
            username=self.user,
            password=self.password,
            host=self.server,
            port=self.port,
            path=self.database
        )

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
    )
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig


settings = Settings()
