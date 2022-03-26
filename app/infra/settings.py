from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    # app envs
    app_name: str = "FastApi"
    app_docker_run: str
    app_test: str
    dev: str
    # database envs
    database_url: str
    database_url_docker: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    """Capture environment variables

    Returns:
        Returns environment variables
    """
    return Settings()


settings = get_settings()
