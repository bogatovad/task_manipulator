from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    user: str = Field(default="cism", validation_alias="POSTGRES_USER")
    password: str = Field(default="password", validation_alias="POSTGRES_PASSWORD")
    db: str = Field(default="cism", validation_alias="POSTGRES_DB")
    host: str = Field(default="db", validation_alias="POSTGRES_HOST")
    port: int = Field(default=5432, validation_alias="POSTGRES_PORT")
    echo: bool = Field(default=False, validation_alias="DATABASE_ECHO")

    model_config = SettingsConfigDict(
        env_file="environments/db.env",
        extra="ignore",
    )

    @property
    def url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.db}"
        )

    @property
    def alembic_url(self) -> str:
        return (
            f"postgresql+psycopg://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.db}"
        )


database_settings = DatabaseSettings()
