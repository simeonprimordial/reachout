from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    brave_search_api_key: str | None = None
    search_provider: str = "brave"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
