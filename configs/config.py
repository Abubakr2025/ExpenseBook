import json
from pydantic import BaseModel


class AuthSettings(BaseModel):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


class Settings(BaseModel):
    database_url: str
    port: int
    host: str
    auth: AuthSettings


def load_config(path: str = "configs/configs.json") -> Settings:
    with open(path, "r", encoding="utf-8") as f:
        config_data = json.load(f)
    return Settings(**config_data)


settings = load_config()
