from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Lead Sales Automation"
    app_env: str = "development"
    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/lead_sales"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    def model_post_init(self, __context: object) -> None:
        # Railway exposes PostgreSQL URLs as postgresql:// (or postgres://).
        # SQLAlchemy otherwise selects the legacy psycopg2 dialect. This
        # project uses psycopg 3, so make the driver explicit.
        if self.database_url.startswith("postgresql://"):
            self.database_url = self.database_url.replace(
                "postgresql://", "postgresql+psycopg://", 1
            )
        elif self.database_url.startswith("postgres://"):
            self.database_url = self.database_url.replace(
                "postgres://", "postgresql+psycopg://", 1
            )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
