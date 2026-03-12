from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str
    default_model: str
    tmdb_api_key: str
    tmdb_base_url: str = "https://api.themoviedb.org/3"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
