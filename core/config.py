from pydantic import Field, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Github Caller"

    github_token: str = Field(alias="GH_TOKEN")

    github_url: HttpUrl = "https://api.github.com"

    github_api_version: str = "2026-03-10"

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8")


settings = Settings()
