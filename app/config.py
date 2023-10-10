from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str
    oauth_secret_key: str
    oauth_algorithm: str
    oauth_token_expire: int

    class Config:
        env_file = '/.env'


settings = Settings()
