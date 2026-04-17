"""Day 6 配置管理。"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置。

    BaseSettings 会自动从环境变量和 `.env` 文件中读取配置。
    后面做数据库、Redis、JWT 时都会继续用这个思路。
    """

    app_name: str = "Day 6 Layered API Demo"
    debug: bool = True
    api_prefix: str = "/api/v1"
    default_page_size: int = 10

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache()
def get_settings() -> Settings:
    """缓存配置对象，避免重复读取。"""

    return Settings()
