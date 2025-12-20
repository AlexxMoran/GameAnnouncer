from pydantic import BaseModel, PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class RunConfig(BaseModel):
    host: str = "localhost"
    port: int = 3000


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
    echo: bool = True
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
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
            path=self.database,
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
            path=self.database,
        )


class CORSConfig(BaseModel):
    backend_cors_origins: list[str] = []
    frontend_host: str = ""
    allow_credentials: bool = True
    allow_methods: list[str] = ["*"]
    allow_headers: list[str] = ["*"]

    @computed_field
    @property
    def all_cors_origins(self) -> list[str]:
        cleaned = [origin.rstrip("/") for origin in self.backend_cors_origins]

        if self.frontend_host not in cleaned:
            cleaned.append(self.frontend_host.rstrip("/"))

        return cleaned


class AuthConfig(BaseModel):
    secret_key: str
    refresh_secret_key: str
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    algorithm: str = "HS256"
    verification_token_secret: str
    reset_password_token_secret: str


class RedisConfig(BaseModel):
    host: str = "redis"
    port: int = 6379
    db: int = 0

    @computed_field
    @property
    def url(self) -> str:
        return f"redis://{self.host}:{self.port}/{self.db}"


class EmailConfig(BaseModel):
    smtp_host: str = "mailpit"
    smtp_port: int = 1025
    smtp_user: str = ""
    smtp_password: str = ""
    from_email: str = "noreply@gameannouncer.com"
    from_name: str = "GameAnnouncer"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="__",
    )
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    db: DatabaseConfig
    cors: CORSConfig = CORSConfig()
    auth: AuthConfig
    redis: RedisConfig = RedisConfig()
    email: EmailConfig = EmailConfig()


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
